import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio
import geopandas as gpd

class VisualizeRaster:
    """ 
    A module to visualize the raster files
    """

    def __init__(self, data_file_path:str, shp_filepath:str) -> None:
        # Open the DEM with Rasterio
        with rio.open(data_file_path) as raster:
            elevation = raster.read(1, masked=True)
        self.elevation = elevation
        self.gdf = gpd.read_file(shp_filepath)
        self.gdf = self.gdf.set_crs(3857, allow_override=True)

    def plot_geodataframe(self, color:str = 'whitesmoke', edgecolor:str = 'red') -> None:
        """
        Plots a Geodataframe with columns such as geometry and elevation

        Parameters:
        -----
        color : color of the plotted image
            (Default value = whitesmoke)
        edgecolor : edgecolor of the plotted image
            (Default value = red)

        Returns:
        --------
        None
        """
        self.gdf.plot(figsize=(15,15), color=color, linestyle=':', edgecolor=edgecolor, aspect=1)
        plt.show()

    def plot_3D_visualzation(self, s: float = 0.01, color: str = "red"):
        """
        Plots a 3D terrain scatter plot of a geopandas dataframe

        Parameters:

            s (float, optional): S value. 
                (Default value = 0.01)
            color (str, optional): color of the points.
                (Default value = red)

        Returns:
        --------
        None
        """

        x = self.gdf.geometry.x
        y = self.gdf.geometry.y
        z = self.gdf.elevation

        points = np.vstack((x, y, z)).transpose()

        _, ax = plt.subplots(1, 1, figsize=(15, 15))
        ax = plt.axes(projection='3d')
        ax.scatter(points[:, 0], points[:, 1],
                points[:, 2],  s=s, color=color)
        plt.show()
    

    def plot_bands(self, hillshade:bool=False, azimuth:int=150)->None:
        """

        Parameters
        ----------
        hillshade:bool : option to plot hillshade over raster image
             (Default value = False)
        azimuth:int : The desired azimuth for the hillshade.
             (Default value = 150)

        Returns
        -------
        None

        """
        if hillshade:
            # Create and plot the hillshade with earthpy
            hillshade = es.hillshade(self.elevation, azimuth=azimuth)

            ep.plot_bands(
                hillshade,
                cbar=False,
                title="Hillshade made from DTM",
                figsize=(15, 15),
            )
            plt.savefig('hillshade.png')
            plt.show()
        else:
            # Plot the data
            ep.plot_bands(
                self.elevation,
                cmap="gist_earth",
                cbar=False,
                title="DTM Without Hillshade",
                figsize=(15, 15),
            )
            plt.savefig('DTM.png')
            plt.show()
                    

    def plot_overlay(self)->None:
        """ 
        Plot Overlays on the raster image
        """
        # Create and plot the hillshade with earthpy
        hillshade = es.hillshade(self.elevation)

        # Plot the DEM and hillshade at the same time
        _, ax = plt.subplots(figsize=(15, 15))
        ep.plot_bands(
            self.elevation,
            ax=ax,
            cmap="terrain",
            cbar=False,
            title="Lidar Digital Elevation Model (DEM)\n overlayed on top of a hillshade",
        )
        ax.imshow(hillshade, cmap="Greys", alpha=0.5)
        plt.show()
        plt.savefig('overlay.png')

    
if __name__ == "__main__":

    dtm = "tif/iowa2.tif"
    viz = VisualizeRaster(data_file_path=dtm)

    viz.plot_bands(hillshade=True)
    viz.plot_bands(hillshade=False, azimuth=130)
    viz.plot_overlay()