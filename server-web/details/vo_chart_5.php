<?php
$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$aggregation = isset($_GET['aggregation']) ? $_GET['aggregation'] : 'WMS';
$pieData = $_SESSION['pieData'.$aggregation];

include "../common/functions.php";

$test = array();
$data = array();
$links = array();

for( $i=0; $i<sizeof($pieData); $i++ ) {
    $data[] = $pieData[$i][3];
    $test["wms"][]=$pieData[$i][0];
    if ($aggregation == 'WMS') {
        $links[] = "../details/details.php?wms=".$test["wms"][$i];
    } else {
        $links[] = "../details/vo_details.php?vo=".$test["wms"][$i];
    }
}

include_once( 'php-ofc-library/open-flash-chart.php' );
$g = new graph();

$g->bg_colour = '#EEEEEE';
$g->pie(60,'#EEEEEE','{display:none;}',false,1);
$g->pie_values( $data, $test["wms"], $links );
$g->pie_slice_colours( array('#d01f3c','#356aa0','#C79810','#32CD32','#FFA07A','#838B83','#EE799F','#9932CC','#8B6508','#404040','#FFFF00') );
$g->set_tool_tip( $aggregation. ': #x_label#<br>Submitted jobs: #val#' );

$g->title( 'Submitted Jobs per '.$aggregation, '{font-size: 11px; color: #000000; margin: 2px 2 2px 2;}');

echo $g->render();
?>
