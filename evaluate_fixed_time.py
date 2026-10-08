import os
import sys
import gymnasium as gym

# Ensure SUMO is found
if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumo_rl import SumoEnvironment

if __name__ == "__main__":
    env = SumoEnvironment(
        net_file="sumo_rl/nets/2way-single-intersection/single-intersection.net.xml",
        route_file="sumo_rl/nets/2way-single-intersection/single-intersection-vhvh.rou.xml",
        single_agent=True,
        use_gui=True, # GUI ENABLED!
        num_seconds=4000, 
        fixed_ts=True # FOLLOW FIXED-TIME SUMO LOGIC
    )

    obs, info = env.reset()
    done = False
    
    print("Starting fixed-time GUI demonstration...")

    # The AI is NOT used here. `env.step(None)` tells the environment to ignore actions
    # and just advance the traffic lights using the preset timed phases.
    while not done:
        obs, reward, terminated, truncated, info = env.step(None)
        done = terminated or truncated

    print("Fixed-time demonstration finished!")
    if info:
        print("Final Evaluation Metrics (Fixed-Time):")
        for key, value in info.items():
            print(f"  {key}: {value}")
    env.close()
