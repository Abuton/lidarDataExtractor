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

    def test_get_version(self):
        actual_version = "1.1.0"
        self.assertEqual(self.ept.get_version(), actual_version)

    def test_get_bounds(self):
        actual_bounds = [
                        -11752672,
                        4740364,
                        -68269,
                        -11610700,
                        4882336,
                        73703
                    ]
        self.assertEqual(self.ept.get_bounds(), actual_bounds)
    
    def test_get_conforming(self):
        actual_bounds_conforming = [
                                -11752670,
                                4750545,
                                1136,
                                -11610701,
                                4872154,
                                4297
                            ]
        self.assertEqual(self.ept.get_conforming(), actual_bounds_conforming)

    def test_get_datatype(self):
        actual_datatype = "laszip"
        self.assertEqual(self.ept.get_datatype(), actual_datatype)

    def test_get_hierachytype(self):
        actual_hierarchy= "json"
        self.assertEqual(self.ept.get_hierarchytype(), actual_hierarchy)


if __name__ == '__main__':
	unittest.main()

    