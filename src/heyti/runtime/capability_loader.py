import importlib.util
import inspect
from collections.abc import Callable, Mapping
from pathlib import Path
from types import ModuleType

from heyti.capabilities.base import Capability
from heyti.registry.registry import CapabilityRegistry


CapabilityFactory = Callable[[], Capability]


class CapabilityLoader:
    """
    Responsable de descubrir, cargar y registrar
    capabilities disponibles para HEYTI Runtime.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
        capability_factories: (
            Mapping[str, CapabilityFactory] | None
        ) = None,
    ) -> None:
        self.registry = registry
        self.capability_factories = dict(
            capability_factories or {}
        )
        self.loaded_capabilities: list[Capability] = []

        if not all(
            isinstance(capability_id, str)
            and capability_id
            and callable(factory)
            for capability_id, factory
            in self.capability_factories.items()
        ):
            raise TypeError(
                "capability_factories debe asociar "
                "identificadores no vacíos con fábricas ejecutables"
            )

    def _is_valid_capability(self, path: Path) -> bool:
        """
        Determina si una ruta contiene la estructura mínima
        de una capability de HEYTI.
        """
        if not path.is_dir():
            return False

        if not (path / "__init__.py").is_file():
            return False

        implementation_files = [
            file
            for file in path.glob("*.py")
            if file.name != "__init__.py"
        ]

        return bool(implementation_files)

    def _scan_directories(
        self,
        root_path: Path,
    ) -> list[Path]:
        """
        Examina los subdirectorios inmediatos de una ruta y devuelve
        únicamente aquellos que cumplen la estructura mínima de una
        capability de HEYTI.
        """
        if not root_path.is_dir():
            return []

        capability_directories = [
            path
            for path in root_path.iterdir()
            if self._is_valid_capability(path)
        ]

        return sorted(capability_directories)

    def discover(
        self,
        root_path: Path,
    ) -> list[Path]:
        """
        Descubre capabilities válidas dentro de una ruta raíz
        y devuelve las rutas encontradas.
        """
        return self._scan_directories(root_path)

    def _load_module(
        self,
        module_path: Path,
    ) -> ModuleType:
        """
        Carga dinámicamente un módulo Python desde una ruta de archivo.
        """
        module_name = (
            f"_heyti_dynamic_"
            f"{module_path.parent.name}_"
            f"{module_path.stem}"
        )

        specification = importlib.util.spec_from_file_location(
            module_name,
            module_path,
        )

        if (
            specification is None
            or specification.loader is None
        ):
            raise ImportError(
                "No fue posible crear la especificación "
                f"del módulo: {module_path}"
            )

        module = importlib.util.module_from_spec(
            specification
        )
        specification.loader.exec_module(module)

        return module

    def _find_capability_class(
        self,
        module: ModuleType,
    ) -> type[Capability]:
        """
        Localiza dentro de un módulo una clase concreta
        que implemente el contrato Capability.
        """
        for _, candidate in inspect.getmembers(
            module,
            inspect.isclass,
        ):
            if candidate is Capability:
                continue

            if not issubclass(candidate, Capability):
                continue

            if inspect.isabstract(candidate):
                continue

            if candidate.__module__ != module.__name__:
                continue

            return candidate

        raise LookupError(
            "No se encontró una clase Capability válida "
            f"en el módulo {module.__name__}"
        )

    def _instantiate_capability(
        self,
        capability_class: type[Capability],
        capability_name: str | None = None,
    ) -> Capability:
        """
        Crea una instancia ejecutable de una clase Capability.

        Cuando existe una fábrica para el identificador descubierto,
        delega en ella la composición de dependencias.
        """
        factory = (
            self.capability_factories.get(capability_name)
            if capability_name is not None
            else None
        )

        capability = (
            factory()
            if factory is not None
            else capability_class()
        )

        if not isinstance(capability, Capability):
            raise TypeError(
                "La fábrica debe devolver una instancia "
                "de Capability"
            )

        return capability

    def _register_capability(
        self,
        capability_directory: Path,
        capability_instance: Capability,
    ) -> None:
        """
        Registra una instancia de Capability utilizando
        el nombre de su directorio como identificador.
        """
        capability_name = capability_directory.name

        self.registry.register(
            capability_name,
            capability_instance,
        )

    def _load_capability_directory(
        self,
        capability_directory: Path,
    ) -> Capability:
        """
        Localiza, carga, instancia y registra la primera
        Capability ejecutable declarada en un directorio.
        """
        python_files = sorted(
            file_path
            for file_path
            in capability_directory.glob("*.py")
            if file_path.name != "__init__.py"
        )

        for module_path in python_files:
            module = self._load_module(module_path)

            try:
                capability_class = (
                    self._find_capability_class(module)
                )
            except LookupError:
                continue

            capability_instance = (
                self._instantiate_capability(
                    capability_class,
                    capability_name=(
                        capability_directory.name
                    ),
                )
            )

            self._register_capability(
                capability_directory,
                capability_instance,
            )

            return capability_instance

        raise LookupError(
            "No se encontró una implementación ejecutable "
            f"de Capability en {capability_directory}"
        )

    def load_all(
        self,
        root_directory: Path,
    ) -> list[Capability]:
        """
        Descubre, carga y registra todas las capabilities
        ejecutables disponibles en el directorio raíz.
        """
        capability_directories = self.discover(
            root_directory
        )

        loaded_instances: list[Capability] = []

        for capability_directory in capability_directories:
            try:
                capability_instance = (
                    self._load_capability_directory(
                        capability_directory
                    )
                )
            except LookupError:
                continue

            loaded_instances.append(
                capability_instance
            )

        self.loaded_capabilities = loaded_instances

        return list(self.loaded_capabilities)
