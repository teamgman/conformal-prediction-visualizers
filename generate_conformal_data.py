import numpy as np
import json
import sys
from scipy.linalg import solve

# --- CONFIGURATION ---
n_points = 100
np.random.seed(42)

# Generate non-linear data
x_train = np.sort(np.random.uniform(0, 6, n_points))
# y = sin(x) + noise (smoother, less sharp)
y_train = np.sin(x_train) + np.random.normal(0, 0.4, n_points)

# Evaluation grid for the left plot
n_grid = 200
x_grid = np.linspace(0, 6, n_grid)

# Trial point configuration
x_test = 4.75
# Ensure x_test is roughly inserted into the sequence
idx_insert = np.searchsorted(x_train, x_test)

n_trials = 200
y_trial_values = np.linspace(-2.0, 1.5, n_trials)

# Kernel Ridge Regression params
bandwidth = 0.8
gamma = 1.0 / (2.0 * bandwidth**2)
lambda_reg = 0.1

def rbf_kernel(X1, X2, gamma):
    # X1: (N, 1), X2: (M, 1) -> K: (N, M)
    dist_sq = (X1[:, None] - X2[None, :]) ** 2
    return np.exp(-gamma * dist_sq)

# Pre-compute training kernel parts (before adding pseudo-point to avoid full O(N^3) each time if possible,
# but N=101 is small enough that we can just solve it from scratch for 200 trials in < 1 second).

out_fitted_curves = []
out_p_values = []
out_test_residuals = []

for i in range(n_trials):
    y_test = y_trial_values[i]
    
    # Augmented dataset
    x_aug = np.insert(x_train, idx_insert, x_test)
    y_aug = np.insert(y_train, idx_insert, y_test)
    
    # Kernel matrix
    K = rbf_kernel(x_aug, x_aug, gamma)
    
    # Solve (K + lambda I) alpha = y
    alpha = solve(K + lambda_reg * np.eye(n_points + 1), y_aug, assume_a='pos')
    
    # Evaluate on evaluation grid (for curve drawing)
    K_eval = rbf_kernel(x_grid, x_aug, gamma)
    y_grid_pred = K_eval @ alpha
    out_fitted_curves.append(y_grid_pred.tolist())
    
    # Evaluate residuals on augmented dataset
    y_aug_pred = K @ alpha
    residuals = np.abs(y_aug - y_aug_pred)
    
    test_residual = residuals[idx_insert]
    out_test_residuals.append(test_residual)
    
    # Compute conformal p-value: proportion of residuals >= test_residual
    # adding 1e-10 for floating point stability on ties
    p_value = np.sum(residuals >= test_residual - 1e-10) / (n_points + 1)
    out_p_values.append(p_value)

data = {
    "x_train": x_train.tolist(),
    "y_train": y_train.tolist(),
    "x_grid": x_grid.tolist(),
    "x_test": x_test,
    "y_trial_values": y_trial_values.tolist(),
    "fitted_curves": out_fitted_curves,
    "p_values": out_p_values,
    "residuals_test": out_test_residuals,
    "metadata": {
        "n_points": n_points,
        "bandwidth": bandwidth,
        "lambda_reg": lambda_reg
    }
}

with open("conformal_data.json", "w") as f:
    json.dump(data, f)
print("conformal_data.json written successfully.")
