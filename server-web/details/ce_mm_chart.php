<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartData'];
//$step = $_SESSION['step'];
$step = 0;
$offset = true;

include "../common/functions.php";

$test = array();

$max = 0;
$emptyChart = 'true';

$bin = ceil(sizeof($chartData)/10);

include_once( 'php-ofc-library/open-flash-chart.php' );
$title = new title( 'CE Matchmaking - All matched CEs' );
$g = new open_flash_chart();
$g->set_title( $title );
$bar = new bar_filled('#9933CC', '#8010A0');

$end=ceil(sizeof($chartData)/10)*10-1;

$test["occurrence_aggr"]=0;
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
                $test["num_ce"][$i] = null;
        }
        if (is_null($test["occurrence"][$i])) {
                $test["occurrence"][$i] = null;
        }

        if ($test["num_ce"][$i] != null || $test["occurrence"][$i] != null) {
                $emptyChart = 'false';
        }

	if (isset($test["occurrence_aggr_ok"][$i])) {
		if ($max < $test["occurrence_aggr_ok"][$i]) {
         	       $max = $test["occurrence_aggr_ok"][$i];
        	}
		$bar_values[$i] = new bar_value($test["occurrence_aggr_ok"][$i]);
		$bar_values[$i]->{'on-click'} = "partialHistogram($bin, $end, $i)";
	}

}

$max_num_ce=$i;
$max_y = getYaxisMaxValue($max, 3, 1.00);
if ($emptyChart == 'false') {
	$bar->set_values( array_values($bar_values) );
	$bar->set_tooltip( "#x_label# CEs matched <br>#val# times" );

	$x_labels = new x_axis_labels();
        $x_labels->set_labels( array_values($test["num_ce_aggr_ok"]) );

	$x_axis_legend='Number of matched CEs (intervals)';
	$y_axis_legend='Occurrences';

	include('chart_config.inc');
} else {
        include('chart_nodata.inc');
}

$g->add_element( $bar );
echo $g->toPrettyString();
?>
