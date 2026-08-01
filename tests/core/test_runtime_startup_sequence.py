"""
Pruebas del Runtime Startup Sequence de HEYTI.
"""

from heyti.runtime.runtime_startup_sequence import RuntimeStartupSequence


def test_runtime_startup_sequence_starts_empty():
    sequence = RuntimeStartupSequence()

    assert sequence.steps == []


def test_runtime_startup_sequence_registers_steps():
    sequence = RuntimeStartupSequence()

    sequence.add_step(
        "Bootstrap",
        "OK",
    )

    sequence.add_step(
        "Capabilities",
        "OK",
    )

    assert sequence.steps == [
        ("Bootstrap", "OK"),
        ("Capabilities", "OK"),
    ]