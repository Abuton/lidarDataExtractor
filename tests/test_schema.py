import unittest
import sys, os
import requests
import numpy as np

sys.path.append(os.path.abspath(os.path.join('../')))

from lidardataextractor.schema import Schema


url = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CO_SoPlatteRiver_Lot5_2013_LAS_2015/ept.json"

class TestSchema(unittest.TestCase):
    """
		A class for unit-testing function in the ept_info.py file

		Args:
        -----
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""

    def setUp(self):
        data = requests.get(url).json()['schema']
        self.schema_obj = Schema(data)
        self.dimesions = self.schema_obj.get_dimensions(data)


    def test_length(self):
        actual_length = 14
        self.assertEqual(len(self.dimesions), actual_length)

    def test_input_value_length(self):
        """
        Provide an assertion level for arg input
        """
        self.assertRaises(TypeError, self.schema_obj.length, True)

    def test_get_dtype(self):
        dt = []
        for d in self.dimesions:
            dim = self.dimesions[d]
            dt.append((dim['name'], dim['dtype']))
        actual_type = np.dtype(dt)
        self.assertEqual(self.schema_obj.get_dtype(), actual_type)

    def test_input_value_dtype(self):
        """
        Provide an assertion level for arg input
        """
        self.assertRaises(TypeError, self.schema_obj.get_dtype, True)

if __name__ == '__main__':
	unittest.main()

    
