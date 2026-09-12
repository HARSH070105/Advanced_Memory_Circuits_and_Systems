# Advanced Memory Circuits and Systems --- Assignment 1

**Name:** Harsh Kapoor\
**Roll No.:** 2023112004\
**Course:** Advanced Memory Circuits and Systems\
**Assignment:** 1\
**Date:** September 12, 2026

This repository contains the simulation files, scripts, configuration
files, logs, plots, and report for Assignment 1 of **Advanced Memory
Circuits and Systems**.

The assignment studies memory behavior at several abstraction levels:

-   **Part A:** 6T SRAM cell using ngspice
-   **Part B:** 2 MB SRAM L2 cache using CACTI 7
-   **Part C:** 2 MB STT-MRAM cache using NVSim
-   **Part D:** DDR4 memory-system behavior using Ramulator 2.0
-   **Part E:** System-level SRAM vs. STT-MRAM cache evaluation using
    gem5

------------------------------------------------------------------------

## Repository Structure

``` text
AMCAS_Assignment1/
│
├── README.md (this file)
│
├── partA_ngspice/
│   ├── 45nm_bulk.txt
│   ├── lab1.sp
│   ├── plotter.py
│   ├── read_task1.csv
│   ├── read_task2.csv
│   ├── read_task4.csv
│   ├── task_1_results.txt
│   ├── task_2_results.txt
│   ├── task_3_plotter.py
│   ├── task_4_results.txt
│   ├── task1_plot.png
│   ├── task2_plot.png
│   ├── task3_plot.png
│   ├── task4_plot.png
│   └── vdd_sweep.csv
│
├── partB_cacti/
│   ├── 45nm.dat
│   ├── cache_task1.cfg
│   ├── cache_task2.cfg
│   ├── cache_task2.cfg.out
│   ├── cache_task3.cfg
│   ├── cache_task3.cfg.out
│   ├── cache.cfg
│   ├── cache_task3.cfg.out
│   ├── task1_log
│   ├── task2_script
│   ├── task3_script
│   ├── task2_plots.png
│   └── plot_task2.py
│
├── partC_nvsim/
│   ├── sample.cell
│   ├── sample_STTRAM.cell
│   ├── sample_STTRAM_aggressive.cell
│   ├── sample_STTRAM_cache.cfg
│   ├── Task1_logs.txt
│   ├── Task2_logs.txt
│   └── Task3_logs.txt
│
├── partD_ramulator/
│   ├── Logs/
│   ├── ddr4.yaml
│   └── l2miss.trace
│
├── partE_gem5/
│   └── Logs/
│       ├── mram_bfs/
│       ├── mram_sssp/
│       ├── mram_bfs_timingsimple/
│       ├── sram_bfs/
│       ├── sram_sssp/
│       ├── real_trace_capture/
│       ├── mram_bfs_run.log
│       ├── mram_bfs_summary.txt
│       ├── mram_bfs_timingsimple_run.log
│       ├── mram_sssp_run.log
│       ├── mram_sssp_summary.txt
│       ├── sram_bfs_summary.txt
│       ├── sram_sssp_run.log
│       └── sram_sssp_summary.txt
│
└── report/
    ├── AMCAS_A1_2023112004_report.pdf
    └── Assignment1_AMCAS.pdf
```

> The exact contents of generated-output directories such as `Logs/` may
> change depending on the simulation runs. The structure above reflects
> the organization used for this submission.

------------------------------------------------------------------------

# Part A --- ngspice: 6T SRAM Read and Read Margin

The first part evaluates a conventional **6T SRAM cell** using ngspice.

### Main setup

-   Technology: 45 nm bulk
-   (V\_{DD}): nominally 1.1 V
-   (W_P = 0.15,`\mu `{=tex}m)
-   (W_N = 0.20,`\mu `{=tex}m)
-   (W\_{access} = 0.16,`\mu `{=tex}m) nominal
-   (L = 0.045,`\mu `{=tex}m)
-   (C\_{BL}=C\_{BLB}=180) fF
-   Transient simulation: 4 ns
-   Maximum timestep: 5 ps
-   Read differential measured at (t=2) ns

