from heyti.runtime.runtime_bootstrap import RuntimeBootstrap
from heyti.runtime.runtime_startup_sequence import RuntimeStartupSequence

def test_runtime_bootstrap_loads_official_capabilities():
    bootstrap = RuntimeBootstrap()

    loaded_capabilities = bootstrap.initialize()

    assert len(loaded_capabilities) == 3
    assert bootstrap.registry.count() == 3

    assert bootstrap.registry.exists("health") is True
    assert bootstrap.registry.exists("system_info") is True
    assert bootstrap.registry.exists("version") is True

def test_runtime_bootstrap_records_startup_sequence():
    sequence = RuntimeStartupSequence()

    bootstrap = RuntimeBootstrap(
        sequence=sequence,
    )

    bootstrap.initialize()

    assert sequence.steps == [
        ("Bootstrap", "STARTED"),
        ("Capabilities", "OK"),
        ("Runtime", "READY"),
    ]