import json
import math
import unicodedata
from heyti.capabilities.describe_universe.municipalities import MUNICIPALITY_NAMES
from hashlib import sha256
from pathlib import Path
from heyti.capabilities.base import Capability

PARTIES = ("PAN", "PRI", "PVEM", "MORENA")
FIELDS = {"state": None, "municipality": "MUNICIPIO", "federal-district": "DISTRITO_F", "local-district": "DISTRITO_L"}


def tracked_outcome(contest):
    status = contest["data_status"]
    total = contest["total_votes"]
    votes = contest["votes_by_tracked_party"]
    if status == "NOT_CONTESTED":
        return "NOT_CONTESTED", None
    if status == "INCONSISTENT":
        return "INCONSISTENT", None
    if total == 0:
        return "ZERO_TOTAL", None
    if any(votes.get(p) is None for p in PARTIES) or total is None:
        return "NO_DATA", None
    if not math.isfinite(total) or total < 0 or any(not math.isfinite(votes[p]) or votes[p] < 0 for p in PARTIES) or sum(votes[p] for p in PARTIES) > total:
        return "INCONSISTENT", None
    maximum = max(votes.values())
    if maximum <= 0:
        return "NO_TRACKED_VOTES", None
    leaders = [p for p in PARTIES if votes[p] == maximum]
    return ("TIE", None) if len(leaders) > 1 else ("TRACKED_LEAD", leaders[0])


def abstention_outcome(contest):
    if contest['data_status'] == 'NOT_CONTESTED':
        return 'NOT_CONTESTED', None
    total, nominal = contest.get('total_votes'), contest.get('nominal_list')
    if total is None or nominal is None:
        return 'NO_DATA', None
    if (contest['data_status'] == 'INCONSISTENT' or not math.isfinite(total)
            or not math.isfinite(nominal) or nominal <= 0 or total < 0 or total > nominal):
        return 'INCONSISTENT', None
    percent = (nominal - total) * 100 / nominal
    band = 'ABS_LOW' if percent < 25 else 'ABS_MID' if percent < 50 else 'ABS_HIGH' if percent < 75 else 'ABS_VERY_HIGH'
    return band, percent


def concentration_outcome(contest):
    status, _ = tracked_outcome(contest)
    if status not in ('TRACKED_LEAD', 'TIE', 'NO_TRACKED_VOTES'):
        return status, None
    total = contest['total_votes']
    index = sum((contest['votes_by_tracked_party'][p] / total) ** 2 for p in PARTIES)
    return ('HHI_HIGH' if index >= .45 else 'HHI_MID' if index >= .30 else 'HHI_LOW'), index


