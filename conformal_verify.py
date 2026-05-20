import argparse
import math
import random

def run_simulation(n, alpha, trials):
    # Calculate target index: k = ceil((1 - alpha) * (n + 1))
    k = math.ceil((1 - alpha) * (n + 1))

    covered_count = 0

    if k > n:
        covered_count = trials
    else:
        gauss = random.gauss
        for _ in range(trials):
            samples = [gauss(0.0, 1.0) for _ in range(n + 1)]
            D_n = samples[:n]
            y_next = samples[n]
            
            # Sort the calibration data
            D_n.sort()
            q_hat = D_n[k - 1]
            
            if y_next <= q_hat:
                covered_count += 1

    empirical_coverage = covered_count / trials
    analytical_expected = k / (n + 1)
    
    return {
        'n': n,
        'alpha': alpha,
        'k': k,
        'analytical': analytical_expected,
        'empirical': empirical_coverage
    }

def print_single_summary(res, trials):
    print("==========================================")
    print("Conformal Prediction Verification Summary")
    print("==========================================")
    print("Input Parameters:")
    print(f"  n      : {res['n']}")
    print(f"  alpha  : {res['alpha']:.4f}")
    print(f"  trials : {trials}")
    print("Evaluation Metrics:")
    print(f"  Target Index (k)           : {res['k']}")
    print(f"  Analytical Expected (k/n+1): {res['analytical']:.6f}")
    print(f"  Empirical Simulated        : {res['empirical']:.6f} ({res['empirical'] * 100:.3f}%)")
    print("==========================================")

def main():
    parser = argparse.ArgumentParser(description="Conformal Prediction Finite-Sample Exchangeable Coverage Verification")
    parser.add_argument('--n', type=int, default=96, help='Number of calibration samples')
    parser.add_argument('--alpha', type=float, default=0.10, help='Nominal significance level')
    parser.add_argument('--trials', type=int, default=50000, help='Number of Monte Carlo trials')
    parser.add_argument('--all', '-a', action='store_true', help='Run all three standard test configurations sequentially and compare')
    args = parser.parse_args()

    if args.all:
        configs = [
            ("Balanced Splitting", 99, 0.10),
            ("Ceiling Over-coverage", 96, 0.10),
            ("Boundary Infinity", 3, 0.05)
        ]
        results = []
        print("Running all three standard test configurations sequentially...")
        for name, n, alpha in configs:
            print(f"Executing: {name} (n={n}, alpha={alpha:.2f})...")
            res = run_simulation(n, alpha, args.trials)
            results.append((name, res))
            print_single_summary(res, args.trials)
            print()
        
        # Print comparison matrix
        print("==========================================================================================")
        print("                           TEST CONFIGURATION COMPARISON MATRIX                           ")
        print("==========================================================================================")
        print(f"{'Scenario Name':<23} | {'n':<4} | {'alpha':<5} | {'k':<3} | {'Expected (k/n+1)':<17} | {'Empirical (%)':<15}")
        print("------------------------+------+-------+-----+-------------------+------------------------")
        for name, res in results:
            expect_str = f"{res['analytical']:.6f}"
            emp_str = f"{res['empirical']:.6f} ({res['empirical']*100:.3f}%)"
            print(f"{name:<23} | {res['n']:<4} | {res['alpha']:<5.2f} | {res['k']:<3} | {expect_str:<17} | {emp_str:<15}")
        print("==========================================================================================")
    else:
        res = run_simulation(args.n, args.alpha, args.trials)
        print_single_summary(res, args.trials)

if __name__ == '__main__':
    main()
