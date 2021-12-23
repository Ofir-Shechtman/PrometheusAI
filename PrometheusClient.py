from prometheus_api_client import PrometheusConnect
from prometheus_api_client.metric_range_df import MetricRangeDataFrame
from datetime import timedelta, datetime
import pandas as pd

OPERATE_FIRST_TOKEN = "sha256~MsCOTLtan_rxQ0Ab3iiwd2lScgPo5eoFhN9bnLdW6xc"
THANOS_URL = "https://thanos-query-frontend-opf-observatorium.apps.smaug.na.operate-first.cloud"


class ThanosConnect(PrometheusConnect):
    def __init__(self):
        super().__init__(url=THANOS_URL,
                         headers={"Authorization": f"Bearer {OPERATE_FIRST_TOKEN}"},
                         disable_ssl=False)


class PrometheusClient:
    def __init__(self):
        self.end_time = datetime.now()
        self.thanos = ThanosConnect()

    def getAllMetrics(self, time_range: timedelta):
        for metric_name in self.thanos.all_metrics():
            df = self.getRangeData(metric_name, time_range)
            if df is not None:
                yield df

    def getRangeData(self, metric_name, time_range: timedelta):
        start_time = self.end_time - time_range
        metric_data = self.thanos.get_metric_range_data(
            metric_name,  # metric name and label config
            start_time=start_time,  # datetime object for metric range start time
            end_time=self.end_time,  # datetime object for metric range end time
            chunk_size=time_range  # timedelta object for duration of metric data downloaded in one request
        )
        if not metric_data:
            return None
        metric_df = MetricRangeDataFrame(metric_data)
        metric_df.index = pd.to_datetime(metric_df.index.tolist(), unit="s", utc=True)
        return metric_df


