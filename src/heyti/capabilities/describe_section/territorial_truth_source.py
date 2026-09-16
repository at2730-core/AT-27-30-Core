from heyti.audit.data_truth.section_truth import (
    resolve_section_truth,
)
from heyti.audit.data_truth.territorial_policy import (
    TerritorialClassification,
    TerritorialSectionPolicy,
)
from heyti.capabilities.describe_section.models import (
    SectionTruthSnapshot,
    SectionWarning,
)


class TerritorialSectionTruthSource:
    """
    Adapta una clasificación territorial auditada al contrato
    requerido por DescribeSectionProvider.

    No consulta fuentes crudas y no modifica la clasificación
    ni la política recibidas.
    """

    def __init__(
        self,
        classification: TerritorialClassification,
        policy: TerritorialSectionPolicy,
    ) -> None:
        if not isinstance(
            classification,
            TerritorialClassification,
        ):
            raise TypeError(
                "classification debe ser "
                "TerritorialClassification"
            )

        if not isinstance(
            policy,
            TerritorialSectionPolicy,
        ):
            raise TypeError(
                "policy debe ser TerritorialSectionPolicy"
            )

        self.classification = classification
        self.policy = policy

    def get_section_truth(
        self,
        section_id: str,
    ) -> SectionTruthSnapshot:
        resolution = resolve_section_truth(
            section_id=section_id,
            classification=self.classification,
            policy=self.policy,
        )

        warning = self._build_warning(resolution)

        warnings = (
            (warning,)
            if warning is not None
            else ()
        )

        return SectionTruthSnapshot(
            content=resolution.to_dict(),
            warnings=warnings,
        )

    @staticmethod
    def _build_warning(
        resolution,
    ) -> SectionWarning | None:
        code = resolution.warning_code
        message = resolution.warning_message

        if code is None and message is None:
            return None

        if not code or not message:
            raise ValueError(
                "La resolución contiene una advertencia incompleta"
            )

        return SectionWarning(
            code=code,
            message=message,
        )
