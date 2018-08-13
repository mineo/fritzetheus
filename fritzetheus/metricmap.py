#!/usr/bin/env python
# coding: utf-8
# Copyright © 2018 Wieland Hoffmann
# License: MIT, see LICENSE for details
import logging
import prometheus_client
import re

from collections import defaultdict
from functools import lru_cache


__all__ = ('create_metrics_for_device')


class Metric:
    def __init__(self, servicetype, method):
        """Initialize a CounterMetric."""
        self.servicetype = servicetype
        self.method = method

    def _collect(self, device):
        control_url = Metric._getControlURL(device, self.servicetype)
        logging.info(f"Calling {self.servicetype}/{self.method} on {control_url}")
        result = device.execute(control_url, self.servicetype, self.method)
        return result

    @staticmethod
    @lru_cache()
    def _getControlURL(device, servicetype):  # noqa: N802
        return device.getControlURL(servicetype)


class ActionGauge(Metric):
    """Wraps Gauges."""

    def __init__(self, servicetype, method, outparams):
        """Initialize a GaugeMetric."""
        super(ActionGauge, self).__init__(servicetype, method)
        self.gauges = {}
        for outparam in outparams:
            self.gauges[outparam] = prometheus_client.Gauge(
                nicename(outparam), "")

    def boop(self, device):
        value = self._collect(device)
        for key, gauge in self.gauges.items():
            gauge.set(value[key])


blacklist = ["RequestFTPServerWAN"]

good_outparam_types = ["i2", "i4", "ui2", "ui4"]


def nicename(name):
    return "tr64_" + re.sub("\W", "_", name).lower()[3:]


def discover_services(device):
    """
    :param device:
    """
    device.loadDeviceDefinitions("http://fritz.box:49000/tr64desc.xml")
    device.loadSCPD()
    scpd = device.deviceSCPD
    services = {}
    for service, actions in scpd.items():
        action_dump = defaultdict(list)
        for action, parameters in actions.items():
            if action in blacklist:
                continue
            if 'inParameter' in parameters:
                logging.debug(f"Dropping {action} because it has inparams")
                continue
            elif "outParameter" not in parameters:
                logging.debug(f"Dropping {action} because it has no outparams")
                continue
            else:
                for param, desc in (parameters["outParameter"].items()):
                    if desc["dataType"] in good_outparam_types:
                        action_dump[action].append(param)
                        logging.debug(f"{action} looks great!")
        services[service] = action_dump
    return services


def create(services):
    metrics = []
    for service, actions in services.items():
        for action, outparams in actions.items():
            try:
                m = ActionGauge(service, action, outparams)
                metrics.append(m)
            except ValueError:
                # TODO: ValueError: Duplicated timeseries in CollectorRegistry: {'tr64_ftpwanport'}
                pass
    return metrics


def create_metrics_for_device(device):
    services = discover_services(device)
    metrics = create(services)
    return metrics
