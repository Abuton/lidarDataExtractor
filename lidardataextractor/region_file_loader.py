import json
import boto3
import logging
import asyncio
from aiohttp import ClientSession
from ept_info import Info

form = logging.Formatter("%(asctime)s : %(levelname)-5.5s : %(message)s")
logger = logging.getLogger()


consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(form)
logger.addHandler(consoleHandler)

logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
bucket = "usgs-lidar-public"
bucket_url = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"

def list_folders(s3_client: str, bucket_name: str):
    """

    Parameters
    ----------
    s3_client: str :
        
    bucket_name: str :
        

    Returns
    -------

    """
    logger.info(f"fetching folders in {bucket_name}")
    paginator = s3_client.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(Bucket=bucket_name, Delimiter='/',
                                           Prefix='')

    for page in response_iterator:
        for content in page.get("CommonPrefixes", []):
            yield content.get('Prefix')

async def fetch(region, url, session):
    async with session.get(url) as response:
        return (region, await response.read())

async def run():
    regions = list_folders(s3, bucket)
    region_info = []
    async with ClientSession() as session:
        logger.info(f"loading the ept.json files from {bucket}")
        for region in regions:
            if region == "USGS_LPC_WA_Western_North_2016_LAS_2018/" or \
                    region == "USGS_LPC_WA_Western_South_2016_LAS_2018/":
                ept_json_path = bucket_url + region + "ept-1.json"
            else:
                ept_json_path = bucket_url + region + "ept.json"
            ept_region_info = asyncio.ensure_future(fetch(region, ept_json_path, session))
            region_info.append(ept_region_info)

        response = await asyncio.gather(*region_info)

    return region_info

def load_ept_json() -> dict:
    """ """
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())
    regions = loop.run_until_complete(future)

    region_ept_info = {}

    for i in range(len(regions)):
        try:
            region_ept_info[regions[i].result()[0]] = Info(regions[i].result()[1].decode())
        except json.decoder.JSONDecodeError as e:
            print(regions[i].result()[0])

    return(region_ept_info)
