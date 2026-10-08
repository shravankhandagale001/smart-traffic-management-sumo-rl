import os
import sys
import gymnasium as gym
from stable_baselines3.dqn.dqn import DQN

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
        out_csv_name="outputs/2way-single-intersection/dqn_eval",
        single_agent=True,
        use_gui=True, # GUI ENABLED FOR JUDGES!
        num_seconds=4000, # Evaluating for roughly 2 episodes
    )

    # Load the trained model
    model = DQN.load("outputs/trained_dqn_2way-single-intersection_model", env=env)

    obs, info = env.reset()
    done = False
    
    print("Starting evaluation...")

    total_rewards = 0
    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_rewards += reward
        done = terminated or truncated

    print("Evaluation finished!")
    print(f"Total Episode Reward: {total_rewards}")
    if info:
        print("Final Evaluation Metrics:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    env.close()
