"""Head-to-head analysis: exact two-sided sign tests of method comparisons within a campaign."""
import math
from collections import defaultdict


def sign_test(a_wins, b_wins):
    """Exact two-sided binomial sign test. Returns p-value."""
    n = a_wins + b_wins
    if n == 0:
        return 1.0
    k = min(a_wins, b_wins)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p if k < n / 2 else 1.0)


def head_to_head(cells, method_a, method_b, rel_tol=1e-9):
    """Compare best_L of method_a vs method_b per (family, n). Returns dict with wins, ties, p."""
    by_inst = defaultdict(dict)
    for c in cells:
        by_inst[(c['family'], c['n'])][c['method']] = c['best_L']
    a = b = t = 0
    detail = []
    for inst in sorted(by_inst):
        m = by_inst[inst]
        if method_a not in m or method_b not in m:
            continue
        la, lb = m[method_a], m[method_b]
        denom = max(abs(la), abs(lb), 1e-300)
        if abs(la - lb) / denom <= rel_tol:
            t += 1
            outcome = 'tie'
        elif la < lb:
            a += 1
            outcome = method_a
        else:
            b += 1
            outcome = method_b
        detail.append({'family': inst[0], 'n': inst[1], method_a: la, method_b: lb, 'winner': outcome})
    return {'method_a': method_a, 'method_b': method_b, 'a_wins': a, 'b_wins': b, 'ties': t,
            'p': sign_test(a, b), 'detail': detail}
