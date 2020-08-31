# UPNP Bandwidth Monitoring for RAC2V1K AKA rt4230w-d187
This repo contains a python script which will SSDP poll, looking for a UPNP capable router that reports as model 'rt4230w-d187', and if found, use UPNP to poll for bytes and packets in/out. This information is exposed on a prometheus webserver, which we can then scrape with prometheus and plot with grafana.

## To use
1. Build and start a container running the monitor
    ```
    docker-compose up --detach
    # Wait a bit, verify if it's working or not
    curl localhost:8888
    ```
2. Add a scrape config to prometheus. See [prometheus_server_config.yml](prometheus_server_config.yml) for the full example, but basically:
    ```
    scrape_configs:
    - job_name: router
        honor_timestamps: true
        scrape_interval: 15s
        scrape_timeout: 10s
        metrics_path: /
        scheme: http
        static_configs:
        - targets:
            - localhost:8888
    ```
3. Optionally, add a panel in grafana. I've included the panel json for the grafana panel I'm using to vis the data: [grafana_panel.json](grafana_panel.json)