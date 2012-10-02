<?php
require_once "../common/functions.php";
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
        <head>
                <title>WMSmon Main Page</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <link href="../common/css/style.css" rel="stylesheet" type="text/css" media="screen"/>

        </head>
        <body>
<table class="details">
<tr class="title">
<?php
$detailsWMSData=getDetailsWMSData($_GET['wms']);
$detailsLBData=getDetailsLBData($_GET['wms']);
$detailsLBDailyData=getDetailsLBDailyData($_GET['wms']);
$status_icon = $detailsWMSData[0]["WMP"] == 0 ? 'check16.png' : 'error16.png';

echo "<td colspan=\"2\">WM Proxy <img src=\"../common/icon/".$status_icon."\" title=\"WMP daemon = ".$detailsWMSData[0]["WMP"]."\"></img></td>";
//echo "</tr><tr>";
//echo "<td>WMP daemon</td><td>".$detailsWMSData[0]["WMP"]."</td>";
echo "</tr><tr>";
echo "<td>PX daemon</td><td>".$detailsWMSData[0]["PX"]."</td>";
echo "</tr><tr title=\"Number of jobs submitted to WMProxy server in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs submitted</td><td>".$detailsLBData[0]["WMP_in"]."</td>";
echo "</tr><tr title=\"Number of job collections  submitted to WMProxy server in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Collections submitted</td><td>".$detailsLBData[0]["WMP_in_col"]."</td>";
echo "</tr><tr title=\"Average number of nodes in job collections submitted to WMProxy server in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Mean nodes per collection</td><td>".$detailsLBData[0]["WMP_in_col_avg"]."</td>";
echo "</tr><tr title=\"Standard Deviation of number of nodes in job collections submitted to WMProxy server in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Std nodes per collection</td><td>".$detailsLBData[0]["WMP_in_col_std"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
$status_icon = $detailsWMSData[0]["WM"] == 0 ? 'check16.png' : 'error16.png';

echo "<td colspan=\"2\">Workload Manager <img src=\"../common/icon/".$status_icon."\" title=\"WM daemon = ".$detailsWMSData[0]["WM"]."\"></img></td>";
echo "</tr><tr title=\"Number of file descriptors opened by process Workload Manager\">";
echo "<td>WM file descriptors</td><td>".$detailsWMSData[0]["FD_WM"]."</td>";
echo "</tr><tr title=\"Number of entries in file /var/edgwl/workload_manager/input.fl (Workload Manager)\">";
echo "<td>WM queue</td><td>".$detailsWMSData[0]["input_fl"]."</td>";
//echo "</tr><tr>";
//echo "<td>WM daemon</td><td>".$detailsWMSData[0]["WM"]."</td>";
echo "</tr><tr title=\"Number of jobs enqueued to WorkLoad Manager in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs -> WM</td><td>".$detailsLBData[0]["WM_in"]."</td>";
echo "</tr><tr title=\"Number of jobs enqueued after Resubmission to WorkLoad Manager in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs Resub -> WM</td><td>".$detailsLBData[0]["WM_in_res"]."</td>";
echo "</tr><tr title=\"Number of VO Views entries in the Information Super Market\">";
echo "<td>VO Views</td><td>".$detailsWMSData[0]["ism_entries"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
$status_icon = $detailsWMSData[0]["LM"] == 0 ? 'check16.png' : 'error16.png';

echo "<td colspan=\"2\">Log Monitor <img src=\"../common/icon/".$status_icon."\" title=\"LM daemon = ".$detailsWMSData[0]["LM"]."\"></img></td>";
echo "</tr><tr>";
echo "<td>LM file descriptors</td><td>".$detailsWMSData[0]["FD_LM"]."</td>";
//echo "</tr><tr>";
//echo "<td>LM daemon</td><td>".$detailsWMSData[0]["LM"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
$status_icon = $detailsWMSData[0]["JC"] == 0 ? 'check16.png' : 'error16.png';

echo "<td colspan=\"2\">Job Controller <img src=\"../common/icon/".$status_icon."\" title=\"JC daemon = ".$detailsWMSData[0]["JC"]."\"></img></td>";
echo "</tr><tr title=\"Number of entries in file /var/edgwl/jobcontrol/queue.fl (Job Controller)\">";
echo "<td>JC queue</td><td>".$detailsWMSData[0]["queue_fl"]."</td>";
echo "</tr><tr title=\"Number of file descriptors opened by process Job Controller\">";
echo "<td>JC file descriptor</td><td>".$detailsWMSData[0]["FD_JC"]."</td>";
//echo "</tr><tr>";
//echo "<td>JC daemon</td><td>".$detailsWMSData[0]["JC"]."</td>";
echo "</tr><tr title=\"Number of jobs enqueued to Job Controller in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs -> JC</td><td>".$detailsLBData[0]["JC_in"]."</td>";
echo "</tr><tr title=\"Number of jobs processed from Job Controller in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs JC -> CE</td><td>".$detailsLBData[0]["JC_out"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
$status_icon = $detailsWMSData[0]["LL"] == 0 ? 'check16.png' : 'error16.png';

echo "<td colspan=\"2\">Local Logger <img src=\"../common/icon/".$status_icon."\" title=\"LL daemon = ".$detailsWMSData[0]["LL"]."\"></img></td>";
//echo "</tr><tr>";
//echo "<td>LL daemon</td><td>".$detailsWMSData[0]["LL"]."</td>";
echo "</tr><tr title=\"Number of dg20logd_* files in directory /var/tmp (Events not yet transferred to the LB server)\">";
echo "<td>LB events delay</td><td>".$detailsWMSData[0]["dg20"]."</td>";
echo "</tr><tr title=\"Number of file descriptors opened by process Local Logger\">";
echo "<td>LL file descriptor</td><td>".$detailsWMSData[0]["FD_LL"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (($detailsWMSData[0]["LB"] == 0 || $detailsWMSData[0]["LB"] == '') && $detailsWMSData[0]["LBPX"] == 0) {
	$status_icon = 'check16.png';
} else {
	$status_icon = 'error16.png';
}

echo "<td colspan=\"2\">Logging & Bookeeping <img src=\"../common/icon/".$status_icon."\" title=\"LB daemon = ".$detailsWMSData[0]["LB"]." - LBPX daemon = ".$detailsWMSData[0]["LBPX"]."\"></img></td></td>";
//echo "</tr><tr>";
//echo "<td>LB daemon</td><td>".$detailsWMSData[0]["LB"]."</td>";
//echo "</tr><tr>";
//echo "<td>LBPX daemon</td><td>".$detailsWMSData[0]["LBPX"]."</td>";
echo "</tr><tr title=\"LB server hostname\">";
echo "<td>LB server</td><td>".$detailsLBDailyData[0]["lbserver"]."</td>";
?>
</tr>
</table>

<br />
<br />

<table class="details">
<tr class="title">
<?php
echo "<td colspan=\"2\">Job Stats (Condor)</td>";
echo "</tr><tr title=\"Number of jobs in 'Running' state in the condor queue\">";
echo "<td>Running jobs</td><td>".$detailsWMSData[0]["running"]."</td>";
echo "</tr><tr title=\"Number of jobs in 'Idle' state in the condor queue\">";
echo "<td>Idle jobs</td><td>".$detailsWMSData[0]["idle"]."</td>";
echo "</tr><tr title=\"Number of jobs in 'Running', 'Idle' or 'Held' state in the condor queue\">";
echo "<td>Total Condor jobs</td><td>".$detailsWMSData[0]["current"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
echo "<td colspan=\"2\">HW Status</td>";
echo "</tr><tr title=\"Occupancy (in %) of directory /var/glite/SandboxDir\">";
echo "<td>Sandbox partition</td><td>".$detailsWMSData[0]["sandbox"]."</td>";
echo "</tr><tr title=\"Occupancy (in %) of directory /tmp\">";
echo "<td>/tmp partition</td><td>".$detailsWMSData[0]["tmp"]."</td>";
echo "</tr><tr title=\"Average load of the machine during the past 15 minutes\">";
echo "<td>CPU load</td><td>".$detailsWMSData[0]["load"]."</td>";
echo "</tr><tr title=\"Click to see lemon monitoring for ".$_GET['wms']."\">";
echo "<td><a href=\"https://yam-server.cnaf.infn.it/lrf/info.php?host=".$_GET['wms']."\">Lemon monitoring</a></td><td></td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
$status_icon = $detailsWMSData[0]["FTPD"] == 0 ? 'check16.png' : 'error16.png';

echo "<td colspan=\"2\">Tranfers <img src=\"../common/icon/".$status_icon."\" title=\"FTPD daemon = ".$detailsWMSData[0]["FTPD"]."\"></img></td></td>";
echo "</tr><tr title=\"Number of gridftp sessions on WMS\">"; 
echo "<td>gftp</td><td>".$detailsWMSData[0]["gftp"]."</td>";
//echo "</tr><tr>";
//echo "<td>FTPD daemon</td><td>".$detailsWMSData[0]["FTPD"]."</td>";
?>
</tr>
</table>

<br />
<br />
<br />
<br />

<div class="chart">
<?php
include 'php-ofc-library/open_flash_chart_object.php';
$wms = $_GET['wms'];
$interval = isset($_GET['interval']) ? $_GET['interval'] : 'week';
$daily = isset($_GET['daily']) ? $_GET['daily'] : 'week';
echo "<div class=\"chart_left\">";
//open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/details_chart.php?wms='.$wms.'&interval='.$interval, false );
open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/chart_1_test.php?wms='.$wms.'&interval='.$interval, false );
echo "<br /><br />";
/*open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/chart_3.php?wms='.$wms.'&interval='.$interval, false );
echo "<br /><br /><br /><br /><br /><br />";
open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/chart_5.php?wms='.$wms.'&daily='.$daily, false );
echo "<br /><br />";
open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/chart_7.php?wms='.$wms.'&daily='.$daily, false );
echo "</div><br /><br /><div class=\"chart_right\">";
open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/chart_2.php?wms='.$wms.'&interval='.$interval, false );
echo "<br /><br />";
open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/chart_4.php?wms='.$wms.'&interval='.$interval, false );
echo "<br /><br /><br /><br /><br /><br />";
open_flash_chart_object( 400, 250, 'https://'. $_SERVER['SERVER_NAME'] .':8443/wmsmon/details/chart_6.php?wms='.$wms.'&daily='.$daily, false );
*/echo "</div><br /><br /><div class=\"interval\">";
echo "<form action=\"details.php\" method=\"get\" name=\"chartForm\">";
echo "<input type=\"hidden\" name=\"wms\" value=\"".$wms."\"/>";
echo "<input type=\"hidden\" name=\"daily\" value=\"".$daily."\"/>";
echo "<select name=\"interval\">";
echo "<option value=\"day\" ";
if ($interval == 'day') {echo "selected=selected";}
echo ">day</option>";
echo "<option value=\"3days\" ";
if ($interval == '3days') {echo "selected=selected";}
echo ">3 days</option>";
echo "<option value=\"week\" ";
if ($interval == 'week') {echo "selected=selected";}
echo ">week</option>";
echo "</select>";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
echo "</div>";
echo "<br /><br /><div class=\"daily\">";
echo "<form action=\"details.php\" method=\"get\" name=\"chartForm2\">";
echo "<input type=\"hidden\" name=\"wms\" value=\"".$wms."\"/>";
echo "<input type=\"hidden\" name=\"interval\" value=\"".$interval."\"/>";
echo "<select name=\"daily\">";
echo "<option value=\"week\" ";
if ($daily == 'week') {echo "selected=selected";}
echo ">week</option>";
echo "<option value=\"2weeks\" ";
if ($daily == '2weeks') {echo "selected=selected";}
echo ">2 weeks</option>";
echo "<option value=\"month\" ";
if ($daily == 'month') {echo "selected=selected";}
echo ">month</option>";
echo "</select>";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
echo "</div>";
?>
</div>

</body>
</html>
