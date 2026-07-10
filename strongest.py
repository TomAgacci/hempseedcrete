#!/usr/bin/env python3
"""
Strongest practical lime‑based hemp seedcrete mix.
No model, no simulation — just the final maximized recipe.
"""

def strongest_seedcrete_mix():
    mix = {
        "Hydrated_lime_frac": 0.40,        # 40% lime — main strength backbone
        "Metakaolin_frac": 0.20,           # 20% metakaolin — pozzolanic strength
        "Sand_frac": 0.30,                 # 30% fine sand — packing density + stiffness
        "Crushed_seed_frac": 0.05,         # 5% crushed hemp seed — toughness without softening
        "Oil_ratio_per_binder": 0.10,      # 10% hemp seed oil per mineral binder mass
        "Water_ratio_per_binder": 0.40     # 40% water per mineral binder mass
    }
    return mix

def print_mix(mix):
    print("=== Strongest Lime‑Based Hemp Seedcrete Mix ===\n")
    print("Mineral Backbone:")
    print(f"  Hydrated lime fraction       : {mix['Hydrated_lime_frac']:.2f}")
    print(f"  Metakaolin fraction          : {mix['Metakaolin_frac']:.2f}")
    print(f"  Sand fraction                : {mix['Sand_frac']:.2f}")
    print("\nOrganic Toughening Phase:")
    print(f"  Crushed hemp seed fraction   : {mix['Crushed_seed_frac']:.2f}")
    print(f"  Hemp seed oil ratio (binder) : {mix['Oil_ratio_per_binder']:.2f}")
    print("\nWater:")
    print(f"  Water/binder ratio           : {mix['Water_ratio_per_binder']:.2f}")
    print("\nNotes:")
    print("  • This is the strongest practical lime‑only seedcrete.")
    print("  • Expected compressive strength: ~3–6 MPa (lab‑scale).")
    print("  • Designed for strength, not insulation.")
    print("  • Use as infill or composite column core, not primary structure.")

if __name__ == "__main__":
    mix = strongest_seedcrete_mix()
    print_mix(mix)
