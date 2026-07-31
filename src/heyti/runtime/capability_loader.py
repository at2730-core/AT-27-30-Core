import importlib.util
from pathlib import Path
from types import ModuleType
import inspect
from heyti.capabilities.base import Capability

from heyti.registry.registry import CapabilityRegistry

class CapabilityLoader:
    """
    Responsable de descubrir, cargar y registrar
    capabilities disponibles para HEYTI Runtime.
    """

    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry
        self.loaded_capabilities: list[Capability] = []

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

    def _scan_directories(self, root_path: Path) -> list[Path]:
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

    def discover(self, root_path: Path) -> list[Path]:
        """
        Descubre capabilities válidas dentro de una ruta raíz
        y devuelve las rutas encontradas.
        """
        return self._scan_directories(root_path)



    def _load_module(self, module_path: Path) -> ModuleType:
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

        if specification is None or specification.loader is None:
            raise ImportError(
                f"No fue posible crear la especificación del módulo: "
                f"{module_path}"
            )

        module = importlib.util.module_from_spec(specification)
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

            # Ignorar la clase base
            if candidate is Capability:
                continue

            # Debe heredar de Capability
            if not issubclass(candidate, Capability):
                continue

            # No debe ser abstracta
            if inspect.isabstract(candidate):
                continue

            # Debe estar definida en ESTE módulo
            if candidate.__module__ != module.__name__:
                continue

            return candidate

        raise LookupError(
            f"No se encontró una clase Capability válida "
            f"en el módulo {module.__name__}"
        )

    def _instantiate_capability(
        self,
        capability_class: type[Capability],
    ) -> Capability:
        """
        Crea una instancia ejecutable de una clase Capability.
        """
        return capability_class()

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
        Carga, instancia y registra una Capability
        desde un directorio válido.
        """
        implementation_files = sorted(
            file_path
            for file_path in capability_directory.glob("*.py")
            if file_path.name != "__init__.py"
        )

        if not implementation_files:
            raise FileNotFoundError(
                "No se encontró un archivo de implementación "
                f"en {capability_directory}"
            )

        module = self._load_module(
            implementation_files[0]
        )

        capability_class = self._find_capability_class(
            module
        )

        capability_instance = self._instantiate_capability(
            capability_class
        )

        self._register_capability(
            capability_directory,
            capability_instance,
        )

        return capability_instance

    def load_all(
        self,
        root_directory: Path,
    ) -> list[Capability]:
        """
        Descubre, carga y registra todas las capabilities
        válidas disponibles en el directorio raíz.
        """
        capability_directories = self.discover(
            root_directory
        )

        loaded_instances: list[Capability] = []

        for capability_directory in capability_directories:
            capability_instance = (
                self._load_capability_directory(
                    capability_directory
                )
            )

            loaded_instances.append(
                capability_instance
            )

        self.loaded_capabilities = loaded_instances

        return list(self.loaded_capabilities)