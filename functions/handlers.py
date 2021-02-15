from covid_etl import covid_etl

# lambda logic only
NYT_DATASET = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
JOHNS_HOPKINS_DATASET = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid" \
                        "-combined.csv"


def run(__, _):

    dataset = {"NYT_DATASET": NYT_DATASET, "JOHNS_HOPKINS_DATASET": JOHNS_HOPKINS_DATASET}
    return covid_etl(dataset)
