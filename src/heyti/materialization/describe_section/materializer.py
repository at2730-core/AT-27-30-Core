from copy import deepcopy
from heyti.capabilities.describe_section.models import (
    SectionDescription,
)

from heyti.materialization.base import Materializer
from heyti.materialization.context import MaterializationContext
from heyti.materialization.contracts import (
    HeytiResponseContract,
    ResponseBlock,
    ResponseTrace,
)
from heyti.materialization.errors import (
    MaterializationError,
    UnsupportedContractVersionError,
)


class DescribeSectionMaterializer(Materializer):
    """
    Materializa SectionDescription hacia HEYTI Response Contract v1.0.

    No ejecuta la capability.
    No consulta fuentes externas.
    No crea significado cognitivo nuevo.
    """

    SUPPORTED_VERSION = "1.0"
    CONTRACT_NAME = "HEYTI_RESPONSE"

    def materialize(
        self,
        cognitive_result: SectionDescription,
        context: MaterializationContext,
    ) -> HeytiResponseContract:
        if not isinstance(cognitive_result, SectionDescription):
            raise MaterializationError(
                "DescribeSectionMaterializer requiere "
                "un SectionDescription"
            )

        if context.contract_version != self.SUPPORTED_VERSION:
            raise UnsupportedContractVersionError(
                f"Versión contractual no soportada: "
                f"{context.contract_version}"
            )

        blocks: list[ResponseBlock] = []

        if cognitive_result.section_id is not None:
            blocks.append(
                ResponseBlock(
                    type="text",
                    role="section_identity",
                    content={
                        "section_id": cognitive_result.section_id,
                    },
                )
            )

        domain_fields = (
            "territorial",
            "electoral",
            "socioeconomic",
            "field",
            "security",
            "risk",
        )

        for field_name in domain_fields:
            value = getattr(cognitive_result, field_name)

            if value is not None:
                blocks.append(
                    ResponseBlock(
                        type="domain",
                        role=field_name,
                        content=deepcopy(value),
                    )
            )

        if cognitive_result.recommendations:
            blocks.append(
                ResponseBlock(
                    type="finding",
                    role="recommendations",
                    content=deepcopy(cognitive_result.recommendations),
                )
            )

        return HeytiResponseContract(
            contract=self.CONTRACT_NAME,
            version=context.contract_version,
            capability_id=context.capability_id,
            status="success",
            blocks=blocks,
            trace=ResponseTrace(
                request_id=context.request_id,
                session_id=context.session_id,
                execution_id=context.execution_id,
                knowledge_version=context.knowledge_version,
            ),
        )
