import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


if len(sys.argv) != 2:
    print("Usage: python plot_vdd.py <path_to_csv>")
    sys.exit(1)

file_path = sys.argv[1]

# Read CSV
df = pd.read_csv(file_path)

# Remove accidental whitespace from column names
df.columns = df.columns.str.strip()

# Check required columns
if "VDD" not in df.columns or "dv" not in df.columns:
    print("Error: File must contain 'VDD' and 'dv' columns.")
    print("Found columns:", list(df.columns))
    sys.exit(1)

# Sort by VDD for a clean plot
df = df.sort_values("VDD")

# Convert ΔV from V to mV
df["dv_mV"] = df["dv"] * 1000

# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["VDD"],
    df["dv_mV"],
    marker="o",
    linewidth=2,
    label=r"$\Delta V$ (BL, BLB)"
)

# Sense amplifier offset
plt.axhline(
    25,
    linestyle="--",
    linewidth=2,
    label="Sense-amp offset = 25 mV"
)

plt.xlabel("VDD (V)")
plt.ylabel(r"$\Delta V$ (mV)")
plt.title("SRAM Read Margin vs VDD")

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

# Save next to input file
output_path = os.path.join(
    os.path.dirname(file_path),
    "task3_plot.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Plot saved to:")
print(output_path)