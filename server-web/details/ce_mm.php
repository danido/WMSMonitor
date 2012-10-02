<?php
$wms = isset($_GET['wms']) ? $_GET['wms'] : '';
$vo = isset($_GET['vo']) ? $_GET['vo'] : '';
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d");
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
$aggregation = isset($_GET['aggregation']) ? $_GET['aggregation'] : '';
if ($aggregation == 'wms') {
	$selectedId = array("WMS_view","Single_instance","Resource_usage_wms","Resource_usage-".str_replace(".", "-", $wms));
	$wmsRepl = str_replace(".", "-", $wms);
	$nameSession = 'ce_mm'.$aggregation.$wmsRepl.$startDate.$endDate;
} else if ($aggregation == 'vo') {
	$selectedId = array("VO_view","Single_VO","Resource_usage_vo","Resource_usage-".$vo);
	$nameSession = 'ce_mm'.$aggregation.$vo.$startDate.$endDate;
}

session_name($nameSession);
session_start();

include "../common/header.inc";
if ($aggregation == 'wms') {
        $_SESSION['ceStatsData'] = getCEStatsWMSData($wms, $startDate, $endDate);
        $url_string = 'aggregation=wms%26wms='.$wms;
} else if ($aggregation == 'vo') {
        $_SESSION['ceStatsData'] = getCEStatsVOData($vo, $startDate, $endDate);
        $url_string = 'aggregation=vo%26vo='.$vo;
}

if ($aggregation == 'wms') {
        $_SESSION['chartData'] = getCEMMWMSData($wms, $startDate, $endDate);
        $url_string = 'aggregation=wms%26wms='.$wms;
	$chartData = $_SESSION['chartData'];
} else if ($aggregation == 'vo') {
//        $_SESSION['chartData'] = getCEMMVOData($vo, $startDate, $endDate);
//        $url_string = 'aggregation%26vo&vo='.$vo;
}
//$chartData = $_SESSION['chartData'];
$_SESSION['step'] = getXaxisSteps($interval);

include "../common/banner.inc";
$limit_from = isset($_GET['limit_from']) ? $_GET['limit_from'] : '';
$limit_to = isset($_GET['limit_to']) ? $_GET['limit_to'] : '';
$ceStatsData = $_SESSION['ceStatsData'];
$ceCount = sizeof($ceStatsData);
$best_limit = isset($_GET['best_limit']) && is_numeric($_GET['best_limit']) && ($_GET['best_limit'] <= $ceCount) ? $_GET['best_limit'] : (($ceCount < 10) && ($ceCount > 0) ? $ceCount : 10);
?>

