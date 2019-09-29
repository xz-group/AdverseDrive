import time
import pandas as pd
import numpy as np

from carla.driving_benchmark import run_driving_benchmark
from carla.driving_benchmark.experiment_suites import AdversarySuite
from imitation.imitation_learning import ImitationLearning
from adversary_generator import AdversaryGenerator

WEATHER_DICT = {
        'Default':         0,
        'ClearNoon':       1,
        'CloudyNoon':      2,
        'WetNoon':         3,
        'WetCloudyNoon':   4,
        'MidRainyNoon':    5,
        'HardRainNoon':    6,
        'SoftRainNoon':    7,
        'ClearSunset' :    8,
        'CloudySunset' :   9,
        'WetSunset':       10,
        'WetCloudySunset': 11,
        'MidRainSunset' :  12,
        'HardRainSunset':  13,
        'SoftRainSunset':  14
}

TASKS = {
    'go-straight',
    'turn-right',
    'turn-left'
}

CARLA_PATH = '~/projects/carla-packaged/carla-cluster/CarlaUE4.sh'
POSITION_RANGE = (0, 200)
ROTATION_RANGE = (0, 180)
WIDTH_RANGE = (0, 50)
LENGTH_RANGE = (0, 200)
COLOR_TUPLE_RANGE = (0, 255)

