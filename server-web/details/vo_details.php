<?php

$view_type = isset($_GET['view_type']) ? $_GET['view_type'] : 'chart';
$selected_type = ($view_type == 'chart') ? 'Charts' : 'Table';
$vo = isset($_GET['vo']) ? $_GET['vo'] : 'cms';

if ($view_type=='table') {
	$selectedId = array("VO_view","Single_VO","Single_VO_Table","Table-".$vo);
} else if ($view_type=='chart') {
	$selectedId = array("VO_view","Single_VO","Single_VO_Charts","Charts-".$vo);
}
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d", time()-(6*86400));

$voRepl = str_replace(".", "-", $vo);
$nameSession = 'vo_details'.$voRepl.$startDate.$endDate;

session_name($nameSession);
session_start();

include "../common/header.inc";
include "../common/banner.inc";

$wmsAggregated=getWMSUsageChartLBDailyDataByUsers($vo, $startDate, $endDate);
?>

<div class="breadcrumb">
<?php
	echo "<a title=\"Click to go to the main page\" href=\"../main/main.php\">WMSMonitor</a> >> VO view >> Single VO >> ".$selected_type."::".$vo;
?>
</div>

<div class="breadcrumb">
Select
<?php
echo "<form class=\"inline\" action=\"vo_details.php\" method=\"get\" name=\"mainForm\">";
echo "<input type=\"hidden\" name=\"view_type\" value=\"".$view_type."\"/>";
echo "<input type=\"hidden\" value=\"".$startDate."\" name=\"startDate\"/>";
echo "<input type=\"hidden\" value=\"".$endDate."\" name=\"endDate\"/>";
echo "<select name=\"vo\">";
$voList = getVOList();
foreach ($voList as $value) {
        if ($value != 'multiVO') {
                echo "<option value=\"".$value."\" ";
                if ($vo == $value) {echo "selected=selected";}
                echo ">".$value."</option>";
        } else {
                $is_there_multi=1;
        }
}
echo "</select>";
echo " VO data ";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
?>
</div>

<?php
if ($view_type == 'chart') {

echo "<table class=\"details charts\">";
echo "<tr class=\"supertitle\">";
echo "<td class=\"form_subtitle\" colspan=\"3\">From ";

echo "<form class=\"inline\" action=\"vo_details.php\" method=\"get\" name=\"chartForm\">";
echo "<input type=\"hidden\" name=\"vo\" value=\"".$vo."\"/>";
echo "<input type=\"hidden\" name=\"view_type\" value=\"".$view_type."\"/>";
echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[1].startDate,'yyyy-mm-dd',this)\">";
echo "    to ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[1].endDate,'yyyy-mm-dd',this)\">";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";

$_SESSION['chartData']=getAggregatedChartLBDailyDataByUsers($vo, $startDate, $endDate);
$_SESSION['step']=getXaxisAggregatedSteps($startDate, $endDate);

$chartData = $_SESSION['chartData'];

$_SESSION['pieDataWMS']=getWMSUsageChartLBDailyDataByUsers($vo, $startDate, $endDate);

include 'php-ofc-library/open-flash-chart-object.php';

$url_parameters='vo='.$vo.'%26startDate='.$startDate.'%26endDate='.$endDate.'%26nameSession='.$nameSession;
$url_1='../details/vo_chart_1.php?'.$url_parameters.'%26variable=final_state';
$url_2='../details/vo_chart_1.php?'.$url_parameters.'%26variable=sub_jss';
$url_3='../details/vo_chart_2.php?'.$url_parameters.'%26variable=JOB_DONE';
$url_4='../details/vo_chart_2.php?'.$url_parameters.'%26variable=JOB_ABORTED';
$url_5='../details/vo_chart_2.php?'.$url_parameters.'%26variable=WMP_in';
$url_6='../details/vo_chart_2.php?'.$url_parameters.'%26variable=JC_out';
?>

<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_1",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_1;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_1_2",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_2;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2",
  "295", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_3;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2_2",
  "295", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_4;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2_3",
  "295", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_5;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "vo_chart_2_4",
  "295", "255", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_6;?>"} );
</script>

<tr><td><div id="vo_chart_1"></div></td><td><div id="vo_chart_2"></div></td><td><div id="vo_chart_2_2"></div></td></tr>
<tr><td><div id="vo_chart_1_2"></div></td><td><div id="vo_chart_2_3"></div></td><td><div id="vo_chart_2_4"></div></td></tr>
<table>

<?php

} else {
echo "<table class=\"aggregated form\">";

echo "<tr class=\"supertitle\">";
echo "<td class=\"form_subtitle\" colspan=\"5\">From ";

echo "<form class=\"inline\" action=\"vo_details.php\" method=\"get\" name=\"chartForm\">";
echo "<input type=\"hidden\" name=\"vo\" value=\"".$vo."\"/>";
echo "<input type=\"hidden\" name=\"view_type\" value=\"".$view_type."\"/>";
echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[1].startDate,'yyyy-mm-dd',this)\">";
echo "    to ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[1].endDate,'yyyy-mm-dd',this)\">";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
echo "</td>";
echo "</tr></table>";

echo "<table class=\"aggregated\"><tr class=\"title\">";
echo "<td class=\"wms_column\" title=\"WMS hostname\">WMS</td>";
echo "<td title=\"Number of jobs submitted to WMProxy\">SUBMITTED</td>";
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
	echo "<td class=\"wms_column\" title=\"Click for more details on ".$wmsAggregated[$i]['wms']."\"><a href=\"../details/details.php?wms=".$wmsAggregated[$i]['wms']."\">".$wmsAggregated[$i]['wms']."</a></td>";
        echo "<td>".$wmsAggregated[$i]['WMP_in']."</td>";
	echo "<td>".$wmsAggregated[$i]['JC_in']."</td>";
	echo "<td>".$wmsAggregated[$i]['JOB_DONE']."</td>";
	echo "<td>".$wmsAggregated[$i]['JOB_ABORTED']."</td>";
	echo "<td>".$wmsAggregated[$i]['WMP_in_col']."</td>";
echo "</tr>";
$wmp_in_tot += $wmsAggregated[$i]['WMP_in'];
$jc_in_tot += $wmsAggregated[$i]['JC_in'];
$done_tot += $wmsAggregated[$i]['JOB_DONE'];
$aborted_tot += $wmsAggregated[$i]['JOB_ABORTED'];
$wmp_in_col_tot += $wmsAggregated[$i]['WMP_in_col'];
}

echo "<tr class=\"total_row\">";
echo "<td>TOTAL</td>";
echo "<td>".$wmp_in_tot."</td>";
echo "<td>".$jc_in_tot."</td>";
echo "<td>".$done_tot."</td>";
echo "<td>".$aborted_tot."</td>";
echo "<td>".$wmp_in_col_tot."</td>";
echo "</tr>";

echo "</table>";
}
?>


</body>
</html>
