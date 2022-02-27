# PrometheusAI
## Table Of Contents:
1. **[Register to OperateFirst](docs/register_to_operate_first.md)**
2. **[Connect to Slack](docs/connect_to_slack.md)**
3. **[JupiterHub](docs/jupiter_hub.md)**
4. **[Intro to Prometheus Client](https://github.com/aicoe-aiops/time-series/blob/master/docs/get-started.md)**
5. **[Generate Personal access token](https://www.operate-first.cloud/apps/content/observatorium/thanos/thanos_programmatic_access.html)**
6. **[How to run our project]()**
7. **[Other useful links](docs/useful_links.md)**

## Predicting the Future Prometheus Metrics of a Kubernetes Cluster
[Kubernetes](https://kubernetes.io/) is a leading open source framework for container orchestration - the process of automating deployment and managing applications in a containerized and clustered environment. At its basic level, Kubernetes runs and coordinates container-based applications across a cluster of machines. It is designed to completely manage the life cycle of containerized applications and services using methods that provide predictability, scalability, and high availability.
A Kubernetes user provides the applications to be deployed in the form of pods - basic units of execution containing one or more tightly-coupled containers. These pods are then assigned to nodes, that represent actual computing resources such as physical or virtual servers. A collection of nodes forms a Kubernetes cluster, managed by the control plane.
One of the most important tasks of a Kubernetes cluster admin is to constantly monitor the status of the cluster and react accordingly when situations of interest occur or anomalies in the workflow are detected (such as an application failure or a malfunctioning node). The de facto standard monitoring software framework utilized to that end is called [Prometheus](https://prometheus.io/). As illustrated in the figure below, Prometheus collects real-time metrics from application services and nodes (up to millions of metrics per second), stores them in a time-series database, and provides a convenient visualization tool for the user to examine, query and analyze the data.
![image](https://user-images.githubusercontent.com/20024246/143770523-331d0298-e1f1-40ea-a1ed-e346d2e02eba.png)

 
While Prometheus is a very powerful monitoring system capable of high-quality real-time data gathering, it entirely lacks one important capability: predicting the expected values of future metrics. By detecting and observing repeatedly occurring patterns and trends in the monitored data and learning from them, it might be possible to not only detect abnormal conditions and situations, but also to forecast their occurrence in advance, thus providing an admin with sufficient time to prevent the possibly harmful or otherwise undesired event.
The goal of this project is to fill this gap by implementing a predictive component for Prometheus metrics. This component will incorporate a variety of well-known time series forecasting (TSF) algorithms, based on statistical methods, deep neural networks, or their combination. It will receive as input a stream of Prometheus updates (i.e., files containing the last recorded values for the monitored metrics) and generate a stream of predicted future values for all involved metrics.
