# lidardataextractor : Overview

[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try)

Lidardataextractor is an open-source python package for retrieving, transforming, and visualizing point cloud data obtained through an aerial LiDAR survey. Using the package, you can select a region of interest, and download the related point cloud dataset with its metadata in different file formats (.laz, .tif, or as an ASCII file), perform transformation and visualization using the downloaded data.

## Requirements

    - AWS Account : Create One [here](https://aws.amazon.com/resources/create-account/)
    - PDAL : Python Data Abstraction Library
    - boto3 : Python API for performing actions/tasks on AWS
    - geopandas : Python library to manipulate geospatial datasets
    - earthpy : Used for Raster data Visualization
    
### Data

The USGS 3D Elevation Program (3DEP) provides access to lidar point cloud data from the 3DEP repository. The adoption of cloud storage and computing by 3DEP allows users to work with massive datasets of lidar point cloud data without having to download them.

The point cloud data is freely accessible from AWS in EPT format. Entwine Point Tile (EPT) is a simple and flexible octree-based storage format for point cloud data. The organization of an EPT dataset contains JSON metadata portions as well as binary point data. The JSON file is core metadata required to interpret the contents of an EPT dataset.

### Installation

a. **Creating conda virtual environment**

    conda create -n venv_name
    conda activate venv_name
    conda config  --env --add channels conda-forge
    conda config --env --set channel_priority strict
    conda install geopandas
    conda install PDAL

b. **Cloning the repo and install the dependency packages using `requirements.txt`**

    git clone `https://github.com/Abuton/lidarDataExtractor.git`
    cd lidarDataExtractor
    `conda install -r requirements.txt`
