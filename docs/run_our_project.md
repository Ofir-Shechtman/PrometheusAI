# Run Our Project

### Prerequisites:
1. Make sure you have a valid access token based on this [guide](https://www.operate-first.cloud/apps/content/observatorium/thanos/thanos_programmatic_access.html)
2. Paste your token in config.py under `OPERATE_FIRST_TOKEN`
3. Validate that the `THANOS_URL` directs to the server
4. Make sure all the packages in the [requirements file](requirements.txt) installed on your environment

### Contents:
1. **thanos_api_client.py** - A wrapper class to PrometheusConnect that adds convenient methods for fetching Prometheus data 
2. **preprocess_thanos.py** - Demonstration of fetching prometheus data and exporting it to csv using our wrapper class
3. **visualizer.py** - Demonstration of fetching prometheus data and showing it on a graph

### Running our script:
* **preprocess_thanos.py** - configure the arguments of `start_preprocessing` method and run preprocess_thanos.py
* **visualizer.py** - Plots the data into a nice graph
* **thanos_api_client** - Consists of the wrapper methods we built over the Prometheus client.  
    `range_query` our custom built-in function that queries the server (usage example is provided in `preprocess_thanos.py`)
    `metric_data_to_df` -   






  
 