### Experiments

1.  Measure the nominal SRAM read differential and read disturbance.
2.  Increase the access-transistor width from 0.16 µm to 0.24 µm.
3.  Sweep (V\_{DD}) and determine the minimum supply voltage at which
    the 25 mV sense-amplifier offset can be overcome.
4.  Repeat the read experiment at (85\^`\circ `{=tex}C).

### Key results

For the nominal configuration:

-   Read differential: **689.041 mV**
-   Maximum storage-node voltage: **198.812 mV**

Increasing (W\_{access}) to 0.24 µm gives:

-   Read differential: **815.023 mV**
-   Maximum storage-node voltage: **276.333 mV**

This demonstrates the SRAM sizing trade-off: a stronger access
transistor improves the read signal but increases read disturb.

The (V\_{DD}) sweep gives a critical supply voltage of approximately:

\[ V\_{DD,crit}`\approx 0.403`{=tex}`\text{ V}`{=tex} \]

for a 25 mV sense-amplifier offset.

At (85\^`\circ `{=tex}C):

-   Read differential: **582.287 mV**
-   Maximum storage-node voltage: **218.750 mV**

The elevated temperature reduces the read differential by approximately
**15.49%** relative to nominal operation.

### Files

-   `lab1.sp` --- ngspice circuit/netlist
-   `45nm_bulk.txt` --- transistor/model data
-   `read_task*.csv` --- simulation data
-   `vdd_sweep.csv` --- supply-voltage sweep data
-   `plotter.py`, `task_3_plotter.py` --- plotting/processing scripts
-   `task_*_results.txt` --- recorded results
-   `task*_plot.png` --- generated plots

------------------------------------------------------------------------

# Part B --- CACTI: 2 MB SRAM L2 Cache

CACTI 7 is used to evaluate a **2 MB SRAM L2 cache at 45 nm**.

### Baseline configuration

-   Capacity: 2 MB
-   Technology: 45 nm
-   Cache block: 64 B
-   Associativity: 8-way
-   Banks: 4
-   One read/write port
-   Temperature: 360 K

The baseline CACTI result is:

  Metric                                                      Result
  ------------------------- ----------------------------------------
  Access time                                             2.90184 ns
  Dynamic read energy                                    0.791312 nJ
  Leakage power                                           651.066 mW
  Area                                                   11.4742 mm²
  Data-array organization     ((N\_{dwl},N\_{dbl},N\_{spd})=(4,2,1))

### Experiments

#### Cache-capacity scaling

The cache capacity is swept from **256 KB to 16 MB**.

The results show:

-   Access time increases with cache capacity.
-   The increase becomes significantly steeper at larger capacities.
-   Area increases strongly with capacity.
-   Dynamic read energy also increases.

The report specifically shows that the access-time increase is **not** a
constant one-gate-delay penalty for every doubling.

#### Design-objective optimization

The 2 MB cache is optimized separately for:

-   Pure delay
-   Pure area
-   (ED\^2)

The pure-area configuration reduces area at the cost of higher access
latency, demonstrating the trade-off between physical organization and
timing.

#### Bitline-delay comparison

CACTI reports a data-array bitline delay of:

\[ t\_{BL,CACTI}=0.406901`\text{ ns}`{=tex} \]

A first-order distributed RC calculation gives approximately:

\[ t\_{BL,RC}=0.00926`\text{ ns}`{=tex} \]

The report discusses why the simple RC estimate is much smaller than the
complete CACTI cache-level delay.

### Files

-   `45nm.dat` --- CACTI technology data
-   `cache.cfg` --- cache configuration
-   `cache_task*.cfg` --- configurations for individual tasks
-   `cache_task*.cfg.out` --- CACTI outputs
-   `task1_log` --- recorded CACTI output
-   `task2_script`, `task3_script` --- experiment scripts
-   `plot_task2.py` --- plotting script
-   `task2_plots.png` --- generated scaling plots

------------------------------------------------------------------------

# Part C --- NVSim: 2 MB STT-MRAM Cache

NVSim is used to evaluate the same **2 MB, 64 B-line, 8-way cache
organization** using an STT-MRAM cell model.

