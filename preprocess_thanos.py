import pandas as pd
from prometheus_api_client import PrometheusApiClientException
from datetime import timedelta
from prometheus_api_client import MetricSnapshotDataFrame
from config import OPERATE_FIRST_TOKEN, THANOS_URL
from thanos_api_client import ThanosConnect
import datetime



# example of use:
if __name__ == '__main__':
    tc = ThanosConnect(THANOS_URL, OPERATE_FIRST_TOKEN)
    label_config = {'cluster': 'moc/smaug', 'job': 'noobaa-mgmt'}
    csv_path = 'noobaa-mgmt.csv'
    step = 60
    clusters = tc.query_label_values(label='cluster')
    if label_config['cluster'] not in clusters:
        raise Exception(f'Cluster {label_config["cluster"]} not found. Try one of: {clusters}')
    jobs = tc.query_label_values(label='job', cluster=label_config["cluster"])
    if label_config['job'] not in jobs:
        raise Exception(f'Cluster {label_config["job"]} not found in cluster {label_config["cluster"]}. Try one of: {jobs}')

    start_time = datetime.datetime.strptime('2022-03-02 14:00:00', "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime('2022-03-02 16:30:00', "%Y-%m-%d %H:%M:%S")
    try:
        metric_data = tc.range_query(metric_name="NooBaa_BGWorkers_nodejs_active_handles",label_config=label_config, start_time=start_time, end_time=end_time, step=step)
    except PrometheusApiClientException as e:
        print(f"this is my exception {e}")
        if e.args[0] != 'HTTP Status Code 400 (b\'exceeded maximum resolution of 11,000 points per timeseries. Try decreasing the query resolution (?step=XX)\')':
            raise e
        chunk_size = timedelta(seconds=step)
        metric_data = tc.get_metric_range_data(metric_name=tc.dict_to_match_query(label_config),
                                               start_time=start_time,
                                               end_time=end_time,
                                               chunk_size=chunk_size)
    if not metric_data:
        raise Exception("Got Empty results")
    metric_df = MetricSnapshotDataFrame(metric_data)
    metric_df['date'] = pd.to_datetime(metric_df['timestamp'], origin='unix', unit='s')
    pivot = metric_df.pivot(index='date', columns=set(metric_df.columns) - {'timestamp', 'date', 'value'})['value']
    r_pivot = pivot.resample(timedelta(seconds=step), label='left', closed='right', origin=start_time).last()
    r_pivot.to_csv(csv_path, header=False)
