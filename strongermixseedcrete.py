#!/usr/bin/env python3
"""
Tama-style seedcrete strength engine
- Hybrid MgO + hemp seed oil binder
- Strength vs oil ratio curve
- Module-specific mix for 10x10 mm exoskeleton geometry
"""

from dataclasses import dataclass
from typing import List, Dict
import math

@dataclass
class ModuleGeometry:
    length_m: float = 0.3   # m
    width_m: float = 0.6    # m
    height_m: float = 0.2   # m
    cavity_fraction: float = 0.6  # fraction of volume available for seedcrete

@dataclass
class SeedcreteMix:
    # Ratios by mass relative to total seedcrete mass
    binder_fraction: float = 0.40   # mineral binder (MgO + NHL + MK)
    seed_powder_fraction: float = 0.20
    shiv_fraction: float = 0.10
    sand_fraction: float = 0.20
    oil_fraction_rel_binder: float = 0.10  # oil mass / binder mass
    water_fraction: float = 0.10           # approximate, for workability

@dataclass
class BinderComposition:
    MgO_frac: float = 0.60
    NHL_frac: float = 0.25
    MK_frac: float = 0.15

@dataclass
class StrengthModelParams:
    fc0_MPa: float = 4.0   # base mineral strength
    k1: float = 80.0       # linear oil contribution
    k2: float = 400.0      # quadratic softening

def module_volume(geom: ModuleGeometry) -> float:
    return geom.length_m * geom.width_m * geom.height_m

def seedcrete_cavity_volume(geom: ModuleGeometry) -> float:
    return module_volume(geom) * geom.cavity_fraction

def seedcrete_mass(geom: ModuleGeometry, density_kg_m3: float = 1400.0) -> float:
    return seedcrete_cavity_volume(geom) * density_kg_m3

def strength_vs_oil_ratio(params: StrengthModelParams, R_oil: float) -> float:
    """
    Simple peak model:
    fc(R) = fc0 + k1*R - k2*R^2
    """
    return params.fc0_MPa + params.k1 * R_oil - params.k2 * (R_oil ** 2)

def generate_strength_curve(params: StrengthModelParams,
                            R_min: float = 0.02,
                            R_max: float = 0.20,
                            n_points: int = 10) -> List[Dict[str, float]]:
    curve = []
    for i in range(n_points):
        R = R_min + (R_max - R_min) * i / (n_points - 1)
        fc = strength_vs_oil_ratio(params, R)
        curve.append({"R_oil": R, "fc_MPa": fc})
    return curve

def module_mix_breakdown(geom: ModuleGeometry,
                         mix: SeedcreteMix,
                         density_kg_m3: float = 1400.0) -> Dict[str, float]:
    m_total = seedcrete_mass(geom, density_kg_m3)

    m_binder = m_total * mix.binder_fraction
    m_seed_powder = m_total * mix.seed_powder_fraction
    m_shiv = m_total * mix.shiv_fraction
    m_sand = m_total * mix.sand_fraction
    m_oil = m_binder * mix.oil_fraction_rel_binder
    m_water = m_total * mix.water_fraction

    return {
        "m_total_kg": m_total,
        "m_binder_kg": m_binder,
        "m_seed_powder_kg": m_seed_powder,
        "m_shiv_kg": m_shiv,
        "m_sand_kg": m_sand,
        "m_oil_kg": m_oil,
        "m_water_kg": m_water,
    }

def print_strength_curve(curve: List[Dict[str, float]]):
    print("=== Seedcrete Strength vs Oil Ratio ===")
    for pt in curve:
        print(f"R_oil={pt['R_oil']:.3f} -> fc≈{pt['fc_MPa']:.2f} MPa")
    print()

def print_mix_breakdown(breakdown: Dict[str, float]):
    print("=== Module-Specific Seedcrete Mix Breakdown ===")
    for k, v in breakdown.items():
        print(f"{k}: {v:.3f} kg")
    print()

def main():
    # Geometry: 0.3 x 0.6 x 0.2 m block, 60% cavity for seedcrete
    geom = ModuleGeometry()
    mix = SeedcreteMix(
        binder_fraction=0.40,
        seed_powder_fraction=0.20,
        shiv_fraction=0.10,
        sand_fraction=0.20,
        oil_fraction_rel_binder=0.10,
        water_fraction=0.10,
    )
    params = StrengthModelParams(
        fc0_MPa=4.0,
        k1=80.0,
        k2=400.0,
    )

    # Generate strength curve for oil ratios
    curve = generate_strength_curve(params, R_min=0.02, R_max=0.20, n_points=10)
    print_strength_curve(curve)

    # Module-specific mass breakdown
    breakdown = module_mix_breakdown(geom, mix, density_kg_m3=1400.0)
    print_mix_breakdown(breakdown)

if __name__ == "__main__":
    main()
