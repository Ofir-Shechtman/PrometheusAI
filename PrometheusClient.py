from prometheus_api_client import PrometheusConnect
from prometheus_api_client.metric_range_df import MetricRangeDataFrame
from datetime import timedelta, datetime
import pandas as pd

OPERATE_FIRST_TOKEN = "sha256~_2MH2RN9JX1-a39wTHPtiGflHN4PSLyMJOvMe__H0lQ"
THANOS_URL = "https://thanos-query-frontend-opf-observatorium.apps.smaug.na.operate-first.cloud"


class PrometheusClient:
    def __init__(self):
        self.end_time = datetime.now()
        self.pc = PrometheusConnect(
            url=THANOS_URL,
            headers={"Authorization": f"Bearer {OPERATE_FIRST_TOKEN}"},
            disable_ssl=False)

    def getAllMetrics(self, time_range: timedelta):
        df_all = pd.DataFrame()
        for metric in self.pc.all_metrics():
            df = self.getRangeData(metric, time_range)
            if df is not None:
                df_all.join(df)
        return df_all

    def getRangeData(self, metric, time_range: timedelta):
        start_time = self.end_time - time_range
        metric_data = self.pc.get_metric_range_data(
            metric,  # metric name and label config
            start_time=start_time,  # datetime object for metric range start time
            end_time=self.end_time,  # datetime object for metric range end time
            chunk_size=time_range  # timedelta object for duration of metric data downloaded in one request
        )
        if not metric_data:
            return None
        metric_df = MetricRangeDataFrame(metric_data)
        metric_df.index = pd.to_datetime(metric_df.index.tolist(), unit="s", utc=True)
        return metric_df
