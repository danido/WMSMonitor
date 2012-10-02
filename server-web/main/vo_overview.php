<?php

$view_type = isset($_GET['view_type']) ? $_GET['view_type'] : 'chart';
$selected_type = ($view_type == table) ? 'Table' : 'Charts'; 
$selectedId = array("VO_view", "Overview_vo", "Overview_vo_".$selected_type);

$volist_type = isset($_GET['volist_type']) ? $_GET['volist_type'] : 'best';

if ($selected_type == 'Table') {
        $volist_type = 'all';
}

$custom_vos = isset($_GET['check_vos']) ? $_GET['check_vos'] : '';

$scope = isset($_GET['scope']) ? $_GET['scope'] : 'all';
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d", time()-(6*86400));

$nameSession = 'vo_overview'.$startDate.$endDate;
session_name($nameSession);
session_start();

include "../common/header.inc";
include "../common/banner.inc";

$_SESSION['chartData']=getVOUsageLBDailyDataByUsers($scope, $startDate, $endDate, $volist_type, $custom_vos);

$result=$_SESSION['chartData'];

// Print data for debugging
//print("<pre>".print_r($result, true)."</pre>");

$all_vos=getVOList();
array_multisort(array_map('strtolower', $all_vos), SORT_ASC, SORT_STRING, $all_vos);

$check_vos=array();

$volist=array();

for ($j=0; $j<sizeof($result); $j++) {
for ($y=0; $y<sizeof($result[$j]); $y++) {
	if (!(in_array($result[$j][$y]["VO"],$volist))) {
		array_push($volist, $result[$j][$y]["VO"]); 
	}
}
}

for ($j=0; $j<sizeof($result); $j++) {
for ($y=0; $y<sizeof($result[$j]); $y++) {
	$done["".$result[$j][$y]["VO"].""]=$done["".$result[$j][$y]["VO"].""]+$result[$j][$y]["JOB_DONE"];
        $aborted["".$result[$j][$y]["VO"].""]=$aborted["".$result[$j][$y]["VO"].""]+$result[$j][$y]["JOB_ABORTED"];
        $wmp_in["".$result[$j][$y]["VO"].""]=$wmp_in["".$result[$j][$y]["VO"].""]+$result[$j][$y]["WMP_in"];
        $jc_out["".$result[$j][$y]["VO"].""]=$jc_out["".$result[$j][$y]["VO"].""]+$result[$j][$y]["JC_out"];
        $wmp_in_col["".$result[$j][$y]["VO"].""]=$wmp_in_col["".$result[$j][$y]["VO"].""]+$result[$j][$y]["WMP_in_col"];
        $wm_in_res["".$result[$j][$y]["VO"].""]=$wm_in_res["".$result[$j][$y]["VO"].""]+$result[$j][$y]["WM_in_res"];                
}
}

$_SESSION['pieDataVO']=array();

for ($i=0; $i<sizeof($volist); $i++) {
        $_SESSION['pieDataVO'][$i]=array('vo' => $volist[$i], 'JOB_DONE' => $done["".$volist[$i].""], 'JOB_ABORTED' => $aborted["".$volist[$i].""], 'WMP_in' => $wmp_in["".$volist[$i].""], 'JC_out' => $jc_out["".$volist[$i].""], 'WMP_in_col' => $wmp_in_col["".$volist[$i].""], 'WM_in_res' => $wm_in_res["".$volist[$i].""]);
}

$wmsAggregated=$_SESSION['pieDataVO'];

$_SESSION['step']=getXaxisAggregatedSteps($startDate, $endDate);
?>

<div class="breadcrumb">
<?php
	echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> VO view >> Overview >> ".$selected_type."::".$scope;
?>
</div>

