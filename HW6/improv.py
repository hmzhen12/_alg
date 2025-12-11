import random

def f(x):
    return x**2 + 4*x + 4   

def improvement_method(start, step_size=0.1, max_iter=1000):
    current_x = start
    current_f = f(current_x)

    for i in range(max_iter):

        left_x = current_x - step_size
        right_x = current_x + step_size

        left_f = f(left_x)
        right_f = f(right_x)

 
        best_x = current_x
        best_f = current_f

        if left_f < best_f:
            best_x = left_x
            best_f = left_f

        if right_f < best_f:
            best_x = right_x
            best_f = right_f

     
        if best_x == current_x:
            print(f"No more improvement at iteration {i}.")
            break
  
        current_x = best_x
        current_f = best_f

        print(f"Iteration {i}: x = {current_x:.4f}, f(x) = {current_f:.6f}")

    return current_x, current_f

best_x, best_f = improvement_method(start=random.uniform(-10, 10))

print("\nFinal result:")
print("Best x:", best_x)
print("Best f(x):", best_f)
