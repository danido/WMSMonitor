#!/bin/bash
cd /opt/WMSMonitor/sensors/bin/; 
python lb-sensor-wrapper.py >> /var/log/WMSMonitor_sensor.log 2>&1

