from datetime import timedelta
from PrometheusClient import PrometheusClient

if __name__ == '__main__':
    pc = PrometheusClient()
    print("Hello falful")
    # for df in pc.getAllMetrics(time_range=timedelta(seconds=5)):
    #     print(df)
    #     # TODO: read alog's implementations to find out how we need to set the dataloader
    #
