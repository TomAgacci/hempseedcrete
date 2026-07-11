#!/usr/bin/env python3
"""
Plywood-like strongest seedcrete panel recipe.
This is a conceptual definition, not a structural design code.
"""

def strongest_seedcrete_core():
    """
    Core mix: strongest lime-based seedcrete we defined earlier,
    tuned for panel use (slightly lower water for stiffness).
    """
    return {
        "Hydrated_lime_frac": 0.40,        # 40% lime
        "Metakaolin_frac": 0.20,           # 20% metakaolin
        "Sand_frac": 0.30,                 # 30% fine sand
        "Crushed_seed_frac": 0.05,         # 5% crushed hemp seed
        "Oil_ratio_per_binder": 0.10,      # 10% hemp seed oil per mineral binder mass
        "Water_ratio_per_binder": 0.38     # slightly lower water for stiffer panels
    }

def plywood_like_panel():
    """
    Define a plywood-like seedcrete panel:
    - Seedcrete core
    - Fiber reinforcement near faces
    - Panel geometry
    """
    core = strongest_seedcrete_core()

    panel = {
        "Thickness_mm": 16,                # total panel thickness
        "Width_mm": 300,                   # example width
        "Length_mm": 600,                  # example length

        "Core_mix": core,

        # Fiber reinforcement layout (conceptual)
        "Fiber_layers": [
            {
                "Position": "top_face",
                "Type": "hemp_fabric",
                "Areal_weight_g_m2": 300
            },
            {
                "Position": "bottom_face",
                "Type": "hemp_fabric",
                "Areal_weight_g_m2": 300
            }
        ],

        # Optional: interlocking edge geometry for LEGO-like behavior
        "Edge_profile": {
            "Type": "tongue_and_groove",
            "Tongue_depth_mm": 8,
            "Tongue_thickness_mm": 6,
            "Groove_depth_mm": 8,
            "Groove_width_mm": 7
        }
    }

    return panel

def print_panel(panel):
    print("=== Plywood-like Strongest Seedcrete Panel ===\n")
    print("Geometry:")
    print(f"  Thickness : {panel['Thickness_mm']} mm")
    print(f"  Width     : {panel['Width_mm']} mm")
    print(f"  Length    : {panel['Length_mm']} mm\n")

    core = panel["Core_mix"]
    print("Core Seedcrete Mix (fractions of total solids):")
    print(f"  Hydrated lime fraction       : {core['Hydrated_lime_frac']:.2f}")
    print(f"  Metakaolin fraction          : {core['Metakaolin_frac']:.2f}")
    print(f"  Sand fraction                : {core['Sand_frac']:.2f}")
    print(f"  Crushed hemp seed fraction   : {core['Crushed_seed_frac']:.2f}")
    print("\nBinder ratios (per mineral binder mass):")
    print(f"  Hemp seed oil ratio          : {core['Oil_ratio_per_binder']:.2f}")
    print(f"  Water/binder ratio           : {core['Water_ratio_per_binder']:.2f}\n")

    print("Fiber Reinforcement:")
    for layer in panel["Fiber_layers"]:
        print(f"  {layer['Position']}: {layer['Type']} ({layer['Areal_weight_g_m2']} g/m²)")
    print("\nEdge Profile (LEGO-like interlock):")
    ep = panel["Edge_profile"]
    print(f"  Type               : {ep['Type']}")
    print(f"  Tongue depth       : {ep['Tongue_depth_mm']} mm")
    print(f"  Tongue thickness   : {ep['Tongue_thickness_mm']} mm")
    print(f"  Groove depth       : {ep['Groove_depth_mm']} mm")
    print(f"  Groove width       : {ep['Groove_width_mm']} mm")
    print("\nNotes:")
    print("  • This panel behaves more like fiber-cement board than true plywood.")
    print("  • Seedcrete core gives compression + mass; fibers give bending toughness.")
    print("  • Edge profile lets panels lock like LEGO between levels.")

if __name__ == "__main__":
    panel = plywood_like_panel()
    print_panel(panel)
