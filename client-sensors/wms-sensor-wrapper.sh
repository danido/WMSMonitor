#!/bin/bash
source /etc/profile.d/grid-env.sh
cd /opt/WMSMonitor/sensors/bin/;
python wms-sensor-wrapper.py >> /var/log/WMSMonitor_sensor.log 2>&1

