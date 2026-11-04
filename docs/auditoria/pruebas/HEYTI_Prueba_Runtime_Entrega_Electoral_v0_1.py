r"""HEYTI: runtime/validation/delivery probe, isolated DB audit plus blocked presentation.

Save at D:\GitHub\AT-27-30-core\docs\auditoria\pruebas\HEYTI_Prueba_Runtime_Entrega_Electoral_v0_1.py
Requires the previously verified DL2021 RP 1080 audit script in the same folder.
GateFixture is synthetic. No real cut is approved; no UI or production wiring.
Local verification: three synthetic runtime cases passed before delivery.
"""
from heyti.capabilities.describe_section.models import SectionTruthSnapshot
from heyti.capabilities.describe_section.provider import DescribeSectionProvider
from heyti.capabilities.describe_section.implementation import DescribeSectionCapability
from heyti.capabilities.describe_section.versioned_electoral_source import VersionedElectoralSource
from heyti.materialization.describe_section.materializer import DescribeSectionMaterializer
from heyti.delivery.adapters.in_memory import InMemoryDeliveryAdapter
from heyti.delivery.validator import DeliveryContractValidator
from heyti.events.event_bus import EventBus
from heyti.registry.registry import CapabilityRegistry
from heyti.session.session_manager import SessionManager
from heyti.runtime.capability_runtime import CapabilityRuntime


def run_runtime_checks(registry, repository):
    # A gate fixture exercises routing; it does not certify a real section.
    class GateFixture:
        def __init__(self, status):
            self.status = status
        def get_section_truth(self, section_id):
            return SectionTruthSnapshot({'publication_status': self.status,
                                         'scope': 'TEST_FIXTURE_NOT_CERTIFICATION'})

    class CountingRepository:
        calls = 0
        def get_snapshot(self, release_id, request):
            self.calls += 1
            return repository.get_snapshot(release_id, request)

    counter = CountingRepository()
    source = VersionedElectoralSource(registry, counter)
    cases = [('ALLOWED', 'RESULT', 'NO_RELEASE_SELECTED'),
             ('BLOCKED', 'RESULT', 'DATA_TRUTH_NOT_ALLOWED'),
             ('ALLOWED', 'NOMINAL_LIST', 'NO_RELEASE_SELECTED')]
    records = []
    for ordinal, (gate, metric, expected) in enumerate(cases, 1):
        provider = DescribeSectionProvider(truth_source=GateFixture(gate),
                                         versioned_electoral_source=source)
        capabilities = CapabilityRegistry()
        capabilities.register('describe_section', DescribeSectionCapability(provider))
        sessions = SessionManager()
        sessions.create('isolated-probe', {'scope': 'TEST_ONLY'})
        bus = EventBus()
        events = []
        bus.subscribe('capability_executed', lambda payload: events.append('capability_executed'))
        bus.subscribe('delivery_completed', lambda payload: events.append('delivery_completed'))
        runtime = CapabilityRuntime(capabilities, sessions, bus)
        adapter = InMemoryDeliveryAdapter()
        result = runtime.execute_delivered(
            'describe_section', 'isolated-probe', 'LOCAL_TEST_ONLY', adapter=adapter,
            materializer=DescribeSectionMaterializer(),
            payload={'section_id': '1080', 'electoral_query': {
                'year': 2021, 'type': 'DL', 'modality': 'RP', 'metric_scope': metric}},
            request_id='electoral-probe-' + str(ordinal), execution_id='execution-' + str(ordinal),
        )
        DeliveryContractValidator().validate_result(result)
        assert result.status == 'DELIVERED', result.status
        assert len(adapter.deliveries) == 1
        envelope = adapter.deliveries[0]
        DeliveryContractValidator().validate_envelope(envelope)
        response = envelope.response
        blocks = [b for b in response.blocks if b.role == 'electoral_versioned']
        assert len(blocks) == 1
        block = blocks[0]
        assert block.type == 'metadata'
        assert block.content['status'] == expected
        assert block.content['data'] is None
        assert not any(b.role == 'electoral' for b in response.blocks)
        assert response.status == 'success_with_warnings'
        assert response.trace.request_id == 'electoral-probe-' + str(ordinal)
        assert envelope.trace.execution_id == 'execution-' + str(ordinal)
        assert envelope.response_id == result.response_id
        assert events == ['capability_executed', 'delivery_completed'], events
        assert counter.calls == 0, 'Blocked presentation unexpectedly read the DB'
        records.append({'gate_fixture': gate, 'metric_scope': metric,
                        'electoral_status': expected, 'delivery_status': result.status,
                        'repository_calls': counter.calls})
        print(gate, metric, '|', expected, '| DELIVERY:', result.status, '| DB calls:', counter.calls)
    return records


if __name__ == '__main__':
    import ast
    import json
    import runpy
    from pathlib import Path

    folder = Path(__file__).resolve().parent
    previous = folder / 'HEYTI_Prueba_Lectura_DL2021_RP_1080_v0_1.py'
    if not previous.is_file():
        raise RuntimeError('Missing previously verified audit script: ' + str(previous))
    tree = ast.parse(previous.read_text(encoding='utf-8-sig'))
    database_values = [ast.literal_eval(node.value) for node in tree.body
                       if isinstance(node, ast.Assign)
                       and any(isinstance(target, ast.Name) and target.id == 'database'
                               for target in node.targets)]
    if database_values != ['heyti_cas_full_probe_d12d6718adb8']:
        raise RuntimeError('Unexpected database in audit script; stopped before execution')
    # Executes the original read-only audit and its assertions, asking once for password.
    scope = runpy.run_path(str(previous), run_name='__heyti_verified_audit__')
    records = run_runtime_checks(scope['registry'], scope['repository'])
    report = {
        'scope': 'ISOLATED_AUDIT_AND_BLOCKED_PRESENTATION_NOT_UI_CERTIFICATION',
        'database': scope['database'],
        'audit_case': 'DL2021 RP SEC:1080; original audit assertions passed',
        'data_truth': 'SYNTHETIC_GATE_FIXTURE_NOT_REAL_CERTIFICATION',
        'runtime_cases': records,
        'limitation': 'No selected real votes traverse runtime; no UI or production connection.',
    }
    destination = folder.parent / 'HEYTI_Resultado_Runtime_Entrega_Electoral_v0_1.json'
    if destination.exists():
        from uuid import uuid4
        destination = destination.with_name(destination.stem + '_' + uuid4().hex[:8] + '.json')
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('RUNTIME/MATERIALIZACION/VALIDACION/DELIVERY: 3 CASOS OK')
    print('Evidence:', destination)
