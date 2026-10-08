import pandas as pd
import glob

files = sorted(glob.glob('outputs/2way-single-intersection/dqn_eval*.csv'))
print(f"Found {len(files)} evaluation files.")
for i, f in enumerate(files):
    df = pd.read_csv(f)
    print(f"--- Evaluation Episode {i+1} ---")
    print(f"Mean Delay: {df['system_mean_waiting_time'].mean():.2f} seconds")
    print(f"Final Total Wait Time: {df['system_total_waiting_time'].iloc[-1]} seconds")
    print(f"Mean Speed: {df['system_mean_speed'].mean():.2f} m/s")
    print(f"Max Stopped Vehicles: {df['system_total_stopped'].max()}")
    print()
