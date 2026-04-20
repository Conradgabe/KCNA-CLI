from collections import Counter

from kcna.sampling import sample_exam, sample_practice
from tests.conftest import make_pool


def test_sampling_totals_65():
    pool = make_pool()
    exam = sample_exam(pool, seed=1)
    assert len(exam) == 65


def test_sampling_domain_weights():
    pool = make_pool()
    exam = sample_exam(pool, seed=1)
    counts = Counter(q.domain for q in exam)
    assert counts["kubernetes-fundamentals"] == 29
    assert counts["container-orchestration"] == 18
    assert counts["cloud-native-delivery"] == 10
    assert counts["cloud-native-architecture"] == 8


def test_sampling_deterministic_with_seed():
    pool = make_pool()
    a = [q.id for q in sample_exam(pool, seed=42)]
    b = [q.id for q in sample_exam(pool, seed=42)]
    assert a == b


def test_sampling_no_duplicates():
    pool = make_pool()
    exam = sample_exam(pool, seed=1)
    assert len(set(q.id for q in exam)) == 65


def test_practice_filter_by_domain():
    pool = make_pool()
    qs = sample_practice(pool, count=10, domain="container-orchestration", seed=1)
    assert len(qs) == 10
    assert all(q.domain == "container-orchestration" for q in qs)


def test_practice_count_clamped_to_pool():
    pool = make_pool()
    qs = sample_practice(pool, count=1000, domain="cloud-native-architecture", seed=1)
    assert len(qs) == 19
