import pandas as pd
from prometheus_api_client import PrometheusConnect, PrometheusApiClientException
from prometheus_api_client.metric_range_df import MetricRangeDataFrame
from datetime import timedelta, datetime
from prometheus_api_client import MetricsList, MetricSnapshotDataFrame
from config import OPERATE_FIRST_TOKEN, THANOS_URL
import datetime


class ThanosConnect(PrometheusConnect):
    def __init__(self, url, op_token):
        super().__init__(url=url,
                         headers={"Authorization": f"Bearer {op_token}"},
                         disable_ssl=False)

    @staticmethod
    def dict_to_match_query(labels_config: dict):
        if labels_config:
            label_list = [f'{key}="{val}"' for key, val in labels_config.items()]
            return f'{{{",".join(label_list)}}}'
        else:
            return ''

    def range_query(self, start_time: datetime, end_time: datetime, step: int, metric_name='',
                    label_config: dict = None):
        query = metric_name + self.dict_to_match_query(label_config)
        metric_data = self.custom_query_range(query=query,
                                              start_time=start_time,
                                              end_time=end_time,
                                              step=str(step))
        return metric_data

    def query_label_values(self, label: str, cluster: str = None):
        if cluster:
            match = {'match[]': self.dict_to_match_query({'cluster': cluster})}
        else:
            match = None
        response = self._session.get(
            '{url}/api/v1/label/{label}/values'.format(url=self.url, label=label),
            params=match,
            verify=self.ssl_verification,
            headers=self.headers,
        )
        if response.status_code == 200:
            data = response.json()["data"]
        else:
            raise PrometheusApiClientException(
                "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
            )

        return data


if __name__ == '__main__':
    tc = ThanosConnect(THANOS_URL, OPERATE_FIRST_TOKEN)
    label_config = {'cluster': 'moc/smaug', 'job': 'noobaa-mgmt'}
    csv_path = 'noobaa-mgmt.csv'
    step=60
    clusters = tc.query_label_values(label='cluster')
    if label_config['cluster'] not in clusters:
        raise Exception(f'Cluster {label_config["cluster"]} not found. Try one of: {clusters}')
    jobs = tc.query_label_values(label='job', cluster=label_config["cluster"])
    if label_config['job'] not in jobs:
        raise Exception(f'Cluster {label_config["job"]} not found in cluster {label_config["cluster"]}. Try one of: {jobs}')

    start_time = datetime.datetime.strptime('2022-02-01 10:00:00', "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime('2022-02-23 22:30:00', "%Y-%m-%d %H:%M:%S")
    try:
        metric_data = tc.range_query(label_config=label_config, start_time=start_time, end_time=end_time, step=step)
    except PrometheusApiClientException as e:
        if e.args[0] != 'HTTP Status Code 400 (b\'exceeded maximum resolution of 11,000 points per timeseries. Try decreasing the query resolution (?step=XX)\')':
            raise e
        chunk_size = timedelta(minutes=1)
        metric_data = tc.get_metric_range_data(metric_name=tc.dict_to_match_query(label_config),
                                               start_time=start_time,
                                               end_time=end_time,
                                               chunk_size=chunk_size)
    metric_df = MetricSnapshotDataFrame(metric_data)
    metric_df['date'] = pd.to_datetime(metric_df['timestamp'], origin='unix', unit='s')
    pivot = metric_df.pivot(index='date', columns=set(metric_df.columns) - {'timestamp', 'date', 'value'})['value']
    r_pivot = pivot.resample(timedelta(seconds=step), label='left', closed='right', origin=start_time).last()
    r_pivot.to_csv(csv_path, header=False)
