# Run Our Project

### Prerequisites:
1. Make sure you have a valid access token based on this [guide](https://www.operate-first.cloud/apps/content/observatorium/thanos/thanos_programmatic_access.html)
2. Paste your token in config.py under `OPERATE_FIRST_TOKEN`
3. Validate that the `THANOS_URL` in config.py directs to the correct server
4. Make sure all the packages in the [requirements file](../requirements.txt) installed on your environment

### Contents:
1. **thanos_api_client.py** - A wrapper class to PrometheusConnect that adds convenient methods for fetching Prometheus data 
2. **preprocess_thanos.py** - Demonstration of fetching prometheus data using our wrapper class, exporting it to csv or plotting it to a graph.

### Running our script:
* **preprocess_thanos.py** - configure the arguments of `start_preprocessing` method and run preprocess_thanos.py   
* **thanos_api_client** - Consists of the wrapper methods we built over the Prometheus client.  
    * `ThanosConnect` - Connects to the Thanos server based on the provided token.
    * `build_query` - A query for the Thanos server consists of two parts - metrics name and labels config. This method formulates a valid query for the server based on the given labels-config and metrics-name.
    * `range_query` our custom built-in function that queries the server (usage example is provided in `preprocess_thanos.py`)  
    * `metric_data_to_df` - A parser method that converts the received metric data into Pandas Dataframe object.  
    * `query_label_values` - Returns all possible values of a given label. We implemented this function based on the official documentation. For more information can check this [link](https://prometheus.io/docs/prometheus/latest/querying/api/#querying-label-values)   





  
 
