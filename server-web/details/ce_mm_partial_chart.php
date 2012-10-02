<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartData'];
$step = 0;
$offset = true;
$limit_from = $_GET['limit_from'];
$limit_to = $_GET['limit_to'];

include "../common/functions.php";

$test = array();

$max = 0;
$emptyChart = 'true';

$bin = ceil(sizeof($chartData)/10);

$y=0;
for ($i=$limit_from; $i<=$limit_to; $i++) {
	$test["num_ce"][$y]=strval($i);
        $test["occurrence"][$y]=intval($chartData[$i]);
        if (is_null($test["num_ce"][$y])) {
                $test["num_ce"][$y] = null;
        }
        if (is_null($test["occurrence"][$y])) {
                $test["occurrence"][$y] = null;
        }

        if ($max < $test["occurrence"][$y] && $test["occurrence"][$y] != null) {
                $max = $test["occurrence"][$y];
        }

        if ($test["occurrence"][$y] != null) {
                $emptyChart = 'false';
        }
	$y++;
}

include_once( 'php-ofc-library/open-flash-chart.php' );

$title = new title( 'CE Matchmaking (From '.$limit_from.' to '.$limit_to.' matched CEs)' );
$g = new open_flash_chart();
$g->set_title( $title );
$bar = new bar_filled('#3334AD', '#191970');
$bar->set_tooltip( "#x_label# CEs matched<br>#val# times" );

$max_y = getYaxisMaxValue($max, 3, 1.00);
if ($emptyChart == 'false') {
        $bar->set_values( $test["occurrence"] );

        $x_labels = new x_axis_labels();
	$x_labels->set_labels( $test["num_ce"] );

	$x_axis_legend='Number of matched CEs';
        $y_axis_legend='Occurrences';

        include('chart_config.inc');
} else {
        include('chart_nodata.inc');
}

$g->add_element( $bar );
echo $g->toPrettyString();
?>
