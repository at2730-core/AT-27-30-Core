import pytest

from heyti.security.scope_assignment import (
    TerritorialScopeType,
)
from heyti.security.scope_profile import (
    TerritorialAccessProfile,
    TerritorialScopeProfile,
    TerritorialScopeProfileService,
)


def municipality_profile():
    return TerritorialScopeProfile(
        scope_id=2,
        scope_name="Municipio 20 - Leon",
        scope_type=(
            TerritorialScopeType.MUNICIPALITY
        ),
        municipality_id=20,
        municipality_code="20",
        municipality_name="Leon de los Aldama",
        section_count=787,
    )


def test_serializes_municipality_profile():
    profile = municipality_profile()

    assert profile.to_dict() == {
        "scope_id": 2,
        "name": "Municipio 20 - Leon",
        "type": "MUNICIPALITY",
        "municipality": {
            "municipality_id": 20,
            "code": "20",
            "name": "Leon de los Aldama",
        },
        "section_count": 787,
    }


def test_global_profile_has_global_access():
    scope = TerritorialScopeProfile(
        scope_id=1,
        scope_name="Acceso global",
        scope_type=TerritorialScopeType.GLOBAL,
        municipality_id=None,
        municipality_code=None,
        municipality_name=None,
        section_count=0,
    )

    profile = TerritorialAccessProfile(
        scopes=(scope,)
    )

    assert profile.global_access is True
    assert profile.to_dict() == {
        "global_access": True,
        "scopes": [
            {
                "scope_id": 1,
                "name": "Acceso global",
                "type": "GLOBAL",
                "municipality": None,
                "section_count": 0,
            }
        ],
    }


def test_municipality_profile_is_not_global():
    profile = TerritorialAccessProfile(
        scopes=(municipality_profile(),)
    )

    assert profile.global_access is False


def test_service_reads_active_scopes():
    expected = municipality_profile()

    class Source:
        def active_scopes(self, *, user_id):
            assert user_id == 4
            return (expected,)

    service = TerritorialScopeProfileService(
        Source()
    )

    result = service.profile(4)

    assert result.scopes == (expected,)
    assert result.global_access is False


def test_service_accepts_profile_without_scopes():
    class Source:
        def active_scopes(self, *, user_id):
            return ()

    result = TerritorialScopeProfileService(
        Source()
    ).profile(4)

    assert result == TerritorialAccessProfile(
        scopes=()
    )


@pytest.mark.parametrize(
    "user_id",
    [
        None,
        True,
        "4",
    ],
)
def test_service_rejects_invalid_user_id_type(
    user_id,
):
    class Source:
        def active_scopes(self, *, user_id):
            return ()

    service = TerritorialScopeProfileService(
        Source()
    )

    with pytest.raises(TypeError):
        service.profile(user_id)


def test_service_rejects_non_positive_user_id():
    class Source:
        def active_scopes(self, *, user_id):
            return ()

    service = TerritorialScopeProfileService(
        Source()
    )

    with pytest.raises(ValueError):
        service.profile(0)


def test_rejects_incompatible_source():
    with pytest.raises(TypeError):
        TerritorialScopeProfileService(object())


def test_municipality_requires_identity():
    with pytest.raises(
        ValueError,
        match="MUNICIPALITY requiere municipio",
    ):
        TerritorialScopeProfile(
            scope_id=2,
            scope_name="Leon",
            scope_type=(
                TerritorialScopeType.MUNICIPALITY
            ),
            municipality_id=None,
            municipality_code=None,
            municipality_name=None,
            section_count=787,
        )


def test_global_rejects_materialized_sections():
    with pytest.raises(
        ValueError,
        match="GLOBAL no materializa secciones",
    ):
        TerritorialScopeProfile(
            scope_id=1,
            scope_name="Global",
            scope_type=TerritorialScopeType.GLOBAL,
            municipality_id=None,
            municipality_code=None,
            municipality_name=None,
            section_count=1,
        )


def test_access_profile_rejects_duplicate_scopes():
    scope = municipality_profile()

    with pytest.raises(
        ValueError,
        match="alcances duplicados",
    ):
        TerritorialAccessProfile(
            scopes=(scope, scope)
        )
