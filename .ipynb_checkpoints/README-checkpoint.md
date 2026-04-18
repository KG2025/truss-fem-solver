# 2D Truss FEM Solver in Python

## Description
This project implements a 2D truss finite element solver in Python using the direct stiffness method.

The solver computes:
- nodal displacements
- support reactions
- axial forces in truss elements
- deformed structural shape

## Features
- element stiffness matrix formulation
- global stiffness matrix assembly
- load vector construction
- boundary condition handling
- linear system solution
- reaction force computation
- axial force post-processing
- deformed shape visualization

## Method
The implementation is based on the direct stiffness method for 2D truss structures:

K u = f

where:
- K = global stiffness matrix
- u = nodal displacement vector
- f = external load vector

## Validation
The model was validated by:
- checking global force equilibrium
- verifying that reaction forces balance external loads
- confirming that the deformation pattern is physically consistent
- checking tension/compression patterns in the truss members

## Example output
The project produces:
- nodal displacements
- support reactions
- element axial forces
- deformed shape plot

## How to run
```bash
python main.py

