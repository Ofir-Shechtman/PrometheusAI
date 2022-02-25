from datetime import timedelta
from PrometheusClient import PrometheusClient, ThanosConnect



if __name__ == '__main__':
    pc = PrometheusClient()
    row_count = 0
    for df in pc.getAllMetrics(time_range=timedelta(seconds=5)):
        print(df["__name__"][0])
        # TODO: read alog's implementations to find out how we need to set the dataloader
