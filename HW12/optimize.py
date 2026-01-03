import math
import random
import copy

def cross_entropy(p, q):
    """
    Calculates the cross entropy between distribution p and q.
    Formula: H(p, q) = - sum(p[i] * log2(q[i]))
    equivalent to sum(p[i] * log2(1/q[i]))
    """
    r = 0
    epsilon = 1e-10 # Small value to prevent division by zero
    for i in range(len(p)):
        # Safety check to avoid log(0)
        q_val = q[i] if q[i] > epsilon else epsilon
        r += p[i] * math.log2(1/q_val)
    return r

def normalize(q):
    """
    Ensures that the sum of the list q equals 1 (Probability Distribution).
    Also ensures no values are negative.
    """
    # 1. Make sure all values are non-negative
    q = [abs(x) for x in q]
    
    # 2. Calculate sum
    total = sum(q)
    
    # 3. Divide each element by the sum
    if total == 0:
        return [1.0/len(q)] * len(q) # Return uniform if sum is 0
        
    return [x/total for x in q]

def hill_climbing_optimization(p, iterations=10000, step_size=0.01):
    """
    Uses Hill Climbing to find a q that minimizes cross_entropy(p, q).
    """
    # Initialize q as a uniform distribution
    n = len(p)
    q = [1/n] * n
    
    current_loss = cross_entropy(p, q)
    
    print(f"Initial q: {q}")
    print(f"Initial Loss: {current_loss:.5f}")
    print("-" * 30)

    for i in range(iterations):
        # Create a candidate q by adding small random noise to current q
        q_candidate = copy.deepcopy(q)
        
        # Mutate: Adjust one or all weights slightly
        for j in range(n):
            change = random.uniform(-step_size, step_size)
            q_candidate[j] += change
        
        # CRITICAL STEP: Normalize to ensure sum(q) == 1
        q_candidate = normalize(q_candidate)
        
        # Calculate new loss
        candidate_loss = cross_entropy(p, q_candidate)
        
        # If the new q is better (lower entropy), keep it
        if candidate_loss < current_loss:
            current_loss = candidate_loss
            q = q_candidate

    return q, current_loss

# --- Main Execution ---

if __name__ == "__main__":
    # Example from the image
    target_p = [0.5, 0.25, 0.25]
    
    print(f"Target Distribution (p): {target_p}")
    
    # Run Optimization
    optimized_q, final_loss = hill_climbing_optimization(target_p)
    
    # Theoretical Minimum (Entropy of p)
    theoretical_min = cross_entropy(target_p, target_p)

    print("-" * 30)
    print(f"Optimization Results:")
    print(f"Optimized q: {[round(x, 4) for x in optimized_q]}")
    print(f"Final Cross Entropy: {final_loss:.5f}")
    print(f"Theoretical Minimum (H(p)): {theoretical_min:.5f}")
    
    # Verification
    print("-" * 30)
    print("Verification:")
    is_close = all(math.isclose(optimized_q[i], target_p[i], abs_tol=0.01) for i in range(len(target_p)))
    
    if is_close:
        print("SUCCESS: Optimized q converged to p!")
    else:
        print("FAILURE: Optimized q did not converge closely enough.")
