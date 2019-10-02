import os
import json
import time
import numpy as np
import pandas as pd
from carla_env import CarlaEnv
from bayes_opt import UtilityFunction
from bayes_opt import BayesianOptimization

with open('config/infraction_params.json') as json_file:
    args = json.load(json_file)

# CARLA parameters
curr_task  = args['task']
curr_scene = args['scene']
curr_port  = args['port']
curr_gpu   = args['GPU']
curr_town  = args['town']

# bayesian parameters
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
        print("ERROR: A directory called {} already exists.".format(directory_to_save))
        print("Please make sure to move the contents as running this program will overwrite the contents of this directory.")
        exit()


now = time.time()
print("Loading the Imitition Network and performing one simulation run for the baseline path..")
os.system("mkdir -p _benchmarks_results")
env = CarlaEnv(task=curr_task, town='Town01_nemesisA', scene=curr_scene,
               port=curr_port, save_images=False, gpu_num=curr_gpu)
print("Complete.")

baseSteer     = env.baseline_steer                   # get the steering angles for the baseline run
MAX_LEN       = int(len(env.baseline_steer)*.8)      # set maximum number of frames to 80 percent of baseline scenario

baseSteer     = baseSteer[:MAX_LEN]                  # subset steering angles to maximum number of allowed frames


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
    if len(attackSteer) < len(baseSteer):
        attackSteer = np.append(attackSteer, baseSteer[len(attackSteer):])

    # return objective function value for this particular run
    return np.sum(np.abs(attackSteer - baseSteer))

controls = {'pos1': (0, 190),
            'rot1': (0, 179),
            'pos2': (0, 200),
            'rot2': (0, 179)}

print("Running the Bayesian Optimizer for {} iterations.".format(str(random_points + search_points)))
# instantiate the bayesian optimizer
optimizer = BayesianOptimization(target, controls, random_state=42)
optimizer.maximize(init_points=random_points, n_iter=search_points, acq=acquisition_function)
