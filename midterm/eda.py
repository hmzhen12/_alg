import numpy as np
import matplotlib.pyplot as plt
import random
import math

class CircuitPlacementEDA:
    def __init__(self, num_blocks, grid_size, connections):
        self.num_blocks = num_blocks
        self.grid_size = grid_size
        self.connections = connections 
        self.placement = {}
        self.initialize_random_placement()

    def initialize_random_placement(self):
        positions = set()
        for i in range(self.num_blocks):
            while True:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if (x, y) not in positions:
                    positions.add((x, y))
                    self.placement[i] = (x, y)
                    break

    def calculate_hpwl(self):
        total_length = 0
        for start, end in self.connections:
            x1, y1 = self.placement[start]
            x2, y2 = self.placement[end]
            total_length += abs(x1 - x2) + abs(y1 - y2)
        return total_length

    def simulated_annealing(self, initial_temp, cooling_rate, max_iter):
        current_cost = self.calculate_hpwl()
        best_cost = current_cost
        best_placement = self.placement.copy()
        temp = initial_temp
        costs_history = []

        print(f"Initial Cost (Wire Length): {current_cost}")

        for i in range(max_iter):
            block_a, block_b = random.sample(range(self.num_blocks), 2)

            pos_a, pos_b = self.placement[block_a], self.placement[block_b]
            self.placement[block_a], self.placement[block_b] = pos_b, pos_a

            new_cost = self.calculate_hpwl()
            delta = new_cost - current_cost

            if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-8)):
                current_cost = new_cost
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_placement = self.placement.copy()
            else:
                self.placement[block_a], self.placement[block_b] = pos_a, pos_b

            temp *= cooling_rate
            costs_history.append(current_cost)

            if i % 500 == 0:
                print(f"Iteration {i}, Current Cost: {current_cost}, Temp: {temp:.4f}")

        self.placement = best_placement
        print(f"Final Optimized Cost: {best_cost}")
        return costs_history

    def visualize(self, title="Circuit Layout"):
        plt.figure(figsize=(8, 8))
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xlim(-1, self.grid_size)
        plt.ylim(-1, self.grid_size)
        plt.title(title)

        for start, end in self.connections:
            x1, y1 = self.placement[start]
            x2, y2 = self.placement[end]
            plt.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, zorder=1)

        for block_id, (x, y) in self.placement.items():
            plt.scatter(x, y, s=300, facecolor='skyblue', edgecolor='black', zorder=2)
            plt.text(x, y, str(block_id), ha='center', va='center', fontweight='bold')

        plt.show()

random.seed(42)
np.random.seed(42)

NUM_BLOCKS = 10
GRID_SIZE = 10 

CONNECTIONS = [(i, i+1) for i in range(NUM_BLOCKS-1)]
CONNECTIONS += [(0, NUM_BLOCKS-1), (2,6), (3,8)]

eda_sim = CircuitPlacementEDA(NUM_BLOCKS, GRID_SIZE, CONNECTIONS)

print("Visualizing Initial Layout...")
eda_sim.visualize("Initial Layout (Random Placement)")

history = eda_sim.simulated_annealing(initial_temp=100.0, cooling_rate=0.99, max_iter=2000)

print("Visualizing Layout After Optimization...")
eda_sim.visualize("Optimized Layout (Wire Length Minimized)")

plt.plot(history, color='blue')
plt.title("Optimization Convergence Process")
plt.xlabel("Iteration")
plt.ylabel("Total Wire Length")
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
