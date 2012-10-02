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


include "../common/banner.inc";
//$mainInfos=getMainInfos($scope);
$mainInfos=getMainLBInfos();
?>

<div class="breadcrumb">
WMSMonitor>> LB view >> Overview 
</div>

<table class="main">
<tr class="title">
<td class="wms_column" title="LB hostname">LB</td>
<td title="Date of the last report">DATE</td>
<td title="Average load of the machine during the past 15 minutes">CPU LOAD</td>
<td title="Number of jobs in 'Running' state in the condor queue">DISK LB</td>
<td title="Number of jobs in 'Idle' statein the condor queue">VARLIBMYSQL</td>
<td title="Number of entries in file /var/glite/workload_manager/input.fl (Workload Manager)">LB CON</td>
<td title="H/W and some WMS parameters status: green if everything is ok">GENERAL STATUS</td>
<td title="Status of daemons: green if everything is ok">DAEMONS STATUS</td>
</tr>
<?php
for ($i=0; $i<sizeof($mainInfos); $i++) {

$date1 = $mainInfos[$i]["date"];
$unix_now = mktime(intval(substr($date1, 11, 2)), intval(substr($date1, 14, 2)), intval(substr($date1, 17, 2)), intval(substr($date1, 5, 2)), intval(substr($date1, 8, 2)), intval(substr($date1, 0, 4)));

$row_color = (($i % 2) == 0) ? 'row2' : 'row1' ; 

if (isset($mainInfos[$i]["daemon_lb"]) && isset($mainInfos[$i]["daemon_ll"]) && isset($mainInfos[$i]["daemon_NTPD"])) {
	if ($mainInfos[$i]["daemon_lb"]==0 && $mainInfos[$i]["daemon_ll"]==0 && $mainInfos[$i]["daemon_NTPD"]==0) {
		$daemon_icon = 'check16.png';
		$daemon_title = 'All daemons ok';
	} else {
		$daemon_icon = 'error16.png';
		$daemon_title = 'At least 1 daemon stopped';
	}
} else if ($mainInfos[$i]["daemon_lb"]!=0 || $mainInfos[$i]["daemon_ll"]!=0 || $mainInfos[$i]["daemon_NTPD"]!=0)  { 
	$daemon_icon = 'error16.png';
        $daemon_title = 'At least 1 daemon stopped';
} else {
	$daemon_icon = 'documenterror16.png';
        $daemon_title = 'No data about at least 1 daemon';
}

if ($mainInfos[$i]["fmetric"] < 0) {
	$status_icon = 'forbidden.png';
        $status_title = 'Not usable WMS instance';
} else if ($mainInfos[$i]["load"]>=20  || $mainInfos[$i]["input_fl"]>=500 || $mainInfos[$i]["queue_fl"]>=500 || $mainInfos[$i]["dg20"]>=1000 || $mainInfos[$i]["FD_WM"]>=900 || $mainInfos[$i]["FD_LM"]>=900 || $mainInfos[$i]["FD_JC"]>=900 || $mainInfos[$i]["FD_LL"]>=900 || $mainInfos[$i]["sandbox"]>=90 || $mainInfos[$i]["tmp"]>=90 || $mainLBInfos[$i]["lb_disk"]>=90 || $mainLBInfos[$i]["load"]>=20 || $mainLBInfos[$i]["LB_CON"]>=30 || (time() - $unix_now) >= 3600 || $mainInfos[$i]["varlog"]>=90 || $mainInfos[$i]["varlibmysql"]>=90 || $mainInfos[$i]["fmetric"] >= 2 || $mainInfos[$i]["fmetric"] < 0) {
        $status_icon = 'error16.png';
        $status_title = 'At least 1 service in alarm';
} else if (($mainInfos[$i]["load"]>10 && $mainInfos[$i]["load"]<20)  || ($mainInfos[$i]["input_fl"]>250 && $mainInfos[$i]["input_fl"]<500) || ($mainInfos[$i]["queue_fl"]>250 && $mainInfos[$i]["queue_fl"]<500) || ($mainInfos[$i]["dg20"]>500 && $mainInfos[$i]["dg20"]<1000) || ($mainInfos[$i]["FD_WM"]>700 && $mainInfos[$i]["FD_WM"]<900) || ($mainInfos[$i]["FD_LM"]>700 && $mainInfos[$i]["FD_LM"]<900) || ($mainInfos[$i]["FD_JC"]>700 && $mainInfos[$i]["FD_JC"]<900) || ($mainInfos[$i]["FD_LL"]>700 && $mainInfos[$i]["FD_LL"]<900) || ($mainInfos[$i]["sandbox"]>80 && $mainInfos[$i]["sandbox"]<90) || ($mainInfos[$i]["tmp"]>80 && $mainInfos[$i]["tmp"]<90) || ($mainLBInfos[$i]["lb_disk"]>80 && $mainLBInfos[$i]["lb_disk"]<90) || ($mainLBInfos[$i]["load"]>10 && $mainLBInfos[$i]["load"]<20) || ($mainLBInfos[$i]["LB_CON"]>20 && $mainLBInfos[$i]["LB_CON"]<30) || ((time() - $unix_now) < 3600 && (time() - $unix_now) > 1800) || ($mainInfos[$i]["varlog"]>80 && $mainInfos[$i]["varlog"]<90) || ($mainInfos[$i]["varlibmysql"]>80 && $mainInfos[$i]["varlibmysql"]<90) || $mainInfos[$i]["fmetric"] >= 1) {
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
$td_string[$key] = $mainInfos[$i][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$field[$key] : "<td>".$field[$key];
}

echo "<tr class=\"".$row_color."\">";
//	echo "<td class=\"lb_column\" title=\"Click for more details on ".$mainInfos[$i]["hostname"]."\"><a href=\"../details/details.php?wms=".$mainInfos[$i]["hostname"]."\">".$mainInfos[$i]["hostname"]."</a></td>";
	echo $td_string["hostname"]."</td>";
	echo $td_string["measure_time"]."</td>";
	echo $td_string["cpu_load"]."</td>";
	echo $td_string["disk_lb"]."</td>";
	echo $td_string["disk_varlibmysql"]."</td>";
        echo $td_string["lb_con"]."</td>";
	echo "<td class=\"icon\"><a href=\"../details/details.php?wms=".$mainInfos[$i]["hostname"]."\"><img src=\"../common/icon/".$status_icon."\" title=\"".$status_title." - Click for details\"></img></a></td>";
	echo "<td class=\"icon\"><a href=\"../details/details.php?wms=".$mainInfos[$i]["hostname"]."\"><img src=\"../common/icon/".$daemon_icon."\" title=\"".$daemon_title." - Click for details\"></img></a></td>";
echo "</tr>";
}
?>
</table>

	</body>
</html>