### Baseline STT-MRAM cell

-   Cell area: (54F\^2)
-   Aspect ratio: 2.0
-   (R\_{on}=3,k`\Omega`{=tex})
-   (R\_{off}=6,k`\Omega`{=tex})
-   Read current: 40 µA
-   Set current: 200 µA
-   Reset current: 200 µA
-   Set/reset pulse duration: 10 ns

### Baseline results

  Metric                   STT-MRAM
  --------------- -----------------
  Read latency             3.674 ns
  Write latency           10.509 ns
  Read energy       0.572 nJ/access
  Write energy      1.538 nJ/access
  Leakage power          437.413 mW
  Area                    0.682 mm²

Compared with the SRAM baseline, STT-MRAM provides substantially lower
area, leakage power, and read energy, while SRAM provides lower read
latency and write energy.

### Additional experiments

#### Increasing TMR

The resistance values are changed to:

-   (R\_{on}=4,k`\Omega`{=tex})
-   (R\_{off}=12,k`\Omega`{=tex})

This increases the resistance ratio from 2 to 3. The resulting
cache-level improvements are small; read latency changes by only about
**0.52%**.

#### Reducing write current

Two cases are evaluated:

1.  Reduce only (I\_{reset}) from 200 µA to 100 µA.
2.  Reduce both (I\_{reset}) and (I\_{set}) to 100 µA.

Reducing both currents substantially lowers write energy:

\[ 1.538`\text{ nJ}`{=tex}`\rightarrow0.845`{=tex}`\text{ nJ}`{=tex} \]

which corresponds to approximately **45.1% reduction**.

The reported cache area remains unchanged for the supplied NVSim
configuration.

### Files

-   `sample.cell` --- supplied cell model
-   `sample_STTRAM.cell` --- STT-MRAM cell model
-   `sample_STTRAM_aggressive.cell` --- modified cell model
-   `sample_STTRAM_cache.cfg` --- cache configuration
-   `Task1_logs.txt`, `Task2_logs.txt`, `Task3_logs.txt` --- NVSim
    outputs/logs

------------------------------------------------------------------------

# Part D --- Ramulator 2.0: DDR4 L2-Miss Stream

Ramulator 2.0 is used to model the DDR4 memory traffic generated by the
L2 cache.

### Workload

The supplied trace contains:

-   **2048 total accesses**
-   **1536 reads**
-   **512 writes**

### Baseline memory configuration

-   DDR4-8Gb-x8
-   2 ranks
-   DDR4-2400
-   Single channel
-   Open-row policy
-   RoBaRaCoCh address mapping
-   All-bank refresh
-   FRFCFS scheduler

### Baseline results

-   Memory cycles: **768**
-   Total read latency: **3916 cycles**
-   Average read latency: **81.5833 cycles**
-   Row-buffer hits: **63**
-   Row-buffer misses: **1**
-   Row-buffer hit rate: **98.4375%**
-   Read throughput: **4801.92 MB/s**
-   Write throughput: **1600.64 MB/s**

### Experiments

The report evaluates:

1.  FRFCFS vs. the available `FRFCFS-RowHit` scheduler.
2.  Modified address mapping with row bits below bank bits.
3.  Increasing the number of channels from one to two.

An important implementation detail is that the installed Ramulator 2.0
build **does not provide a true FCFS scheduler**, so `FRFCFS-RowHit` was
used as the available alternative. Therefore, the reported scheduler
comparison should not be interpreted as a genuine FCFS-vs-FRFCFS
comparison.

Similarly, the supplied trace has all channel fields mapped to channel
0. Consequently, adding a second channel produces no measurable benefit
because channel 1 remains unused.

### Files

-   `ddr4.yaml` --- DDR4 configuration
-   `l2miss.trace` --- L2 miss/access trace
-   `Logs/` --- Ramulator simulation outputs

------------------------------------------------------------------------

# Part E --- gem5: System-Level SRAM vs. STT-MRAM

The final part evaluates the effect of the cache technologies at the
**system level** using gem5.

### Configurations

