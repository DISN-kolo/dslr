import numpy as np
import math

from utils.additional_exceptions import (
    ItsNoneError,
    ZeroElementsError,
    LessThanOneElError,
)

def ft_count(it):
    if (it is None):
        raise ItsNoneError

    ctr: int = 0
    for element in it:
        ctr += 1
    return ctr

def ft_mean(it, ctr: int):
    if (ctr < 1):
        raise LessThanOneElError

    m: float = 0.0
    for element in it:
        m += element/ctr

    return m

def ft_sum(it):
    if (it is None):
        raise ItsNoneError

    s: float = 0
    for element in it:
        s += element

    return s

# Do Bessel's correction by default 
def ft_std(it, ctr: int, mean: float, bessels: bool = True):
    if (it is None):
        raise ItsNoneError
    if (ctr == 1):
        return 0
    if (ctr <= 0):
        raise LessThanOneElError

    total_sum: float = ft_sum((it - mean) ** 2)
    if (bessels):
        return np.sqrt(total_sum/(ctr - 1))
    return np.sqrt(total_sum/ctr)

def ft_min(it):
    if (it is None):
        raise ItsNoneError

    m = it[0]
    for element in it:
        if (element < m):
            m = element

    return m

def ft_max(it):
    if (it is None):
        raise ItsNoneError

    m = it[0]
    for element in it:
        if (element > m):
            m = element

    return m

def ft_merge(it, l: int, m: int, r: int):
    l_len = m - l + 1
    r_len = r - m

    l_it = np.zeros(l_len)
    r_it = np.zeros(r_len)

    for i in range(l_len):
        l_it[i] = it[l + i]
    for j in range(r_len):
        r_it[j] = it[m + 1 + j]

    i = j = 0
    l_sweep = l

    while (i < l_len and j < r_len):
        if (l_it[i] <= r_it[j]):
            it[l_sweep] = l_it[i]
            i += 1
        else:
            it[l_sweep] = r_it[j]
            j += 1
        l_sweep += 1

    while (i < l_len):
        it[l_sweep] = l_it[i]
        i += 1
        l_sweep += 1
    while (j < r_len):
        it[l_sweep] = r_it[j]
        j += 1
        l_sweep += 1

def ft_merge_sort(it, l: int, r: int):
    if l < r:
        m = l + (r - l) // 2
        ft_merge_sort(it, l, m)
        ft_merge_sort(it, m + 1, r)
        ft_merge(it, l, m, r)

def ft_percentile(s_it, ctr: int, mi: float, ma: float, p: float):
    if (s_it is None):
        raise ItsNoneError
    if (ctr <= 0):
        raise LessThanOneElError

    p_ctr = 0
    ctr_max = math.ceil(p*(ctr - 1))
    p_elem = s_it[0]
    for element in s_it:
        if (p_ctr > ctr_max):
            p_elem = element
            break
        p_ctr += 1
    return p_elem
