"""Audit-only derived candidate; deliberately separate from presentation selection."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from .versioned_electoral_source import ReadRequest, SeriesKey, VersionedElectoralSource


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


class JudicialDerivedAuditSource:
    """Build once from a pinned manifest and a complete batch of audit responses.

    Hashes are reproducibility checks, not authority signatures or certification.
    There is no policy override and no automatic choice of a candidate.
    """
    def __init__(self, manifest, expected_manifest_sha256, responses):
        manifest = deepcopy(manifest)
        require(digest(manifest) == expected_manifest_sha256, "MANIFEST_HASH_MISMATCH")
        require(manifest["contract"] == "HEYTI_JUDICIAL_AUDIT_CANDIDATE_v1", "MANIFEST_CONTRACT")
        require(manifest["series"] == {"year": 2024, "type": "A", "modality": "UNICA"}, "UNSUPPORTED_SERIES")
        require(manifest["municipality_code"] == "3", "UNSUPPORTED_SCOPE")
        require((manifest["expected_units"], manifest["expected_ordinary_units"], manifest["expected_special_units"]) == (106, 105, 1), "SCOPE_COUNTS")
        self.series = SeriesKey(2024, "A", "UNICA")
        columns = manifest["columns"]
        require(len(columns) == 17 and len({c["ordinal"] for c in columns}) == 17, "COLUMN_COVERAGE")
        require(len(manifest["restorations"]) == 4, "RESTORATION_COVERAGE")
        restoration_keys = [(r["unit_key"], r["acta_literal"]) for r in manifest["restorations"]]
        require(len(set(restoration_keys)) == 4, "DUPLICATE_RESTORATION")
        require(not set(restoration_keys) & {(r["unit_key"], r["acta_literal"]) for r in manifest["exclusions"]}, "EXCLUSION_RESTORED")
        require(len(responses) == 106, "UNIT_COVERAGE")
        units, source_provenance = {}, None
        for response in responses:
            require(response["status"] == "AUDIT_SOURCE_AS_PUBLISHED" and response["purpose"] == "AUDIT" and response["metric_scope"] == "RESULT", "AUDIT_RESULT_REQUIRED")
            snapshot = deepcopy(response["data"])
            require(isinstance(snapshot, dict), "SNAPSHOT_REQUIRED")
            identity, provenance = snapshot["identity"], snapshot["provenance"]
            require(all(identity.get(k) == v for k, v in manifest["series"].items()), "SERIES_IDENTITY")
            require(identity.get("municipality_code") == "3", "MUNICIPALITY_SCOPE")
            require(identity["unit_kind"] in ("ORDINARY_SECTION", "SPECIAL_SECTION_ROW"), "UNIT_KIND")
            if identity["unit_kind"] == "SPECIAL_SECTION_ROW":
                special = manifest["special_unit"]
                require(all(identity.get(k) == special[k] for k in ("unit_kind", "unit_key", "section_literal", "original_identity")), "SPECIAL_IDENTITY_MISMATCH")
                require(identity.get("current_section_fk") is None, "SPECIAL_CURRENT_SECTION_FK")
            key = identity["unit_key"]
            require(isinstance(key, str) and key and key not in units, "DUPLICATE_OR_INVALID_UNIT")
            require(all(provenance.get(k) == v for k, v in manifest["source"].items()), "SOURCE_HASH_IDENTITY")
            require(response["provenance"] == provenance, "RESPONSE_PROVENANCE")
            if source_provenance is None:
                source_provenance = provenance
            require(provenance == source_provenance, "MIXED_SOURCE_RELEASES")
            result = snapshot["result"]
            require(VersionedElectoralSource._valid_result(result), "INVALID_LITERAL_RESULT")
            require(type(result["total_votes"]) is int, "NULL_BASE_TOTAL")
            options = sorted(result["options"], key=lambda c: c["ordinal"])
            require(len(options) == 17, "OPTION_COVERAGE")
            require(all(all(o.get(k) == col[k] for k in ("ordinal", "raw_column", "option_kind")) for o, col in zip(options, columns)), "OPTION_IDENTITY")
            require(all(type(o["votes"]) is int and o["votes"] >= 0 for o in options), "NULL_OR_INVALID_OPTION")
            units[key] = {"base_snapshot": snapshot, "base_vector": [o["votes"] for o in options], "delta_vector": [0] * 17, "delta_total": 0, "restoration_evidence": []}
        require(sum(x["base_snapshot"]["identity"]["unit_kind"] == "ORDINARY_SECTION" for x in units.values()) == 105, "ORDINARY_COVERAGE")
        require(sum(x["base_snapshot"]["identity"]["unit_kind"] == "SPECIAL_SECTION_ROW" for x in units.values()) == 1, "SPECIAL_COVERAGE")
        for rule in manifest["restorations"] + manifest["exclusions"]:
            require(rule["unit_key"] in units, "RESTORATION_UNIT_ABSENT")
            unit = units[rule["unit_key"]]
            matches = [c for c in unit["base_snapshot"]["cas_evidence"] if c["original_identity"].get("ACTA_CASILLA-MEC") == rule["acta_literal"]]
            require(len(matches) == 1, "CAS_ABSENT_OR_AMBIGUOUS")
            cas = matches[0]
            require(cas["original_identity"].get("SECCION") == rule["unit_key"].split(":", 1)[1] and cas["original_identity"].get("ID_MUNICIPIO") == "3", "CAS_IDENTITY")
            require(cas["source_line"] == rule["source_line"] and cas["raw_line_sha256"] == rule["raw_line_sha256"], "CAS_ROW_HASH")
            require(cas["TRIBUNAL"] == "ANULADA" and cas["total_votes"] == rule["total"] and cas["total_raw"] == str(rule["total"]), "CAS_RAW_STATUS")
            if rule not in manifest["restorations"]:
                continue
            opts = sorted(cas["options"], key=lambda c: c["ordinal"])
            require(len(opts) == 17 and all(all(o.get(k) == col[k] for k in ("ordinal", "raw_column", "option_kind")) for o, col in zip(opts, columns)), "CAS_OPTION_IDENTITY")
            require(all(type(o["votes"]) is int and o["votes"] == v and o["raw_value"] == str(v) for o, v in zip(opts, rule["votes"])), "CAS_VECTOR_MISMATCH")
            unit["delta_vector"] = [a + b for a, b in zip(unit["delta_vector"], rule["votes"])]
            unit["delta_total"] += rule["total"]
            unit["restoration_evidence"].append(deepcopy(rule))
        require(sum(u["base_snapshot"]["result"]["total_votes"] for u in units.values()) == manifest["base_total"], "BASE_TOTAL_MISMATCH")
        require([sum(u["base_vector"][i] for u in units.values()) for i in range(17)] == manifest["base_vector"], "BASE_VECTOR_MISMATCH")
        for unit in units.values():
            vector = [a + b for a, b in zip(unit["base_vector"], unit["delta_vector"])]
            total = unit["base_snapshot"]["result"]["total_votes"] + unit["delta_total"]
            def check(values, control):
                valid = sum(v for v, col in zip(values, columns) if col["option_kind"] in ("PARTY", "COALITION_COMBINATION", "INDEPENDENT"))
                subtotal = sum(v for v, col in zip(values, columns) if col["option_kind"] != "VALID_VOTE_TOTAL")
                aux = [v for v, col in zip(values, columns) if col["option_kind"] == "VALID_VOTE_TOTAL"]
                require(aux == [valid] and subtotal == control, "UNIT_ARITHMETIC")
            check(unit["base_vector"], unit["base_snapshot"]["result"]["total_votes"])
            check(vector, total)
            unit["derived_result"] = {"total_votes": total, "options": [dict(col, votes=v) for col, v in zip(columns, vector)], "value_origin": "JUDICIAL_DERIVATION", "nominal_list_origin": "UNCHANGED_BASE_SNAPSHOT"}
        require([sum(u["derived_result"]["options"][i]["votes"] for u in units.values()) for i in range(17)] == manifest["derived_vector"], "DERIVED_VECTOR_MISMATCH")
        require(sum(u["derived_result"]["total_votes"] for u in units.values()) == manifest["derived_total"], "DERIVED_TOTAL_MISMATCH")
        require(sum(u["delta_total"] != 0 for u in units.values()) == 4, "DELTA_SCOPE")
        payload = {"contract": manifest["contract"], "manifest": manifest, "manifest_sha256": expected_manifest_sha256, "source_provenance": source_provenance, "units": units}
        self.candidate_id = manifest["candidate_label"] + ":" + digest(payload)
        self._bytes = canonical(payload)
        self.generated_at = datetime.now(timezone.utc).isoformat()

    def read(self, request: ReadRequest, *, candidate_id: str):
        response = {"status": "NO_RELEASE_SELECTED", "purpose": request.purpose, "metric_scope": request.metric_scope, "data": None, "candidate_id": candidate_id, "selection_status": "UNDECIDED", "certification_status": "NOT_CERTIFIED", "winner": None, "margin": None}
        if request.purpose != "AUDIT":
            return response
        if candidate_id != self.candidate_id or request.series != self.series:
            response["status"] = "DERIVED_IDENTITY_MISMATCH"
            return response
        if request.metric_scope != "RESULT":
            response["status"] = "DERIVED_METRIC_NOT_SUPPORTED"
            return response
        payload = json.loads(self._bytes)
        if request.release_id is not None and request.release_id != payload["source_provenance"]["release_id"]:
            response["status"] = "DERIVED_IDENTITY_MISMATCH"
            return response
        unit = payload["units"].get(request.unit_key)
        if unit is None or unit["base_snapshot"]["identity"]["unit_kind"] != request.unit_kind:
            response["status"] = "UNIT_OUTSIDE_DERIVED_SCOPE"
            return response
        response.update(status="AUDIT_JUDICIAL_DERIVED_CANDIDATE", data=unit, provenance={"source": payload["source_provenance"], "manifest_sha256": payload["manifest_sha256"], "judicial_refs": payload["manifest"]["judicial_refs"], "generated_at": self.generated_at, "candidate_content_sha256": hashlib.sha256(self._bytes).hexdigest(), "authority": "HEYTI_DERIVATION_NOT_AUTHORITY_RELEASE"})
        return response
