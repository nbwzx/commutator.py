"""
Commutator (https://github.com/nbwzx/commutator.py)
Copyright (c) 2022-2024 Zixing Wang <zixingwang.cn@gmail.com>
Licensed under MIT (https://github.com/nbwzx/commutator.py/blob/main/LICENSE)
"""

from .commutator import (
    expand,
    search
)

from .commutator_555 import (
    expand as expand_555,
    search as search_555
)

from .commutator_555_final import (
    expand as expand_555_final,
    search as search_555_final,
    finalReplaceCommutator,
    finalReplaceAlg
)
