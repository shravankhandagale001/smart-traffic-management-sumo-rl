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
        out_csv_name="outputs/2way-single-intersection/ppo",
        single_agent=True,
        use_gui=False,
        num_seconds=4000, # Train on episodes of 4000
    )

    # SWITCHING ARCHITECTURE: PPO (Proximal Policy Optimization) 
    # PPO learns an explicitly stochastic policy, preventing the catastrophic "gridlock loop"
    # that DQN suffers from during early epsilon-greedy exploration.
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=0.001,
        verbose=1,
    )
    
    # 20,000 steps is sufficient for PPO to converge on a simple single-intersection
    print("Training PPO Architecture...")
    model.learn(total_timesteps=6000)
    model.save("outputs/trained_ppo_2way-single-intersection_model")
    print("Training complete and model saved.")
    env.close()
