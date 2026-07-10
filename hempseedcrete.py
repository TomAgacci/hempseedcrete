#!/usr/bin/env python3
"""
Tama-style quantitative model for hemp-seed-oil / lime hybrid binder.
Mix design + property prediction.

Assumptions:
- m_L, m_S, m_O in kg (or any consistent mass unit)
- P_c in MPa (curing pressure)
- Constants tuned heuristically; adjust with lab data.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class MixDesign:
    m_L: float  # lime mass
    m_S: float  # seed powder mass
    m_O: float  # hemp seed oil mass
    phi0: float # base porosity (0-1)
    P_c: float  # curing pressure (MPa)

@dataclass
class ModelConstants:
    alpha_L: float = 1.0
    alpha_O: float = 0.6
    alpha_S: float = 0.3
    k_P: float = 0.10   # porosity reduction per MPa
    k_O: float = 0.15   # porosity reduction per R_OL
    C1: float = 10.0    # compressive strength scale
    C2: float = 5.0     # flexural strength scale
    beta: float = 2.0   # porosity penalty
    gamma: float = 1.5  # toughness boost from organic phase

def compute_ratios(mix: MixDesign):
    m_L, m_S, m_O = mix.m_L, mix.m_S, mix.m_O
    R_SL = m_S / m_L if m_L > 0 else 0.0
    R_OL = m_O / m_L if m_L > 0 else 0.0
    R_OS = m_O / m_S if m_S > 0 else 0.0
    return R_SL, R_OL, R_OS

def compute_binder_eff(mix: MixDesign, const: ModelConstants):
    m_L, m_S, m_O = mix.m_L, mix.m_S, mix.m_O
    return (const.alpha_L * m_L +
            const.alpha_O * m_O +
            const.alpha_S * m_S)

def compute_porosity(mix: MixDesign, const: ModelConstants):
    _, R_OL, _ = compute_ratios(mix)
    phi = mix.phi0 - const.k_P * mix.P_c - const.k_O * R_OL
    # clamp to [0, 0.8] for sanity
    return max(0.0, min(0.8, phi))

def compute_strengths(mix: MixDesign, const: ModelConstants):
    B_eff = compute_binder_eff(mix, const)
    phi = compute_porosity(mix, const)
    m_L, m_S, m_O = mix.m_L, mix.m_S, mix.m_O

    # Compressive strength
    fc = const.C1 * (B_eff / (1.0 + const.beta * phi))

    # Flexural strength
    if B_eff > 0:
        mineral_frac = m_L / B_eff
        organic_frac = (m_O + m_S) / B_eff
    else:
        mineral_frac = organic_frac = 0.0

    ff = const.C2 * (mineral_frac + const.gamma * organic_frac)

    return fc, ff, phi, B_eff

def describe_mix(mix: MixDesign, const: ModelConstants):
    R_SL, R_OL, R_OS = compute_ratios(mix)
    fc, ff, phi, B_eff = compute_strengths(mix, const)

    return {
        "m_L": mix.m_L,
        "m_S": mix.m_S,
        "m_O": mix.m_O,
        "R_SL": R_SL,
        "R_OL": R_OL,
        "R_OS": R_OS,
        "phi": phi,
        "B_eff": B_eff,
        "fc_MPa": fc,
        "ff_MPa": ff,
        "P_c_MPa": mix.P_c,
    }

def print_mix_summary(label: str, summary: dict):
    print(f"=== {label} ===")
    print(f"m_L={summary['m_L']:.3f}, m_S={summary['m_S']:.3f}, m_O={summary['m_O']:.3f}")
    print(f"R_SL={summary['R_SL']:.3f}, R_OL={summary['R_OL']:.3f}, R_OS={summary['R_OS']:.3f}")
    print(f"Porosity phi={summary['phi']:.3f}")
    print(f"B_eff={summary['B_eff']:.3f}")
    print(f"fc (compressive) ≈ {summary['fc_MPa']:.2f} MPa")
    print(f"ff (flexural)   ≈ {summary['ff_MPa']:.2f} MPa")
    print(f"Curing pressure P_c={summary['P_c_MPa']:.2f} MPa")
    print()

def main():
    const = ModelConstants()

    # Example regimes (normalized lime mass = 1.0)
    mixes: List[MixDesign] = [
        MixDesign(m_L=1.0, m_S=0.3, m_O=0.03, phi0=0.40, P_c=0.2),  # mineral-dominant
        MixDesign(m_L=1.0, m_S=0.5, m_O=0.10, phi0=0.40, P_c=0.4),  # hybrid balanced
        MixDesign(m_L=1.0, m_S=0.7, m_O=0.20, phi0=0.40, P_c=0.6),  # organic-rich
        MixDesign(m_L=1.0, m_S=0.8, m_O=0.30, phi0=0.40, P_c=0.8),  # resin-dominant
    ]

    labels = [
        "Mineral-dominant",
        "Hybrid balanced",
        "Organic-rich",
        "Resin-dominant",
    ]

    for label, mix in zip(labels, mixes):
        summary = describe_mix(mix, const)
        print_mix_summary(label, summary)

if __name__ == "__main__":
    main()
