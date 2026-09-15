from heyti.audit.data_truth.territorial_policy import (
    TerritorialSectionPolicy,
)


GUANAJUATO_2023_POLICY_ID = "GUANAJUATO_2023"
GUANAJUATO_2023_POLICY_VERSION = "1.0"

GUANAJUATO_2023_EVIDENCE = (
    "docs/architecture/data/"
    "HEYTI_Data_Truth_Governance_v1.0.md"
)

GUANAJUATO_2023_CERTIFIED_LINEAGE = {
    343: tuple(range(3290, 3300)),
    1059: tuple(range(3300, 3308)),
    1110: tuple(range(3308, 3314)),
    1634: tuple(range(3278, 3284)),
    1647: tuple(range(3284, 3290)),
}

GUANAJUATO_2023_UNRESOLVED_HISTORICAL = (
    145,
    315,
    336,
    878,
    892,
    899,
    966,
    1078,
    1099,
    1268,
    1285,
    1477,
    1490,
    1494,
    1495,
    1509,
    1614,
    1642,
    1681,
    1687,
    2190,
    2193,
    2477,
    2514,
    2860,
    2907,
)

GUANAJUATO_2023_SYNTHETIC_CANDIDATES = (
    9001,
    9002,
    9003,
    9004,
    9005,
    9006,
    9007,
    9008,
    9009,
    9010,
    9011,
    9012,
    9013,
    9014,
    9015,
    9016,
    9017,
    9018,
    9019,
    9020,
    9021,
    9022,
    9023,
    9024,
    9025,
    9026,
    9027,
    9028,
    9029,
    9030,
    9031,
    9032,
    9033,
    9034,
    9035,
    9036,
    9037,
    9038,
    9039,
    9040,
    9041,
    9043,
    9044,
    9045,
    9046,
)

GUANAJUATO_2023_V1 = TerritorialSectionPolicy(
    policy_id=GUANAJUATO_2023_POLICY_ID,
    version=GUANAJUATO_2023_POLICY_VERSION,
    certified_lineage=GUANAJUATO_2023_CERTIFIED_LINEAGE,
    unresolved_historical=(
        GUANAJUATO_2023_UNRESOLVED_HISTORICAL
    ),
    synthetic_candidates=(
        GUANAJUATO_2023_SYNTHETIC_CANDIDATES
    ),
    evidence_reference=GUANAJUATO_2023_EVIDENCE,
)
