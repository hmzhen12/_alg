# Simulated Annealing for Circuit Placement

---

## Introduction
Circuit placement is a critical step in VLSI (Very Large Scale Integration) design, where electronic components (blocks) must be arranged on a chip to minimize wiring cost, delay, and power consumption.  

**Simulated Annealing (SA)** is a probabilistic optimization technique inspired by the annealing process in metallurgy. It allows exploration of the solution space, accepting worse solutions with a decreasing probability, which helps escape local minima.  

This project demonstrates the application of SA for optimizing circuit block placement on a grid.  

---

## Problem Description
The circuit placement problem can be formally described as:  

- **Input:**  
  - A set of blocks \( B = \{b_1, b_2, ..., b_n\} \)  
  - A grid of positions \( G = m \times m \)  
  - A set of connections (nets) between blocks  

- **Objective:**  
  Minimize the total wirelength:  
  \[
  \text{Wirelength} = \sum_{\text{all connections}} \text{Manhattan distance between connected blocks}
  \]

- **Constraints:**  
  - Each block occupies one unique position on the grid  
  - No two blocks can share the same position  

---

## Simulated Annealing Overview
Simulated annealing mimics the physical process of heating and slowly cooling a material to reach a low-energy crystalline state.  

**Algorithm Steps:**
1. Start with a random placement of blocks.  
2. Set an initial temperature \( T_0 \).  
3. Repeat until stopping criteria (e.g., minimal temperature or max iterations):  
   - Generate a neighbor solution (swap two blocks randomly).  
   - Calculate the change in cost \( \Delta E \).  
   - If \( \Delta E < 0 \), accept the new solution (improvement).  
   - If \( \Delta E > 0 \), accept with probability \( p = e^{-\Delta E / T} \).  
   - Decrease the temperature according to a cooling schedule \( T = \alpha T \).  

This probabilistic acceptance of worse solutions allows the algorithm to escape local minima and approximate the global optimum.  

---

## Mathematical Background

- **Cost Function:**  
  \[
  C(\text{placement}) = \sum_{(i,j) \in \text{connections}} |x_i - x_j| + |y_i - y_j|
  \]  
  where \((x_i, y_i)\) is the position of block \(i\).

- **Acceptance Probability:**  
  For a worse solution with cost increase \(\Delta E\):  
  \[
  P(\text{accept}) = e^{-\Delta E / T}
  \]

- **Cooling Schedule:**  
  A typical geometric cooling schedule:  
  \[
  T_{k+1} = \alpha \cdot T_k, \quad 0 < \alpha < 1
  \]

- **Neighbor Function:**  
  Swap two blocks at random positions to generate a new placement.  

---

## References

1. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). **Optimization by Simulated Annealing**. *Science*, 220(4598), 671–680.  
   [Link to article](https://www.science.org/doi/10.1126/science.220.4598.671)

2. Chen, W. K. (2003). **The VLSI Handbook**. CRC Press.  
   [Publisher link](https://www.crcpress.com/The-VLSI-Handbook/Chen/p/book/9780849315398)

3. Cohoon, J. P., & MacDonald, J. W. (1990). **Simulated Annealing for VLSI Design**. *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, 9(7), 694–705.  
   [IEEE link](https://ieeexplore.ieee.org/document/57265)

4. Python `random` and `math` module documentation:  
   [Python `random`](https://docs.python.org/3/library/random.html)  
   [Python `math`](https://docs.python.org/3/library/math.html)

---

## Implementation Details

A simplified Python implementation:

```python
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

# ----------------------
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
plt.show()```

