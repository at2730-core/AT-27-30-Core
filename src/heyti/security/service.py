from heyti.security.authorization import (
    AuthorizationEvaluator,
)
from heyti.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    AuthorizationResource,
)


class AuthorizationService:
    def __init__(
        self,
        source,
        evaluator=None,
    ):
        if source is None:
            raise TypeError(
                "source es obligatorio"
            )

        if not callable(
            getattr(source, "identity", None)
        ):
            raise TypeError(
                "source debe proporcionar identity"
            )

        if not callable(
            getattr(source, "grants", None)
        ):
            raise TypeError(
                "source debe proporcionar grants"
            )

        if evaluator is None:
            evaluator = AuthorizationEvaluator()

        if not callable(
            getattr(evaluator, "evaluate", None)
        ):
            raise TypeError(
                "evaluator debe proporcionar evaluate"
            )

        self._source = source
        self._evaluator = evaluator

    def authorize(
        self,
        *,
        user_id: int,
        session_id: str,
        permission_code: str,
        resource: AuthorizationResource,
    ) -> AuthorizationDecision:
        identity = self._source.identity(
            user_id=user_id,
            session_id=session_id,
        )

        grants = ()

        if identity is not None and identity.active:
            grants = self._source.grants(
                identity.role
            )

        request = AuthorizationRequest(
            permission_code=permission_code,
            session_id=session_id,
            resource=resource,
            identity=identity,
        )

        return self._evaluator.evaluate(
            request,
            grants,
        )
