1- WMSMonitor SERVER package content:

Starting from root directory /opt/WMSMonitor/ you find the following content in the package

/opt/WMSMonitor/
.
|-- README-WMSMonitor-Server-01032012.txt
|-- collector
|   `-- bin
|       |-- CE_MM_collector.py
|       |-- CEclass.py
|       |-- __init__.py
|       |-- activemq_consumer_daemon.py
|       |-- activemq_consumer_daemon1.py
|       |-- activemq_consumer_wmsnagiostest.py
|       |-- cli.py
|       |-- collector_lb_class.py
|       |-- collector_wms_class.py
|       |-- create_daily.py
|       |-- daemon_class.py
|       |-- data_collector.py
|       |-- data_collector_daemon.py
|       |-- data_collector_main_autoup.py
|       |-- data_lb_refill_main.py
|       |-- data_sensor_trigger.py
|       |-- exception.py
|       |-- get_LB_CE_stats_func.py
|       |-- get_LB_userstats_func.py
|       |-- get_WMS_usermap_func.py
|       |-- get_result_CEMM_func.py
|       |-- get_result_LB_func.py
|       |-- get_result_WMS_func.py
|       |-- headers_class.py
|       |-- istance_class.py
|       |-- lb_autoupdater_func.py
|       |-- lb_class.py
|       |-- lbclass.py
|       |-- listen_and_dump.py
|       |-- listener.py
|       |-- logpredef.py
|       |-- long_file_collector_func.py
|       |-- map_users_func.py
|       |-- node_class.py
|       |-- old_file_garbage_coll.py
|       |-- old_vo_stats_recovery.py
|       |-- query_to_insert_CE_func.py
|       |-- query_to_insert_user_func.py
|       |-- readconf_func.py
|       |-- snmp_collector_module_func.py
|       |-- stomp.py
|       |-- update_CE_stats_table_func.py
|       |-- update_CE_stats_tmp_func.py
|       |-- update_user_stats_table_func.py
|       |-- update_user_tmp_func.py
|       |-- user_class.py
|       |-- usermap_class.py
|       |-- utils.py
|       |-- wms_class.py
|       |-- wmsdata_class.py
|       `-- wmsmonitor_server.py
|-- common
|   |-- classes
|   |   |-- daemon_class.py
|   |   |-- istance_class.py
|   |   |-- lb_class.py
|   |   |-- node_class.py
|   |   |-- user_class.py
|   |   |-- usermap_class.py
|   |   |-- wms_class.py
|   |   `-- wmsdata_class.py
|   |-- readconf_func.py
|   |-- wmsmon_default.conf
|   `-- wmsmon_site-info.def
|-- deployment
|   |-- WMSMonitor.cron
|   |-- WMSMonitor_logrotate.conf
|   |-- WMSMonitor_logrotate.cron
|   `-- wmsmon3.0_dumpfile.sql
|-- loadbalancing
|   |-- host_usagetest_consumer.py
|   |-- plot_wmslist_inALIAS.py
|   `-- wms_balancing_arbiter.py
|-- msgold
|-- msgtmp
