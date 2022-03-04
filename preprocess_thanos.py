import pandas as pd
from prometheus_api_client import PrometheusApiClientException
from datetime import timedelta
from config import OPERATE_FIRST_TOKEN, THANOS_URL
from thanos_api_client import ThanosConnect
import datetime


def export_to_csv(data, csv_path: str, start_time: datetime):
    metric_df = ThanosConnect.metric_data_to_df(data)
    metric_df['date'] = pd.to_datetime(metric_df['timestamp'], origin='unix', unit='s')
    pivot = metric_df.pivot(index='date', columns=set(metric_df.columns) - {'timestamp', 'date', 'value'})['value']
    r_pivot = pivot.resample(timedelta(seconds=60), label='left', closed='right', origin=start_time).last()
    r_pivot.to_csv(csv_path, header=True)


def start_preprocessing(csv_path: str, label_config: dict, start_time: datetime, end_time: datetime, step: int):
    """
    Saves the desired Prometheus data according to the label_config into a csv file based on the csv_path
    :param csv_path: path for saving the csv
    :param label_config: Metric names we query the server upon
    :param start_time: The query's start time
    :param end_time: The query's end time
    :param step: the resolution between two samples.
    """
    tc = ThanosConnect(THANOS_URL, OPERATE_FIRST_TOKEN)
    clusters = tc.query_label_values(label='cluster')
    if label_config['cluster'] not in clusters:
        raise Exception(f'Cluster {label_config["cluster"]} not found. Try one of: {clusters}')
    jobs = tc.query_label_values(label='job', cluster=label_config["cluster"])
    if label_config['job'] not in jobs:
        raise Exception(f'Cluster {label_config["job"]} not found in cluster {label_config["cluster"]}. Try one of: {jobs}')

    try:
        metric_data = tc.range_query(metric_name="NooBaa_BGWorkers_nodejs_active_handles", label_config=label_config, start_time=start_time, end_time=end_time, step=step)
    except PrometheusApiClientException as e:
        print(f"this is my exception {e}")
        if e.args[0] != 'HTTP Status Code 400 (b\'exceeded maximum resolution of 11,000 points per timeseries. Try decreasing the query resolution (?step=XX)\')':
            raise e
        chunk_size = timedelta(seconds=step)
        metric_data = tc.get_metric_range_data(metric_name=tc.build_query(label_config),
                                               start_time=start_time,
                                               end_time=end_time,
                                               chunk_size=chunk_size)
    if not metric_data:
        raise Exception("Got empty results")

    return metric_data


# usage example:
if __name__ == '__main__':
    _csv_path = 'noobaa-mgmt.csv'
    _label_config = {'cluster': 'moc/smaug', 'job': 'noobaa-mgmt'}
    _start_time = datetime.datetime.strptime('2022-03-02 14:00:00', "%Y-%m-%d %H:%M:%S")
    _end_time = datetime.datetime.strptime('2022-03-02 16:30:00', "%Y-%m-%d %H:%M:%S")
    _step = 60  # seconds
    _metric_data = start_preprocessing(_csv_path, _label_config, _start_time, _end_time, _step)
    export_to_csv(_metric_data, _csv_path, _start_time)


