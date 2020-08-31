import time

import upnpclient
from prometheus_client import start_http_server, Gauge

PROM_HTTP_PORT = 8888

router_connection_uptime = Gauge('router_connection_uptime', '')
router_connection_status = Gauge('router_connection_status', '')
router_bytes_sent = Gauge('router_bytes_sent', '')
router_bytes_received = Gauge('router_bytes_received', '')
router_packets_sent = Gauge('router_packets_sent', '')
router_packets_received = Gauge('router_packets_received', '')

def main():
    router = None
    while router == None:
        print("upnp discover looking for router")
        devices = upnpclient.discover()
        print(devices)
        for device in devices:
            print(device)
            print(device.model_name)
            if device.model_name == 'rt4230w-d187 router':
                router = device
                print("upnp router found")
                break
        print("upnp router not found, retrying")
    print("starting prom metrics http server on port %s", PROM_HTTP_PORT)
    start_http_server(PROM_HTTP_PORT)

    print("main metrics collection loop")
    while True:
        time.sleep(1)
        conn_status = router.WANIPConn1.GetStatusInfo()
        router_connection_uptime.set(conn_status.get('NewUptime', -1))
        if conn_status.get('NewConnectionStatus', '') == 'Connected':
            router_connection_status.set(1)
        else:
            router_connection_status.set(0)
        router_bytes_sent.set(router.WANCommonIFC1.GetTotalBytesSent().get('NewTotalBytesSent', -1))
        router_bytes_received.set(router.WANCommonIFC1.GetTotalBytesReceived().get('NewTotalBytesReceived', -1))
        router_packets_sent.set(router.WANCommonIFC1.GetTotalPacketsSent().get('NewTotalPacketsSent', -1))
        router_packets_received.set(router.WANCommonIFC1.GetTotalPacketsReceived().get('NewTotalPacketsReceived', -1))

if __name__ == '__main__':
    main()
