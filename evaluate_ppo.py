import os
import sys

if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumo_rl import SumoEnvironment
from stable_baselines3 import PPO

if __name__ == "__main__":
    env = SumoEnvironment(
        net_file="sumo_rl/nets/2way-single-intersection/single-intersection.net.xml",
        route_file="sumo_rl/nets/2way-single-intersection/single-intersection-vhvh.rou.xml",
        out_csv_name="outputs/2way-single-intersection/ppo_eval",
        single_agent=True,
        use_gui=True, # GUI ENABLED FOR JUDGES!
        num_seconds=4000, 
    )

    # Load the highly optimized PPO model
    model = PPO.load("outputs/trained_ppo_2way-single-intersection_model.zip", env=env)

    obs, info = env.reset()
    done = False
    
    print("Starting PPO evaluation...")

    total_rewards = 0
    while not done:
        action, _states = model.predict(obs, deterministic=False)
        obs, reward, terminated, truncated, info = env.step(action)
        total_rewards += reward
        done = terminated or truncated

    print("Evaluation finished!")
    print(f"Total Episode Reward: {total_rewards}")
    if info:
        print("Final Evaluation Metrics (PPO RL Model):")
        for key, value in info.items():
            print(f"  {key}: {value}")
    env.close()
