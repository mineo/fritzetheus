#!/usr/bin/env python
# coding: utf-8
# Copyright © 2018 Wieland Hoffmann
# License: MIT, see LICENSE for details
import prometheus_client

from functools import lru_cache


class Metric:
    def __init__(self, servicetype, method, key=None):
        """Initialize a CounterMetric."""
        self.servicetype = servicetype
        self.method = method
        if key is None:
            key = "New" + method[3:]
        self.key = key

    def _collect(self, device):
        control_url = Metric._getControlURL(device, self.servicetype)
        result = device.execute(control_url, self.servicetype, self.method)
        return result[self.key]

    @staticmethod
    @lru_cache()
    def _getControlURL(device, servicetype):  # noqa: N802
        return device.getControlURL(servicetype)


class GaugeMetric(Metric):
    """Wraps Counters."""

    def __init__(self, name, description, servicetype, method, key=None):
        """Initialize a GaugeMetric."""
        super(GaugeMetric, self).__init__(servicetype, method, key)
        self.name = name
        self.description = description
        self.counter = prometheus_client.Gauge(name, description)

    def boop(self, device):
        value = self._collect(device)
        self.counter.set(value)


# TODO: It should be possible to just generate this from the xml files
METRICS = [
    GaugeMetric("fritzbox_uptime", "Uptime", "urn:dslforum-org:service:DeviceInfo:1", "GetInfo", "NewUpTime"),  # noqa: E501
    GaugeMetric("fritzbox_layer1_upstreammaxbitrate", "", "urn:dslforum-org:service:WANCommonInterfaceConfig:1", "GetCommonLinkProperties", "NewLayer1UpstreamMaxBitRate"),
    GaugeMetric("fritzbox_layer1_downstreammaxbitrate", "", "urn:dslforum-org:service:WANCommonInterfaceConfig:1", "GetCommonLinkProperties", "NewLayer1DownstreamMaxBitRate"),
    GaugeMetric("fritzbox_wan_totalbytessent", "", "urn:dslforum-org:service:WANCommonInterfaceConfig:1", "GetTotalBytesSent"),
    GaugeMetric("fritzbox_wan_totalbytesreceived", "", "urn:dslforum-org:service:WANCommonInterfaceConfig:1", "GetTotalBytesSent"),
    GaugeMetric("fritzbox_wan_totalpacketssent", "", "urn:dslforum-org:service:WANCommonInterfaceConfig:1", "GetTotalPacketsSent"),
    GaugeMetric("fritzbox_wan_totalpacketsreceived", "", "urn:dslforum-org:service:WANCommonInterfaceConfig:1", "GetTotalPacketsReceived"),
    GaugeMetric("fritzbox_wandsl_upstreamcurrrate", "", "urn:dslforum-org:service:WANDSLInterfaceConfig:1", "GetInfo", "NewUpstreamCurrRate"),
    GaugeMetric("fritzbox_wandsl_downstreamcurrrate", "", "urn:dslforum-org:service:WANDSLInterfaceConfig:1", "GetInfo", "NewDownstreamCurrRate"),
]
