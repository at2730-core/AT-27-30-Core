from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_loader import CapabilityLoader
from heyti.capabilities.base import Capability
from types import ModuleType
from pathlib import Path


def test_capability_loader_starts_without_loaded_capabilities():
    registry = CapabilityRegistry()

    loader = CapabilityLoader(registry=registry)

    assert loader.loaded_capabilities == []

def test_capability_loader_identifies_valid_capability_directory(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    capability_directory = tmp_path / "sample_capability"
    capability_directory.mkdir()

    (capability_directory / "__init__.py").touch()
    (capability_directory / "sample.py").touch()

    assert loader._is_valid_capability(capability_directory) is True


def test_capability_loader_rejects_directory_without_init_file(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    capability_directory = tmp_path / "invalid_capability"
    capability_directory.mkdir()

    (capability_directory / "sample.py").touch()

    assert loader._is_valid_capability(capability_directory) is False


def test_capability_loader_rejects_directory_without_implementation_file(
    tmp_path,
    ):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    capability_directory = tmp_path / "invalid_capability"
    capability_directory.mkdir()

    (capability_directory / "__init__.py").touch()

    assert loader._is_valid_capability(capability_directory) is False

def test_capability_loader_rejects_file_path(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    capability_file = tmp_path / "sample.py"
    capability_file.touch()

    assert loader._is_valid_capability(capability_file) is False

def test_capability_loader_scans_only_valid_capability_directories(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    valid_capability = tmp_path / "valid_capability"
    valid_capability.mkdir()
    (valid_capability / "__init__.py").touch()
    (valid_capability / "implementation.py").touch()

    invalid_capability = tmp_path / "invalid_capability"
    invalid_capability.mkdir()
    (invalid_capability / "__init__.py").touch()

    discovered_directories = loader._scan_directories(tmp_path)

    assert discovered_directories == [valid_capability]

def test_capability_loader_discovers_valid_capabilities(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    first_capability = tmp_path / "first_capability"
    first_capability.mkdir()
    (first_capability / "__init__.py").touch()
    (first_capability / "implementation.py").touch()

    second_capability = tmp_path / "second_capability"
    second_capability.mkdir()
    (second_capability / "__init__.py").touch()
    (second_capability / "implementation.py").touch()

    discovered_capabilities = loader.discover(tmp_path)

    assert discovered_capabilities == [
        first_capability,
        second_capability,
    ]
    assert loader.loaded_capabilities == []

def test_capability_loader_loads_python_module(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    module_file = tmp_path / "sample_capability.py"
    module_file.write_text(
        "VALUE = 'loaded'\n",
        encoding="utf-8",
    )

    loaded_module = loader._load_module(module_file)

    assert isinstance(loaded_module, ModuleType)
    assert loaded_module.VALUE == "loaded"

def test_capability_loader_finds_capability_class_in_module(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    module_file = tmp_path / "sample_capability.py"
    module_file.write_text(
        "\n".join(
            [
                "from heyti.capabilities.base import Capability",
                "",
                "class SampleCapability(Capability):",
                "    def execute(self, session, payload=None):",
                "        return {'status': 'OK'}",
            ]
        ),
        encoding="utf-8",
    )

    loaded_module = loader._load_module(module_file)
    capability_class = loader._find_capability_class(loaded_module)

    assert issubclass(capability_class, Capability)
    assert capability_class.__name__ == "SampleCapability"

def test_capability_loader_instantiates_capability_class(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    module_file = tmp_path / "sample_capability.py"
    module_file.write_text(
        "\n".join(
            [
                "from heyti.capabilities.base import Capability",
                "",
                "class SampleCapability(Capability):",
                "    def execute(self, session, payload=None):",
                "        return {'status': 'OK'}",
            ]
        ),
        encoding="utf-8",
    )

    loaded_module = loader._load_module(module_file)
    capability_class = loader._find_capability_class(loaded_module)
    capability_instance = loader._instantiate_capability(
        capability_class
    )

    assert isinstance(capability_instance, Capability)
    assert capability_instance.execute(session=None) == {
        "status": "OK"
    }

def test_capability_loader_registers_capability_instance(tmp_path):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    capability_directory = tmp_path / "sample_capability"
    capability_directory.mkdir()

    module_file = capability_directory / "implementation.py"
    module_file.write_text(
        "\n".join(
            [
                "from heyti.capabilities.base import Capability",
                "",
                "class SampleCapability(Capability):",
                "    def execute(self, session, payload=None):",
                "        return {'status': 'OK'}",
            ]
        ),
        encoding="utf-8",
    )

    loaded_module = loader._load_module(module_file)
    capability_class = loader._find_capability_class(loaded_module)
    capability_instance = loader._instantiate_capability(
        capability_class
    )

    loader._register_capability(
        capability_directory,
        capability_instance,
    )

    assert registry.exists("sample_capability") is True
    assert registry.get("sample_capability") is capability_instance

def test_capability_loader_loads_capability_from_directory(
    tmp_path,
    ):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    capability_directory = tmp_path / "sample_capability"
    capability_directory.mkdir()

    init_file = capability_directory / "__init__.py"
    init_file.write_text("", encoding="utf-8")

    implementation_file = (
        capability_directory / "implementation.py"
    )
    implementation_file.write_text(
        "\n".join(
            [
                "from heyti.capabilities.base import Capability",
                "",
                "class SampleCapability(Capability):",
                "    def execute(self, session, payload=None):",
                "        return {'status': 'OK'}",
            ]
        ),
        encoding="utf-8",
    )

    capability_instance = loader._load_capability_directory(
        capability_directory
    )

    assert isinstance(capability_instance, Capability)
    assert registry.exists("sample_capability") is True
    assert (
        registry.get("sample_capability")
        is capability_instance
    )
    assert capability_instance.execute(
        session=None
    ) == {"status": "OK"}

def test_capability_loader_loads_all_discovered_capabilities(
    tmp_path,
):
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry=registry)

    for capability_name in [
        "first_capability",
        "second_capability",
    ]:
        capability_directory = tmp_path / capability_name
        capability_directory.mkdir()

        init_file = capability_directory / "__init__.py"
        init_file.write_text("", encoding="utf-8")

        implementation_file = (
            capability_directory / "implementation.py"
        )
        implementation_file.write_text(
            "\n".join(
                [
                    "from heyti.capabilities.base import Capability",
                    "",
                    "class SampleCapability(Capability):",
                    "    def execute(self, session, payload=None):",
                    f"        return {{'name': '{capability_name}'}}",
                ]
            ),
            encoding="utf-8",
        )

    loaded_capabilities = loader.load_all(tmp_path)

    assert len(loaded_capabilities) == 2
    assert len(loader.loaded_capabilities) == 2

    assert registry.exists("first_capability") is True
    assert registry.exists("second_capability") is True

    assert registry.get("first_capability").execute(
        session=None
    ) == {"name": "first_capability"}

    assert registry.get("second_capability").execute(
        session=None
    ) == {"name": "second_capability"}

def test_capability_loader_loads_real_heyti_capabilities():
        registry = CapabilityRegistry()
        loader = CapabilityLoader(registry=registry)

        capabilities_root = Path("src/heyti/capabilities")

        loaded_capabilities = loader.load_all(
            capabilities_root
        )

        assert len(loaded_capabilities) == 3
        assert registry.count() == 3

        assert registry.exists("health") is True
        assert registry.exists("system_info") is True
        assert registry.exists("version") is True