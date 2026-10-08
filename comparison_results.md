# Experimental comparison results

These results were generated locally from the project models using SUMO in headless mode.

## Scope

- Single-agent PPO and DQN were trained for 6,000 environment timesteps, as configured in their training scripts.
- The local multi-agent PPO checkpoint was trained for 5 PPO iterations. Each iteration collected 512 environment steps and 8,192 agent steps, for approximately 2,560 environment steps and 40,960 agent steps total. The script default is 10 iterations, but this reported checkpoint used 5.
- Single-intersection controllers were evaluated for 500 simulated seconds. Because the environment uses a 5-second action interval, this produced 100 control decisions.
- Multi-agent PPO was evaluated for 499 one-second grid control steps using the 4x4 SUMO grid and 16 signal agents.
- The traffic networks and traffic demand differ between the single-intersection and grid experiments, so these values are diagnostic results, not a directly controlled scientific comparison across network sizes.
- The multi-agent PPO result uses the locally trained Ray checkpoint and is not a GitHub-hosted checkpoint.

| Controller | Simulated scenario | Control steps | Total reward | Mean waiting time (s) | Mean speed (m/s) | Mean stopped vehicles | Final waiting time (s) | Final arrived | Final departed | Final backlog | Final teleported |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fixed-time | 2-way single intersection / 500 s | 100 | -66.18 | 15.883 | 3.762 | 31.47 | 790 | 271 | 330 | 20 | 0 |
| DQN | 2-way single intersection / 500 s | 100 | -72.19 | 25.537 | 4.634 | 22.23 | 7,163 | 282 | 342 | 8 | 0 |
| Single-agent PPO | 2-way single intersection / 500 s | 100 | -46.28 | 33.139 | 4.167 | 28.19 | 4,201 | 295 | 350 | 0 | 0 |
| Multi-agent PPO | 4x4 grid / 499 s | 499 | -3.57 | 0.504 | 8.304 | 33.57 | 168 | 1,078 | 1,336 | 0 | 0 |

## Metrics used

- **Total reward:** Sum of rewards returned by the environment. The default reward is based on the change in accumulated waiting time.
- **Mean waiting time:** Average waiting time of vehicles present in the simulation at each recorded step, averaged over the run.
- **Mean speed:** Average vehicle speed in metres per second, averaged over recorded steps.
- **Mean stopped vehicles:** Average number of vehicles travelling below SUMO's halting threshold.
- **Final waiting time:** Total waiting time at the final recorded step.
- **Final arrived/departed vehicles:** Cumulative vehicles that arrived at or departed into the network.
- **Final backlog:** Vehicles still pending departure at the final recorded step.
- **Final teleported vehicles:** Vehicles SUMO teleported because of excessive blockage; lower is better.

## Interpretation

The multi-agent PPO run completed successfully and controlled all 16 grid signals. Its numbers should not be ranked directly against the single-intersection controllers because the network, traffic demand, number of agents, and control interval differ. A fair comparison should run all controllers on the same network, route file, duration, random seed, and repeated episodes.
