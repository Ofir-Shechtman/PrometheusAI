from prometheus_api_client import PrometheusConnect
from prometheus_api_client.metric_range_df import MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta
import pandas as pd


if __name__ == '__main__':
    operate_first_token = "sha256~RT0D8Zyftqt80pXThIZsGWfnO9cpuer7KQ_Q4Hw7RQY"
    thanos_url = 'https://thanos-query-frontend-opf-observatorium.apps.smaug.na.operate-first.cloud'
    pc = PrometheusConnect(
        url=thanos_url,
        headers={"Authorization": f"Bearer {operate_first_token}"},
        disable_ssl=False
    )
    pd.DataFrame(pc.all_metrics(), columns={"metrics"})
    pc.get_current_metric_value("http_requests_total")
