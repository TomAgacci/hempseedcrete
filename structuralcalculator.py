#!/usr/bin/env python3
"""
Toy structural calculator for modular aluminum exoskeleton
with hemp-seed-crete infill (non-structural).

This is NOT a design tool. It is a conceptual calculator to show
how story count would be derived under simple gravity loading.
"""

from dataclasses import dataclass
import math

@dataclass
class ModuleGeometry:
    floor_length: float = 3.0   # m
    floor_width: float = 3.0    # m
    story_height: float = 3.0   # m
    n_columns: int = 4          # vertical columns per module

@dataclass
class LoadAssumptions:
    dead_load_kN_m2: float = 3.0  # kN/m^2
    live_load_kN_m2: float = 2.0  # kN/m^2

@dataclass
class AluminumSection:
    outer_dim_m: float = 0.05   # m (e.g. 50 mm square tube)
    thickness_m: float = 0.003  # m (e.g. 3 mm wall)
    fy_MPa: float = 250.0       # MPa (yield strength)
    safety_factor: float = 2.0  # global safety factor

def column_area(section: AluminumSection) -> float:
    """
    Approximate area of square tube:
    A = 4 * t * (b - t)
    """
    b = section.outer_dim_m
    t = section.thickness_m
    return 4.0 * t * (b - t)

def column_capacity_kN(section: AluminumSection) -> float:
    """
    Axial capacity per column (factored).
    N_allow = A * fy / gamma_SF
    fy in MPa, A in m^2 -> convert to kN:
    1 MPa = 1e6 N/m^2, 1 kN = 1e3 N
    """
    A = column_area(section)
    fy = section.fy_MPa * 1e6  # Pa
    gamma = section.safety_factor
    N_allow_N = A * fy / gamma
    return N_allow_N / 1e3  # kN

def module_floor_area(geom: ModuleGeometry) -> float:
    return geom.floor_length * geom.floor_width

def floor_load_kN(geom: ModuleGeometry, loads: LoadAssumptions) -> float:
    A = module_floor_area(geom)
    q_total = loads.dead_load_kN_m2 + loads.live_load_kN_m2
    return q_total * A

def max_stories(geom: ModuleGeometry,
                loads: LoadAssumptions,
                section: AluminumSection) -> int:
    cap_per_col = column_capacity_kN(section)
    total_cap = cap_per_col * geom.n_columns
    floor_load = floor_load_kN(geom, loads)
    if floor_load <= 0:
        return 0
    return int(total_cap // floor_load)

def main():
    # Default assumptions
    geom = ModuleGeometry()
    loads = LoadAssumptions()
    section = AluminumSection()

    A_col = column_area(section)
    cap_col = column_capacity_kN(section)
    A_floor = module_floor_area(geom)
    floor_load = floor_load_kN(geom, loads)
    stories = max_stories(geom, loads, section)

    print("=== Toy Structural Calculator ===")
    print(f"Module floor area: {A_floor:.2f} m^2")
    print(f"Dead + live load: {loads.dead_load_kN_m2 + loads.live_load_kN_m2:.2f} kN/m^2")
    print(f"Floor load per story per module: {floor_load:.2f} kN")
    print()
    print(f"Aluminum column area: {A_col*1e6:.2f} mm^2")
    print(f"Column axial capacity (factored): {cap_col:.2f} kN")
    print(f"Total axial capacity (all columns): {cap_col * geom.n_columns:.2f} kN")
    print()
    print(f"Estimated max stories (gravity only, toy model): {stories}")
    print()
    print("NOTE: This ignores buckling, lateral loads, connection design,")
    print("      and material nonlinearity. It is NOT safe for real-world design.")

if __name__ == "__main__":
    main()
