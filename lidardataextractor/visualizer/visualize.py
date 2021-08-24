import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio
from shapely.geometry import box
import geopandas as gpd
from rasterio.transform import from_bounds, from_origin
from rasterio.warp import reproject, Resampling

class VisualizeRaster:
    """ 
    A module to visualize the raster files
    """

    def __init__(self, data_file_path) -> None:
        # Open the DEM with Rasterio
        with rio.open(data_file_path) as raster:
            elevation = raster.read(1, masked=True)
        self.elevation = elevation

    def plot_bands(self, hillshade:bool=False, azimuth:int=150)->None:
        """

        Parameters
        ----------
        hillshade:bool :
             (Default value = False)
        azimuth:int :
             (Default value = 150)

        Returns
        -------

        """
        if hillshade:
            # Create and plot the hillshade with earthpy
            hillshade = es.hillshade(self.elevation, azimuth=azimuth)

            ep.plot_bands(
                hillshade,
                cbar=False,
                title="Hillshade made from DTM",
                figsize=(10, 6),
            )
            plt.savefig('images/hillshade.png')
            plt.show()
        else:
            # Plot the data
            ep.plot_bands(
                self.elevation,
                cmap="gist_earth",
                cbar=False,
                title="DTM Without Hillshade",
                figsize=(10, 6),
            )
            plt.savefig('images/DTM.png')
            plt.show()
                    

    def plot_overlay(self)->None:
        """ 
        Plot Overlays on the raster image
        """
        # Create and plot the hillshade with earthpy
        hillshade = es.hillshade(self.elevation)

        # Plot the DEM and hillshade at the same time
        _, ax = plt.subplots(figsize=(10, 6))
        ep.plot_bands(
            self.elevation,
            ax=ax,
            cmap="terrain",
            cbar=False,
            title="Lidar Digital Elevation Model (DEM)\n overlayed on top of a hillshade",
        )
        ax.imshow(hillshade, cmap="Greys", alpha=0.5)
        plt.show()
        plt.savefig('images/overlay.png')

    def explore(self, tif_path, product:str=None) -> None:
        """

        Parameters
        ----------
        tif_path : tif file path
            
        product:str :
             (Default value = None)

        Returns
        -------

        """
        raster = rio.open(tif_path)
        bounds = raster.bounds
        west, south, east, north = bounds
        src_crs = raster.crs
        src_shape = src_height, src_width = raster.shape

        # The src_transform is the Affine transformation for the source georeferenced raster.
        # We calculate it using the from_bounds function provided by rasterio
        src_transform = from_bounds(west, south, east, north, src_width, src_height)
        source = raster.read(1)

        dst_crs = {'init': 'EPSG:26915'}
        dst_transform = from_origin(268000.0, 5207000.0, 250, 250)
        dem_array = np.zeros((451, 623))
        dem_array[:] = np.nan

        reproject(source,
            dem_array,
            src_transform=src_transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear)

        topocmap = 'Spectral_r'
    
        vmin = 180
        vmax = 575
        plt.figure(figsize=(10, 6))
        ax = sns.displot(dem_array.ravel())
        ax.set_xlabels('Elevation (m)')
        ax = plt.gca()
        ax.get_figure().savefig('images/1.png')

        extent = xmin, xmax, ymin, ymax = 268000.0, 423500.0, 5094500.0, 5207000.0

        def hillshade(array, azimuth, angle_altitude):
            """

            Parameters
            ----------
            array : raster array files
                
            azimuth :
                
            angle_altitude :
                

            Returns
            -------

            """

            # Source: http://geoexamples.blogspot.com.br/2014/03/shaded-relief-images-using-gdal-python.html

            x, y = np.gradient(array)
            slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
            aspect = np.arctan2(-x, y)
            azimuthrad = azimuth*np.pi / 180.
            altituderad = angle_altitude*np.pi / 180.


            shaded = np.sin(altituderad) * np.sin(slope) \
            + np.cos(altituderad) * np.cos(slope) \
            * np.cos(azimuthrad - aspect)
            return 255*(shaded + 1)/2

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        ax.matshow(hillshade(dem_array, 30, 30),  cmap='Greys', alpha=.5, zorder=10)
        cax = ax.contourf(dem_array, np.arange(vmin, vmax, 10),
                        cmap=topocmap, vmin=vmin, vmax=vmax, origin='image')
        fig.colorbar(cax, ax=ax)
        fig.savefig('images/2.png')


if __name__ == "__main__":

    dtm = "tif/iowa2.tif"
    viz = VisualizeRaster(data_file_path=dtm)

    viz.plot_bands(hillshade=True)
    viz.plot_bands(hillshade=False, azimuth=130)
    viz.plot_overlay()
    viz.explore(tif_path='tif/SoPlatteRiver.tif')