import unittest
import numpy as np
from auxiliary import chi_squared_test

class TestChiSquaredAlpha(unittest.TestCase):

    def test_type_1_error_rate(self):
        # Test parameters
        num_intervals = 10
        mean = 10
        variance = 4
        alpha = 0.05  # Significance level (Type I error rate)
        num_trials = 1000 # Number of trials (increase for higher accuracy)


        type_1_errors = 0
        for _ in range(num_trials):
            # Generate data from the null distribution (normal in this case)
            work_times = np.random.normal(loc=mean, scale=np.sqrt(variance), size=100)

            _, _, p_value, _ = chi_squared_test(num_intervals, work_times, mean, variance, alpha)

            if p_value <= alpha:
                type_1_errors += 1

        # Calculate the empirical Type I error rate
        empirical_error_rate = type_1_errors / num_trials


        # Use assertAlmostEqual for comparing floating-point numbers with a tolerance
        self.assertAlmostEqual(empirical_error_rate, alpha, delta=0.02)  # Allow a small delta for randomness


if __name__ == '__main__':
    unittest.main()