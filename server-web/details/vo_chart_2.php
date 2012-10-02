<?php
$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$aggregation = isset($_GET['aggregation']) ? $_GET['aggregation'] : 'WMS';
$pieData = $_SESSION['pieData'.$aggregation];
$variable = isset($_GET["variable"]) ? $_GET["variable"] : "JOB_DONE";

switch ($variable) {
        case 'JOB_DONE':
                $variableDisplay='Jobs Done';
                break;
        case 'JOB_ABORTED':
                $variableDisplay='Jobs Aborted';
                break;
        case 'WMP_in':
                $variableDisplay='Submitted Jobs';
                break;
        case 'JC_out':
                $variableDisplay='JSS Jobs';
                break;
}


include "../common/functions.php";

$test = array();
$data = array();
$links = array();
$d = array();

include_once( 'php-ofc-library/open-flash-chart.php' );
$g = new open_flash_chart();
$title_string = $variableDisplay.' per '.$aggregation;
$title = new title( $title_string );
$g->set_title( $title );
$g->set_bg_colour( '#EEEEEE' );

$protocol = $_SERVER['HTTPS'] != "on" ? "http://" : "https://";

for( $i=0; $i<sizeof($pieData); $i++ ) {
    $data[] = floatval($pieData[$i][$variable]);
//    $test["wms"][]=$pieData[$i]['vo'];
    if ($aggregation == 'WMS') {
	$test["wms"][]=$pieData[$i]['wms'];
        $links[] = $protocol.$_SERVER['HTTP_HOST']."/".$config->wmsmonWebDir."details/details.php?wms=".$test["wms"][$i];
    } else {
	$test["wms"][]=$pieData[$i]['vo'];
        $links[] = $protocol.$_SERVER['HTTP_HOST']."/".$config->wmsmonWebDir."details/vo_details.php?vo=".$test["wms"][$i];
    }
    $d[] = new pie_value(floatval($pieData[$i][$variable]), $test["wms"][$i]);
    $d[$i]->on_click($links[$i]);
}

$pie = new pie();
$pie->set_alpha(0.6);
$pie->set_start_angle( 35 );
$pie->add_animation( new pie_fade() );
$pie->add_animation( new pie_bounce(4) );
$pie->set_tooltip( '#label#<br>'.$variableDisplay.': #val# of #total#<br>#percent#' );
$pie->set_colours( array('#d01f3c','#356aa0','#C79810','#32CD32','#FFA07A','#838B83','#EE799F','#9932CC','#8B6508','#404040','#FFFF00') );
$pie->set_values( $d );
$pie->set_no_labels();
$g->add_element( $pie );

echo $g->toPrettyString();
?>
