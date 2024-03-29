import argparse
import matplotlib.pyplot as plt
import pickle
import statistics as stats


def create_training_reward_plot(*sets_of_results_for_each_algorithm):
    plt.title('Mean Agent Reward for Validation Experiments Performed During Training')
    plt.xlabel('Training Timestep')
    plt.ylabel('Mean Reward')

    plot_line_colours = ['#0238fa', '#09b800', '#f20c0c', '#e39d10']
    plot_fill_between_face_colours = ['#03c2fc', '#16ff0a', '#ff7370', '#fab11e']
    plot_labels = ['DDPG', 'TD3', 'CEM-DDPG', 'CEM-TD3']

    for index, results_for_one_algorithm in enumerate(sets_of_results_for_each_algorithm):
        reward_mean_for_each_validation_experiment = []
        reward_stdev_for_each_validation_experiment = []

        plot_x_vals_num_training_steps = []
        num_training_steps = 0

        for val_experiment_num, rewards_for_given_validation_experiment in enumerate(results_for_one_algorithm):

            reward_mean = stats.mean(rewards_for_given_validation_experiment)
            reward_mean_for_each_validation_experiment.append(reward_mean)

            reward_std_dev = stats.stdev(rewards_for_given_validation_experiment)
            reward_stdev_for_each_validation_experiment.append(reward_std_dev)

            reward_median = stats.median(rewards_for_given_validation_experiment)
            reward_best = max(rewards_for_given_validation_experiment)

            print(f'{plot_labels[index]}: Validation Experiment {val_experiment_num + 1}: '
                  f'Reward mean: {reward_mean}, '
                  f'Reward std_dev: {reward_std_dev}, '
                  f'Reward median: {reward_median}',
                  f'Reward best (max): {reward_best}')

            plot_x_vals_num_training_steps.append(num_training_steps)

            # DDPG and TD3 were evaluated every 5000 steps, while
            # CEM-RL (DDPG) and CEM-RL (TD3) period was specified as 5000 but varied
            # (typically occurred less frequently) due to variance in episode survival
            # length for each agent in the population causing step counters to be reset
            # e.g. if step counter = 9000 steps since last evaluation, 9000 > 5000 so evaluate,
            # then set step counter = 0. 4000 steps count 'lost', leading to less frequent
            # evaluations. Nonetheless, each algorithm underwent regular evaluations across
            # the 400000 training timesteps.
            if index < 2:
                num_training_steps += 5000
            elif index == 2:
                num_training_steps += 9300
            else:
                num_training_steps += 8350

        mean_rewards_minus_stdev = []
        mean_rewards_plus_stdev = []

        for j in range(len(reward_mean_for_each_validation_experiment)):
            mean_rewards_minus_stdev.append(reward_mean_for_each_validation_experiment[j]
                                            - reward_stdev_for_each_validation_experiment[j])
            mean_rewards_plus_stdev.append(reward_mean_for_each_validation_experiment[j]
                                           + reward_stdev_for_each_validation_experiment[j])

        plt.plot(plot_x_vals_num_training_steps, reward_mean_for_each_validation_experiment,
                 label=plot_labels[index], color=plot_line_colours[index])
        plt.fill_between(plot_x_vals_num_training_steps, mean_rewards_minus_stdev, mean_rewards_plus_stdev, alpha=0.2,
                         facecolor=plot_fill_between_face_colours[index])

    plt.legend()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--ddpg_training_results_pkl_path', default='', type=str)
    parser.add_argument('--td3_training_results_pkl_path', default='', type=str)
    parser.add_argument('--cem_rl_ddpg_training_results_pkl_path', default='', type=str)
    parser.add_argument('--cem_rl_td3_training_results_pkl_path', default='', type=str)

    args = parser.parse_args()

    ddpg_training_results = None
    td3_training_results = None
    cem_rl_ddpg_training_results = None
    cem_rl_td3_training_results = None

    try:
        with open(args.ddpg_training_results_pkl_path, 'rb') as results_file:
            ddpg_training_results = pickle.load(results_file)
    except FileNotFoundError:
        print(f'DDPG training results file not found at: {args.ddpg_training_results_pkl_path}')

    try:
        with open(args.td3_training_results_pkl_path, 'rb') as results_file:
            td3_training_results = pickle.load(results_file)
    except FileNotFoundError:
        print(f'TD3 training results file not found at: {args.td3_training_results_pkl_path}')

    try:
        with open(args.cem_rl_ddpg_training_results_pkl_path, 'rb') as results_file:
            cem_rl_ddpg_training_results = pickle.load(results_file)
    except FileNotFoundError:
        print(f'CEM-RL DDPG training results file not found at: {args.cem_rl_ddpg_training_results_pkl_path}')

    try:
        with open(args.cem_rl_td3_training_results_pkl_path, 'rb') as results_file:
            cem_rl_td3_training_results = pickle.load(results_file)
    except FileNotFoundError:
        print(f'CEM-RL TD3 training results file not found at: {args.cem_rl_td3_training_results_pkl_path}')

    create_training_reward_plot(ddpg_training_results, td3_training_results,
                                cem_rl_ddpg_training_results, cem_rl_td3_training_results)
