#!/usr/bin/env python3
"""
Extended toy structural calculator for modular aluminum exoskeleton
with hemp-seed-crete infill as secondary load path.

- Includes Euler buckling check
- Includes hempcrete vertical capacity contribution
- Still NOT a design tool; purely conceptual.
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
    E_GPa: float = 70.0         # GPa (elastic modulus)
    safety_factor: float = 2.0  # global safety factor
    K: float = 1.0              # effective length factor (1.0 = pinned-pinned)

@dataclass
class HempcreteProperties:
    fc_MPa: float = 0.5         # conservative compressive strength
    area_m2: float = 1.0        # effective vertical load area per module
    safety_factor: float = 2.0

def module_floor_area(geom: ModuleGeometry) -> float:
    return geom.floor_length * geom.floor_width

def floor_load_kN(geom: ModuleGeometry, loads: LoadAssumptions) -> float:
    A = module_floor_area(geom)
    q_total = loads.dead_load_kN_m2 + loads.live_load_kN_m2
    return q_total * A

def column_area(section: AluminumSection) -> float:
    """
    Approximate area of square tube:
    A = b^2 - (b - 2t)^2
    """
    b = section.outer_dim_m
    t = section.thickness_m
    return b**2 - (b - 2.0 * t)**2

def column_I(section: AluminumSection) -> float:
    """
    Second moment of area for square tube:
    I = (b^4 - (b - 2t)^4) / 12
    """
    b = section.outer_dim_m
    t = section.thickness_m
    return (b**4 - (b - 2.0 * t)**4) / 12.0

def column_capacity_yield_kN(section: AluminumSection) -> float:
    A = column_area(section)
    fy = section.fy_MPa * 1e6  # Pa
    gamma = section.safety_factor
    N_allow_N = A * fy / gamma
    return N_allow_N / 1e3  # kN

def column_capacity_buckling_kN(section: AluminumSection, geom: ModuleGeometry) -> float:
    I = column_I(section)
    E = section.E_GPa * 1e9  # Pa
    L = geom.story_height
    K = section.K
    gamma = section.safety_factor

    N_cr_N = (math.pi**2 * E * I) / ((K * L)**2)
    N_allow_N = N_cr_N / gamma
    return N_allow_N / 1e3  # kN

def column_capacity_governing_kN(section: AluminumSection, geom: ModuleGeometry) -> float:
    Ny = column_capacity_yield_kN(section)
    Nb = column_capacity_buckling_kN(section, geom)
    return min(Ny, Nb)

def hempcrete_capacity_kN(hemp: HempcreteProperties) -> float:
    fc = hemp.fc_MPa * 1e6  # Pa
    A = hemp.area_m2
    gamma = hemp.safety_factor
    N_allow_N = fc * A / gamma
    return N_allow_N / 1e3  # kN

def max_stories(geom: ModuleGeometry,
                loads: LoadAssumptions,
                section: AluminumSection,
                hemp: HempcreteProperties) -> int:
    floor_load = floor_load_kN(geom, loads)
    col_cap = column_capacity_governing_kN(section, geom)
    total_col_cap = col_cap * geom.n_columns
    hemp_cap = hempcrete_capacity_kN(hemp)
    total_cap = total_col_cap + hemp_cap

    if floor_load <= 0:
        return 0
    return int(total_cap // floor_load)

def main():
    geom = ModuleGeometry()
    loads = LoadAssumptions()
    section = AluminumSection()
    hemp = HempcreteProperties(
        fc_MPa=0.5,   # conservative hempcrete strength
        area_m2=3.0,  # say 3 m^2 effective vertical area per module
        safety_factor=2.0
    )

    A_floor = module_floor_area(geom)
    floor_load = floor_load_kN(geom, loads)
    col_area = column_area(section)
    I_col = column_I(section)
    Ny = column_capacity_yield_kN(section)
    Nb = column_capacity_buckling_kN(section, geom)
    col_cap = column_capacity_governing_kN(section, geom)
    hemp_cap = hempcrete_capacity_kN(hemp)
    total_cap = col_cap * geom.n_columns + hemp_cap
    stories = max_stories(geom, loads, section, hemp)

    print("=== Extended Toy Structural Calculator ===")
    print(f"Module floor area: {A_floor:.2f} m^2")
    print(f"Floor load per story per module: {floor_load:.2f} kN")
    print()
    print(f"Aluminum column area: {col_area*1e6:.2f} mm^2")
    print(f"Column I: {I_col*1e12:.2f} mm^4")
    print(f"Yield capacity per column: {Ny:.2f} kN")
    print(f"Buckling capacity per column: {Nb:.2f} kN")
    print(f"Governing capacity per column: {col_cap:.2f} kN")
    print(f"Total column capacity (all columns): {col_cap * geom.n_columns:.2f} kN")
    print()
    print(f"Hempcrete capacity per module (vertical share): {hemp_cap:.2f} kN")
    print(f"Total vertical capacity (columns + hempcrete): {total_cap:.2f} kN")
    print()
    print(f"Estimated max stories (gravity + buckling, toy model): {stories}")
    print()
    print("NOTE: This is a conceptual tool only. It ignores lateral loads,")
    print("      connection design, frame bracing, and real code requirements.")

if __name__ == "__main__":
    main()
