"""Explicit demonstration read, independent of versioned source selection."""
import re

PARTIES = ("PAN", "PRI", "PVEM", "MORENA")
CONTESTS = ("A", "DL", "DF", "G", "S", "P")


def describe_section_demo(source, payload):
    sid = payload.get("section_id")
    if set(payload) != {"operation", "section_id"} or not isinstance(sid, str) or not re.fullmatch(r"[1-9][0-9]*", sid):
        raise ValueError("La consulta de demostración requiere una sección positiva y sin parámetros electorales adicionales")
    response = {
        "contract": "HEYTI_UNIVERSE_RESPONSE", "version": "1.0",
        "capability_id": "describe_universe", "section_id": sid,
        "view": "SECTION_DEMO", "source_mode": "DEMO_MASTER", "provenance": dict(source.provenance),
        "modality": "UNSPECIFIED_IN_MASTER", "years": [],
    }
    # Same territorial gates as universe maps; no source read before authorization.
    if sid not in source.members or source.truth.get_section_truth(sid).content.get("publication_status") != "ALLOWED":
        return {**response, "status": "TERRITORIAL_BLOCKED"}
    if source.geometry.get_section_territorial(sid) is None:
        return {**response, "status": "GEOMETRY_UNAVAILABLE"}
    electoral = source.electoral.get_section_electoral(sid)
    if electoral is None:
        return {**response, "status": "NO_DATA"}
    if electoral.get("section_id") != sid:
        raise ValueError("Identidad electoral de demostración discordante")
    all_years = [electoral, *electoral.get("historical_elections", [])]
    years = []
    for year in (2018, 2021, 2024):
        matches = [e for e in all_years if e.get("election_year") == year]
        if len(matches) != 1:
            raise ValueError("Cobertura anual de demostración inválida")
        contests = matches[0]["contests"]
        years.append({"year": year, "contests": {
            cid: {"status": contests[cid]["data_status"],
                  "total": contests[cid]["total_votes"],
                  "nominal": contests[cid]["nominal_list"],
                  "votes": {p: contests[cid]["votes_by_tracked_party"][p] for p in PARTIES}}
            for cid in CONTESTS}})
    return {**response, "status": "DEMO_AVAILABLE", "years": years}
