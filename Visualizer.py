import matplotlib.pyplot as plt
from PrometheusClient import PrometheusClient
from datetime import timedelta

if __name__ == '__main__':
    pc = PrometheusClient()
    _metric_df = pc.getRangeData("node_memory_Active_bytes", timedelta(minutes=1))
    _metric_df['value'] = _metric_df['value'].astype(float).div(1e9)
    x = _metric_df.index
    y = _metric_df['value']
    plt.scatter(x, y, s=2.0)
    plt.locator_params(axis="y", nbins=20)
    plt.xlabel('Time GMT+0')
    plt.ylabel('Bytes [GB]')
    plt.title('Node memory active bytes')
    plt.show()
