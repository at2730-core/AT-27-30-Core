"""Presentation-only electoral request for an ordinary DescribeSection unit."""

from typing import Any
from heyti.capabilities.describe_section.versioned_electoral_source import ReadRequest, SeriesKey


def ordinary_section_key(section_id: Any) -> str:
    if type(section_id) not in (str, int):
        raise ValueError("Ordinary section must be a positive integer identity")
    literal = str(section_id).strip()
    if not literal.isascii() or not literal.isdecimal() or int(literal) <= 0:
        raise ValueError("DescribeSection cannot address SEC0 or special acts")
    return "SEC:" + str(int(literal))


def parse_electoral_query(section_id: Any, query: dict[str, Any]) -> ReadRequest:
    if not isinstance(query, dict):
        raise TypeError("electoral_query must be a dict")
    required = {"year", "type", "modality"}
    optional = {"release_id", "policy_id", "metric_scope"}
    if not required <= query.keys() or query.keys() - required - optional:
        raise ValueError("Explicit year/type/modality required; unsupported query fields")
    for key in ("release_id", "policy_id"):
        value = query.get(key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(key + " must be a nonblank string or null")
    return ReadRequest(
        SeriesKey(query["year"], query["type"], query["modality"]),
        "ORDINARY_SECTION", ordinary_section_key(section_id),
        purpose="PRESENTATION", release_id=query.get("release_id"),
        policy_id=query.get("policy_id"), metric_scope=query.get("metric_scope", "RESULT"),
    )


def validate_section_request(section_id: Any, request: ReadRequest) -> None:
    if not isinstance(request, ReadRequest):
        raise TypeError("electoral_request must be ReadRequest")
    if (request.purpose != "PRESENTATION" or request.unit_kind != "ORDINARY_SECTION"
            or request.unit_key != ordinary_section_key(section_id)):
        raise ValueError("Electoral request must match the ordinary section and presentation purpose")
