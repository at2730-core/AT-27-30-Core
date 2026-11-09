import unittest

from heyti.capabilities.describe_field.implementation import (
    DescribeFieldCapability,
)


class FakeFieldSource:
    def summary(self):
        return {
            "total_records": 45,
            "geolocated_records": 44,
            "records_without_geometry": 1,
            "unassigned_records": 0,
            "by_role": {
                "SIMPATIZANTE": 25,
                "LIDER": 4,
                "ADVERSARIO": 5,
                "OBSERVADOR": 5,
                "REP_CASILLA": 3,
                "REP_GENERAL": 3,
            },
        }

    def map_points(self, section_code=None):
        records = [
            {
                "actor_uuid": "actor-example-one",
                "section_code": "1001",
                "role_code": "LIDER",
                "longitude": -101.68,
                "latitude": 21.12,
                "full_name": "NO DEBE SALIR",
                "phone": "NO DEBE SALIR",
                "address": "NO DEBE SALIR",
            },
            {
                "actor_uuid": "actor-example-two",
                "section_code": "1002",
                "role_code": "SIMPATIZANTE",
                "longitude": None,
                "latitude": None,
                "observations": "NO DEBE SALIR",
            },
        ]

        if section_code is None:
            return records

        return [
            record
            for record in records
            if record["section_code"] == section_code
        ]


class DescribeFieldTests(unittest.TestCase):
    def setUp(self):
        self.capability = DescribeFieldCapability(
            FakeFieldSource()
        )

    def test_summary_preserves_certified_counts(self):
        response = self.capability.execute(
            payload={"operation": "summary"}
        )

        self.assertEqual(
            response["contract"],
            "HEYTI_FIELD_RESPONSE",
        )
        self.assertEqual(
            response["summary"]["total_records"],
            45,
        )
        self.assertEqual(
            sum(
                response["summary"]["by_role"].values()
            ),
            45,
        )

    def test_map_redacts_personal_data(self):
        response = self.capability.execute(
            payload={"operation": "map"}
        )

        self.assertEqual(
            response["privacy"]["mode"],
            "PERSONAL_DATA_REDACTED",
        )
        self.assertEqual(
            response["coverage"]["records"],
            2,
        )

        serialized = repr(response["points"]).lower()

        for prohibited in [
            "no debe salir",
            "full_name",
            "phone",
            "address",
            "observations",
            "actor_uuid",
        ]:
            self.assertNotIn(
                prohibited,
                serialized,
            )

        self.assertTrue(
            response["points"][0]["actor_ref"].startswith(
                "FIELD-"
            )
        )

    def test_missing_geometry_is_explicit(self):
        response = self.capability.execute(
            payload={
                "operation": "map",
                "section_code": "1002",
            }
        )

        self.assertEqual(
            response["coverage"],
            {
                "records": 1,
                "geolocated_records": 0,
                "records_without_geometry": 1,
            },
        )
        self.assertEqual(
            response["points"][0]["geometry_status"],
            "NO_GEOMETRY",
        )
        self.assertIsNone(
            response["points"][0]["longitude"]
        )
        self.assertIsNone(
            response["points"][0]["latitude"]
        )


if __name__ == "__main__":
    unittest.main()
