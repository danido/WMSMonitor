<?php
$wms = isset($_GET['wms']) ? $_GET['wms'] : '';
$selectedId = array("WMS_view","Single_instance","Custom","Custom-".str_replace(".", "-", $wms));
$chart_type = isset($_GET['chart_type']) ? $_GET['chart_type'] : 'current';
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : ($chart_type=='current' ? date("Y-m-d", time()) : date("Y-m-d", time()-86400*6));
$startDateDaily = $startDate==$endDate ? date("Y-m-d", time()-86400*6) : $startDate;
$format = isset($_GET['format']) ? $_GET['format'] : 'flash';
$date_start = $startDate." 00:00:00";
$date_end = $endDate." 23:59:59";
$date_start_epoch = mktime(intval(substr($date_start, 11, 2)), intval(substr($date_start, 14, 2)), intval(substr($date_start, 17, 2)), intval(substr($date_start, 5, 2)), intval(substr($date_start, 8, 2)), intval(substr($date_start, 0, 4)));
$date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));
$num_days = ceil(($date_end_epoch-$date_start_epoch)/86400);
$days_limit = 60;

$plot_names = array("custom_openflash");

$wmsRepl = str_replace(".", "-", $wms);
$nameSession = 'custom'.$wmsRepl.$startDate.$endDate;
session_name($nameSession);
session_start();

include "../common/header.inc";
include "../common/banner.inc";

// arrays containing the metrics that will compose the select statement 
$hwFields = array('cpu_load' => 'CPU Load', 'disk_sandbox' => 'Sandbox partition', 'disk_varlog' => '/var/log partition', 'disk_varlibmysql' => '/var/lib/mysql part.');
$serviceFields = array('condor_running' => 'Running condor', 'condor_idle' => 'Idle condor', 'ism_entries' => 'VO views', 'wm_queue' => 'WM queue', 'jc_queue' => 'JC queue', 'lb_event' => 'LB events queue');
$loadbFields = array('loadb_memusage' => 'Memory usage', 'loadb_fmetric' => 'fmetric', 'loadb_fdrain' => 'fdrain', 'loadb_fload' => 'fload', 'loadb_ftraversaltime' => 'ftraversaltime');
$allSensorFields = array_merge($hwFields, $serviceFields, $loadbFields);
$jobRatesFields = array('WMP_in' => 'Jobs -> WMProxy', 'WM_in' => 'Jobs -> WM', 'WM_in_res' => 'Jobs Resub -> WM', 'JC_in' => 'Jobs -> JC', 'JC_out' => 'Jobs JC -> Condor', 'WMP_in_col' => 'Collections', 'JOB_DONE' => 'Job done', 'JOB_ABORTED' => 'Job aborted');

$_SESSION['customHW'] = array();
$_SESSION['customService'] = array();
$_SESSION['customJob'] = array();
$_SESSION['customDaily'] = array();

$_SESSION['customHW'] = (isset($_GET['checkHW']) || isset($_GET['checkService']) || isset($_GET['checkJob']) || isset($_GET['checkMetric'])) ? (isset($_GET['checkHW']) ? $_GET['checkHW'] : '') : (isset($_SESSION['customHW']) ? $_SESSION['customHW'] : '');
$_SESSION['customService'] = (isset($_GET['checkHW']) || isset($_GET['checkService']) || isset($_GET['checkJob']) || isset($_GET['checkMetric'])) ? (isset($_GET['checkService']) ? $_GET['checkService'] : '') : (isset($_SESSION['customService']) ? $_SESSION['customService'] : '');
$_SESSION['customJob'] = (isset($_GET['checkHW']) || isset($_GET['checkService']) || isset($_GET['checkJob']) || isset($_GET['checkMetric'])) ? (isset($_GET['checkJob']) ? $_GET['checkJob'] : '') : (isset($_SESSION['customJob']) ? $_SESSION['customJob'] : '');

$_SESSION['customDaily'] = isset($_GET['checkDaily']) ? $_GET['checkDaily'] : (isset($_SESSION['customDaily']) ? $_SESSION['customDaily'] : '');
$_SESSION['customMetric'] = (isset($_GET['checkHW']) || isset($_GET['checkService']) || isset($_GET['checkJob']) || isset($_GET['checkMetric'])) ? (isset($_GET['checkMetric']) ? $_GET['checkMetric'] : '') : (isset($_SESSION['customMetric']) ? $_SESSION['customMetric'] : '');

if (!(isset($_GET['checkHW']) || isset($_GET['checkService']) || isset($_GET['checkJob']) || isset($_GET['checkMetric']))) {
	$_SESSION['customService']['Running condor'] = 'Running condor';
	$_SESSION['customService']['Idle condor'] = 'Idle condor';
}

