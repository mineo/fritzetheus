#!/usr/bin/env python3
# coding: utf-8
# Copyright © 2018 Wieland Hoffmann
# License: MIT, see LICENSE for details
import argparse
import prometheus_client
import simpletr64


from .metricmap import create_metrics_for_device


def build_arg_parser():
    """Build the ArgumentParser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--fritzbox", default="fritz.box")
    parser.add_argument("-u", "--username", default="dslf-config")
    parser.add_argument("-p", "--password", required=True)
    return parser


def connect(hostname, username, password):
    """Connect to the FritzBox.

    :param hostname:
    :param username:
    :param password:
    :rtype: simpletr64.System
    """
    device = simpletr64.System(hostname)
    device.setupTR64Device("fritz.box")
    device.username = username
    device.password = password
    return device


def main():
    """Main."""
    parser = build_arg_parser()
    args = parser.parse_args()
    connect(args.fritzbox, args.username, args.password)
    device = connect(args.fritzbox, args.username, args.password)
    prometheus_client.start_http_server(8000)
    metrics = create_metrics_for_device(device)
    while True:
        for metric in metrics:
            metric.boop(device)
        import time
        time.sleep(2)


if __name__ == "__main__":
    main()
