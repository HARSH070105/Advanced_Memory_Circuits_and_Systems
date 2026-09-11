import pandas as pd
import matplotlib.pyplot as plt

# Load the ngspice CSV data
# ngspice puts a bunch of spaces in the headers, so we clean them up
df = pd.read_csv('read_task1.csv', delim_whitespace=True)
df.columns = ['time', 'v_bl', 'time2', 'v_blb', 'time3', 'v_q', 'time4', 'v_qb']

plt.figure(figsize=(8, 5))
plt.plot(df['time'] * 1e9, df['v_q'], label='V(q)', color='red', linewidth=2)
plt.plot(df['time'] * 1e9, df['v_qb'], label='V(qb)', color='blue', linewidth=2)

plt.title('SRAM Read (W_access = 0.16 µm)')
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('task1_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved as task1_plot.png")