class UniverseSource:
    """Uses the composed territorial/electoral sources; never authorizes by geometry alone."""
    def __init__(self, geometry_path, master_path, truth, geometry, electoral, master_only_unmapped):
        self.master_only_unmapped = master_only_unmapped
        self.truth, self.geometry, self.electoral = truth, geometry, electoral
        geo_bytes = Path(geometry_path).read_bytes()
        self.provenance = {"geometry_sha256": sha256(geo_bytes).hexdigest(), "master_sha256": sha256(Path(master_path).read_bytes()).hexdigest(), "territorial_policy": "GUANAJUATO_2023:1.0", "grouping_basis": "PROPERTIES_OF_CURRENT_GEOJSON", "electoral_scope": "TRACKED_PARTIES_ONLY", "electoral_validation": "AUDIT_PENDING"}
        features = json.loads(geo_bytes.decode("utf-8-sig"))["features"]
        self.members = {}
        for f in features:
            p = f["properties"]
            sid = str(int(p["SECCION"]))
            if sid in self.members:
                raise ValueError("Duplicate section in universe source")
            self.members[sid] = {field: str(int(p[field])) for field in FIELDS.values() if field}
        self.catalog = [{"level": "state", "id": "11", "label": "Guanajuato", "sections": len(self.members)}]
        for level, field in FIELDS.items():
            if field is None:
                continue
            counts = {}
            for p in self.members.values():
                counts[p[field]] = counts.get(p[field], 0) + 1
            name = {"municipality": "Municipio", "federal-district": "Distrito federal", "local-district": "Distrito local"}[level]
            self.catalog += [{"level": level, "id": key, "label": MUNICIPALITY_NAMES[key] if level == "municipality" else f"{name} {key}", "sections": count} for key, count in sorted(counts.items(), key=lambda pair: unicodedata.normalize("NFKD", MUNICIPALITY_NAMES[pair[0]]).encode("ascii", "ignore").decode().casefold() if level == "municipality" else int(pair[0]))]

    def query(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("La consulta debe ser un objeto")
        result = {"contract": "HEYTI_UNIVERSE_RESPONSE", "version": "1.0", "capability_id": "describe_universe", "provenance": dict(self.provenance)}
        if payload.get("operation") == "section-demo":
            from .section_demo import describe_section_demo
            return describe_section_demo(self, payload)
        if payload.get("operation") == "catalog":
            return {**result, "catalog": list(self.catalog)}
        if payload.get("operation") != "map":
            raise ValueError("Operación no soportada")
        metric = payload.get('metric', 'leaders')
        if metric not in ('leaders', 'abstention', 'concentration'):
            raise ValueError('Métrica no soportada')
        level, uid = payload.get("level"), payload.get("id")
        year, contest_id = payload.get("year"), payload.get("contest")
        universe = next((u for u in self.catalog if u["level"] == level and u["id"] == uid), None)
        if universe is None or type(year) is not int or year not in (2018, 2021, 2024) or contest_id not in ("A", "DL", "DF", "G", "S", "P"):
            raise ValueError("Universo, año o contienda inválidos")
        if metric == 'concentration' and year != 2024:
            raise ValueError('Concentración disponible solo para 2024')
        field = FIELDS[level]
        ids = [sid for sid, p in self.members.items() if field is None or p[field] == uid]
        sections, counts = [], {}
        trend = {y: {'year': y, 'valid_sections': 0, 'nominal': 0, 'votes': 0} for y in (2018, 2021, 2024)}
        aggregate = {'valid_sections': 0, 'total': 0, 'votes': dict.fromkeys(PARTIES, 0)}
        blocked = 0
        for sid in sorted(ids, key=int):
            truth = self.truth.get_section_truth(sid).content
            if truth.get("publication_status") != "ALLOWED":
                blocked += 1
                continue
            geom = self.geometry.get_section_territorial(sid)
            electoral = self.electoral.get_section_electoral(sid)
            if geom is None or electoral is None:
                blocked += 1
                continue
            election = electoral if year == electoral["election_year"] else next((e for e in electoral["historical_elections"] if e["election_year"] == year), None)
            if election is None:
                raise ValueError("Año no disponible en la fuente compuesta")
            contest = election["contests"][contest_id]
            status, leader = tracked_outcome(contest)
            abstention = None
            if metric == 'abstention':
                status, abstention = abstention_outcome(contest)
                leader = None
                for y, summary in trend.items():
                    e = electoral if y == electoral['election_year'] else next((e for e in electoral['historical_elections'] if e['election_year'] == y), None)
                    if e is None:
                        continue
                    c = e['contests'][contest_id]
                    _, value = abstention_outcome(c)
                    if value is not None:
                        summary['valid_sections'] += 1
                        summary['nominal'] += c['nominal_list']
                        summary['votes'] += c['total_votes']
            index = None
            if metric == 'concentration':
                status, index = concentration_outcome(contest)
                leader = None
                if index is not None:
                    aggregate['valid_sections'] += 1
                    aggregate['total'] += contest['total_votes']
                    for p in PARTIES:
                        aggregate['votes'][p] += contest['votes_by_tracked_party'][p]
            missing_reason = None
            if status == 'NO_DATA':
                missing_reason = 'TOTAL_OR_NOMINAL_MISSING' if metric == 'abstention' else 'TOTAL_MISSING' if contest['total_votes'] is None else 'TRACKED_BREAKDOWN_MISSING'
            key = leader if leader is not None else status
            counts[key] = counts.get(key, 0) + 1
            sections.append({"section_id": sid, "geometry": geom["geometry"], "crs": geom["crs"], "status": status, "leader": leader, "votes": contest["votes_by_tracked_party"], "total": contest["total_votes"], "missing_reason": missing_reason, **({"concentration": index} if metric == "concentration" else {}), **({"nominal": contest["nominal_list"], "abstention": abstention} if metric == "abstention" else {})})
        extra = {}
        if metric == 'abstention':
            for summary in trend.values():
                summary['abstention'] = (summary['nominal'] - summary['votes']) * 100 / summary['nominal'] if summary['nominal'] > 0 else None
            extra = {'metric': metric, 'trend': list(trend.values()), 'classification': 'FIXED_25_PERCENT_BANDS'}
        if metric == 'concentration':
            aggregate['index'] = sum((v / aggregate['total']) ** 2 for v in aggregate['votes'].values()) if aggregate['total'] else None
            aggregate['tracked_coverage'] = sum(aggregate['votes'].values()) / aggregate['total'] if aggregate['total'] else None
            extra = {'metric': metric, 'summary': aggregate, 'classification': 'PARTIAL_HHI_V1_THRESHOLDS'}
        return {**result, **extra, "universe": dict(universe), "year": year, "contest": contest_id, "sections": sections, "counts": counts, "coverage": {"geographic_sections": len(ids), "represented_sections": len(sections), "blocked_sections": blocked, "master_only_unmapped": self.master_only_unmapped}}


class DescribeUniverseCapability(Capability):
    def __init__(self, source=None):
        self.source = source

    def execute(self, session=None, payload=None):
        if self.source is None:
            raise ValueError("La fuente de universos no está configurada")
        return self.source.query(payload)
