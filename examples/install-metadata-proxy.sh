#!/bin/bash
#
# Configure local virtual machine to use proxy to reach the metadata service.
#
# This enables keeping all AWS credentials outside of the virtual machine.
# In this environment, the local virtual machine is trusted to provide the desired Role ARN,
# enabling many local virtual machines to share the same metadata service.
#
# 1. Configure local interface to enable binding to 169.254.169.254
# 2. Configure nginx proxy to forward 169.254.169.254:80 requests to
#    $metadata_host:$metadata_port with additional X-Role-ARN header.
#

metadata_host=$1
metadata_port=$2
role_arn=$3

# Install nginx.
yum install -y nginx

# Configure local interface alias.
cat >/etc/sysconfig/network-scripts/ifcfg-lo:0 <<EOF
NM_CONTROLLED=no
DEVICE=lo  # lo - adds ip address to lo interface, lo:0 - adds alias device
ONBOOT=yes
BOOTPROTO=none
IPADDR=169.254.169.254
NETMASK=255.255.255.255
EOF
ifup lo

# Configure nginx.
cat >/etc/nginx/conf.d/ectou-metadata.conf <<EOF
server {
    listen 169.254.169.254:80;
    server_name ectou_metadata;

    location / {
        proxy_set_header X-Role-ARN ${role_arn};
        proxy_pass http://${metadata_host}:${metadata_port};
    }

    access_log /var/log/nginx/ectou-metadata-access.log;
    error_log /var/log/nginx/ectou-metadata-errors.log;
}
EOF
chkconfig nginx on
service nginx restart
