import pandas as pd
import boto3
from datetime import datetime
import logging

COUNTER_TABLE_NAME = "CovidETLCounter"
DATA_TABLE_NAME = "CovidData"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def covid_etl(datasets):

    # starting date
    start_date = get_start_date()

    # extract and transform NYT_DATASET
    logger.info("Extract and transform NYT_DATASET")
    nyt_data = extract_data(datasets['NYT_DATASET'])

    nyt_clean_data = transform_nyt_dataset(nyt_data, start_date=start_date)

    # extract and transform JOHNS_HOPKINS_DATASET
    logger.info("Extract and transform JOHNS_HOPKINS_DATASET")
    jhu_data = extract_data(datasets['JOHNS_HOPKINS_DATASET'])
    jhu_clean_data = transform_jhu_dataset(jhu_data)

    # join both datasets
    logger.info("Join both datasets")
    covid_data = nyt_clean_data.join(jhu_clean_data, on="date", how="inner")

    # write data to database
    logger.info("Write data to database")
    return load_dataset_to_db(covid_data)


def extract_data(dataset_url):
    try:
        data = pd.read_csv(dataset_url)
        return data
    except Exception as e:
        print(e)

    return None


def transform_nyt_dataset(nyt_data, start_date=None):

    # convert the columns to datetime
    nyt_data['date'] = pd.to_datetime(nyt_data['date'])

    # set the date column as index
    nyt_data = nyt_data.set_index("date")

    if start_date is None:
        start_date = nyt_data.index[0]

    today = datetime.today()
    date_range = pd.date_range(start_date, today)

    # filter new york times records to the desired date range
    nyt_data = nyt_data[nyt_data.index.isin(date_range)]
    logger.info("Done transforming nyt data")
    return nyt_data


def transform_jhu_dataset(jhu_data):

    # clean the date column
    jhu_data = jhu_data.rename(columns={"Date": "date"})
    jhu_data['date'] = pd.to_datetime(jhu_data['date'])
    jhu_data = jhu_data.set_index("date")

    # filter jhu dataset to US region only
    jhu_data = jhu_data[jhu_data["Country/Region"] == "US"]

    # drop unneeded columns and NAs
    jhu_data.drop(["Country/Region", "Province/State", "Confirmed", "Deaths"], axis=1, inplace=True)
    jhu_data = jhu_data.dropna()

    # format the column types
    jhu_data = jhu_data.astype({'Recovered': 'int64'})

    logger.info("Done transforming jhu data")
    return jhu_data


def get_start_date():
    logger.info("Get start date")
    dynamodb = boto3.client("dynamodb")
    response = dynamodb.get_item(
        Key={
            'ID': {
                'N': "1",
            }
        },
        TableName=COUNTER_TABLE_NAME,
    )

    item = response.get("Item", None)
    if item is None:
       return None

    return item.get("LastSuccessfulRecord")["S"]


def update_start_date(last_successful):
    logger.info("Update start date")
    dynamodb = boto3.client('dynamodb')
    key = {
        "ID": {
            "N": "1"
        }
    }

    _ = dynamodb.update_item(
        TableName=COUNTER_TABLE_NAME,
        Key=key,
        ReturnValues="ALL_NEW",
        ExpressionAttributeNames={
            "#LSR": "LastSuccessfulRecord",
        },
        ExpressionAttributeValues={
            ":lsr": {
                "S": str(last_successful)
            }
        },
        UpdateExpression="SET #LSR = :lsr"
    )


def load_dataset_to_db(dataset):

    dynamodb = boto3.client("dynamodb")
    error = False
    errored_date = None
    for index, row in dataset.iterrows():
        response = dynamodb.put_item(
            Item={
                'Date': {
                    'S': str(index),
                },
                'Cases': {
                    'N': str(row['cases']),
                },
                'Death': {
                    'N': str(row['deaths']),
                },
                'Recovered': {
                    'N': str(row['Recovered']),
                }
            },
            ReturnConsumedCapacity='TOTAL',
            TableName=DATA_TABLE_NAME,
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            error = True
            errored_date = index
            logging.error(f"Failed to write data for date: {index}")
            break

    if error:
        update_start_date(errored_date)
        return False

    update_start_date(datetime.today())
    return True
