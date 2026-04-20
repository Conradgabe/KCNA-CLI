from kcna.loader import load_bank


def test_package_bank_loads_and_has_enough_per_domain():
    bank = load_bank()
    assert len(bank) >= 65
    counts = {}
    for q in bank:
        counts[q.domain] = counts.get(q.domain, 0) + 1
    assert counts.get("kubernetes-fundamentals", 0) >= 29
    assert counts.get("container-orchestration", 0) >= 18
    assert counts.get("cloud-native-delivery", 0) >= 10
    assert counts.get("cloud-native-architecture", 0) >= 8


def test_all_ids_unique():
    bank = load_bank()
    ids = [q.id for q in bank]
    assert len(ids) == len(set(ids))


def test_all_questions_have_single_correct():
    bank = load_bank()
    for q in bank:
        correct = [o for o in q.options if o.correct]
        assert len(correct) == 1, f"{q.id} has {len(correct)} correct options"
