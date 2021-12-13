# lidardataextractor : Overview

[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try)

Lidardataextractor is an open-source python package for retrieving, transforming, and visualizing point cloud data obtained through an aerial LiDAR survey. Using the package, you can select a region of interest, and download the related point cloud dataset with its metadata in different file formats (.laz, .tif, or as an ASCII file), perform transformation and visualization using the downloaded data

## Requirements

    - AWS Account : Create One [here](https://aws.amazon.com/resources/create-account/)
    - PDAL : Python Data Abstraction Library
    - boto3 : Python API for performing actions/tasks on AWS
    - geopandas/rasterio : Python library to manipulate geospatial datasets
    - earthpy : Used for Raster data Visualization

### Data

The USGS 3D Elevation Program (3DEP) provides access to lidar point cloud data from the 3DEP repository. The adoption of cloud storage and computing by 3DEP allows users to work with massive datasets of lidar point cloud data without having to download them.

The point cloud data is freely accessible from AWS in EPT format. Entwine Point Tile (EPT) is a simple and flexible octree-based storage format for point cloud data. The organization of an EPT dataset contains JSON metadata portions as well as binary point data. The JSON file is core metadata required to interpret the contents of an EPT dataset.

### Installation

a. **How to create a conda virtual environment**

    conda create -n venv_name
    conda activate venv_name
    conda config  --env --add channels conda-forge
    conda config --env --set channel_priority strict
    conda install geopandas
    conda install PDAL

b. **Clone the repo and install the dependency packages using `requirements.txt`**

    git clone https://github.com/Abuton/lidarDataExtractor.git
    cd lidarDataExtractor
    conda install -r requirements.txt

### Usage

The *notebook_walkthrough* folder contains notebook that shows how to use each function in the package

    `my_viz.ipynb` notebook shows some visuals using folium python package to plot raster image on street maps. It also shows point heatmaps, markers and point cloud data
    `raster_getter_demo.ipynb` notebook shows how to use the package to get a raster terrain file by passing the bound. It also shows how to reproject crs
    `visualization_demo.ipynb` notebook shows how to use the *visualize* module to visualize the tif and shp files
