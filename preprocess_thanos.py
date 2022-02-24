import datetime
import os
import pandas as pd

from thanos_api_client import ThanosConnect
from prometheus_api_client import MetricsList, MetricSnapshotDataFrame
from datetime import timedelta
from config import OPERATE_FIRST_TOKEN, THANOS_URL
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_to_dataframe():
    tc = ThanosConnect(THANOS_URL, OPERATE_FIRST_TOKEN)
    label_config = {'cluster': 'moc/smaug', 'job': 'noobaa-mgmt'}
    start_time = datetime.datetime.strptime('2022-02-19 22:00:00', DATETIME_FORMAT)
    end_time = datetime.datetime.strptime('2022-02-22 22:30:00', DATETIME_FORMAT)
    metric_data = tc.range_query(label_config=label_config, start_time=start_time, end_time=end_time, step="300")
    return MetricSnapshotDataFrame(metric_data)



if __name__ == '__main__':
    global save_path
    save_name = 'thanos'
    name = 'noobaa-mgmt.csv'


    save_path = os.path.join('data', save_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    csv_path = os.path.join(save_path, name)
    if not os.path.exists(csv_path):
        start_time = datetime.datetime.strptime(train_start, DATETIME_FORMAT)  # parse_datetime("10m")
        end_time = datetime.datetime.strptime(test_end, DATETIME_FORMAT)  # parse_datetime("now")
        chunk_size = timedelta(minutes=1)
        tc = ThanosConnect()
        # label_config = {'cluster': 'moc/smaug', 'job': 'noobaa-mgmt'}
        metric_data = tc.get_metric_range_data(metric_name='{cluster="moc/smaug", job="noobaa-mgmt"}',
                                               start_time=start_time,
                                               end_time=end_time,
                                               chunk_size=chunk_size)

        metric_object_list = MetricsList(metric_data)
        metric_df = MetricSnapshotDataFrame(metric_data)
        metric_df['date'] = pd.to_datetime(metric_df['timestamp'], origin='unix', unit='s')
        pivot = metric_df.pivot(index='date', columns=set(metric_df.columns) - {'timestamp', 'date', 'value'})['value']
        r_pivot = pivot.resample('1min', label='left', closed='right', origin=start_time).last()
        # r_pivot.index = r_pivot.index.strftime(DATETIME_FORMAT)
        r_pivot.to_csv(csv_path, header=False)

