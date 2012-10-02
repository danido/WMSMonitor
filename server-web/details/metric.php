<?php
$wms = isset($_GET['wms']) ? $_GET['wms'] : '';
$selectedId = array("WMS_view","Single_instance","Load_balancing","Load_balancing-".str_replace(".", "-", $wms));
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d");
$date_start = $startDate." 00:00:00";
$date_end = $endDate." 23:59:59";
$date_start_epoch = mktime(intval(substr($date_start, 11, 2)), intval(substr($date_start, 14, 2)), intval(substr($date_start, 17, 2)), intval(substr($date_start, 5, 2)), intval(substr($date_start, 8, 2)), intval(substr($date_start, 0, 4)));
$date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));
$num_days = ceil(($date_end_epoch-$date_start_epoch)/86400);
$days_limit = 60;

$wmsRepl = str_replace(".", "-", $wms);
$nameSession = 'metric'.$wmsRepl.$startDate.$endDate;
session_name($nameSession);
session_start();

include "../common/header.inc";
include "../common/banner.inc";
include 'php-ofc-library/open-flash-chart-object.php';

$serverPort = $_SERVER['SERVER_PORT'] != 80 ? (':'.  $_SERVER['SERVER_PORT']) : '';
$webDir = '/'.$config->wmsmonWebDir;
$protocol = isset($_SERVER['HTTPS']) ? 'https://' : 'http://';
?>

<div class="breadcrumb">
	<a title="Click to go to the main page" href="../main/main.php">WMSMonitor</a> >> WMS view >> Single instance >> Load balancing::<?php echo $wms; ?>
</div>

<?php
echo "<table class=\"details charts metric\"><tr><td>";
echo "<form class=\"inline\" action=\"metric.php\" method=\"get\" name=\"chartForm\">";

#$wmsList = getMetricWMSList();
$wmsList = getWMSList('all','all','all','all');
echo "WMS:";
echo "<select name=\"wms\">";
for ($i=0; $i<sizeof($wmsList); $i++) {
	echo "<option value=\"".$wmsList[$i]."\" ";
        if ($wmsList[$i] == $wms) {echo "selected=selected";}
        echo ">".$wmsList[$i]."</option>";
}
echo "</select>";

echo "   From: ";
echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].startDate,'yyyy-mm-dd',this)\">";
echo " To: ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";
echo "    (max ".$days_limit." days)";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "<input type=button OnClick=\"change_format('chart_metric_1', 'chart_metric_2', 'chart_metric_3');\" value=\"png version\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";
echo "<tr><td><div id=\"open_flash_chart\">";

if ($num_days <= $days_limit) {

$_SESSION['chartData'] = getMetricData($wms, $startDate, $endDate);
$chartData = $_SESSION['chartData'];
$_SESSION['step'] = getCustomXaxisSteps($startDate, $endDate);


$url_parameters='startDate='.$startDate.'%26endDate='.$endDate.'%26nameSession='.$nameSession;
$url_1='chart_metric_1.php?'.$url_parameters;
$url_2='chart_metric_2.php?'.$url_parameters;
$url_3='chart_metric_3.php?'.$url_parameters;
?>

<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_metric_1",
  "750", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_1;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_metric_2",
  "750", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_2;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_metric_3",
  "750", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_3;?>"} );

</script>

<?php

	if (sizeof($chartData)!=0) {
		echo "<div id=\"chart_metric_1\"></div><div class='separator'></div><div id=\"chart_metric_2\"></div><div class='separator'></div><div id=\"chart_metric_3\"></div></div></td></tr></table>";
	} else {
		echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";	
	}

} else {
	echo "<div>The period chosen is too long. Please choose a different period.</div>";
	echo "</div></td></tr></table>";
}

?>
