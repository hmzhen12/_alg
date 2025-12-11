import numpy as np

def greedy_search(features, targets, start_params=None, step=0.1, max_iter=500):
    if start_params is None:
        w = np.zeros(features.shape[1])
    else:
        w = np.array(start_params, dtype=float)

    def mse(w):
        pred = features @ w
        return np.mean((pred - targets)**2)

    current_loss = mse(w)

    for _ in range(max_iter):
        improved = False

        for i in range(len(w)):
            for direction in [+step, -step]:
                new_w = w.copy()
                new_w[i] += direction
                new_loss = mse(new_w)

                if new_loss < current_loss:
                    w = new_w
                    current_loss = new_loss
                    improved = True

        if not improved:
            break

    return w, current_loss

X = np.array([[1, 2], [2, 1], [3, 2]], float)
y = np.array([5, 6, 10], float)

best_w, best_loss = greedy_search(X, y)
print("Greedy Method Result:", best_w, best_loss)
