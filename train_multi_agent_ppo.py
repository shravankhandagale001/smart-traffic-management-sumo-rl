"""Train a shared-policy multi-agent PPO controller on a SUMO grid."""

import argparse
import os
import sys
from pathlib import Path

if "SUMO_HOME" not in os.environ:
    raise SystemExit("Please declare the environment variable 'SUMO_HOME'")
sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))

import ray
import sumo_rl
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from ray.tune.registry import register_env


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_NAME = "sumo_multi_agent_4x4"


def build_env(_env_config):
    """Create a PettingZoo parallel environment for RLlib."""
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
    parser = argparse.ArgumentParser(description="Train multi-agent PPO for SUMO traffic signals")
    parser.add_argument("--iterations", type=int, default=10, help="Number of PPO training iterations")
    parser.add_argument("--checkpoint-dir", default="outputs/multi_agent_ppo", help="Checkpoint directory")
    parser.add_argument("--num-workers", type=int, default=0, help="Ray rollout workers")
    args = parser.parse_args()
    checkpoint_dir = Path(args.checkpoint_dir).expanduser()
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    register_env(ENV_NAME, build_env)
    os.environ.setdefault("RAY_AUTH_MODE", "disabled")
    ray_kwargs = {"ignore_reinit_error": True}
    if os.environ.get("RAY_TMPDIR"):
        ray_kwargs["_temp_dir"] = os.environ["RAY_TMPDIR"]
    ray.init(**ray_kwargs)

    # Keep Ray/Tune logs beside the requested checkpoints instead of the
    # default user-home directory, which may be unavailable on restricted hosts.
    import ray.tune.trainable.trainable as trainable

    trainable.DEFAULT_STORAGE_PATH = str(checkpoint_dir / "ray_results")

    config = (
        PPOConfig()
        .environment(env=ENV_NAME, disable_env_checking=True)
        .api_stack(enable_rl_module_and_learner=False, enable_env_runner_and_connector_v2=False)
        .env_runners(num_env_runners=args.num_workers, rollout_fragment_length=128)
        .training(
            train_batch_size=512,
            lr=2e-5,
            gamma=0.95,
            lambda_=0.9,
            use_gae=True,
            clip_param=0.2,
            entropy_coeff=0.01,
            vf_loss_coeff=0.25,
            minibatch_size=64,
            num_epochs=10,
        )
        .framework(framework="torch")
        .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")))
        .debugging(log_level="ERROR")
    )

    algorithm = config.build()

    try:
        for iteration in range(1, args.iterations + 1):
            result = algorithm.train()
            print(
                f"iteration={iteration} "
                f"timesteps={result.get('timesteps_total')} "
                f"episode_reward_mean={result.get('episode_reward_mean')}"
            )
            checkpoint = algorithm.save(str(checkpoint_dir))
            print(f"checkpoint={checkpoint}")
    finally:
        algorithm.stop()
        ray.shutdown()


if __name__ == "__main__":
    main()
