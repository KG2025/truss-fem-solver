from input_data import nodes, load_cases
import numpy as np

# DOF mapping
def node_dofs(node_id):
    base = 2 * (node_id - 1)
    return [base, base + 1]

def element_stiffness(x1, y1, x2, y2, E, A):
    dx = x2 - x1
    dy = y2 - y1
    L = (dx**2 + dy**2)**0.5

    c = dx / L
    s = dy / L

    import numpy as np
    k = (E * A / L) * np.array([
        [ c*c,  c*s, -c*c, -c*s],
        [ c*s,  s*s, -c*s, -s*s],
        [-c*c, -c*s,  c*c,  c*s],
        [-c*s, -s*s,  c*s,  s*s]
    ])

    return k, L, c, s

def assemble_K(nodes, elements, E):
    n_nodes = len(nodes)
    n_dofs = 2 * n_nodes
    K = np.zeros((n_dofs, n_dofs))

    for eid, elem in elements.items():
        n1 = elem["n1"]
        n2 = elem["n2"]
        A = elem["A"]

        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]

        ke, _, _, _ = element_stiffness(x1, y1, x2, y2, E, A)
        dofs = node_dofs(n1) + node_dofs(n2)

        for i in range(4):
            for j in range(4):
                K[dofs[i], dofs[j]] += ke[i, j]

    return K

def assemble_f(nodes, loads):
    n_dofs = 2 * len(nodes)
    f = np.zeros(n_dofs)
    
    for node_id, (Fx, Fy) in loads.items():
        dofs = node_dofs(node_id)
        print(f"Node {node_id}: Fx={Fx}, Fy={Fy}, DOFs={dofs}")
    
        f[dofs[0]] += Fx
        f[dofs[1]] += Fy
    
    print("\nGlobal load vector f:")
    print(f)

    return f

def get_fixed_dofs(nodes, fixed_dofs):
    fixed = []

    for node_id, (fix_x, fix_y) in fixed_dofs.items():
        dofs = node_dofs(node_id)
    
        if fix_x:
            fixed.append(dofs[0])
        if fix_y:
            fixed.append(dofs[1])
    
    fixed = np.array(sorted(fixed))
    print("Fixed DOFs:", fixed)

    n_dofs = 2 * len(nodes)
    all_dofs = np.arange(n_dofs)
    free = np.setdiff1d(all_dofs, fixed)
    
    print("All DOFs: ", all_dofs)
    print("Free DOFs:", free)
    print("Fixed DOFs:", fixed)

    return fixed, free

def solve(K,f,free):
    K_ff = K[np.ix_(free, free)]
    f_f = f[free]
    
    u = np.zeros(len(f))
    u[free] = np.linalg.solve(K_ff, f_f)

    reactions = K @ u - f
    
    return u, reactions

def compute_axial_forces(nodes, elements, E, u):

    forces = {}

    for eid, elem in elements.items():
        n1 = elem["n1"]
        n2 = elem["n2"]
        A = elem["A"]

        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]

        dx = x2 - x1
        dy = y2 - y1
        L = np.sqrt(dx**2 + dy**2)

        c = dx / L
        s = dy / L

        dofs = node_dofs(n1) + node_dofs(n2)
        u_elem = u[dofs]

        delta = np.array([-c, -s, c, s]) @ u_elem
        N = E * A / L * delta

        forces[eid] = N

    return forces
