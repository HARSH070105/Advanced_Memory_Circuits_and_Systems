import matplotlib.pyplot as plt
import numpy as np
import csv

# Initialize lists to hold our data
capacities_bytes = []
access_times_ns = []
areas_mm2 = []
read_energies_nj = []

# Read the CACTI .out file
filename = 'cache_task2.cfg.out'
with open(filename, 'r') as f:
    # skipinitialspace handles the spaces after the commas in CACTI's output
    reader = csv.DictReader(f, skipinitialspace=True) 
    for row in reader:
        try:
            capacities_bytes.append(float(row['Capacity (bytes)']))
            access_times_ns.append(float(row['Access time (ns)']))
            areas_mm2.append(float(row['Area (mm2)']))
            read_energies_nj.append(float(row['Dynamic read energy (nJ)']))
        except (ValueError, KeyError):
            # Skips any malformed rows or empty lines
            continue

# Convert to numpy arrays for math operations
capacities_bytes = np.array(capacities_bytes)
access_times_ns = np.array(access_times_ns)
areas_mm2 = np.array(areas_mm2)
read_energies_nj = np.array(read_energies_nj)

# Calculate log2(Capacity) for the Amrutur & Horowitz plot
log2_cap = np.log2(capacities_bytes)
capacity_mb = capacities_bytes / (1024 * 1024)

# Setup the figure
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('CACTI 45nm Cache Scaling Trends (256KB - 16MB)', fontsize=16)

# Plot A: Access Time vs log2(Capacity) (Task 2 Requirement)
axes[0].plot(log2_cap, access_times_ns, marker='o', color='b', linewidth=2)
axes[0].set_title('Task 2: Access Time vs log2(Capacity)')
axes[0].set_xlabel('log2(Capacity in Bytes)')
axes[0].set_ylabel('Access Time (ns)')
axes[0].grid(True, linestyle='--', alpha=0.7)
# Annotate the points to see the step difference
for i, txt in enumerate(access_times_ns):
    axes[0].annotate(f"{txt:.2f}", (log2_cap[i], access_times_ns[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Plot B: Area vs Capacity
axes[1].plot(capacity_mb, areas_mm2, marker='s', color='r', linewidth=2)
axes[1].set_title('Area vs Capacity')
axes[1].set_xlabel('Capacity (MB)')
axes[1].set_ylabel('Area (mm²)')
axes[1].grid(True, linestyle='--', alpha=0.7)

# Plot C: Dynamic Read Energy vs Capacity
axes[2].plot(capacity_mb, read_energies_nj, marker='^', color='g', linewidth=2)
axes[2].set_title('Dynamic Read Energy vs Capacity')
axes[2].set_xlabel('Capacity (MB)')
axes[2].set_ylabel('Read Energy (nJ)')
axes[2].grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()