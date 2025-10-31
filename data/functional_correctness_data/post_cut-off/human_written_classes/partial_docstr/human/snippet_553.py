import os
import json
import numpy as np

class ConvergenceUtils:

    def __init__(self, root_path):
        self.root_path = root_path
        self.data = None
        self.rounds = None
        self.avg_scores, self.stds = (None, None)

    def load_data(self, root_path):
        """
        Read JSON file, create a new file if it doesn't exist, then return the data.
        """
        rounds_dir = self.root_path
        result_file = os.path.join(rounds_dir, 'results.json')
        os.makedirs(rounds_dir, exist_ok=True)
        if not os.path.exists(result_file):
            with open(result_file, 'w') as file:
                json.dump([], file)
        with open(result_file, 'r') as file:
            return json.load(file)

    def process_rounds(self):
        """
        Organize data by round, return a dictionary of scores by round.
        """
        self.data = self.load_data(root_path=self.root_path)
        rounds = {}
        for entry in self.data:
            round_number = entry['round']
            score = entry['score']
            if round_number not in rounds:
                rounds[round_number] = []
            rounds[round_number].append(score)
        return rounds

    def calculate_avg_and_std(self):
        """
        Calculate average score and standard deviation for each round, return two lists: average scores and standard deviations.
        """
        self.rounds = self.process_rounds()
        sorted_rounds = sorted(self.rounds.items(), key=lambda x: x[0])
        avg_scores = []
        stds = []
        for round_number, scores in sorted_rounds:
            avg_scores.append(np.mean(scores))
            stds.append(np.std(scores))
        return (avg_scores, stds)

    def check_convergence(self, top_k=3, z=0, consecutive_rounds=5):
        """
        Check for convergence. z is the z-score corresponding to the confidence level.
        consecutive_rounds is the number of consecutive rounds that must meet the stop condition.
        """
        self.avg_scores, self.stds = self.calculate_avg_and_std()
        if len(self.avg_scores) < top_k + 1:
            return (False, None, None)
        convergence_count = 0
        previous_y = None
        sigma_y_previous = None
        for i in range(len(self.avg_scores)):
            top_k_indices = np.argsort(self.avg_scores[:i + 1])[::-1][:top_k]
            top_k_scores = [self.avg_scores[j] for j in top_k_indices]
            top_k_stds = [self.stds[j] for j in top_k_indices]
            y_current = np.mean(top_k_scores)
            sigma_y_current = np.sqrt(np.sum([s ** 2 for s in top_k_stds]) / top_k ** 2)
            if previous_y is not None:
                delta_y = y_current - previous_y
                sigma_delta_y = np.sqrt(sigma_y_current ** 2 + sigma_y_previous ** 2)
                if abs(delta_y) <= z * sigma_delta_y:
                    convergence_count += 1
                    if convergence_count >= consecutive_rounds:
                        return (True, i - consecutive_rounds + 1, i)
                else:
                    convergence_count = 0
            previous_y = y_current
            sigma_y_previous = sigma_y_current
        return (False, None, None)

    def print_results(self):
        """
        Print average score and standard deviation for all rounds.
        """
        self.avg_scores, self.stds = self.calculate_avg_and_std()
        for i, (avg_score, std) in enumerate(zip(self.avg_scores, self.stds), 1):
            print(f'Round {i}: Average Score = {avg_score:.4f}, Standard Deviation = {std:.4f}')