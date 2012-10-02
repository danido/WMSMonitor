<?php
session_start();
include "../common/header.inc";
include '../details/php-ofc-library/open_flash_chart_object.php';
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d");
$_SESSION['selectedWMS'] = isset($_GET['checkWMS']) ? $_GET['checkWMS'] : '';
$selectedWMS=$_SESSION['selectedWMS'];
?>

<div class="banner main">
<?php
        echo "<div><a title=\"Click to go to the main page\" href=\"../main/main.php\"><img src=\"../common/icon/logo.jpg\"></img></a></div>";
        echo "<ul id=\"nav\">";
                echo "<li><a href=\"../main/main.php\" class=\"selected_item\">WMS view</a>";
                        echo "<ul>";
                                echo "<li><a href=\"../main/main.php\">Overview</a></li>";
                                echo "<li><a href=\"../details/metric_all_wms.php\" class=\"selected_item\">Load balancing</a></li>";
                        echo "</ul>";
                echo "</li>";
                echo "<li><a href=\"../main/vo_overview.php?view_type=table\">VO view</a>";
                        echo "<ul>";
                                echo "<li><a href=\"../main/vo_overview.php?view_type=table\">Table</a></li>";
                                echo "<li><a href=\"../main/vo_overview.php?view_type=chart\">Charts</a></li>";
                                echo "<li><a href=\"../details/ce_mm.php\">Resource usage</a></li>";
                        echo "</ul>";
                echo "</li>";
?>
                <li><a href="https://twiki.cnaf.infn.it/cgi-bin/twiki/view/WMSMonitor/WebDocumentation">Documentation</a></li>
                <li><a href="https://twiki.cnaf.infn.it/cgi-bin/twiki/view/WMSMonitor/WebAbout">Credits</a></li>
        </ul>
</div>

<div class="breadcrumb">
	<a title="Click to go to the main page" href="../main/main.php">WMSMonitor Main</a> >> WMS view >> Load balancing
</div>

<?php
echo "<table class=\"details charts\"><tr><td>";
echo "<tr class=\"supertitle chart_form\">";
echo "<td class=\"form_subtitle\" colspan=\"2\">";

echo "<form class=\"inline\" action=\"metric_all_wms.php\" method=\"get\" name=\"chartForm\">";
echo "   From: ";
echo "<input type=\"text\" size=\"10\" value=\"".$startDate."\" readonly name=\"startDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].startDate,'yyyy-mm-dd',this)\">";
echo " To: ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";

$wmsList = getWMSList('all','all','all','all');
echo "<table class=\"checklist\"><tr>";
echo "<td>WMS:</td></tr><tr>";
echo "<td><ul class=\"customchecklist lb\">";
        echo "<li>";
                foreach ($wmsList as $value) {
                	echo "<input type=\"checkbox\" name=\"checkWMS[$value]\" value=\"".$value."\""; if (isset($selectedWMS[$value])) {echo "checked";} echo "/>$value<br />";
                }
        echo "</li>";
echo "</ul></td></tr></table>";

echo "<input type=\"submit\" value=\"Submit\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";
echo "<tr><td>";

echo "<div id=\"open_flash_chart\">";
$_SESSION['chartData'] = getVOMetricData($wmsList, $startDate, $endDate);
$chartData = $_SESSION['chartData'];
$_SESSION['step'] = getCustomXaxisSteps($startDate, $endDate);

open_flash_chart_object( 800, 600, 'https://'. $_SERVER['SERVER_NAME'] .':8443/'.$config->wmsmonWebDir.'/details/chart_metric_all_wms.php?startDate='.$startDate.'&endDate='.$endDate, false );

echo "</div>";
echo "</td></tr></table>";
?>
