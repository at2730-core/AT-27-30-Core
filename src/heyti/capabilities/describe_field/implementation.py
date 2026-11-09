import hashlib
import math

from heyti.capabilities.base import Capability


CONTRACT = "HEYTI_FIELD_RESPONSE"
VERSION = "1.0"
PRIVACY_MODE = "PERSONAL_DATA_REDACTED"


def _anonymous_reference(actor_uuid):
    if not isinstance(actor_uuid, str) or not actor_uuid.strip():
        raise ValueError("actor_uuid inv?lido")

    digest = hashlib.sha256(
        actor_uuid.strip().encode("utf-8")
    ).hexdigest()

    return f"FIELD-{digest[:16].upper()}"


def _public_point(record):
    section_code = str(record.get("section_code", "")).strip()
    role_code = str(
        record.get("role_code") or "UNASSIGNED"
    ).strip().upper()

    if not section_code:
        raise ValueError("section_code inv?lido")

    longitude = record.get("longitude")
    latitude = record.get("latitude")

    if longitude is None and latitude is None:
        geometry_status = "NO_GEOMETRY"
    elif longitude is None or latitude is None:
        raise ValueError("Geometr?a incompleta")
    else:
        longitude = float(longitude)
        latitude = float(latitude)

        if (
            not math.isfinite(longitude)
            or not math.isfinite(latitude)
            or not -180 <= longitude <= 180
            or not -90 <= latitude <= 90
        ):
            raise ValueError("Coordenadas inv?lidas")

        geometry_status = "AVAILABLE"

    return {
        "actor_ref": _anonymous_reference(
            str(record.get("actor_uuid", ""))
        ),
        "section_code": section_code,
        "role_code": role_code,
        "geometry_status": geometry_status,
        "longitude": longitude,
        "latitude": latitude,
    }


class DescribeFieldCapability(Capability):
    def __init__(self, source=None):
        self.source = source

    def execute(self, session=None, payload=None):
        if self.source is None:
            raise ValueError(
                "La fuente de Campo no est? configurada"
            )

        if not isinstance(payload, dict):
            raise ValueError(
                "La consulta de Campo debe ser un objeto"
            )

        operation = payload.get("operation")

        base = {
            "contract": CONTRACT,
            "version": VERSION,
            "capability_id": "describe_field",
            "operation": operation,
            "privacy": {
                "mode": PRIVACY_MODE,
                "excluded_fields": [
                    "full_name",
                    "phone",
                    "address",
                    "observations",
                    "promoter_pin",
                    "actor_uuid",
                ],
            },
        }

        if operation == "summary":
            summary = self.source.summary()

            total = int(summary["total_records"])
            geolocated = int(summary["geolocated_records"])
            without_geometry = int(
                summary["records_without_geometry"]
            )
            unassigned = int(
                summary.get("unassigned_records", 0)
            )
            by_role = {
                str(role): int(count)
                for role, count
                in summary["by_role"].items()
            }

            if (
                min(
                    total,
                    geolocated,
                    without_geometry,
                    unassigned,
                    *by_role.values(),
                ) < 0
                or geolocated + without_geometry != total
                or sum(by_role.values()) + unassigned != total
            ):
                raise ValueError(
                    "Resumen de Campo inconsistente"
                )

            return {
                **base,
                "summary": {
                    "total_records": total,
                    "geolocated_records": geolocated,
                    "records_without_geometry": (
                        without_geometry
                    ),
                    "unassigned_records": unassigned,
                    "by_role": dict(sorted(by_role.items())),
                },
            }

        if operation != "map":
            raise ValueError(
                "Operaci?n de Campo no soportada"
            )

        section_code = payload.get("section_code")

        if section_code is not None:
            section_code = str(section_code).strip()
            if not section_code:
                raise ValueError(
                    "section_code no puede estar vac?o"
                )

        points = [
            _public_point(record)
            for record in self.source.map_points(
                section_code=section_code
            )
        ]

        geolocated = sum(
            point["geometry_status"] == "AVAILABLE"
            for point in points
        )

        return {
            **base,
            "filter": {
                "section_code": section_code,
            },
            "points": points,
            "coverage": {
                "records": len(points),
                "geolocated_records": geolocated,
                "records_without_geometry": (
                    len(points) - geolocated
                ),
            },
        }
