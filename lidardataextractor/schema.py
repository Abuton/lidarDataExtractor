import numpy as np

class Schema(object):
    """ 
    A class that gives more information about ept.json files
    ept.json files are entwine files and contains informations about
    lidar point cloud data.
    """
    def __init__(self, data) -> None:
        self.dimesions = self.get_dimensions(data)

    def length(self) -> int:
        """ 
        Gets the length of the raster data
        """
        return len(self.dimesions)

    def get_dimensions(self, data) -> dict:
        """

        Parameters
        ----------
        data : the ept file to be quaried
            

        Returns
        -------
        Dictionary 

        """
        dimensions = {}

        for d in data:
            name = d['name']

            kind = 'i'
            if d['type'] == 'unsigned':
                kind = 'u'
            elif d['type'] == "signed":
                kind = 'i'
            elif d['type'] == 'float':
                kind = 'f'
            else:
                raise TypeError(f"Unrecognised type{d['type']}, cannot convert {d['type']}"
                                "to numpy dtype")

            d['dtype'] = kind + str(d['size'])
            dimensions[name] = d

        return dimensions

    def get_dtype(self) -> np.dtype:
        """
        gets the data type of the keys in an entwine file
        """
        dt = []
        for d in self.dimesions:
            dim = self.dimesions[d]
            dt.append((dim['name'], dim['dtype']))

        return np.dtype(dt)
    dtype = property(get_dtype)
