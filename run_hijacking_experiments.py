import os
import json
import time
import numpy as np
import pandas as pd
from carla_env import CarlaEnv
from bayes_opt import UtilityFunction
from bayes_opt import BayesianOptimization
from carla.driving_benchmark import run_driving_benchmark
from carla.driving_benchmark.experiment_suites import AdversarySuite

with open('config/hijacking_params.json') as json_file:
    args = json.load(json_file)

baseline_task = args['baseline_task']
target_task   = args['target_task']
curr_scene    = args['scene']
curr_port     = args['port']
curr_gpu      = args['GPU']
curr_town     = args['town']

random_points        = args['random_points']
search_points         = args['search_points']
acquisition_function = args['acquisition_function']

overwrite_experiment = args['overwrite_experiment']

directory_to_save = './_benchmarks_results/{}'.format(curr_town)
if os.path.exists(directory_to_save):
    if overwrite_experiment:
        print("Removing {}".format(directory_to_save))
        os.system("rm -rf {}".format(directory_to_save))
    else:
        print("WARNING: A directory called {} already exists.".format(directory_to_save))
        print("Please make sure to move the contents to a new location as running this program will overwrite the contents of this directory.")
        exit()

os.system("mkdir -p _benchmarks_results")
print("Loading the Imitition Network and performing one simulation run for the target path..")
env = CarlaEnv(task=target_task, town=curr_town, scene=curr_scene,
               port=curr_port, save_images=False, gpu_num=curr_gpu)
print("Complete.")

targetSteer       = env.get_steer()                  # get the steering angles for the target run
MAX_LEN           = int(len(env.get_steer())*.8)      # set maximum number of frames to 80 percent of target scenario
targetSteer      = targetSteer[:MAX_LEN]                  # subset steering angles to maximum number of allowed frames

env.task  = baseline_task
env.scene = curr_scene
env.experiment_name = 'baseline'

# reset experiment suite with base task + scene
env.experiment_suite = AdversarySuite(env.town, env.task, env.weather, env.iterations, env.scene)

# run the baseline simulation
print("Running the simulation for the baseline path.")
run_driving_benchmark(env.agent, env.experiment_suite, log_name=env.experiment_name,
                    city_name=env.town, port=env.port, save_images=False)
print("Complete.")
baseSteer      = env.get_steer()
MAX_LEN_B      = int(len(baseSteer)*.8)
baseSteer      = baseSteer[:MAX_LEN_B]


def target(pos1, rot1, pos2=0, rot2=0, width=10, length=200, colorR=0, colorG=0, colorB=0):
    # specify our attack (in this case double black lines) as a dictionary to pass to the CarlaEnv object.
    dict_params = {
        # the first line
        0:{
            'pos': int(pos1),
            'rot': rot1,
            'width': int(width),
            'length': int(length),
            'color': (int(colorB), int(colorG), int(colorR), 255)
        },
        # the second line
        1:{
            'pos': int(pos2),
            'rot': rot2,
            'width': int(width),
            'length': int(length),
            'color': (0, 0, 0, 255)
        }
    }

    # run the simulation with that attack and fetch the data from that run
    metrics = env.step(dict_params)

    # calculate the objective function we are trying to maximize
    attackSteer    = metrics['steer'][:MAX_LEN]

    # if attackSteer vector is shorter than baseSteer, extend attackSteer with baseSteer.
    # This takes care of difference in vector lengths without changing the L1 value
    # as extended part of attackSteer will have zero difference with same part of baseSteer
    if len(attackSteer) < len(targetSteer):
        attackSteer = np.append(attackSteer, targetSteer[len(attackSteer):])

    # return objective function value for this particular run
    return -1 * np.sum(np.abs(attackSteer - targetSteer))


# define the bounds for our attack parameters.
# in our case, the position of both lines can start between pixel 0 and pixel 190.
# the rotation of each line can over pi radians.
controls = {'pos1': (0, 190),
            'rot1': (0, 179),
            'pos2': (0, 200),
            'rot2': (0, 179)}
print("Running the Bayesian Optimizer for {} iterations.".format(str(random_points + search_points)))
# instantiate the bayesian optimizer
optimizer = BayesianOptimization(target, controls, random_state=42)
optimizer.maximize(init_points=random_points, n_iter=search_points, acq=acquisition_function)
