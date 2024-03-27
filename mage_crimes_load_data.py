import io
import pandas as pd
import requests
from datetime import datetime
from json import loads
import time


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def get_fbi_wanted(page):

    content = None

    headers = {
        "Accept" : "application/json"
        , "Connection" : "keep-alive"
        , "Host" : "api.fbi.gov"
        , "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"
        , "Accept-Language" : "en-GB,en;q=0.9"
    }

    res = requests.get(f"https://api.fbi.gov/wanted/v1/list?page={page}", headers=headers)
    try:
        content = loads(res.content)
    except Exception as ex:
        print(res.content)

    return content




@data_loader
def load_data_from_api(*args, **kwargs):

    data_list = []

#run scripts to form dataframe
    page = 1

    fbi_wanted = get_fbi_wanted(page)

    while fbi_wanted["total"] > page * len(fbi_wanted["items"]):

        #increment page
        page += 1

        #sleep to avoid security blocking
        time.sleep(60)
        
        #get data
        content = get_fbi_wanted(page)
        
        data_list.extend(content['items'])
        
        print(page, page * len(fbi_wanted["items"]), fbi_wanted["total"])


    current_datetime = datetime.now()

    df_crimes = pd.json_normalize(data_list)

    df_crimes['check_datetime'] = current_datetime

    """
    Template for loading data from API
    """

    return df_crimes


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
