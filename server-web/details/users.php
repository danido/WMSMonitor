<?php
include "../common/config.php";

include "../common/functions.php";

if ($config->protectedPages==1) {
	$dn = $_SERVER['SSL_CLIENT_S_DN'];

	$dnEnabledList = array();
	$dnEnabledList=getDNEnabledList();

	$enabled = 0;
	for ($i=0; $i<sizeof($dnEnabledList); $i++) {
       	if ($dnEnabledList[$i][0] == $dn) {
                	$enabled = 1;
                	break;
        	}
	}

	if ($enabled==0) {
        	header("location: ../details/users_noaccess.php");
	}
}



$wms = isset($_GET['wms']) ? $_GET['wms'] : '';
$vo = isset($_GET['vo']) ? $_GET['vo'] : '';
$orderedBy = isset($_GET['orderedBy']) ? $_GET['orderedBy'] : 'Jobs_submitted';
$aggregation = isset($_GET['aggregation']) ? $_GET['aggregation'] : 'wms';
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d");
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
if ($aggregation == 'wms') {
	$selectedId = array("WMS_view","Single_instance","Users_activity_wms","Users_activity-".str_replace(".", "-", $wms));
	$wmsRepl = str_replace(".", "-", $wms);
	$nameSession = 'users'.$aggregation.$wmsRepl.$orderedBy.$startDate.$endDate;
} else if ($aggregation == 'vo') {
	$selectedId = array("VO_view","Single_VO","Users_activity_vo","Users_activity-".$vo);
	$nameSession = 'users'.$aggregation.$vo.$orderedBy.$startDate.$endDate;
}
$limit_from = isset($_GET['limit_from']) ? $_GET['limit_from'] : '';
$limit_to = isset($_GET['limit_to']) ? $_GET['limit_to'] : '';

session_name($nameSession);
session_start();

include "../common/header.inc";
include "../common/banner.inc";

if ($aggregation == 'wms') {
	$_SESSION['ceStatsData'] = getUsersStatsWMSData($wms, $startDate, $endDate, $orderedBy);
	$url_string = 'aggregation=wms%26wms='.$wms;
} else if ($aggregation == 'vo') {
	$_SESSION['ceStatsData'] = getUsersStatsVOData($vo, $startDate, $endDate, $orderedBy);
	$url_string = 'aggregation=vo%26vo='.$vo;
}

$ceStatsData = $_SESSION['ceStatsData'];

//print_r($ceStatsData);

$ceCount = sizeof($ceStatsData);
$best_limit = isset($_GET['best_limit']) && is_numeric($_GET['best_limit']) && ($_GET['best_limit'] != 0) && ($_GET['best_limit'] <= $ceCount) ? $_GET['best_limit'] : ($ceCount < 10 ? $ceCount : 10);
?>

<div class="breadcrumb">
<?php
	if ($aggregation == 'wms') {
		echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> WMS view >> Single instance >> Users activity::".$wms;
	} else if ($aggregation == 'vo') {
		echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> VO view >> Single VO >> Users activity::".$vo;
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


						<table class="details charts users">

<?php
echo "<tr class=\"supertitle chart_form\">";
echo "<td class=\"form_subtitle\" id=\"ce_mm_subtitle\">";

echo "<form class=\"inline\" action=\"users.php\" method=\"get\" name=\"chartForm\">";
//echo "<input type=\"hidden\" name=\"daily\" value=\"".$daily."\"/>";
//echo "<input type=\"hidden\" name=\"chart_type\" value=\"".$chart_type."\"/>";
echo "<input type=\"hidden\" name=\"limit_from\" value=\"".$limit_from."\"/>";
echo "<input type=\"hidden\" name=\"limit_to\" value=\"".$limit_to."\"/>";
echo "<input type=\"hidden\" name=\"aggregation\" value=\"".$aggregation."\"/>";

if ($aggregation=='wms') {
	$wmsList = getWMSList('all','all','all','all');
	echo "WMS:";
	echo "<select name=\"wms\">";
	for ($i=0; $i<sizeof($wmsList); $i++) {
        	echo "<option value=\"".$wmsList[$i]."\" ";
        	if ($wmsList[$i] == $wms) {echo "selected=selected";}
        	echo ">".$wmsList[$i]."</option>";
	}
	echo "</select>";
} else if ($aggregation=='vo') {
	$voList = getVOList();
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
echo "<p>Plot the <input type=\"text\" size=\"3\" value=\"".$best_limit."\" name=\"best_limit\"/> most active users (out of $ceCount) </p>";
echo "Ordered by:  ";
echo "<input type=\"radio\" name=\"orderedBy\" value=\"Jobs_submitted\"";
if ($orderedBy=='Jobs_submitted') {echo " checked=checked";}
echo "\><span class=\"right_separator\">Jobs_submitted</span>";
echo "<input type=\"radio\" name=\"orderedBy\" value=\"Jobs_done\"";
if ($orderedBy=='Jobs_done') {echo " checked=checked";}
echo "\><span class=\"right_separator\">Jobs_done</span>";
echo "<input type=\"radio\" name=\"orderedBy\" value=\"Jobs_aborted\"";
if ($orderedBy=='Jobs_aborted') {echo " checked=checked";}
echo "\><span class=\"right_separator\">Jobs_aborted</span>";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "<input type=button OnClick=\"change_format('users_stats_chart','users_stats_chart_2','users_stats_chart_3');\" value=\"png version\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";

$url_parameters=$url_string.'%26interval='.$interval.'%26endDate='.$endDate.'%26best_limit='.$best_limit.'%26nameSession='.$nameSession;
$url_1='users_stats_chart.php?'.$url_parameters.'%26variable=Jobs_submitted';
$url_2='users_stats_chart.php?'.$url_parameters.'%26variable=Jobs_done';
$url_3='users_stats_chart.php?'.$url_parameters.'%26variable=Jobs_aborted';
?>

<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "users_stats_chart",
  "630", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_1;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "users_stats_chart_2",
  "630", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_2;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "users_stats_chart_3",
  "630", "600", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_3;?>"} );

</script>

<?php

if (sizeof($ceStatsData)!=0) {
	echo "<tr><td><div id=\"users_stats_chart\"></div></td></tr><tr><td><br /><br /><br /></td></tr>";
	echo "<tr><td><div id=\"users_stats_chart_2\"></div></td></tr><tr><td><br /><br /><br /></td></tr>";
	echo "<tr><td><div id=\"users_stats_chart_3\"></div></td></tr>";
} else {
	echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";
}
?>
						</table>
					</td>
				</tr>
			</table>
		</td>
	</tr>
</table>


</body>
</html>