Two L2 cache configurations are evaluated with an O3CPU and DDR4-2400
backing memory:

  Configuration            L2 Capacity   L2 Hit Latency
  ---------------------- ------------- ----------------
  SRAM baseline                  2 MiB         7 cycles
  STT-MRAM alternative           8 MiB        14 cycles

The simulations are performed for the `bfs` and `sssp` kernels.

> In the current environment, the GAPBS executables were unavailable.
> Compact deterministic stand-in programs using the same kernel names
> were therefore used for the reported experiments.

### O3CPU results

  Kernel   Cache             IPC   L2 Miss Rate   simSeconds
  -------- ---------- ---------- -------------- ------------
  bfs      SRAM         0.681882       0.867524     0.000182
  bfs      STT-MRAM     0.644431       0.867786     0.000192
  sssp     SRAM          1.43357       0.876168     0.000285
  sssp     STT-MRAM      1.38557       0.875978     0.000294

For both workloads, the **SRAM configuration performs better**. The
larger STT-MRAM cache does not reduce the L2 miss rate enough to
compensate for its additional seven cycles of hit latency.

### TimingSimpleCPU

The SRAM configuration is also rerun with TimingSimpleCPU:

  Kernel          IPC   L2 Miss Rate   simSeconds
  -------- ---------- -------------- ------------
  bfs        0.240794       0.880444     0.000515
  sssp       0.300071       0.887759      0.00136

The substantially lower IPC compared with O3CPU illustrates the effect
of out-of-order latency hiding: O3CPU can execute independent
instructions while outstanding memory operations are being serviced,
whereas TimingSimpleCPU exposes more of the memory latency directly.

### Files

-   `Logs/mram_bfs/` --- STT-MRAM BFS results
-   `Logs/mram_sssp/` --- STT-MRAM SSSP results
-   `Logs/mram_bfs_timingsimple/` --- TimingSimpleCPU results
-   `Logs/sram_bfs/` --- SRAM BFS results
-   `Logs/sram_sssp/` --- SRAM SSSP results
-   `Logs/real_trace_capture/` --- trace-capture results
-   `*_run.log` --- simulation logs
-   `*_summary.txt` --- summarized results

------------------------------------------------------------------------

# Overall Conclusions

The assignment evaluates memory from the **cell level through the full
system level**.

### 6T SRAM

A stronger access transistor produces a larger read differential but
also increases read disturb. Lowering (V\_{DD}) eventually causes the
generated read differential to approach the sense-amplifier offset.
Temperature also degrades the read differential and increases the
storage-node disturbance.

### SRAM Cache

Increasing cache capacity improves storage capacity but causes
increasing access time, area, and dynamic energy. CACTI optimization
demonstrates that there is no universally optimal internal cache
organization: the best organization depends on whether delay, area, or
an energy-delay objective is being optimized.

### STT-MRAM

STT-MRAM provides a major density advantage and lower leakage power,
along with lower read energy in the evaluated configuration. Its
disadvantages are higher read latency and higher write energy.
Increasing TMR has only a small effect at the complete-cache level for
the evaluated configuration.

### DDR4 Memory System

The supplied workload exhibits very high row locality under the baseline
mapping. Changing the address mapping to reduce row locality
substantially lowers the row-buffer hit rate and increases average read
latency. Adding a second channel has no effect because the supplied
trace does not exercise it.

### System-Level Cache Choice

For the evaluated gem5 workloads, the **2 MiB SRAM L2 remains faster
than the 8 MiB STT-MRAM L2**. The larger MRAM cache does not achieve a
sufficient reduction in miss rate to compensate for its higher hit
latency.

Thus, the results illustrate the central memory-system trade-off:

> **SRAM favors speed, while STT-MRAM favors density, leakage, and
> read-energy efficiency.**

The preferred technology ultimately depends on workload locality, cache
capacity, timing assumptions, and the surrounding memory system.

------------------------------------------------------------------------

## Report

The complete assignment report is available under:

``` text
report/
├── AMCAS_A1_2023112004_report.pdf
└── Assignment1_AMCAS.pdf
```

The report contains the detailed simulation methodology, numerical
results, plots, comparisons, and discussion for all five parts.