if (!(isset($_GET['checkDaily']))) {
        $_SESSION['customDaily']['Job done'] = 'Job done';
        $_SESSION['customDaily']['Job aborted'] = 'Job aborted';
}

?>

<div class="breadcrumb">
<a title="Click to go to the main page" href="../main/main.php">WMSMonitor</a> >> WMS view >> Single instance >> Custom charts::<?php echo $wms; ?> 
</div>

<table class="main_container">
<tr>
<td class="td_tabcontainer">
<div id="tabcontainer">
<ul class="tabbedvoice">
<?php
	include 'php-ofc-library/open-flash-chart-object.php';





	if ($chart_type == 'current') {
		echo "<li class=\"tabbedvoiceUP\">Detailed View</li>";
		echo "<li class=\"tabbedvoiceDOWN\"><a href=\"custom.php?chart_type=daily&wms=".$wms."&startDate=".$startDateDaily."&endDate=".$endDate."\">Daily View</a></li>";
	} else {
		echo "<li class=\"tabbedvoiceDOWN\"><a href=\"custom.php?chart_type=current&wms=".$wms."&startDate=".$startDate."&endDate=".$endDate."\">Detailed View</a></li>";
		echo "<li class=\"tabbedvoiceUP\">Daily View</li>";
	}
?>
</ul>
</div>