<?php
if ($view_type == 'chart') {

echo "<table class=\"details charts vo_overview\">";
echo "<tr class=\"supertitle\">";

echo "<td class=\"form_subtitle\" colspan=\"3\">Statistics on ";

echo "<form class=\"inline\" action=\"vo_overview.php\" method=\"get\" name=\"chartForm\">";

echo "<select id=\"volist_type_group\" name=\"volist_type\">";
echo "<option value=\"best\""; if ($volist_type == 'best') {echo "selected=selected";} echo ">the best 10 (by jobs done)</option>";
echo "<option value=\"lhc\""; if ($volist_type == 'lhc') {echo "selected=selected";} echo ">LHC</option>";
echo "<option value=\"lhc-nonlhc\""; if ($volist_type == 'lhc-nonlhc') {echo "selected=selected";} echo ">LHC / non-LHC</option>";
echo "<option value=\"all\""; if ($volist_type == 'all') {echo "selected=selected";} echo ">all</option>";
echo "<option value=\"custom\""; if ($volist_type == 'custom') {echo "selected=selected";} echo ">a customized set of</option>";
echo "</select>";

echo " VOs    from:";

echo "<input type=\"hidden\" name=\"scope\" value=\"".$scope."\"/>";
echo "<input type=\"hidden\" name=\"view_type\" value=\"".$view_type."\"/>";
echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].startDate,'yyyy-mm-dd',this)\">";
echo "    to ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";

echo "<input type=\"submit\" value=\"Submit\"/>";
echo "<input type=button OnClick=\"change_format('vo_all_1','vo_all_1_2','vo_all_1_3','vo_all_1_4','vo_chart_2','vo_chart_2_1','vo_chart_2_2','vo_chart_2_3');\" value=\"png version\"/>";
echo "</td>";
echo "</tr>";
echo "<tr>";
echo "<td></td>";
echo "<td id=\"vochecklist\">";
echo "Choose the VOs: <ul class=\"customchecklist\">";
        echo "<li>";
                foreach ($all_vos as $value) {
                                echo "<input type=\"checkbox\" name=\"check_vos[$value]\" value=\"".$value."\""; if (in_array($value, $volist)) {echo "checked";} echo "/>$value<br />";
                }
        echo "</li>";
echo "</ul>";
echo "</form>";
echo "</td>";
echo "</tr>";


include '../details/php-ofc-library/open-flash-chart-object.php';

$url_parameters='scope='.$scope.'%26startDate='.$startDate.'%26endDate='.$endDate.'%26nameSession='.$nameSession;
$url_1='../details/vo_all_1.php?'.$url_parameters.'%26variable=JOB_DONE';
$url_2='../details/vo_all_1.php?'.$url_parameters.'%26variable=JOB_ABORTED';
$url_3='../details/vo_all_1.php?'.$url_parameters.'%26variable=WMP_in';
$url_4='../details/vo_all_1.php?'.$url_parameters.'%26variable=JC_out';
$url_5='../details/vo_chart_2.php?'.$url_parameters.'%26aggregation=VO%26variable=JOB_DONE';
$url_6='../details/vo_chart_2.php?'.$url_parameters.'%26aggregation=VO%26variable=JOB_ABORTED';
$url_7='../details/vo_chart_2.php?'.$url_parameters.'%26aggregation=VO%26variable=WMP_in';
$url_8='../details/vo_chart_2.php?'.$url_parameters.'%26aggregation=VO%26variable=JC_out';
?>

<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_all_1",
  "430", "258", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_1;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_all_1_2",
  "430", "258", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_2;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_all_1_3",
  "430", "258", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_3;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_all_1_4",
  "430", "258", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_4;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2",
  "330", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_5;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2_1",
  "330", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_6;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2_2",
  "330", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_7;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2_3",
  "330", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_8;?>"} );

</script>

<?php

if (sizeof($wmsAggregated)!=0) {


echo "<tr><td><div id=\"vo_all_1\"></div></td><td><div id=\"vo_chart_2\"></div></td></tr>";
echo "<tr><td><div id=\"vo_all_1_2\"></div></td><td><div id=\"vo_chart_2_1\"></div></td></tr>";
echo "<tr><td><div id=\"vo_all_1_3\"></div></td><td><div id=\"vo_chart_2_2\"></div></td></tr>";
echo "<tr><td><div id=\"vo_all_1_4\"></div></td><td><div id=\"vo_chart_2_3\"></div></td></tr>";

} else {
	echo "<tr><td class='no_data'>No data available for the chosen period!</td><td></td></tr>";
}

