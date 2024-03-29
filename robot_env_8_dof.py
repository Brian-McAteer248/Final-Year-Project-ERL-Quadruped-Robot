from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import gym
import math
import numpy as np


class RobotEnv8DOF(gym.Env):
    def __init__(self):
        client = RemoteAPIClient()  # connects to the local machine by default
        self.sim = client.require('sim')  # access the 'sim' remote object

        # This object has a script function to remove and load the robot model.
        # This is suitable because this floor tile object will persist throughout
        # the simulation as the robot model gets added and removed for episodes.
        floor_primary = self.sim.getObject('/floor_primary')
        self.floor_primary_script = self.sim.getScript(self.sim.scripttype_childscript, floor_primary,
                                                       '/floor_primary')

        # Obtained in reset() function after robot model is loaded into the scene
        self.robot_script = None

        self.joints_names = [
            'back_left_leg_hip_pitch_rev_joint',
            'front_left_leg_hip_pitch_rev_joint',
            'back_right_leg_hip_pitch_rev_joint',
            'front_right_leg_hip_pitch_rev_joint',
            'back_left_leg_knee_pitch_rev_joint',
            'front_left_leg_knee_pitch_rev_joint',
            'back_right_leg_knee_pitch_rev_joint',
            'front_right_leg_knee_pitch_rev_joint'
        ]

        self.leg_bottoms_names = ['back_left_leg_bottom', 'front_left_leg_bottom', 'back_right_leg_bottom',
                                  'front_right_leg_bottom']

        self.max_steps = self.steps_left = 2000

        torso_position_vals = ['torso_position_' + axis for axis in ['x', 'y', 'z']]
        torso_orientation_vals = ['torso_orientation_' + axis for axis in ['x', 'y', 'z']]
        torso_linear_velocity_vals = ['torso_linear_velocity_' + axis for axis in ['x', 'y', 'z']]
        torso_angular_velocity_vals = ['torso_angular_velocity_' + axis for axis in ['x', 'y', 'z']]

        # Joint position values will be radian values
        joint_position_vals = [joint + '_position' for joint in self.joints_names]

        # Joint velocities are angular velocities - radians per second
        joint_velocity_vals = [joint + '_velocity' for joint in self.joints_names]

        feet_contact_forces_vals = [foot + '_contact_force_' + axis for axis in ['x', 'y', 'z']
                                    for foot in self.leg_bottoms_names]

        joint_positions_prev_time_step_vals = [joint + '_positions' for joint in self.joints_names]

        observations = []
        observations.extend(torso_position_vals)
        observations.extend(torso_orientation_vals)
        observations.extend(torso_linear_velocity_vals)
        observations.extend(torso_angular_velocity_vals)
        observations.extend(joint_position_vals)
        observations.extend(joint_velocity_vals)
        observations.extend(feet_contact_forces_vals)
        observations.extend(joint_positions_prev_time_step_vals)

        # Negative infinity lower bound for all obsevations (each are from a continuous observation space)
        lower_obs_bounds = np.array([-np.inf for observation in observations])

        # Positive infinity upper bound for all obsevations (each are from a continuous observation space)
        upper_obs_bounds = np.array([np.inf for observation in observations])

        obs_space_shape = (len(observations),)

        self.observation_space = gym.spaces.Box(low=lower_obs_bounds, high=upper_obs_bounds, shape=obs_space_shape,
                                                dtype=np.float64)

        # Radians
        min_joint_position = -0.7
        max_joint_position = 0.7

        # For each joint, allow positions ranging from min_joint_position radians to max_joint_position radians
        lower_action_bounds = np.array([min_joint_position for i in range(len(self.joints_names))])
        upper_action_bounds = np.array([max_joint_position for i in range(len(self.joints_names))])

        # Num actions is equal to the number of joints
        action_space_shape = (len(self.joints_names),)

        self.action_space = gym.spaces.Box(low=lower_action_bounds, high=upper_action_bounds, shape=action_space_shape,
                                           dtype=np.float64)

        # Rememeber that the simulation must be running in order to call simulation script functions
        self.sim.startSimulation()

    def seed(self, seed):
        print(f'seed(): seed {seed}')

        # Reset method is used to initialise a new episode

    def reset(self, seed=None, options=None):
        print('reset()')
        self.robot_script = self.sim.callScriptFunction('remove_and_load_robot_model', self.floor_primary_script)

        self.steps_left = self.max_steps

        # Vary the initial contains (initial joint positions) to allow the agent to better explore
        random_action_sample = self.action_space.sample().tolist()

        self.sim.callScriptFunction('reset', self.robot_script, random_action_sample)

        return self.observation(), {}

    def close(self):
        print('close()')
        self.sim.stopSimulation()

    def render(self, mode=None):
        print('render()')

    def observation(self):
        observations = self.sim.callScriptFunction('get_observations', self.robot_script)
        return np.array(observations)

    def step(self, action):
        print(f'step(): self.steps_left: {self.steps_left}')

        positions_list = action.tolist()
        self.sim.callScriptFunction('apply_positions', self.robot_script, positions_list)

        reward, robot_fallen = self.sim.callScriptFunction('get_reward_and_if_robot_fallen', self.robot_script,
                                                           self.max_steps, self.steps_left, positions_list)

        self.steps_left -= 1
        # Finish episode if no steps left or if robot has fallen over
        done = self.steps_left <= 0 or robot_fallen

        truncated = robot_fallen

        # Fifth return value (empty dictionary) corresponds to 'info'
        return self.observation(), reward, done, truncated, {}
