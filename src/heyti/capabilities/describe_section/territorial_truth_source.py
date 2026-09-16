from heyti.audit.data_truth.contracts import (
    PUBLICATION_ALLOWED,
    TRUTH_OBSERVED,
)
from heyti.audit.data_truth.section_truth import (
    CLASSIFICATION_REQUIRES_REPOSITORY_CONFIRMATION,
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


CLASSIFICATION_CURRENT_TERRITORIAL_SECTION = (
    "CURRENT_TERRITORIAL_SECTION"
)
CONFIRMATION_MASTER_AND_GEOMETRY = (
    "MASTER_AND_GEOMETRY_INTERSECTION"
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
        current_section_ids: tuple[int, ...] = (),
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

        if not isinstance(current_section_ids, tuple):
            raise TypeError(
                "current_section_ids debe ser tuple"
            )

        if not all(
            isinstance(section_id, int)
            and not isinstance(section_id, bool)
            and section_id > 0
            for section_id in current_section_ids
        ):
            raise ValueError(
                "current_section_ids debe contener "
                "exclusivamente enteros positivos"
            )

        self.classification = classification
        self.policy = policy
        self.current_section_ids = frozenset(
            current_section_ids
        )

    def get_section_truth(
        self,
        section_id: str,
    ) -> SectionTruthSnapshot:
        resolution = resolve_section_truth(
            section_id=section_id,
            classification=self.classification,
            policy=self.policy,
        )

        if (
            resolution.classification
            == CLASSIFICATION_REQUIRES_REPOSITORY_CONFIRMATION
            and resolution.section_id
            in self.current_section_ids
        ):
            content = resolution.to_dict()
            content.update(
                {
                    "classification": (
                        CLASSIFICATION_CURRENT_TERRITORIAL_SECTION
                    ),
                    "truth_status": TRUTH_OBSERVED,
                    "publication_status": PUBLICATION_ALLOWED,
                    "warning_code": None,
                    "warning_message": None,
                    "confirmation_basis": (
                        CONFIRMATION_MASTER_AND_GEOMETRY
                    ),
                }
            )

            return SectionTruthSnapshot(
                content=content,
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
