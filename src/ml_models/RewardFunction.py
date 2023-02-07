class RewardFunction:

    def __init__(self):
        # Constants
        self.deal_cleaning_time = 60
        self.window_size = 7

        # variables
        self.reward_functions = []
        self.weights = []

    def add_reward_function(self, reward_function, weight):
        self.reward_functions.append(reward_function)
        self.weights.append(weight)

    def __call__(self, state, action, next_state):
        reward = 0
        for i, reward_function in enumerate(self.reward_functions):
            reward += reward_function(state, action, next_state) * self.weights[i]
        return reward

    def reward_total_cleaning_time(self, state, action, next_state):
        total_cleaning_time = 0
        ideal_cleaning_time = 240

        for i in range(len(state) - self.window_size, len(state)):
            total_cleaning_time += state[i]["cleaning_time"]

        reward = (1 - abs(ideal_cleaning_time - total_cleaning_time)/ideal_cleaning_time)
        return reward

    def reward_cleaning_sessions(self, state, action, next_state):
        cleaning_sessions = []
        reward = 0
        ideal_cleaning_time = 60

        for session in cleaning_sessions:
            reward += (1 - abs(ideal_cleaning_time - session)/ideal_cleaning_time)

        return reward

    def penalty_devices_connected(self, state, action, next_state):
        if next_state["devices_connected"] > 0:
            return next_state["devices_connected"]
        return 0


reward_function = RewardFunction()
reward_function.add_reward_function(reward_function.reward_total_cleaning_time, 0.25)
reward_function.add_reward_function(reward_function.reward_cleaning_sessions, 0.2)
reward_function.add_reward_function(reward_function.penalty_devices_connected, 0.6)
