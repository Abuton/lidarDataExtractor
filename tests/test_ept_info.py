import unittest
import sys, os
import requests

sys.path.append(os.path.abspath(os.path.join('../')))

from lidardataextractor.ept_info import Info

url = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CO_SoPlatteRiver_Lot5_2013_LAS_2015/ept.json"

class TestInfo(unittest.TestCase):
    """
		A class for unit-testing function in the ept_info.py file

		Args:
        -----
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""

    def setUp(self):
        data = requests.get(url).text
        self.ept = Info(data)

    def test_length(self):
        actual_points = 33711288742
        self.assertEqual(self.ept.length(), actual_points)

    def test_get_span(self):
        actual_span = 256
        self.assertEqual(self.ept.get_span(), actual_span)




if __name__ == '__main__':
	unittest.main()

    