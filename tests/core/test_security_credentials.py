import pytest

from heyti.security.credentials import (
    Argon2CredentialHasher,
    PasswordVerification,
)


def test_hash_password_generates_argon2id():
    hasher = Argon2CredentialHasher()

    credential_hash = hasher.hash_password(
        "Una-clave-segura-2026"
    )

    assert credential_hash.startswith(
        "$argon2id$"
    )
    assert "Una-clave-segura-2026" not in (
        credential_hash
    )


def test_verify_password_accepts_correct_password():
    hasher = Argon2CredentialHasher()
    credential_hash = hasher.hash_password(
        "Una-clave-segura-2026"
    )

    result = hasher.verify_password(
        credential_hash,
        "Una-clave-segura-2026",
    )

    assert result == PasswordVerification(
        valid=True,
        needs_rehash=False,
    )


def test_verify_password_rejects_wrong_password():
    hasher = Argon2CredentialHasher()
    credential_hash = hasher.hash_password(
        "Una-clave-segura-2026"
    )

    result = hasher.verify_password(
        credential_hash,
        "Clave-incorrecta",
    )

    assert result == PasswordVerification(
        valid=False,
        needs_rehash=False,
    )


def test_verify_password_rejects_invalid_hash():
    hasher = Argon2CredentialHasher()

    result = hasher.verify_password(
        "$argon2id$hash-incompleto",
        "Una-clave-segura-2026",
    )

    assert result == PasswordVerification(
        valid=False,
        needs_rehash=False,
    )


@pytest.mark.parametrize(
    "password",
    [
        None,
        123,
        b"binary-password",
    ],
)
def test_password_must_be_text(password):
    hasher = Argon2CredentialHasher()

    with pytest.raises(TypeError):
        hasher.hash_password(password)


def test_password_cannot_be_empty():
    hasher = Argon2CredentialHasher()

    with pytest.raises(
        ValueError,
        match="password no puede estar vacio",
    ):
        hasher.hash_password("")


@pytest.mark.parametrize(
    "credential_hash",
    [
        None,
        123,
    ],
)
def test_credential_hash_must_be_text(
    credential_hash,
):
    hasher = Argon2CredentialHasher()

    with pytest.raises(TypeError):
        hasher.verify_password(
            credential_hash,
            "Una-clave-segura-2026",
        )


def test_credential_hash_cannot_be_empty():
    hasher = Argon2CredentialHasher()

    with pytest.raises(
        ValueError,
        match=(
            "credential_hash no puede estar vacio"
        ),
    ):
        hasher.verify_password(
            "   ",
            "Una-clave-segura-2026",
        )


def test_rejects_incompatible_provider():
    with pytest.raises(TypeError):
        Argon2CredentialHasher(
            password_hasher=object()
        )
