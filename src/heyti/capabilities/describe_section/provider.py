from heyti.capabilities.describe_section.models import (
    SectionDescription,
)


class DescribeSectionProvider:
    """
    Proveedor inicial de información para DescribeSection.

    Esta primera versión construye el modelo raíz sin acceder
    todavía a una fuente de datos externa.
    """

    def get_section(
        self,
        section_id: str,
    ) -> SectionDescription:
        description = SectionDescription()
        description.section_id = section_id

        return description