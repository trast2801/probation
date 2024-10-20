import unittest
import solution
import pandas as pd

data = pd.read_csv('data_test.csv', encoding='windows-1251')
class TestSum(unittest.TestCase):

    def test_calculate_and_display_average_price(self):
        global  data
        #solution.calculate_and_display_average_price(data)
        self.assertEqual(solution.calculate_and_display_average_price(data),228.578181180087, "Should be 228.578181180087")

    def test_notify_if_strong_fluctuations(self):
        global  data
        threshold = 5
        self.assertEqual(solution.notify_if_strong_fluctuations(data, threshold), 5.822951906379625, "Should be 5.82")


if __name__ == '__main__':
    unittest.main()