<table class="details charts custom">
<?php
	echo "<tr class=\"supertitle chart_form\">";

	echo "<td class=\"form_subtitle\" colspan=\"2\">";

	echo "<form class=\"inline\" action=\"custom.php\" method=\"get\" name=\"chartForm\">";
	echo "<input type=\"hidden\" name=\"chart_type\" value=\"".$chart_type."\"/>";

	$wmsList = getWMSList('all','all','all','all');
	echo "WMS:";
	echo "<select name=\"wms\">";
	for ($i=0; $i<sizeof($wmsList); $i++) {
        	echo "<option value=\"".$wmsList[$i]."\" ";
        	if ($wmsList[$i] == $wms) {echo "selected=selected";}
        	echo ">".$wmsList[$i]."</option>";
	}
	echo "</select>";

	echo "    from:";
	echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
	echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].startDate,'yyyy-mm-dd',this)\">";
	echo "    to:";
	echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
	echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";

	echo "    (max ".$days_limit." days)";

	$serverPort = $_SERVER['SERVER_PORT'] != 80 ? (':'.  $_SERVER['SERVER_PORT']) : '';
	$webDir = '/'.$config->wmsmonWebDir;
	$protocol = isset($_SERVER['HTTPS']) ? 'https://' : 'http://';

	if ($chart_type == 'current') {

		if ($num_days <= $days_limit) {
			$_SESSION['step'] = getCustomXaxisSteps($startDate, $endDate);

			$customHW = $_SESSION['customHW'];
			$customService = $_SESSION['customService'];
			$customJob = $_SESSION['customJob'];
			$customMetric = $_SESSION['customMetric'];

			$_SESSION['chartJobData'] = getCustomJobData($wms, $startDate, $endDate, $jobRatesFields);
			$_SESSION['chartAllData'] = getCustomAllData($wms, $startDate, $endDate, $allSensorFields);
			$_SESSION['customAll'] = array();
			$_SESSION['customRates'] = array();

			if (!empty($customService)) {
				foreach ($customService as $key) {
					array_push($_SESSION['customAll'], $key);
				}
			}
			if (!empty($customHW)) {
				foreach ($customHW as $key) {
        				array_push($_SESSION['customAll'], $key);
				}
			}
			if (!empty($customMetric)) {
				foreach ($customMetric as $key) {
        				array_push($_SESSION['customAll'], $key);
				}
			}

			if (sizeof($customJob) != 0) {
				foreach ($customJob as $key) {
        				array_push($_SESSION['customRates'], $key);
				}
			}

			$chartJobData = $_SESSION['chartJobData'];

			$step = $_SESSION['step'];

			echo "<form class=\"inline\" action=\"custom.php\" method=\"get\" name=\"chartForm\">";
			echo "<input type=\"hidden\" name=\"chart_type\" value=\"".$chart_type."\"/>";
			echo "<table class=\"checklist\"><tr>";
			echo "<td>Hardware</td><td>Services</td><td>Job rates</td><td>Load balancing</td></tr><tr>";
			echo "<td><ul class=\"customchecklist\">";
			echo "<li>";
			foreach ($hwFields as $key => $value) {
				echo "<input type=\"checkbox\" name=\"checkHW[$value]\" value=\"".$value."\""; if (isset($customHW[$value])) {echo "checked";} echo "/>$value<br />";
			}
        		echo "</li>";
			echo "</ul></td>";
			echo "<td><ul class=\"customchecklist\">";
        		echo "<li>";
			foreach ($serviceFields as $key => $value) {
                        	echo "<input type=\"checkbox\" name=\"checkService[$value]\" value=\"".$value."\""; if (isset($customService[$value])) {echo "checked";} echo "/>$value<br />";
                	}
        		echo "</li>";
			echo "</ul></td>";
			echo "<td><ul class=\"customchecklist\">";
        		echo "<li>";
			foreach ($jobRatesFields as $key => $value) {
                        	echo "<input type=\"checkbox\" name=\"checkJob[$value]\" value=\"".$value."\""; if (isset($customJob[$value])) {echo "checked";} echo "/>$value<br />";
                	}
        		echo "</li>";
			echo "</ul></td>";
			echo "<td><ul class=\"customchecklist\">";
        		echo "<li>";
			foreach ($loadbFields as $key => $value) {
                        	echo "<input type=\"checkbox\" name=\"checkMetric[$value]\" value=\"".$value."\""; if (isset($customMetric[$value])) {echo "checked";} echo "/>$value<br />";
                	}
        		echo "</li>";
			echo "</ul></td>";

			echo "</tr></table>";
			echo "<input type=\"submit\" value=\"Submit\"/>";
			echo "<input type=button OnClick=\"change_format('custom_openflash');\" value=\"png version\"/>";
			echo "</form>";
			echo "</td>";
			echo "</tr>";

			$url_parameters='wms='.$wms.'%26startDate='.$startDate.'%26endDate='.$endDate.'%26nameSession='.$nameSession;
			$url_1='custom_openflash.php?'.$url_parameters;
?>


<script type="text/javascript">
swfobject.embedSWF(
  "open-flash-chart.swf", "<?php echo $plot_names[0];?>",
  "800", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_1;?>"} );
</script>

<?php
			if (sizeof($_SESSION['chartJobData'])!=0 || sizeof($_SESSION['chartAllData'])!=0) {
        			echo "<tr><td><div id=".$plot_names[0]."></div></td></tr>";
			} else {
				echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";
			}


		} else {
			echo "<input type=\"submit\" value=\"Submit\"/>";
			echo "<div>The period chosen is too long. Please visit the \"Daily View\" section to obtain a chart with daily interval.</div>";
		}






// if $chart_type!='current'
	} else {

		$_SESSION['chartDailyData'] = getCustomJobDailyData($wms, $startDate, $endDate, $jobRatesFields);
		$customDaily = $_SESSION['customDaily'];
		$chartDailyData = $_SESSION['chartDailyData'];
		$step = $_SESSION['stepDaily'];
		$_SESSION['customDailyRates'] = array();

		if (sizeof($customDaily) != 0) {
			foreach ($customDaily as $key) {
        			array_push($_SESSION['customDailyRates'], $key);
			}
		}

		echo "<table class=\"checklist\"><tr>";
		echo "<td>Job flow</td></tr><tr>";
		echo "<td><ul class=\"customchecklist\">";
        	echo "<li>";

		foreach ($jobRatesFields as $key => $value) {
                        echo "<input type=\"checkbox\" name=\"checkDaily[$value]\" value=\"".$value."\""; if (isset($customDaily[$value])) {echo "checked";} echo "/>$value<br />";
		}

        	echo "</li>";
		echo "</ul></td>";
		echo "</tr></table>";

		echo "<input type=\"submit\" value=\"Submit\"/>";
		echo "<input type=button OnClick=\"change_format('custom_openflash');\" value=\"png version\"/>";
		echo "</form>";
		echo "</td>";
		echo "</tr>";
		echo "<tr><td><div id=\"open_flash_chart\">";

		$url_parameters='chart_type=daily%26wms='.$wms.'%26startDate='.$startDate.'%26endDate='.$endDate.'%26nameSession='.$nameSession;
		$url_1='custom_openflash.php?'.$url_parameters;
?>


<script type="text/javascript">
swfobject.embedSWF(
  "open-flash-chart.swf", "<?php echo $plot_names[0];?>",
  "800", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_1;?>"} );
</script>

<?php
if (sizeof($chartDailyData)!=0 || sizeof($_SESSION['customDailyRates'])!=0) {
	echo "<tr><td><div id=".$plot_names[0]."></div></td></tr>";
} else {
	echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";	
}
?>
<?php
	}
?>
</table>

</td>
</tr>
</table>

</body>
</html>
