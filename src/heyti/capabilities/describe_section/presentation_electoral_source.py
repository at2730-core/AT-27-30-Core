"""Unselected presentation composition. No credentials, policy or selection inferred."""
import os
from pathlib import Path
from heyti.capabilities.describe_section.versioned_electoral_source import ReleaseRegistry, VersionedElectoralSource
from heyti.capabilities.describe_section.staging_electoral_repository import StagingCutBinding, StagingElectoralRepository


def _connect_readonly():
    database = os.environ.get("HEYTI_ELECTORAL_AUDIT_DB")
    if not database:
        raise RuntimeError("HEYTI_ELECTORAL_AUDIT_DB_NOT_CONFIGURED")
    import psycopg2
    return psycopg2.connect(dbname=database, options="-c default_transaction_read_only=on")


def build_unselected_electoral_source(matrix_path: Path, connection_factory=None):
    # No policy is installed here. Presentation therefore returns before DB access.
    registry = ReleaseRegistry.from_matrix(matrix_path) if matrix_path.is_file() else ReleaseRegistry(())
    bindings = [StagingCutBinding(
        r.release_id, "SOURCE_AS_PUBLISHED_UNVERIFIED_DATE",
        "Explicit unselected presentation wiring; not electoral certification",
    ) for r in registry.releases]
    repository = StagingElectoralRepository(registry, connection_factory or _connect_readonly, bindings)
    return VersionedElectoralSource(registry, repository)
