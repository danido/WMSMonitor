<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartDailyData'];
$step = $_SESSION['stepDaily'];
$custom = $_SESSION['customDaily'];

include "../common/functions.php";

$test = array();
$p = array();

$max = 0;
$emptyChart = 'true';

for ($i=0; $i<sizeof($chartData); $i++) {
        $test["date"][$i]=substr($chartData[$i]["date"], 5, 5);

        foreach ($custom as $key => $value) {
                if (isset($custom[$key])) {
                        $test[$key][$i]=$chartData[$i][$key];
                        if ($test[$key][$i] == '') {
                               $test[$key][$i] = 'null';
                        }
                }
		if ($max < $chartData[$i][$key]) {
                	$max = $chartData[$i][$key];
        	}
        
        if ($test[$key][$i] != 'null') {
                $emptyChart = 'false';
        }
	}
}

include_once( 'php-ofc-library/open-flash-chart.php' );
$g = new graph();
//$g->title( 'Customized chart', '{font-size: 11px; font-weight: bold; color: #000000; margin: 2px 2 2px 2;}');

$colors = array('#d01f3c','#356aa0','#C79810','#32CD32','#FFA07A','#838B83','#EE799F','#9932CC','#8B6508','#404040','#FFFF00');

if ($emptyChart == 'false') {
	$max_y = getYaxisMaxValue($max, 3, 1.00);

	$i = 0;
	foreach ($custom as $key => $value) {
		$g->set_data( $test[$key] );
		$g->line( sizeof($custom)-$i, $colors[$i], $key, 10 );
		$i++;
	}

	$g->set_y_legend( 'Number', 11, '#000000' );
	$g->set_x_labels( $test["date"] );
	$g->set_x_offset( false );
	
	include('chart_config.inc');

} else {
	include('chart_nodata.inc');
}

echo $g->render();
?>
