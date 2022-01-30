from prometheus_api_client import PrometheusConnect
from prometheus_api_client.metric_range_df import MetricRangeDataFrame
from datetime import timedelta, datetime
from config import OPERATE_FIRST_TOKEN, THANOS_URL
import pandas as pd


class PrometheusClient:
    def __init__(self):
        self.pc = PrometheusConnect(
            url=THANOS_URL,
            headers={"Authorization": f"Bearer {OPERATE_FIRST_TOKEN}"},
            disable_ssl=False)

    def getRangeData(self, metric, time_range: timedelta):
        end_time = datetime.now()
        start_time = end_time - time_range
        metric_data = self.pc.get_metric_range_data(
            metric,  # metric name and label config
            start_time=start_time,  # datetime object for metric range start time
            end_time=end_time,  # datetime object for metric range end time
            chunk_size=time_range  # timedelta object for duration of metric data downloaded in one request
        )
        metric_df = MetricRangeDataFrame(metric_data)
        metric_df.index = pd.to_datetime(metric_df.index.tolist(), unit="s", utc=True)
        print(metric_df)
        return metric_df