class CarlaEnv:
    def __init__(self, town='Town01_nemesisA',
                task='turn-right', scene=1, weather='ClearNoon',
                port=2000, save_images=False, gpu_num=0,
                experiment_name='baseline'):
        """
        Adversary environment for Carla Simulator
        """
        print("Starting CARLA gym environment")
        print("Ensure that CARLA is running on port", port)
        self.town = town
        self.task = task
        self.scene = scene
        self.weather = WEATHER_DICT[weather]
        self.port = port
        self.save_images = save_images
        self.gpu_num = gpu_num
        self.experiment_name = experiment_name
        self.counter = 0 # counter if more than 1 experiments are run

        self.agent = None
        self.avoid_stopping = False
        self.iterations = 1

        # uses town name and avoid stopping arguements to load agent into
        # self.agent
        self._load_agent()

        # defines what kinds of experiments are going to be run
        self.experiment_suite = AdversarySuite(self.town, self.task,
                            self.weather, self.iterations, self.scene)

        # load the adversary generator
        self.adversary = AdversaryGenerator(self.town)

        self.log_dir = '_benchmarks_results/' + self.town + '/'
        self.update_csv_file()

        print("Running the baseline scenario.")
        # runs the experiment for the baseline case (no attack)
        run_driving_benchmark(self.agent, self.experiment_suite,
                            log_name=self.experiment_name, city_name=self.town,
                            port=self.port, save_images=save_images)

        # some metrics that are collected
        self.baseline_steer_grad = self.get_steer_gradient()
        self.baseline_steer = self.get_steer()
        self.positions = self.get_xy()

        # add new metrics here as needed

    def _load_agent(self):
        """
        Loads the imitation learning model
        """
        if not self.agent:
            print("Loading Imitation Learning model")
            self.agent = ImitationLearning(self.town, self.avoid_stopping,
                                gpu_num=self.gpu_num)

    def step(self, adversary_parameters):
        """
        runs the CARLA simulator and extracts measurement results into a dictionary
        called metrics.
        Format example of adversary_parameters (with two black lines):
        adversary_parameters = {
        # the first black line
            0:{
                'pos': int(pos1),
                'rot': rot1,
                'width': int(width),
                'length': int(length),
                'color': (int(colorB), int(colorG), int(colorR), 255)
            },
            # the second black line
            1:{
                'pos': int(pos2),
                'rot': rot2,
                'width': int(width),
                'length': int(length),
                'color': (0, 0, 0, 255)
            }
        }
        """
        self.counter += 1
        self.experiment_name = 'adversary_{}'.format(self.counter)
        self.update_csv_file()

        # generate a multi-line attack using the adversary_parameters dictionary
        self.adversary.multi_lines(adversary_parameters)

        # runs a particular scenario
        run_driving_benchmark(self.agent, self.experiment_suite, log_name=self.experiment_name,
                            city_name=self.town, port=self.port, save_images=self.save_images)

        # below is a dictionary of metrics that would be returned for each step
        # modify it as required
        metrics = {
                    'steer_sum': self.get_steer_sum(),
                    'steer'    : self.get_steer(),
                    'infraction': self.get_infractions(),
                    'steer_grad': self.get_steer_gradient(),
                    'positions' : self.get_xy(),
                    'intersection_offroad': self.get_intersection_offroad(),
                    'intersection_otherlane': self.get_intersection_otherlane(),
                    'collision_other': self.get_collision_other()
                    }
        return metrics

    def update_csv_file(self):
        """
        updates csv file name with new parameters including experiment name
        and experiment suite.
        """
        self.csv_file = self.log_dir + self.experiment_name + '_' + \
                        str(type(self.experiment_suite).__name__) + \
                        '_' + self.town + '/' + 'measurements.csv'

    def get_steer_sum(self):
        """
        returns the sum of steering angles over all frames for the last run.
        """
        df = pd.read_csv(self.csv_file)
        steersum = df['steer'].sum()
        return steersum

    def get_intersection_offroad(self):
        """
        returns a numpy array containing the percentage of the vehicle that was
        offroad for each frame.
        """
        df = pd.read_csv(self.csv_file)
        return df['intersection_offroad']

    def get_intersection_otherlane(self):
        """
        returns a numpy array containing the percentage of the vehicle that was
        in the otherlane for each frame.
        """
        df = pd.read_csv(self.csv_file)
        return df['intersection_otherlane']

    def get_collision_other(self):
        """
        returns a numpy array containing the intensity of collisions the vehicle
        is experiencing at each frame. Note that the collision intensities returned
        by CARLA are accumulated over the frames so this number may be quite
        large toward the end of the array.
        """
        df = pd.read_csv(self.csv_file)
        return df['collision_other']

    def get_steer_gradient(self):
        """
        return a numpy array of the gradient of the steering angles over all frames
        """
        df = pd.read_csv(self.csv_file)
        steergrad = np.gradient(df['steer'])
        return steergrad

    def get_steer(self):
        """
        return a numpy array of the steering angles over all frames
        """
        df = pd.read_csv(self.csv_file)
        steer = df['steer']
        return steer

    def get_xy(self):
        """
        return numpy array of x and y GPS coordinates of the agent over
        an episode
        """
        df = pd.read_csv(self.csv_file)
        x, y = df['pos_x'], df['pos_y']
        return x, y

    def get_infractions(self):
        """
        Get infraction information including a weighted sum of otherlane and
        offroad violations and collisions.
        """
        df = pd.read_csv(self.csv_file)
        c1, c2, c3 = 1, 1, 0.1 # some weighting factors because collision is in terms of intensity
        infraction = df['intersection_otherlane'].mean() * c1 + \
                    df['intersection_offroad'].sum() * c2 + \
                    df['collision_other'].max() * c3
        return infraction

    def reset(self, experiment_name='baseline'):
        """
        resets the environment to its default values and runs the baseline
        scenario
        """
        self.iterations = 1
        self.experiment_name = experiment_name
        self.counter = 0 # counter if more than 1 experiments are run

        # defines what kinds of experiments are going to be run
        self.experiment_suite = AdversarySuite(self.town, self.task,
                            self.weather, self.iterations, self.scene)

        # load the adversary generator
        self.adversary = AdversaryGenerator(self.town)

        self.log_dir = '_benchmarks_results/' + self.town + '/'
        self.update_csv_file()
        # runs the experiment for the baseline case (no attack)
        run_driving_benchmark(self.agent, self.experiment_suite,
                            log_name=self.experiment_name, city_name=self.town,
                            port=self.port, save_images=self.save_images)

        # some metrics that are collected
        self.baseline_steer_grad = self.get_steer_gradient()
        self.baseline_steer = self.get_steer()
        self.positions = self.get_xy()

if __name__ == "__main__":
    env = CarlaEnv()
    dict_params = {
        'pos': 100,
        'rot': 60,
        'width': 10,
        'color': (0, 0, 0, 255)
    }
    env.step(dict_params)
