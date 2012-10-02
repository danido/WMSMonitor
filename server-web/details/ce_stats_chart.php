<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['ceStatsData'];
$step = $_SESSION['step'];
$best_limit = isset($_GET['best_limit']) ? $_GET['best_limit'] : 10;
$offset = true;

include "../common/functions.php";

$test = array();

$max = 0;
$emptyChart = 'true';

for ($i=0; $i<$best_limit; $i++) {
	$test["occurrence"][$i]=floatval($chartData[$i]["occurrence"]);

	$test["ce"][$i]=$chartData[$i]["ce"];
  
	if (is_null($test["ce"][$i])) {
                $test["ce"][$i] = null;
        }
        if (is_null($test["occurrence"][$i])) {
                $test["occurrence"][$i] = null;
        }

        if ($max < $test["occurrence"][$i]) {
                $max = $test["occurrence"][$i];
        }

        if ($test["ce"][$i] != null || $test["occurrence"][$i] != null) {
                $emptyChart = 'false';
        }
}

include_once( 'php-ofc-library/open-flash-chart.php' );

$max_y = getYaxisMaxValue($max, 3, 1.00);
$title = new title( $best_limit.' most used CEs' );
$g = new open_flash_chart();
$g->set_title( $title );

$bar = new bar_filled('#FFFF00', '#8B6508');
$bar->set_values( $test["occurrence"] );
$bar->set_tooltip( "#x_label#<br>this CE has been matched #val# times" );

if ($emptyChart == 'false') {
	$font_size = ($best_limit > 50) ? 8 : 12;
        $x_labels = new x_axis_labels();
        $x_labels->set_vertical();
        $x_labels->set_labels( $test["ce"] );
	$x_labels->set_size( $font_size );
	
	$x_axis_legend='CE name';
        $y_axis_legend='Occurrences';

        include('chart_config.inc');
} else {
        include('chart_nodata.inc');
}

$g->add_element( $bar );
echo $g->toPrettyString();
?>
