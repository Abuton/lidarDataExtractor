import ast
import pdal
import json
from lidardataextractor import region_file_loader
import logging
import geopandas as gpd
from osgeo import ogr, osr, gdal
import sys
import numpy as np

form = logging.Formatter("%(asctime)s : %(levelname)-5.5s : %(message)s")
logger = logging.getLogger()

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(form)
if not logger.handlers:
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.INFO)

class RasterGetter:
    """Get raster and laz files based on pdal pipeline"""

    def __init__(self, bounds:str, crs:int) -> None:
        self.bounds = bounds 
        self.crs = crs   
        self.public_data_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
        # get region based in bounds
        self.regions = self.get_regions()
        self.load_pipeline()

    def get_regions(self):
        """The function get region based on input bound from the user

        Parameters
        ----------
        bounds : str : the boundary of a region
            

        Returns
        -------

        """
        logger.info(" Finding bounds region")
        region_ept_info = region_file_loader.load_ept_json()
        user_bounds = ast.literal_eval(self.bounds)
        regions = []

        for key, value in region_ept_info.items():
            if value.bounds[0] <= user_bounds[0][0] and \
                value.bounds[1] <= user_bounds[1][0] and \
                value.bounds[3] >= user_bounds[0][1] and \
                value.bounds[4] >= user_bounds[1][1]:
                regions.append(key)

        return regions

    def construct_pipeline(self):
    
        self.dynamic_pipeline = []
        reader = {
            "bounds": "",
            "filename": "",
            "type": "readers.ept",
            "tag": "readdata"
        }
        self.dynamic_pipeline.append(reader)
        classification_filter = {
            "limits": "Classification![2:7], Classification![9:9]", 
            "type": "filters.range",
            "tag": "nonoise"

        }
        self.dynamic_pipeline.append(classification_filter)
        reprojection = {
            "in_srs": "EPSG:3857",
            "out_srs": "EPSG:3857",
            "tag": "reprojectUTM",
            "type": "filters.reprojection"
        }
        self.dynamic_pipeline.append(reprojection)
        laz_writer = {
            "filename": "",
            "inputs": [ "reprojectUTM" ],
            "tag": "writerslas",
            "type": "writers.las"
        }
        self.dynamic_pipeline.append(laz_writer)
        tif_writer = {
            "filename": "",
            "gdalopts": "tiled=yes,     compress=deflate",
            "inputs": [ "writerslas" ],
            "nodata": -9999,
            "output_type": "idw",
            "resolution": 1,
            "type": "writers.gdal",
            "window_size": 6
        }
        self.dynamic_pipeline.append(tif_writer)

        # self.dynamic_pipeline = pdal.Pipeline(json.dumps(self.dynamic_pipeline))
    
        return self.dynamic_pipeline

    def load_pipeline(self) -> None:
        """The Function loads a pipeline 

        Parameters
        ----------

        Returns
        -------
        None

        """
        try:
            self.external_pipeline = self.construct_pipeline()
            logger.info("Pipeline Succefully Constructed")
        except Exception as e:
            print(e)
            logger.info("Pipeline Could not be Constructed")

    def get_raster_terrain(self, region:str) -> None:
        """The Function gets the raster terrain of a given region
            It saves the laz and tif files in the specified 

        Parameters
        ----------
        bounds : str : bounds of the region to be computed
            
        region:str : region of the given bound
            

        Returns
        -------
        
        """

        logger.info(f"Fetching Laz and tiff files for {region}")
        PUBLIC_ACCESS_PATH = self.public_data_path + str(region) + "ept.json"

        # dynamically update template pipeline
        self.external_pipeline[0]['bounds'] = self.bounds
        self.external_pipeline[0]['filename'] = PUBLIC_ACCESS_PATH
        self.external_pipeline[3]['filename'] = f"{str(region).strip('/')}.laz"
        self.external_pipeline[4]['filename'] = f"{str(region).strip('/')}.tif"

        # create pdal pipeline
        pipeline = pdal.Pipeline(json.dumps(self.external_pipeline))
        logger.info("Pipeline Dumped and Ready for use")
        # execute pipeline
        pipe_exec = pipeline.execute()
        metadata = pipeline.metadata
        log = pipeline.log
        logger.info("Pipeline Complete Execution Succefully ")

    def get_geodataframe(self, tif_file: str, region:str):
        """Compute the Elevations in a raster tif file

        Parameters
        ----------
        tif_file : str : filename/location of a tif image
   
        region:str :
            
        save: bool :
             (Default value = True)
        viz:bool :
             (Default value = False)

        Returns
        -------
        A GeoDataFrame

        """
        self.get_point_elevation_twi(tif_filename=tif_file, shp_filename=f"{str(region).strip('/')}.shp", 
                                point_elevation_filename=f"{str(region).strip('/')}.csv")

    def reproject_crs(self, df, region:str, src_epsg:int=3857, target_epsg:int=4326) ->  gpd.GeoDataFrame: 
        """
        The function will reproject a geodataframe
        if the save argument is True, the geodataframe will be saved
        and can be used for visualization on the map

        Parameters
        ----------
        df : a geopandas dataframe
            
        region:str : the region of the geo dataframe
            
        save :
             (Default value = True)

        Returns
        -------
        A GeoDataFrame
        """
        points = df['geometry']

        source = osr.SpatialReference()
        source.ImportFromEPSG(src_epsg)

        target = osr.SpatialReference()
        target.ImportFromEPSG(target_epsg)

        transform = osr.CoordinateTransformation(source, target)
        new_points = []
        for p in points:
            point = ogr.CreateGeometryFromWkt(f"{p}")
            point.Transform(transform)
            new_points.append(point.ExportToWkt())

        new_df = gpd.GeoDataFrame(data=zip(df.elevation, new_points, df.twi), columns=['elevation', 'geometry', 'twi'])
        
        new_df.to_csv(f"{str(region).strip('/')}_reprojected.csv", index=False)
        logger.info(f"file saved succesfully here {str(region).strip('/')}")

    def save_geodataframe(self, csv_filename:str) -> None:
        """Save a GeoDataFrame into a csv

        Parameters
        ----------
        csv_filename : str : filename of the csv to be created

        Returns
        -------

        """
        self.gdf.to_csv(csv_filename, index=False)
        logger.info(f"GeoDataframe Elevation File Successfully Saved here {csv_filename}")

    def year_gpd_dict(self) -> dict:
        """Get year column based on bound"""
        year_gpd = {}
        if len(self.regions) == 0:
            logger.info("Bound Error! No region Found")
            sys.exit(1)

        logger.info(f'Getting laz and tif files from {len(self.regions)} Regions')
        for region in self.regions:
            year = region.split("_")[-1][:-1]
            if not year.isdigit():
                year = region
            try:
                logger.info(f"\nGetting DEM for {year}")
                self.get_raster_terrain(region)
                year_gpd[year] = self.get_geodataframe(f"{str(region).strip('/')}.tif", region=region, save=True, viz=True)
                self.save_geodataframe(csv_filename=f"data/{str(region).strip('/')}.csv")

            except Exception as e:
                logger.info(f'{e} Region Overlayed')
                if len(self.regions) > 1:
                    continue
                logger.info('\nMoving to next region')
        return year_gpd

    def tif_shp(self, shp_filename:str, tif_filename:str) -> None:
        """
        The function converts a tif file to a shp file

        Parameters
        ----------
        shp_filename:str : filename/path of the converted shp file
            
        tif_filename:str : filename/path of the tif file to be converted

        Returns
        -------
        None

        """
        # mapping between gdal type and ogr field type
        type_mapping = { gdal.GDT_Byte: ogr.OFTInteger,
                        gdal.GDT_UInt16: ogr.OFTInteger,   
                        gdal.GDT_Int16: ogr.OFTInteger,    
                        gdal.GDT_UInt32: ogr.OFTInteger,
                        gdal.GDT_Int32: ogr.OFTInteger,
                        gdal.GDT_Float32: ogr.OFTReal,
                        gdal.GDT_Float64: ogr.OFTReal,
                        gdal.GDT_CInt16: ogr.OFTInteger,
                        gdal.GDT_CInt32: ogr.OFTInteger,
                        gdal.GDT_CFloat32: ogr.OFTReal,
                        gdal.GDT_CFloat64: ogr.OFTReal}

        # this allows GDAL to throw Python Exceptions
        gdal.UseExceptions()
        logger.info("reading tif file...")
        try:
            ds = gdal.Open(tif_filename)
        except RuntimeError as e:
            logger.info('Unable to open file')
            print(e)
            sys.exit(1)
        try:
            srcband = ds.GetRasterBand(1)
        except RuntimeError as e:
            logger.info('Band ( %i ) not found' % 1)
            print(e)
            sys.exit(1)

        # create shapefile datasource from geotiff file
        logger.info("creating shapefile...")
        dst_layername = "Shape"
        drv = ogr.GetDriverByName("ESRI Shapefile")
        dst_ds = drv.CreateDataSource(shp_filename)
        dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
        raster_field = ogr.FieldDefn('elevation', type_mapping[srcband.DataType])
        dst_layer.CreateField(raster_field)
        gdal.Polygonize(srcband, None, dst_layer, 0, [], callback=None) 
        logger.info(f'Shp file created successfully here {shp_filename}')

    def get_point_elevation_twi(self, tif_filename:str, shp_filename:str, point_elevation_filename:str, resolution:int=5)-> gpd.GeoDataFrame:
        """
        The function computes and returns a geodataframe

        Parameters
        ----------
        tif_filename:str : filename/path of the converted tof file
            
        shp_filename:str : filename/path of the converted shp file
            
        point_elevation_filename:str :  filename/path of the converted csv file
            
        resolution:int : the resolution of the raster data
             (Default value = 5)

        Returns
        -------
        A GeoDataFrame

        """
        self.tif_shp(shp_filename=shp_filename, tif_filename=tif_filename)
        df = gpd.read_file(shp_filename)
        logger.info('Shp file read successfully')
        # get area
        df['area'] = df.set_crs(epsg=3857)['geometry'].area
        df['geometry'] = df['geometry'].centroid
        df['slope'] = np.arctan(df['elevation']/resolution)
        df['twi'] = np.log(df['area'] / df['slope'])
        
        df[['elevation', 'geometry', 'twi']].to_csv(f'{point_elevation_filename}', index=False)
        logger.info(f"Point Elevation csv File saved here {point_elevation_filename}")
        

if __name__ == "__main__":
    # BOUNDS = "([-93.756155, -93.747334], [41.918015, 41.921429])"

    # ([minx, maxx], [miny, maxy])
    BOUNDS = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"
    MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]

    raster = RasterGetter(bounds=BOUNDS, crs=3857)
    # year_dict = raster.year_gpd_dict()
    # pprint(year_dict)
    raster.get_geodataframe(f"IA_FullState.tif", "IA_FullState")