<div class="breadcrumb">
<?php
        if ($aggregation == 'wms') {
                echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> WMS view >> Single instance >> Resource usage::".$wms;
        } else if ($aggregation == 'vo') {
                echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> VO view >> Single VO >> Resource usage::".$vo;
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

						<table class="details charts ce_mm">

<?php
echo "<tr class=\"supertitle chart_form\">";
echo "<td class=\"form_subtitle\" id=\"ce_mm_subtitle\">";

$serverPort = $_SERVER['SERVER_PORT'] != 80 ? (':'.  $_SERVER['SERVER_PORT']) : '';
$webDir = '/'.$config->wmsmonWebDir;
$protocol = isset($_SERVER['HTTPS']) ? 'https://' : 'http://';

echo "<form class=\"inline\" action=\"ce_mm.php\" method=\"get\" name=\"chartForm\">";
//echo "<input type=\"hidden\" name=\"daily\" value=\"".$daily."\"/>";
//echo "<input type=\"hidden\" name=\"chart_type\" value=\"".$chart_type."\"/>";
echo "<input type=\"hidden\" name=\"limit_from\" value=\"".$limit_from."\"/>";
echo "<input type=\"hidden\" name=\"limit_to\" value=\"".$limit_to."\"/>";
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

if ((isset($chartData) && sizeof($chartData)!=0) || sizeof($ceStatsData)!=0) {
	echo "<span id=\"best_limit\">Plot the <input type=\"text\" size=\"3\" value=\"".$best_limit."\" name=\"best_limit\"/> most used CEs (out of $ceCount) </span>";
}

echo "<input type=\"submit\" value=\"Submit\"/>";
echo "<input type=button OnClick=\"change_format('ce_mm_chart','ce_stats_chart');\" value=\"png version\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";

/*
if ($aggregation == 'wms') {
        $_SESSION['chartData'] = getCEMMWMSData($wms, $startDate, $endDate);
        $url_string = 'aggregation=wms%26wms='.$wms;
} else if ($aggregation == 'vo') {
        $_SESSION['chartData'] = getCEMMVOData($vo, $startDate, $endDate);
        $url_string = 'aggregation%26vo&vo='.$vo;
}
$chartData = $_SESSION['chartData'];
$_SESSION['step'] = getXaxisSteps($interval);
*/
//print_r($chartData);


$url_parameters=$url_string.'%26interval='.$interval.'%26endDate='.$endDate.'%26best_limit='.$best_limit.'%26nameSession='.$nameSession;
$url_1='ce_mm_chart.php?'.$url_parameters;
$url_3='ce_stats_chart.php?'.$url_parameters;


if ($aggregation=='wms') {


if (sizeof($chartData)!=0 || sizeof($ceStatsData)!=0) {	

echo "<tr><td><div id=\"ce_mm_chart\">";
echo "</div></td>";

$bin = ceil(sizeof($chartData)/10);
$test["occurrence_aggr"]=0;
$bar_values=array();
for ($i=0; $i<(ceil(sizeof($chartData)/10)*10); $i++) {

        if (($i+1) % $bin != 0) {
                $test["occurrence_aggr"]=$test["occurrence_aggr"]+intval($chartData[$i]);
	} else if ($bin==1){
                if (isset($chartData[$i])) {
                        $test["occurrence_aggr"]=intval($chartData[$i]);
                        $test["occurrence_aggr_ok"][$i]=$test["occurrence_aggr"];
                } else {
                        $test["occurrence_aggr"]=0;
                        $test["occurrence_aggr_ok"][$i]=0;
                }
        } else {
                $test["occurrence_aggr_ok"][$i]=$test["occurrence_aggr"];
                $test["num_ce_aggr_ok"][$i]=($i-$bin+1)."-".$i;
                $test["occurrence_aggr"]=0;
        }

        $test["num_ce"][$i]=$i;
        $test["occurrence"][$i]=intval($chartData[$i]);
        
	if (is_null($test["num_ce"][$i])) {
                $test["num_ce"][$i] = 'null';
        }
        if (is_null($test["occurrence"][$i])) {
                $test["occurrence"][$i] = 'null';
        }
}

//print_r($test["occurrence_aggr_ok"]);
//print_r($test["num_ce"]);
//print_r($bar_values);

//$metrics_1=array("Total Jobs -> WM", "Jobs -> JC", "Jobs -> JSS");

//$_SESSION['metrics_1'] = $metrics_1;


//print_r($ceStatsData);
//echo $nameSession;

//$url_parameters=$url_string.'%26interval='.$interval.'%26endDate='.$endDate.'%26best_limit='.$best_limit.'%26nameSession='.$nameSession;
//$url_1='ce_mm_chart.php?'.$url_parameters;
//$url_3='ce_stats_chart.php?'.$url_parameters;

$url_2=array();
$divname=array();
$i=0;
foreach ($test["occurrence_aggr_ok"] as $key => $value) {
	$limit_from=$key+1-$bin;
	$limit_to=$key;
	$url_2[$i]='ce_mm_partial_chart.php?'.$url_parameters.'%26limit_from='.$limit_from.'%26limit_to='.$limit_to;
	$divname[$i]="ce_mm_partial_chart".$limit_to;

	echo "<td class=\"partial_histogram\" id=\"partial".$key."\"><div id=\"ce_mm_partial_chart".$key."\"></div></td>";

	echo "<script type=\"text/javascript\">";
	echo "swfobject.embedSWF(";
	echo "\"open-flash-chart.swf\", \"".$divname[$i]."\",";
	echo "\"570\", \"400\", \"9.0.0\", \"expressInstall.swf\",";
	echo "{\"data-file\":\"".$url_2[$i]."\"} );";
	echo "</script>";
	$i++;
}
	
echo "</tr>";
echo "<tr><td class=\"separator\"></td></tr>";
echo "<tr><td>";
echo "</td></tr>";

//} else {
  //      echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";

echo "<script type=\"text/javascript\">";
echo "swfobject.embedSWF(";
echo "\"open-flash-chart.swf\", \"ce_mm_chart\",";
echo "\"660\", \"400\", \"9.0.0\", \"expressInstall.swf\",";
echo "{\"data-file\":\"".$url_1."\"} );";
echo "</script>";

} 
else {
	echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";
}


}

?>

<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "ce_stats_chart",
  "660", "700", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_3;?>"} );
</script>

<?php
if (sizeof($ceStatsData)!=0) {
	echo "<tr><td><div id='ce_stats_chart'></div></td></tr>";
} else if ($aggregation=='vo' || (isset($chartData) && sizeof($chartData)!=0)) {
	echo "<tr><td class='no_data'>No data available for the chosen period!</td></tr>";
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
