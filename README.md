<img src="docs/_static/logo.png" align="right" width="30%"/>

[![DOI](https://zenodo.org/badge/161216111.svg)](https://zenodo.org/doi/10.5281/zenodo.10869789)
[![tests](https://github.com/LucasAlegre/sumo-rl/actions/workflows/linux-test.yml/badge.svg)](https://github.com/LucasAlegre/sumo-rl/actions/workflows/linux-test.yml)
[![PyPI version](https://badge.fury.io/py/sumo-rl.svg)](https://badge.fury.io/py/sumo-rl)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/LucasAlegre/sumo-rl/blob/main/LICENSE)

# Smart Traffic Management with PPO and SUMO-RL

This repository contains a smart traffic-signal-control project built with
[SUMO](https://eclipse.dev/sumo/) and reinforcement learning. The main custom
experiment uses **Proximal Policy Optimization (PPO)** on a two-way single
intersection. DQN and fixed-time signal control are included as comparison
baselines.

The project is built on top of the open-source
[SUMO-RL](https://github.com/LucasAlegre/sumo-rl) environment. The original
SUMO-RL license and attribution are retained in this repository.

## Project workflow

```text
SUMO network and vehicle routes
        ↓
SumoEnvironment
        ↓
Traffic observations: phase, density, and queues
        ↓
PPO or DQN action
        ↓
Traffic-light phase control in SUMO
        ↓
Waiting-time reward and traffic metrics
        ↓
Trained model and CSV evaluation results
```

The default reward is based on the change in accumulated waiting time. The
agent is rewarded when total waiting decreases and penalized when congestion
increases.

## Main implementation files

| File | Purpose |
| --- | --- |
| `train_ppo_2way.py` | Train and save the PPO controller. |
| `evaluate_ppo.py` | Evaluate the trained PPO controller. |
| `evaluate_dqn.py` | Evaluate the trained DQN controller. |
| `evaluate_fixed_time.py` | Run the traditional fixed-time baseline. |
| `evaluation.py` | Summarize generated CSV traffic metrics. |
| `sumo_rl/environment/env.py` | Gymnasium/SUMO environment and metrics. |
| `sumo_rl/environment/traffic_signal.py` | Signal actions and reward functions. |
| `sumo_rl/environment/observations.py` | Traffic-signal observation space. |
| `sumo_rl/nets/2way-single-intersection/` | Network, route, and SUMO configuration files. |

An additional Ray RLlib PPO experiment is available at
`experiments/ppo_4x4grid.py`. It uses a separate 4×4 grid environment.

## Quick start

### Windows

Install SUMO from the [official SUMO website](https://eclipse.dev/sumo/), then
open PowerShell from the repository root and set `SUMO_HOME`:

```powershell
$env:SUMO_HOME = "C:\Program Files (x86)\Eclipse\Sumo"
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
pip install stable-baselines3 torch
```

If the project already includes a working virtual environment, activate it
instead:

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux

Install SUMO and set `SUMO_HOME` according to the SUMO installation path:

```bash
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
export SUMO_HOME="/usr/share/sumo"
python -m venv venv
source venv/bin/activate
pip install -e .
pip install stable-baselines3 torch
```

## Run the project

Run all commands from the repository root because the experiment scripts use
project-relative SUMO network and output paths.

Train PPO:

```bash
python train_ppo_2way.py
```

Evaluate PPO, DQN, and fixed-time control:

```bash
python evaluate_ppo.py
python evaluate_dqn.py
python evaluate_fixed_time.py
```

The evaluation scripts currently enable the SUMO GUI. For servers, CI, or
headless systems, change `use_gui=True` to `use_gui=False` in the evaluation
scripts.

Summarize CSV results:

```bash
python evaluation.py
```

Trained model files are stored in `outputs/`. Generated CSV logs should
normally remain local and should not be committed unless they are being used
as documented experiment artifacts.

## Evaluation metrics

The environment reports metrics including:

- Total and mean waiting time.
- Mean traffic speed.
- Number of stopped vehicles.
- Arrived and departed vehicles.
- Teleported vehicles.
- Cumulative RL reward.

Results can vary between runs because SUMO traffic simulations and RL policies
can be stochastic. For a fair scientific comparison, evaluate each controller
over the same traffic seeds and multiple episodes.

## Repository structure

```text
.
├── train_ppo_2way.py
├── evaluate_ppo.py
├── evaluate_dqn.py
├── evaluate_fixed_time.py
├── evaluation.py
├── experiments/
├── sumo_rl/
│   ├── environment/
│   └── nets/
├── outputs/
│   ├── trained_ppo_2way-single-intersection_model.zip
│   └── trained_dqn_2way-single-intersection_model.zip
├── architecture_prototype_explanation.md
├── pyproject.toml
├── setup.py
└── LICENSE
```

## Attribution

This project extends and uses the
[Lucas Alegre SUMO-RL project](https://github.com/LucasAlegre/sumo-rl).
Please retain the included `LICENSE` and `CITATION.bib` files when publishing
or redistributing this repository.

<!-- start intro -->

SUMO-RL provides a simple interface to instantiate Reinforcement Learning (RL) environments with [SUMO](https://github.com/eclipse/sumo) for Traffic Signal Control.

Goals of this repository:
- Provide a simple interface to work with Reinforcement Learning for Traffic Signal Control using SUMO
- Support Multiagent RL
- Compatibility with gymnasium.Env and popular RL libraries such as [stable-baselines3](https://github.com/DLR-RM/stable-baselines3) and [RLlib](https://docs.ray.io/en/main/rllib.html)
- Easy customisation: state and reward definitions are easily modifiable

The main class is [SumoEnvironment](https://github.com/LucasAlegre/sumo-rl/blob/main/sumo_rl/environment/env.py).
If instantiated with parameter 'single-agent=True', it behaves like a regular [Gymnasium Env](https://github.com/Farama-Foundation/Gymnasium).
For multiagent environments, use [env](https://github.com/LucasAlegre/sumo-rl/blob/main/sumo_rl/environment/env.py) or [parallel_env](https://github.com/LucasAlegre/sumo-rl/blob/main/sumo_rl/environment/env.py) to instantiate a [PettingZoo](https://github.com/PettingZoo-Team/PettingZoo) environment with AEC or Parallel API, respectively.
[TrafficSignal](https://github.com/LucasAlegre/sumo-rl/blob/main/sumo_rl/environment/traffic_signal.py) is responsible for retrieving information and actuating on traffic lights using [TraCI](https://sumo.dlr.de/wiki/TraCI) API.

For more details, check the [documentation online](https://lucasalegre.github.io/sumo-rl/).

<!-- end intro -->

## Install

<!-- start install -->

### Install SUMO latest version:

```bash
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
```
Don't forget to set SUMO_HOME variable (default sumo installation path is /usr/share/sumo)
```bash
echo 'export SUMO_HOME="/usr/share/sumo"' >> ~/.bashrc
source ~/.bashrc
```
Important: for a huge performance boost (~8x) with Libsumo, you can declare the variable:
```bash
export LIBSUMO_AS_TRACI=1
```
Notice that you will not be able to run with sumo-gui or with multiple simulations in parallel if this is active ([more details](https://sumo.dlr.de/docs/Libsumo.html)).

### Install SUMO-RL

Stable release version is available through pip
```bash
pip install sumo-rl
```

Alternatively, you can install using the latest (unreleased) version
```bash
git clone https://github.com/LucasAlegre/sumo-rl
cd sumo-rl
pip install -e .
```

<!-- end install -->

## MDP - Observations, Actions and Rewards

### Observation

<!-- start observation -->

The default observation for each traffic signal agent is a vector:
```python
    obs = [phase_one_hot, min_green, lane_1_density,...,lane_n_density, lane_1_queue,...,lane_n_queue]
```
- ```phase_one_hot``` is a one-hot encoded vector indicating the current active green phase
- ```min_green``` is a binary variable indicating whether min_green seconds have already passed in the current phase
- ```lane_i_density``` is the number of vehicles in incoming lane i dividided by the total capacity of the lane
- ```lane_i_queue```is the number of queued (speed below 0.1 m/s) vehicles in incoming lane i divided by the total capacity of the lane

You can define your own observation by implementing a class that inherits from [ObservationFunction](https://github.com/LucasAlegre/sumo-rl/blob/main/sumo_rl/environment/observations.py) and passing it to the environment constructor.

<!-- end observation -->

### Action

<!-- start action -->

The action space is discrete.
Every 'delta_time' seconds, each traffic signal agent can choose the next green phase configuration.

E.g.: In the [2-way single intersection](https://github.com/LucasAlegre/sumo-rl/blob/main/experiments/dqn_2way-single-intersection.py) there are |A| = 4 discrete actions, corresponding to the following green phase configurations:

<p align="center">
<img src="docs/_static/actions.png" align="center" width="75%"/>
</p>

Important: every time a phase change occurs, the next phase is preeceded by a yellow phase lasting ```yellow_time``` seconds.

<!-- end action -->

### Rewards

<!-- start reward -->

The default reward function is the change in cumulative vehicle delay:

<p align="center">
<img src="docs/_static/reward.png" align="center" width="25%"/>
</p>

That is, the reward is how much the total delay (sum of the waiting times of all approaching vehicles) changed in relation to the previous time-step.

You can choose a different reward function (see the ones implemented in [TrafficSignal](https://github.com/LucasAlegre/sumo-rl/blob/main/sumo_rl/environment/traffic_signal.py)) with the parameter `reward_fn` in the [SumoEnvironment](https://github.com/LucasAlegre/sumo-rl/blob/main/sumo_rl/environment/env.py) constructor.

It is also possible to implement your own reward function:

```python
def my_reward_fn(traffic_signal):
    return traffic_signal.get_average_speed()

env = SumoEnvironment(..., reward_fn=my_reward_fn)
```

<!-- end reward -->

## API's (Gymnasium and PettingZoo)

### Gymnasium Single-Agent API

<!-- start gymnasium -->

If your network only has ONE traffic light, then you can instantiate a standard Gymnasium env (see [Gymnasium API](https://gymnasium.farama.org/api/env/)):
```python
import gymnasium as gym
import sumo_rl
env = gym.make('sumo-rl-v0',
                net_file='path_to_your_network.net.xml',
                route_file='path_to_your_routefile.rou.xml',
                out_csv_name='path_to_output.csv',
                use_gui=True,
                num_seconds=100000)
obs, info = env.reset()
done = False
while not done:
    next_obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    done = terminated or truncated
```

<!-- end gymnasium -->

### PettingZoo Multi-Agent API

<!-- start pettingzoo -->

For multi-agent environments, you can use the PettingZoo API (see [Petting Zoo API](https://pettingzoo.farama.org/api/parallel/)):

```python
import sumo_rl
env = sumo_rl.parallel_env(net_file='nets/RESCO/grid4x4/grid4x4.net.xml',
                  route_file='nets/RESCO/grid4x4/grid4x4_1.rou.xml',
                  use_gui=True,
                  num_seconds=3600)
observations = env.reset()
while env.agents:
    actions = {agent: env.action_space(agent).sample() for agent in env.agents}  # this is where you would insert your policy
    observations, rewards, terminations, truncations, infos = env.step(actions)
```

<!-- end pettingzoo -->

### RESCO Benchmarks

In the folder [nets/RESCO](https://github.com/LucasAlegre/sumo-rl/tree/main/sumo_rl/nets/RESCO) you can find the network and route files from [RESCO](https://github.com/jault/RESCO) (Reinforcement Learning Benchmarks for Traffic Signal Control), which was built on top of SUMO-RL. See their [paper](https://people.engr.tamu.edu/guni/Papers/NeurIPS-signals.pdf) for results.

<p align="center">
<img src="sumo_rl/nets/RESCO/maps.png" align="center" width="60%"/>
</p>

### Experiments

Check [experiments](https://github.com/LucasAlegre/sumo-rl/tree/main/experiments) for examples on how to instantiate an environment and train your RL agent.

### [Q-learning](https://github.com/LucasAlegre/sumo-rl/blob/main/agents/ql_agent.py) in a one-way single intersection:
```bash
python experiments/ql_single-intersection.py
```

### [RLlib PPO](https://docs.ray.io/en/latest/_modules/ray/rllib/algorithms/ppo/ppo.html) multiagent in a 4x4 grid:
```bash
python experiments/ppo_4x4grid.py
```

### [stable-baselines3 DQN](https://github.com/DLR-RM/stable-baselines3/blob/master/stable_baselines3/dqn/dqn.py) in a 2-way single intersection:
Obs: you need to install stable-baselines3 with ```pip install "stable_baselines3[extra]>=2.0.0a9"``` for [Gymnasium compatibility](https://stable-baselines3.readthedocs.io/en/master/guide/install.html).
```bash
python experiments/dqn_2way-single-intersection.py
```

### Plotting results:
```bash
python outputs/plot.py -f outputs/4x4grid/ppo_conn0_ep2
```
<p align="center">
<img src="outputs/result.png" align="center" width="50%"/>
</p>

## Citing

<!-- start citation -->

If you use this repository in your research, please cite:
```bibtex
@misc{sumorl,
    author = {Lucas N. Alegre},
    title = {{SUMO-RL}},
    year = {2019},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/LucasAlegre/sumo-rl}},
}
```

<!-- end citation -->

<!-- start list of publications -->

List of publications that use SUMO-RL (please open a pull request to add missing entries):
- [Quantifying the impact of non-stationarity in reinforcement learning-based traffic signal control (Alegre et al., 2021)](https://peerj.com/articles/cs-575/)
- [Information-Theoretic State Space Model for Multi-View Reinforcement Learning (Hwang et al., 2023)](https://openreview.net/forum?id=jwy77xkyPt)
- [A citywide TD-learning based intelligent traffic signal control for autonomous vehicles: Performance evaluation using SUMO (Reza et al., 2023)](https://onlinelibrary.wiley.com/doi/full/10.1111/exsy.13301)
- [Handling uncertainty in self-adaptive systems: an ontology-based reinforcement learning model (Ghanadbashi et al., 2023)](https://link.springer.com/article/10.1007/s40860-022-00198-x)
- [Multiagent Reinforcement Learning for Traffic Signal Control: a k-Nearest Neighbors Based Approach (Almeida et al., 2022)](https://ceur-ws.org/Vol-3173/3.pdf)
- [From Local to Global: A Curriculum Learning Approach for Reinforcement Learning-based Traffic Signal Control (Zheng et al., 2022)](https://ieeexplore.ieee.org/abstract/document/9832372)
- [Poster: Reliable On-Ramp Merging via Multimodal Reinforcement Learning (Bagwe et al., 2022)](https://ieeexplore.ieee.org/abstract/document/9996639)
- [Using ontology to guide reinforcement learning agents in unseen situations (Ghanadbashi & Golpayegani, 2022)](https://link.springer.com/article/10.1007/s10489-021-02449-5)
- [Information upwards, recommendation downwards: reinforcement learning with hierarchy for traffic signal control (Antes et al., 2022)](https://www.sciencedirect.com/science/article/pii/S1877050922004185)
- [A Comparative Study of Algorithms for Intelligent Traffic Signal Control (Chaudhuri et al., 2022)](https://link.springer.com/chapter/10.1007/978-981-16-7996-4_19)
- [An Ontology-Based Intelligent Traffic Signal Control Model (Ghanadbashi & Golpayegani, 2021)](https://ieeexplore.ieee.org/abstract/document/9564962)
- [Reinforcement Learning Benchmarks for Traffic Signal Control (Ault & Sharon, 2021)](https://openreview.net/forum?id=LqRSh6V0vR)
- [EcoLight: Reward Shaping in Deep Reinforcement Learning for Ergonomic Traffic Signal Control (Agand et al., 2021)](https://s3.us-east-1.amazonaws.com/climate-change-ai/papers/neurips2021/43/paper.pdf)

<!-- end list of publications -->
