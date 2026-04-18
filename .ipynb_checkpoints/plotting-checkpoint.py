import matplotlib.pyplot as plt
from solver import node_dofs

import matplotlib.pyplot as plt

def plot_truss(nodes, elements, loads, title="Truss with external loads"):
    plt.figure(figsize=(10, 5))

    # staven tekenen
    for eid, elem in elements.items():
        n1 = elem["n1"]
        n2 = elem["n2"]

        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]

        plt.plot([x1, x2], [y1, y2], 'k-')

        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2
        plt.text(xm, ym, f'E{eid}', color='blue', fontsize=9)

    # nodes tekenen
    for node_id, (x, y) in nodes.items():
        plt.plot(x, y, 'ro')
        plt.text(x + 0.3, y + 0.3, f'N{node_id}', fontsize=9)

    # externe belastingen tekenen
    scale = 5000

    for node_id, (Fx, Fy) in loads.items():
        x, y = nodes[node_id]

        plt.quiver(
            x, y,
            Fx / scale, Fy / scale,
            angles='xy',
            scale_units='xy',
            scale=1,
            color='green'
        )

        plt.text(x + 1, y - 3, f'({Fx:.0f}, {Fy:.0f})', fontsize=8, color='green')

    plt.axis('equal')
    plt.title(title)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True)
    plt.show()

def plot_deformed_shape(nodes, elements, u, scale=100, title="Deformed shape", save_path=None):
    import matplotlib.pyplot as plt
    from solver import node_dofs

    plt.figure(figsize=(10, 5))

    # undeformed
    for _, elem in elements.items():
        n1 = elem["n1"]
        n2 = elem["n2"]

        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]

        plt.plot([x1, x2], [y1, y2], "k--", linewidth=1)

    # deformed
    for _, elem in elements.items():
        n1 = elem["n1"]
        n2 = elem["n2"]

        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]

        dofs1 = node_dofs(n1)
        dofs2 = node_dofs(n2)

        ux1, uy1 = u[dofs1[0]], u[dofs1[1]]
        ux2, uy2 = u[dofs2[0]], u[dofs2[1]]

        x1_def = x1 + scale * ux1
        y1_def = y1 + scale * uy1
        x2_def = x2 + scale * ux2
        y2_def = y2 + scale * uy2

        plt.plot([x1_def, x2_def], [y1_def, y2_def], "r-", linewidth=2)

    plt.axis("equal")
    plt.title(title)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")

    plt.show()