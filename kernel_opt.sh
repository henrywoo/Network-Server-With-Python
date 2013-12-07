#!/bin/bash

#WARNING! The default value of rmem_max and wmem_max is about 128 KB in most Linux distributions, which may be enough for a low-latency general purpose network environment or for apps such as DNS / Web server. However, if the latency is large, the default size might be too small. Please note that the following settings going to increase memory usage on your server.
echo 'net.core.wmem_max=12582912' >> /etc/sysctl.conf
echo 'net.core.rmem_max=12582912' >> /etc/sysctl.conf
#
#You also need to set minimum size, initial size, and maximum size in bytes:
#
echo 'net.ipv4.tcp_rmem= 10240 87380 12582912' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem= 10240 87380 12582912' >> /etc/sysctl.conf
#
#Turn on window scaling which can be an option to enlarge the transfer window:
#
echo 'net.ipv4.tcp_window_scaling = 1' >> /etc/sysctl.conf
#
#Enable timestamps as defined in RFC1323:
#
echo 'net.ipv4.tcp_timestamps = 1' >> /etc/sysctl.conf
#
#Enable select acknowledgments:
#
echo 'net.ipv4.tcp_sack = 1' >> /etc/sysctl.conf
#
#By default, TCP saves various connection metrics in the route cache when the connection closes, so that connections established in the near future can use these to set initial conditions. Usually, this increases overall performance, but may sometimes cause performance degradation. If set, TCP will not cache metrics on closing connections.
#
echo 'net.ipv4.tcp_no_metrics_save = 1' >> /etc/sysctl.conf
#
#Set maximum number of packets, queued on the INPUT side, when the interface receives packets faster than kernel can process them.
#
echo 'net.core.netdev_max_backlog = 5000' >> /etc/sysctl.conf


sysctl -p
