<?php
$wms = isset($_GET['wms']) ? $_GET['wms'] : '';
$vo = isset($_GET['vo']) ? $_GET['vo'] : '';
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d");
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
$aggregation = isset($_GET['aggregation']) ? $_GET['aggregation'] : 'wms';
if ($aggregation == 'wms') {
	$selectedId = array("WMS_view","Single_instance","Resource_usage_wms","Resource_usage-".str_replace(".", "-", $wms));
	$wmsRepl = str_replace(".", "-", $wms);
	$nameSession = 'err_stats'.$aggregation.$wmsRepl.$startDate.$endDate;
} else if ($aggregation == 'vo') {
	$selectedId = array("VO_view","Single_VO","Resource_usage_vo","Resource_usage-".$vo);
	$nameSession = 'err_stats'.$aggregation.$vo.$startDate.$endDate;
}

session_name($nameSession);
session_start();

include "../common/header.inc";
if ($aggregation == 'wms') {
        $_SESSION['ceStatsData'] = getErrStatsWMSData($wms, $startDate, $endDate);
        $url_string = 'aggregation=wms%26wms='.$wms;
} else if ($aggregation == 'vo') {
        $_SESSION['ceStatsData'] = getErrStatsVOData($vo, $startDate, $endDate);
        $url_string = 'aggregation=vo%26vo='.$vo;
}

include "../common/banner.inc";
$ceStatsData = $_SESSION['ceStatsData'];
$ceCount = sizeof($ceStatsData);
$best_limit = isset($_GET['best_limit']) && is_numeric($_GET['best_limit']) && ($_GET['best_limit'] <= $ceCount) ? $_GET['best_limit'] : (($ceCount < 10) && ($ceCount > 0) ? $ceCount : 10);
?>

<div class="breadcrumb">
<?php
        if ($aggregation == 'wms') {
                echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> WMS view >> Single instance >> Error stats::".$wms;
        } else if ($aggregation == 'vo') {
                echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> VO view >> Single VO >> Error stats::".$vo;
        }
?>
</div>

<table class="main_container">
				<tr>
					<td class="separator"></td><td colspan="3">

<?php
include 'php-ofc-library/open-flash-chart-object.php';
$interval = isset($_GET['interval']) ? $_GET['interval'] : 'day';
?>

	<table class="details charts err_stats">

<?php
echo "<tr class=\"supertitle chart_form\">";
echo "<td class=\"form_subtitle\" id=\"globus_err_subtitle\">";

$serverPort = $_SERVER['SERVER_PORT'] != 80 ? (':'.  $_SERVER['SERVER_PORT']) : '';
$webDir = '/'.$config->wmsmonWebDir;
$protocol = isset($_SERVER['HTTPS']) ? 'https://' : 'http://';

echo "<form class=\"inline\" action=\"err_stats.php\" method=\"get\" name=\"chartForm\">";
echo "<input type=\"hidden\" name=\"aggregation\" value=\"".$aggregation."\"/>";

if ($aggregation=='wms') {
        $wmsList = getWMSListCEStats();
        echo "WMS:";
        echo "<select name=\"wms\">";
        for ($i=0; $i<sizeof($wmsList); $i++) {
                echo "<option value=\"".$wmsList[$i]."\" ";
                if ($wmsList[$i] == $wms) {echo "selected=selected";}
                echo ">".$wmsList[$i]."</option>";
        }
        echo "</select>";
} else if ($aggregation=='vo') {
        $voList = getVOListCEStats();
        echo "VO:";
        echo "<select name=\"vo\">";
        for ($i=0; $i<sizeof($voList); $i++) {
                echo "<option value=\"".$voList[$i]."\" ";
                if ($voList[$i] == $vo) {echo "selected=selected";}
                echo ">".$voList[$i]."</option>";
        }
        echo "</select>";
}

echo "    from:";
echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].startDate,'yyyy-mm-dd',this)\">";

echo " to: ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";

echo "<br /><span>Plot the <input type=\"text\" size=\"3\" value=\"".$best_limit."\" name=\"best_limit\"/> most happened errors (out of $ceCount) </span>";

echo "<input type=\"submit\" value=\"Submit\"/>";
echo "<input type=button OnClick=\"change_format('err_stats_chart');\" value=\"png version\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";


$url_parameters=$url_string.'%26interval='.$interval.'%26endDate='.$endDate.'%26best_limit='.$best_limit.'%26nameSession='.$nameSession;
$url='err_stats_chart.php?'.$url_parameters;

?>

<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "err_stats_chart",
  "600", "700", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url;?>"} );

</script>

<?php

if (sizeof($ceStatsData)!=0) {
	echo "<tr><td><div id=\"err_stats_chart\"></div></td></tr>";
} else {
	echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";
}

?>
			</table>
		</td>
	</tr>
</table>


</body>
</html>
