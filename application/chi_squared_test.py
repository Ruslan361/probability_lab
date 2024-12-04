import unittest
import numpy as np
from auxiliary import chi_squared_test  # Replace your_module

class TestChiSquared(unittest.TestCase):

    def test_chi_squared_alpha(self):
        # Test data and parameters
        num_intervals = 10
        work_times = np.random.normal(loc=10, scale=2, size=100)  # Example data
        mean = 10
        variance = 4
        alpha = 0.05  # Set alpha to 0.05

        # Perform the chi-squared test
        expected_frequencies, chi2_statistic, p_value, message = chi_squared_test(
            num_intervals, work_times, mean, variance, alpha
        )

        # Assertions based on alpha = 0.05
        if p_value <= alpha:
            self.assertTrue("отклонена" in message.lower())  # Check if the message indicates rejection
        else:
            self.assertTrue("не отклонена" in message.lower())  # Check if the message indicates non-rejection

        # Repeat the test with a different alpha (e.g., 0.2)
        alpha = 0.2
        expected_frequencies, chi2_statistic, p_value, message = chi_squared_test(
            num_intervals, work_times, mean, variance, alpha
        )


        if p_value <= alpha:
            self.assertTrue("отклонена" in message.lower())
        else:
            self.assertTrue("не отклонена" in message.lower())



if __name__ == '__main__':
    unittest.main()