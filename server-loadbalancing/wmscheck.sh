#!/bin/bash
mysql -u root -pcnaftuttobene nagios -e "SELECT last_check,current_state,check_command_args FROM nagios_services,nagios_servicestatus WHERE display_name like '%WMProxy-Run%' and nagios_services.service_object_id=nagios_servicestatus.service_object_id;" > /var/www/html/wmschecks.txt
