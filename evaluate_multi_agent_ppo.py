"""Evaluate a multi-agent PPO checkpoint on the SUMO 4x4 grid."""

import argparse
import os
import sys
from pathlib import Path

if "SUMO_HOME" not in os.environ:
    raise SystemExit("Please declare the environment variable 'SUMO_HOME'")
sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))

import ray
import sumo_rl
from ray.rllib.algorithms.algorithm import Algorithm
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from ray.tune.registry import register_env


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_NAME = "sumo_multi_agent_4x4"


def build_env(_env_config):
    return ParallelPettingZooEnv(
        sumo_rl.parallel_env(
            net_file=str(PROJECT_ROOT / "sumo_rl/nets/4x4-Lucas/4x4.net.xml"),
            route_file=str(PROJECT_ROOT / "sumo_rl/nets/4x4-Lucas/4x4c1c2c1c2.rou.xml"),
            out_csv_name=None,
            use_gui=False,
            num_seconds=3600,
        )
    )


def main():
    parser = argparse.ArgumentParser(description="Evaluate multi-agent PPO for SUMO traffic signals")
    parser.add_argument("checkpoint", help="Path returned by train_multi_agent_ppo.py")
    parser.add_argument("--seconds", type=int, default=3600, help="Simulation duration")
    parser.add_argument("--out-csv", default=None, help="Optional CSV output prefix")
    args = parser.parse_args()

    checkpoint_dir = Path(args.checkpoint).resolve().parent
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("RAY_AUTH_MODE", "disabled")
    os.environ.setdefault("RAY_TMPDIR", str(checkpoint_dir / "ray_tmp"))

    import ray.tune.trainable.trainable as trainable

    trainable.DEFAULT_STORAGE_PATH = str(checkpoint_dir / "ray_results")
    register_env(ENV_NAME, build_env)
    ray.init(ignore_reinit_error=True, _temp_dir=os.environ["RAY_TMPDIR"])
    algorithm = Algorithm.from_checkpoint(args.checkpoint)
    env = sumo_rl.parallel_env(
        net_file=str(PROJECT_ROOT / "sumo_rl/nets/4x4-Lucas/4x4.net.xml"),
        route_file=str(PROJECT_ROOT / "sumo_rl/nets/4x4-Lucas/4x4c1c2c1c2.rou.xml"),
        out_csv_name=args.out_csv,
        use_gui=False,
        num_seconds=args.seconds,
    )

    try:
        observations, _ = env.reset()
        total_reward = 0.0
        steps = 0
        done = False
        final_info = {}

        # PettingZoo's conversion wrapper can stall on the exact SUMO horizon
        # boundary; stop one step before it and report the completed prefix.
        while not done and steps < max(1, args.seconds - 1):
            actions = {}
            for agent_id, observation in observations.items():
                action = algorithm.compute_single_action(
                    observation,
                    policy_id="default_policy",
                    explore=False,
                )
                actions[agent_id] = action[0] if isinstance(action, tuple) else action

            observations, rewards, terminations, truncations, infos = env.step(actions)
            total_reward += sum(float(value) for value in rewards.values())
            steps += 1
            final_info = next(iter(infos.values()), {})
            done = terminations.get("__all__", False) or truncations.get("__all__", False)

        print(f"steps={steps}")
        print(f"total_reward={total_reward:.6f}")
        for key, value in final_info.items():
            if key.startswith("system"):
                print(f"{key}={value}")
    finally:
        env.close()
        algorithm.stop()
        ray.shutdown()


if __name__ == "__main__":
    main()