?>

</table>

<?php

} else {

echo "<table class=\"aggregated form\">";

echo "<tr class=\"supertitle\">";
echo "<td class=\"form_subtitle\" colspan=\"5\">From ";

echo "<form class=\"inline\" action=\"vo_overview.php\" method=\"get\" name=\"chartForm\">";
echo "<input type=\"hidden\" name=\"scope\" value=\"".$scope."\"/>";
echo "<input type=\"hidden\" name=\"view_type\" value=\"".$view_type."\"/>";
echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].startDate,'yyyy-mm-dd',this)\">";
echo "    to ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
echo "</td>";
echo "</tr></table>";

if (sizeof($wmsAggregated)!=0) {

echo "<table class=\"aggregated\"><tr class=\"title\">";
echo "<td class=\"wms_column\" title=\"VO name\">VO</td>";
echo "<td title=\"Number of jobs submitted to WMProxy\">SUBMITTED</td>";
echo "<td title=\"Number of jobs resubmitted to WM\">RESUBMITTED</td>";
echo "<td title=\"Number of jobs successfully enqueued to Job Submission Service\">JSS</td>";
echo "<td title=\"Number of jobs done with exit status 0\">DONE</td>";
echo "<td title=\"Number of jobs aborted\">ABORTED</td>";
echo "<td title=\"Number of submitted collections\">COLLECTIONS</td>";
echo "</tr>";

$wmp_in_tot = 0;
$jc_out_tot = 0;
$done_tot = 0;
$aborted_tot = 0;
$wmp_in_col_tot = 0;

for ($i=0;$i<sizeof($wmsAggregated);$i++) {
$row_color = (($i % 2) == 0) ? 'row2' : 'row1' ;
echo "<tr class=\"".$row_color."\">";        
	echo "<td class=\"wms_column\" title=\"Click for more details on ".$wmsAggregated[$i]['vo']."\"><a href=\"../details/vo_details.php?vo=".$wmsAggregated[$i]['vo']."\">".$wmsAggregated[$i]['vo']."</a></td>";
        echo "<td>".$wmsAggregated[$i]['WMP_in']."</td>";
	echo "<td>".$wmsAggregated[$i]['WM_in_res']."</td>";
	echo "<td>".$wmsAggregated[$i]['JC_out']."</td>";
	echo "<td>".$wmsAggregated[$i]['JOB_DONE']."</td>";
	echo "<td>".$wmsAggregated[$i]['JOB_ABORTED']."</td>";
	echo "<td>".$wmsAggregated[$i]['WMP_in_col']."</td>";
echo "</tr>";
$wmp_in_tot += $wmsAggregated[$i]['WMP_in'];
$wm_in_res_tot += $wmsAggregated[$i]['WM_in_res'];
$jc_out_tot += $wmsAggregated[$i]['JC_out'];
$done_tot += $wmsAggregated[$i]['JOB_DONE'];
$aborted_tot += $wmsAggregated[$i]['JOB_ABORTED'];
$wmp_in_col_tot += $wmsAggregated[$i]['WMP_in_col'];
}

echo "<tr class=\"total_row\">";
echo "<td>TOTAL</td>";
echo "<td>".$wmp_in_tot."</td>";
echo "<td>".$wm_in_res_tot."</td>";
echo "<td>".$jc_out_tot."</td>";
echo "<td>".$done_tot."</td>";
echo "<td>".$aborted_tot."</td>";
echo "<td>".$wmp_in_col_tot."</td>";
echo "</tr>";

echo "</table>";

} else {
echo "<div class='no_data'>No data available for the chosen period!</div>";
}

}
?>

</body>
</html>
