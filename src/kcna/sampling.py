from __future__ import annotations

import random
from collections import defaultdict

from kcna.config import DOMAIN_WEIGHTS, EXAM_LEN
from kcna.models import Question


def _largest_remainder(weights: dict[str, float], total: int) -> dict[str, int]:
    raw = {d: total * w for d, w in weights.items()}
    floors = {d: int(v) for d, v in raw.items()}
    remainder = total - sum(floors.values())
    fractional = sorted(
        ((d, raw[d] - floors[d]) for d in weights),
        key=lambda kv: kv[1],
        reverse=True,
    )
    for i in range(remainder):
        d, _ = fractional[i % len(fractional)]
        floors[d] += 1
    return floors


def _redistribute(targets: dict[str, int], pool_sizes: dict[str, int]) -> dict[str, int]:
    final = dict(targets)
    overflow = 0
    capped: set[str] = set()
    for d, t in targets.items():
        available = pool_sizes.get(d, 0)
        if available < t:
            overflow += t - available
            final[d] = available
            capped.add(d)

    while overflow > 0:
        remaining_domains = [d for d in final if d not in capped]
        if not remaining_domains:
            break
        remaining_weights = {d: DOMAIN_WEIGHTS[d] for d in remaining_domains}
        total_w = sum(remaining_weights.values()) or 1.0
        remaining_weights = {d: w / total_w for d, w in remaining_weights.items()}
        extra = _largest_remainder(remaining_weights, overflow)
        overflow = 0
        for d, e in extra.items():
            headroom = pool_sizes.get(d, 0) - final[d]
            if e <= headroom:
                final[d] += e
            else:
                final[d] += headroom
                overflow += e - headroom
                capped.add(d)
    return final


def sample_exam(
    pool: list[Question],
    count: int = EXAM_LEN,
    seed: int | None = None,
) -> list[Question]:
    rng = random.Random(seed)

    by_domain: dict[str, list[Question]] = defaultdict(list)
    for q in pool:
        by_domain[q.domain].append(q)

    targets = _largest_remainder(DOMAIN_WEIGHTS, count)
    pool_sizes = {d: len(by_domain.get(d, [])) for d in DOMAIN_WEIGHTS}
    targets = _redistribute(targets, pool_sizes)

    sampled: list[Question] = []
    for domain, n in targets.items():
        if n <= 0:
            continue
        domain_pool = by_domain.get(domain, [])
        if len(domain_pool) < n:
            n = len(domain_pool)
        sampled.extend(rng.sample(domain_pool, n))

    rng.shuffle(sampled)
    return sampled


def sample_practice(
    pool: list[Question],
    count: int,
    domain: str | None = None,
    difficulty: str | None = None,
    seed: int | None = None,
) -> list[Question]:
    rng = random.Random(seed)
    candidates = pool
    if domain:
        candidates = [q for q in candidates if q.domain == domain]
    if difficulty:
        candidates = [q for q in candidates if q.difficulty == difficulty]
    if not candidates:
        return []
    n = min(count, len(candidates))
    return rng.sample(candidates, n)
