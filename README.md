# Final Year Project Repository
## Investigate using Evolutionary Reinforcement Learning (ERL) to Train Control Policies that are Robust to Environmental Changes
## Brian McAteer - Student ID 20328186

### Notes:

* The quadruped robot models in the folder `CoppeliaSim Robot Model(s)` are identical apart from:
  * Their default world coordinates when loaded into a CoppeliaSim scene.
  * The expression used in the `reset()` function their respective scripts (also viewable in the folder `CoppeliaSim Scripts as Python Modules`) to determine if the robot has fallen over (as outlined in Pages `43` and `44` of the report).
* The Python module `plot_creator.py` was used to generate the training learning curve graph as well as to calculate and output the test results summary statistics (mean, standard deviation, median, best) to the console, which were transcribed into the report.
