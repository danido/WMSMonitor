<div class="banner main">
<?php
$scope = isset($scope) ? $scope : 'all';
$host_owner = isset($host_owner) ? $host_owner : 'all';
$service_usage = isset($service_usage) ? $service_usage : 'all';
$vo_group = isset($vo_group) ? $vo_group : 'all';

$wmsList = array();
$voList = array();
$wmsList = getWMSList($scope,$host_owner,$vo_group,$service_usage);
$voList = getVOList();
        echo "<div><a title=\"Click to go to the main page\" href=\"../main/main.php\"><img src=\"../common/icon/logo.jpg\"></img></a></div>";
        echo "<ul id=\"nav\">";
                echo "<li><a href=\"#\" id=\"WMS_view\">WMS view</a>";
                        echo "<ul id=\"nav2_wms\" onmouseover=\"hiddenChart('transparent')\" onmouseout=\"visibleChart('transparent')\">";
                                echo "<li><a href=\"../main/main.php\" id=\"Overview_wms\">Overview</a></li>";
                                echo "<li><a href=\"#\" id=\"Single_instance\">Single instance</a>";
                                        echo "<ul id=\"nav3_wms\" onmouseover=\"hiddenChart('transparent')\" onmouseout=\"visibleChart('transparent')\">";
                                                echo "<li><a href=\"#\" id=\"Details\">Details</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($wmsList); $i++) {
                                                                        echo "<li><a href=\"../details/details.php?wms=".$wmsList[$i]."\" id=\"Details-".str_replace(".", "-", $wmsList[$i])."\">".$wmsList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                                echo "<li><a href=\"#\" id=\"Custom\">Custom charts</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($wmsList); $i++) {
                                                                        echo "<li><a href=\"../details/custom.php?wms=".$wmsList[$i]."\" id=\"Custom-".str_replace(".", "-", $wmsList[$i])."\">".$wmsList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                                echo "<li><a href=\"#\" id=\"Resource_usage_wms\">Resource usage</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($wmsList); $i++) {
                                                                        echo "<li><a href=\"../details/ce_mm.php?aggregation=wms&wms=".$wmsList[$i]."\" id=\"Resource_usage-".str_replace(".", "-", $wmsList[$i])."\">".$wmsList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                                echo "<li><a href=\"#\" id=\"Users_activity_wms\">Users activity</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($wmsList); $i++) {
                                                                        echo "<li><a href=\"../details/users.php?aggregation=wms&wms=".$wmsList[$i]."\" id=\"Users_activity-".str_replace(".", "-", $wmsList[$i])."\">".$wmsList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                                echo "<li><a href=\"#\" id=\"Load_balancing\">Load balancing</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($wmsList); $i++) {
                                                                        echo "<li><a href=\"../details/metric.php?wms=".$wmsList[$i]."\" id=\"Load_balancing-".str_replace(".", "-", $wmsList[$i])."\">".$wmsList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
						echo "<li><a href=\"#\" id=\"Error_stats_wms\">Error stats</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($wmsList); $i++) {
                                                                        echo "<li><a href=\"../details/err_stats.php?aggregation=wms&wms=".$wmsList[$i]."\" id=\"Error_stats-".str_replace(".", "-", $wmsList[$i])."\">".$wmsList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                        echo "</ul>";
                                echo "</li>";
                        echo "</ul>";
		echo "</li>";
                echo "<li><a href=\"#\" id=\"VO_view\">VO view</a>";
                        echo "<ul id=\"nav2_vo\" onmouseover=\"hiddenChart('transparent')\" onmouseout=\"visibleChart('transparent')\">";
                                echo "<li><a href=\"../main/vo_overview.php?view_type=table\" id=\"Overview_vo\">Overview</a>";
                                        echo "<ul id=\"nav3_vo\" onmouseover=\"hiddenChart('transparent')\" onmouseout=\"visibleChart('transparent')\">";
                                                echo "<li><a href=\"../main/vo_overview.php?view_type=table\" id=\"Overview_vo_Table\">Table</a></li>";
                                                echo "<li><a href=\"../main/vo_overview.php?view_type=chart\" id=\"Overview_vo_Charts\">Charts</a></li>";
                                        echo "</ul>";
                                echo "</li>";
                                echo "<li><a href=\"#\" id=\"Single_VO\">Single VO</a>";
                                        echo "<ul id=\"nav3_vo\" onmouseover=\"hiddenChart('transparent')\" onmouseout=\"visibleChart('transparent')\">";
                                                echo "<li><a href=\"#\" id=\"Single_VO_Table\">Table</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($voList); $i++) {
                                                                        echo "<li><a href=\"../details/vo_details.php?view_type=table&vo=".$voList[$i]."\" id=\"Table-".$voList[$i]."\">".$voList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                                echo "<li><a href=\"#\" id=\"Single_VO_Charts\">Charts</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($voList); $i++) {
                                                                        echo "<li><a href=\"../details/vo_details.php?view_type=chart&vo=".$voList[$i]."\" id=\"Charts-".$voList[$i]."\">".$voList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                                echo "<li><a href=\"#\" id=\"Resource_usage_vo\">Resource usage</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($voList); $i++) {
                                                                        echo "<li><a href=\"../details/ce_mm.php?aggregation=vo&vo=".$voList[$i]."\" id=\"Resource_usage-".$voList[$i]."\">".$voList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                                echo "<li><a href=\"#\" id=\"Users_activity_vo\">Users activity</a>";
                                                        echo "<ul>";
                                                                for ($i=0; $i<sizeof($voList); $i++) {
                                                                        echo "<li><a href=\"../details/users.php?aggregation=vo&vo=".$voList[$i]."\" id=\"Users_activity-".$voList[$i]."\">".$voList[$i]."</a></li>";
                                                                }
                                                        echo "</ul>";
                                                echo "</li>";
                                        echo "</ul>";
                                echo "</li>";
                        echo "</ul>";
                echo "</li>";
?>
                <li><a href="http://wiki.italiangrid.it/twiki/bin/view/WMSMonitor/WebDownload3">Documentation</a></li>
                <li><a href="http://wiki.italiangrid.it/twiki/bin/view/WMSMonitor/WebAbout">Credits</a></li>
        </ul>
</div>
