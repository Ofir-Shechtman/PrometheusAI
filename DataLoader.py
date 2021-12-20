from datetime import timedelta
from PrometheusClient import PrometheusClient

if __name__ == '__main__':
    pc = PrometheusClient()
    df_all = pc.getAllMetrics(time_range=timedelta(seconds=5))
    pass

