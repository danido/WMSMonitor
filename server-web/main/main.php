<?php

/*
$GLOBALS['sessionid'] = @$_COOKIE['sessionid'];
	if(!$GLOBALS['sessionid'])
        {
		setcookie("query", $_SERVER['QUERY_STRING']);
                Header('Location: login.php');
        }
*/

$selectedId = array("WMS_view","Overview_wms");
include "../common/header.inc";
$scope = isset($_GET['scope']) ? $_GET['scope'] : 'all';

$service_usage = isset($_GET['service_usage']) ? $_GET['service_usage'] : 'all';
$vo_group = isset($_GET['vo_group']) ? $_GET['vo_group'] : 'all';
$host_owner = isset($_GET['host_owner']) ? $_GET['host_owner'] : 'all';
$lb_owner = isset($_GET['lb_owner']) ? $_GET['lb_owner'] : 'all';

include "../common/banner.inc";
$mainInfos=getMainInfos($scope,$host_owner,$vo_group,$service_usage);
$mainLBInfos=getMainLBInfos($lb_owner);
$serviceUsageList=getServiceUsageList($scope);
$voGroupList=getVOGroupList($scope);
$hostOwnerList=getHostOwnerList($scope);
$lbOwnerList=getLBOwnerList();
$staticVOList=getStaticVOList();
?>

<div class="breadcrumb">
WMSMonitor >> WMS view >> Overview::<?php echo $scope; ?> 
</div>

<div class="breadcrumb">
Select WMS running at: 
<?php
echo "<form class=\"inline\" action=\"main.php\" method=\"get\" name=\"mainForm\">";

echo "<select name=\"host_owner\">";
echo "<option value=\"all\" ";
if ($host_owner == 'all') {echo "selected=selected";}
echo ">everywhere</option>";
foreach ($hostOwnerList as $value) {
        echo "<option value=\"".$value."\" ";
        if ($host_owner == $value) {echo "selected=selected";}
        echo ">".$value."</option>";
}
echo "</select>";


echo "<span> for VO: </span>";
echo "<select id=\"instance_scope\" name=\"scope\" onchange=\"this.form.submit();\">";
echo "<option value=\"all\" ";
if ($scope == 'all') {echo "selected=selected";}
echo ">all</option>";
foreach ($staticVOList as $value) {
        if ($value != 'multiVO') {
                echo "<option value=\"".$value."\" ";
                if ($scope == $value) {echo "selected=selected";}
                echo ">".$value."</option>";
        } else {
                $is_there_multi=1;
        }
}
if ($is_there_multi == 1){
echo "<option value=\"multi\" ";
if ($scope == 'multi') {echo "selected=selected";}
echo ">multiVO</option>";
}
echo "</select>";

echo "<span> Service usage: </span>"; 
echo "<select name=\"service_usage\">";
echo "<option value=\"all\" ";
if ($service_usage == 'all') {echo "selected=selected";}
echo ">all</option>";
foreach ($serviceUsageList as $value) {
        echo "<option value=\"".$value."\" ";
        if ($service_usage == $value) {echo "selected=selected";}
        echo ">".$value."</option>";
}
echo "</select>";

echo "<span> VO group: </span>";
echo "<select name=\"vo_group\">";
echo "<option value=\"all\" ";
if ($vo_group == 'all') {echo "selected=selected";}
echo ">all</option>";
foreach ($voGroupList as $value) {
        echo "<option value=\"".$value."\" ";
        if ($vo_group == $value) {echo "selected=selected";}
        echo ">".$value."</option>";
}
echo "</select>";

echo "<span> and LB running at: </span>";
echo "<select name=\"lb_owner\">";
echo "<option value=\"all\" ";
if ($lb_owner == 'all') {echo "selected=selected";}
echo ">everywhere</option>";
foreach ($lbOwnerList as $value) {
        echo "<option value=\"".$value."\" ";
        if ($lb_owner == $value) {echo "selected=selected";}
        echo ">".$value."</option>";
}
echo "</select>";

echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
?>
</div>

<div class="cont">
<span id="cont_wms">


<table id="main_wms">
<div id="expand_wms" onclick="visibleColumns('wms')">Expand wms summary</div>
<tr class="title">
<td class="wms_column" title="WMS hostname">WMS</td>
<td title="Date of the last report">DATE</td>
<td title="VO to which the WMS is dedicated (multi stands for multi-VO WMS)">VO</td>
<td title="Number of jobs in 'Running' state in the condor queue">RUNNING</td>
<td title="Number of jobs in 'Idle' statein the condor queue">IDLE</td>
<td class="hide_show_wms" title="Number of entries in file /var/glite/workload_manager/input.fl (Workload Manager)">WM QUEUE</td>
<td class="hide_show_wms" title="Number of entries in file /var/glite/jobcontrol/queue.fl (Job controler)">JC QUEUE</td>
<td class="hide_show_wms" title="Number of VO Views entries in the Information Super Market">VO VIEWS</td>
<td class="hide_show_wms" title="Number of dg20logd_* files in directory /var/glite/log (Events not yet transferred to the LB server)">LB QUEUE</td>
<td class="hide_show_wms" title="Average load of the machine during the past 15 minutes">CPU LOAD</td>
<td class="hide_show_wms" title="Occupancy (in %) of directory /var/glite/SandboxDir">SANDBOX PART.</td>
<td title="H/W and some WMS parameters status: green if everything is ok">GENERAL</td>
<td title="Status of daemons: green if everything is ok">DAEMONS</td>
</tr>
<?php
for ($i=0; $i<sizeof($mainInfos); $i++) {

$date1 = $mainInfos[$i]["measure_time"];
$unix_now = mktime(intval(substr($date1, 11, 2)), intval(substr($date1, 14, 2)), intval(substr($date1, 17, 2)), intval(substr($date1, 5, 2)), intval(substr($date1, 8, 2)), intval(substr($date1, 0, 4)));

$row_color = (($i % 2) == 0) ? 'row2' : 'row1' ; 

if (isset($mainInfos[$i]["daemon_wm"]) && isset($mainInfos[$i]["daemon_wmp"]) && isset($mainInfos[$i]["daemon_jc"]) && isset($mainInfos[$i]["daemon_px"]) && isset($mainInfos[$i]["daemon_lm"]) && isset($mainInfos[$i]["daemon_ll"]) && isset($mainInfos[$i]["daemon_lbpx"]) && isset($mainInfos[$i]["daemon_ftpd"]) && isset($mainInfos[$i]["daemon_ntpd"]) && isset($mainInfos[$i]["daemon_ice"]) && isset($mainInfos[$i]["daemon_bdii"])) {
	if ($mainInfos[$i]["daemon_wm"]==0 && $mainInfos[$i]["daemon_wmp"]==0 && $mainInfos[$i]["daemon_jc"]==0 && $mainInfos[$i]["daemon_px"]==0 && $mainInfos[$i]["daemon_lm"]==0 && $mainInfos[$i]["daemon_ll"]==0 && $mainInfos[$i]["daemon_lbpx"]==0 && $mainInfos[$i]["daemon_ftpd"]==0 && $mainLBInfos[$i]["daemon_ntpd"]==0 && $mainInfos[$i]["daemon_ice"]==0 && $mainInfos[$i]["daemon_bdii"]==0) {
		$daemon_icon = 'check16.png';
		$daemon_title = 'All daemons ok';
	} else {
		$daemon_icon = 'error16.png';
		$daemon_title = 'At least 1 daemon stopped';
	}
} else if ($mainInfos[$i]["daemon_wm"]!=0 || $mainInfos[$i]["daemon_wmp"]!=0 || $mainInfos[$i]["daemon_jc"]!=0 || $mainInfos[$i]["daemon_px"]!=0 || $mainInfos[$i]["daemon_lm"]!=0 || $mainInfos[$i]["daemon_ll"]!=0 || $mainInfos[$i]["daemon_lbpx"]!=0 || $mainInfos[$i]["daemon_ftpd"]!=0 || $mainLBInfos[$i]["daemon_ntpd"]!=0 || $mainInfos[$i]["daemon_ice"]!=0 || $mainInfos[$i]["daemon_bdii"]!=0)  { 
	$daemon_icon = 'error16.png';
        $daemon_title = 'At least 1 daemon stopped';
} else {
	$daemon_icon = 'documenterror16.png';
        $daemon_title = 'No data about at least 1 daemon';
}

if ($mainInfos[$i]["loadb_fdrain"] == -1) {
        $status_icon = 'server_forbidden.png';
        $status_title = 'WMS instance in drain status';
} else if ($mainInfos[$i]["loadb_fmetric"] < 0) {
	$status_icon = 'forbidden.png';
        $status_title = 'Not usable WMS instance';
} else if ($mainInfos[$i]["cpu_load"]>=20  || $mainInfos[$i]["wm_queue"]>=500 || $mainInfos[$i]["jc_queue"]>=500 || $mainInfos[$i]["lb_event"]>=1000 || $mainInfos[$i]["fd_wm"]>=900 || $mainInfos[$i]["fd_lm"]>=900 || $mainInfos[$i]["fd_jc"]>=900 || $mainInfos[$i]["fd_ll"]>=900 || $mainInfos[$i]["disk_sandbox"]>=90 || $mainInfos[$i]["disk_tmp"]>=90 || (time() - $unix_now) >= 3600 || $mainInfos[$i]["disk_varlog"]>=90 || $mainInfos[$i]["disk_varlibmysql"]>=90 || $mainInfos[$i]["loadb_fmetric"] >= 2 || $mainInfos[$i]["loadb_fmetric"] < 0) {
        $status_icon = 'error16.png';
        $status_title = 'At least 1 service in alarm';
} else if (($mainInfos[$i]["cpu_load"]>10 && $mainInfos[$i]["cpu_load"]<20)  || ($mainInfos[$i]["wm_queue"]>250 && $mainInfos[$i]["wm_queue"]<500) || ($mainInfos[$i]["jc_queue"]>250 && $mainInfos[$i]["jc_queue"]<500) || ($mainInfos[$i]["lb_event"]>500 && $mainInfos[$i]["lb_event"]<1000) || ($mainInfos[$i]["fd_wm"]>700 && $mainInfos[$i]["fd_wm"]<900) || ($mainInfos[$i]["fd_lm"]>700 && $mainInfos[$i]["fd_lm"]<900) || ($mainInfos[$i]["fd_jc"]>700 && $mainInfos[$i]["fd_jc"]<900) || ($mainInfos[$i]["fd_ll"]>700 && $mainInfos[$i]["fd_ll"]<900) || ($mainInfos[$i]["disk_sandbox"]>80 && $mainInfos[$i]["disk_sandbox"]<90) || ($mainInfos[$i]["disk_tmp"]>80 && $mainInfos[$i]["disk_tmp"]<90) || ((time() - $unix_now) < 3600 && (time() - $unix_now) > 1800) || ($mainInfos[$i]["disk_varlog"]>80 && $mainInfos[$i]["disk_varlog"]<90) || ($mainInfos[$i]["disk_varlibmysql"]>80 && $mainInfos[$i]["disk_varlibmysql"]<90) || $mainInfos[$i]["loadb_fmetric"] >= 1) {
        $status_icon = 'warning16.png';
        $status_title = 'At least 1 service in warning';
} else {
        $status_icon = 'check16.png';
        $status_title = 'Everything ok';
}

$field = array();
$td_string = array();

foreach ($mainInfos[$i] as $key => $value) {
$field[$key] = $mainInfos[$i][$key] == '' ? 'N/A' : $mainInfos[$i][$key];
$td_string[$key] = $mainInfos[$i][$key] == '' ? "<td class=\"not_available hide_show_wms\" title=\"Not Available\">".$field[$key] : "<td class=\"hide_show_wms\">".$field[$key];
}

$td_string["condor_running"]=$mainInfos[$i][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$mainInfos[$i]['condor_running'] : "<td>".$mainInfos[$i]['condor_running'];
$td_string["condor_idle"]=$mainInfos[$i][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$mainInfos[$i]['condor_idle'] : "<td>".$mainInfos[$i]['condor_idle'];

echo "<tr class=\"".$row_color."\">";
	echo "<td class=\"wms_column\" title=\"Click for more details on ".$mainInfos[$i]["hostname"]."\"><a href=\"../details/details.php?wms=".$mainInfos[$i]["hostname"]."\">".$mainInfos[$i]["hostname"]."</a></td>";
	echo "<td>".substr($mainInfos[$i]["measure_time"], 0, -3)."</td>";
	echo "<td>".$mainInfos[$i]["vo"]."</td>";
	echo $td_string["condor_running"]."</td>";
	echo $td_string["condor_idle"]."</td>";
        echo $td_string["wm_queue"]."</td>";
        echo $td_string["jc_queue"]."</td>";
	echo $td_string["ism_entries"]."</td>";
	echo $td_string["lb_event"]."</td>";
	echo $td_string["cpu_load"]."</td>";
	echo $td_string["disk_sandbox"]."</td>";
	echo "<td class=\"icon\"><a href=\"../details/details.php?wms=".$mainInfos[$i]["hostname"]."\"><img src=\"../common/icon/".$status_icon."\" title=\"".$status_title." - Click for details\"></img></a></td>";
	echo "<td class=\"icon\"><a href=\"../details/details.php?wms=".$mainInfos[$i]["hostname"]."\"><img src=\"../common/icon/".$daemon_icon."\" title=\"".$daemon_title." - Click for details\"></img></a></td>";
echo "</tr>";
}
?>
</table>

</span>




<span id="cont_lb">
<table id="main_lb">
<div id="expand_lb" onclick="visibleColumns('lb')">Expand lb summary</div>
<tr class="title">
<td class="wms_column" title="LB hostname">LB</td>
<td title="Date of the last report">DATE</td>
<td class="hide_show_lb" title="Average load of the machine during the past 15 minutes">CPU LOAD</td>
<td class="hide_show_lb" title="Number of jobs in 'Running' state in the condor queue">DISK LB</td>
<td class="hide_show_lb" title="Number of jobs in 'Idle' statein the condor queue">VARLIBMYSQL</td>
<td class="hide_show_lb" title="Number of entries in file /var/glite/workload_manager/input.fl (Workload Manager)">LB CON</td>
<td class="hide_show_lb" title="Current status of LB daemon">LB DAEMON</td>
<td class="hide_show_lb" title="Current status of LL daemon">LL DAEMON</td>
<td class="hide_show_lb" title="Current status of NTPD daemon">NTPD DAEMON</td>
<td title="H/W and some WMS parameters status: green if everything is ok">GENERAL</td>
<td title="Status of daemons: green if everything is ok">DAEMONS</td>
</tr>
<?php
for ($i=0; $i<sizeof($mainLBInfos); $i++) {

$date1 = $mainLBInfos[$i]["measure_time"];
$unix_now = mktime(intval(substr($date1, 11, 2)), intval(substr($date1, 14, 2)), intval(substr($date1, 17, 2)), intval(substr($date1, 5, 2)), intval(substr($date1, 8, 2)), intval(substr($date1, 0, 4)));

$row_color = (($i % 2) == 0) ? 'row2' : 'row1' ;

if (isset($mainLBInfos[$i]["daemon_lb"]) && isset($mainLBInfos[$i]["daemon_ll"]) && isset($mainLBInfos[$i]["daemon_NTPD"])) {
        if ($mainLBInfos[$i]["daemon_lb"]==0 && $mainLBInfos[$i]["daemon_ll"]==0 && $mainLBInfos[$i]["daemon_NTPD"]==0) {
                $daemon_icon = 'check16.png';
                $daemon_title = 'All daemons ok';
        } else {
                $daemon_icon = 'error16.png';
                $daemon_title = 'At least 1 daemon stopped';
        }
} else if ($mainLBInfos[$i]["daemon_lb"]!=0 || $mainLBInfos[$i]["daemon_ll"]!=0 || $mainLBInfos[$i]["daemon_NTPD"]!=0)  {
        $daemon_icon = 'error16.png';
        $daemon_title = 'At least 1 daemon stopped';
} else {
        $daemon_icon = 'documenterror16.png';
        $daemon_title = 'No data about at least 1 daemon';
}

if ($mainLBInfos[$i]["cpu_load"]>=20 || $mainLBInfos[$i]["disk_lb"]>=90 || $mainLBInfos[$i]["lb_con"]>100 || (time() - $unix_now) >= 3600 || $mainLBInfos[$i]["disk_varlibmysql"]>=90) {
        $status_icon = 'error16.png';
        $status_title = 'At least 1 service in alarm or measure time older than 1 hour ago';
} else if (($mainLBInfos[$i]["cpu_load"]>10 && $mainLBInfos[$i]["cpu_load"]<20) || ($mainLBInfos[$i]["disk_lb"]>80 && $mainLBInfos[$i]["disk_lb"]<90) || ($mainLBInfos[$i]["lb_con"]>80 && $mainLBInfos[$i]["lb_con"]<=100) || ((time() - $unix_now) < 3600 && (time() - $unix_now) > 1800) || ($mainLBInfos[$i]["varlibmysql"]>80 && $mainLBInfos[$i]["varlibmysql"]<90)) {
        $status_icon = 'warning16.png';
        $status_title = 'At least 1 service in warning or measure time older than 30 mins ago';
} else {
        $status_icon = 'check16.png';
        $status_title = 'Everything ok';
}

$field = array();
$td_string = array();

foreach ($mainLBInfos[$i] as $key => $value) {
$field[$key] = $mainLBInfos[$i][$key] == '' ? 'N/A' : $mainLBInfos[$i][$key];
$td_string[$key] = $mainLBInfos[$i][$key] == '' ? "<td class=\"not_available hide_show_wms\" title=\"Not Available\">".$field[$key] : "<td class=\"hide_show_lb\">".$field[$key];
}

echo "<tr class=\"".$row_color."\">";
//      echo "<td class=\"lb_column\" title=\"Click for more details on ".$mainInfos[$i]["hostname"]."\"><a href=\"../details/details.php?wms=".$mainInfos[$i]["hostname"]."\">".$mainInfos[$i]["hostname"]."</a></td>";
        echo "<td class=\"wms_column\">".$mainLBInfos[$i]["hostname"]."</td>";
        echo "<td>".substr($mainLBInfos[$i]["measure_time"], 0, -3)."</td>";
        echo $td_string["cpu_load"]."</td>";
        echo $td_string["disk_lb"]."</td>";
        echo $td_string["disk_varlibmysql"]."</td>";
        echo $td_string["lb_con"]."</td>";
	echo $td_string["daemon_lb"]."</td>";
	echo $td_string["daemon_ll"]."</td>";
	echo $td_string["daemon_NTPD"]."</td>";
//        echo "<td class=\"icon\"><a href=\"../details/details.php?wms=".$mainLBInfos[$i]["hostname"]."\"><img src=\"../common/icon/".$status_icon."\" title=\"".$status_title." - Click for details\"></img></a></td>";
//        echo "<td class=\"icon\"><a href=\"../details/details.php?wms=".$mainLBInfos[$i]["hostname"]."\"><img src=\"../common/icon/".$daemon_icon."\" title=\"".$daemon_title." - Click for details\"></img></a></td>";
	echo "<td class=\"icon\"><img src=\"../common/icon/".$status_icon."\" title=\"".$status_title."\"></img></td>";
        echo "<td class=\"icon\"><img src=\"../common/icon/".$daemon_icon."\" title=\"".$daemon_title."\"></img></td>";
echo "</tr>";
}
?>
</span>
</div>

	</body>
</html>

