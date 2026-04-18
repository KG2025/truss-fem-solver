import numpy as np
import matplotlib.pyplot as plt

# Materiaal
E = 210e9  # Pa

# Knooppunten (id: (x, y))
nodes = {
    1: (0.0, 0.0),
    2: (20, 0.0),
    3: (20.0, 10.0),
    4: (42.5, 7.5),
    5: (45, 0),
    6: (70,0),
}

# Elementen (id: node1, node2, area in m^2)
elements = {
    1: {"n1": 1, "n2": 2, "A": 0.05},
    2: {"n1": 1, "n2": 3, "A": 0.005},
    3: {"n1": 2, "n2": 3, "A": 0.06},
    4: {"n1": 2, "n2": 5, "A": 0.03},
    5: {"n1": 3, "n2": 5, "A": 0.005},
    6: {"n1": 3, "n2": 4, "A": 0.005},
    7: {"n1": 5, "n2": 4, "A": 0.02},
    8: {"n1": 5, "n2": 6, "A": 0.02},
    9: {"n1": 4, "n2": 6, "A": 0.005},
}

# Belastingen (node: (Fx, Fy) in [N])
load_cases = {
    "base_case": {
        1: (0.0, -80000.0),
        6: (0.0, -65000.0),
    },
    "left_only": {
        1: (0.0, -80000.0),
    },
    "right_only": {
        6: (0.0, -65000.0),
    },
}

# Opleggingen (node: (fix_x, fix_y))
fixed_dofs = {
    2: (True, True),   # scharnier
    3: (True, False),  # rol
}
