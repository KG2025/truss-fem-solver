import numpy as np
from input_data import nodes, elements, load_cases, fixed_dofs, E
from solver import (
    node_dofs,
    assemble_K,
    assemble_f,
    get_fixed_dofs,
    solve,
    compute_axial_forces,
)
from plotting import plot_deformed_shape
from plotting import plot_truss


def main():
    for name, loads in load_cases.items():
        print(f"\nRunning {name}")
        K = assemble_K(nodes, elements, E)
        f = assemble_f(nodes, loads)
        fixed, free = get_fixed_dofs(nodes, fixed_dofs)
    
        u, reactions = solve(K, f, free)
        forces = compute_axial_forces(nodes, elements, E, u)

    print("\nDisplacements:")
    for node_id in nodes:
        dofs = node_dofs(node_id)
        ux = u[dofs[0]]
        uy = u[dofs[1]]
        print(f"Node {node_id}: ux = {ux:.6e}, uy = {uy:.6e}")

    print("\nEquilibrium check:")
    Fx_ext = np.sum(f[0::2])
    Fy_ext = np.sum(f[1::2])
    Fx_reac = np.sum(reactions[0::2])
    Fy_reac = np.sum(reactions[1::2])

    print(f"Fx external   = {Fx_ext:.6e}")
    print(f"Fx reactions  = {Fx_reac:.6e}")
    print(f"Fx total      = {Fx_ext + Fx_reac:.6e}")
    print(f"Fy external   = {Fy_ext:.6e}")
    print(f"Fy reactions  = {Fy_reac:.6e}")
    print(f"Fy total      = {Fy_ext + Fy_reac:.6e}")

    print("\nSupport reactions:")
    for node_id in fixed_dofs:
        dofs = node_dofs(node_id)
        rx = reactions[dofs[0]]
        ry = reactions[dofs[1]]
        print(f"Node {node_id}: Rx = {rx:.2f} N, Ry = {ry:.2f} N")

    print("\nElement forces:")
    for eid, force in forces.items():
        state = "Tension" if force > 0 else "Compression"
        print(f"Element {eid}: {float(force):.2f} N ({state})")

    scale = 100
    for name, loads in load_cases.items():
        print(f"\nRunning {name}")
    
        K = assemble_K(nodes, elements, E)
        f = assemble_f(nodes, loads)
        fixed, free = get_fixed_dofs(nodes, fixed_dofs)
    
        u, reactions = solve(K, f, free)
    
        plot_truss(nodes, elements, loads, title=name)
        plot_deformed_shape(
            nodes,
            elements,
            u,
            scale=scale,
            title=f"Deformed shape - {name} - scale={scale}",
            save_path=f"{name}_deformed.png"
        )


if __name__ == "__main__":
    main()

    