<?php
include "../common/functions.php";

$chart_type = $_SESSION['chart_type'];
$test = array();
$max = 0;
$emptyChart = 'true';

if (sizeof($chartData) != 0) {
for ($i=0; $i<sizeof($chartData); $i++) {
	if ($chart_type=='current') {
        	$test["date"][$i]=substr($chartData[$i]["date"], 5, -3);
	} else {
		$test["date"][$i]=substr($chartData[$i]["date"], 5, 5);
	}
        foreach ($metrics as $value) {
		if ($chartData[$i][$value] == '') {
			if ($i==0) {
				$test[$value][$i] = floatval(0.00);
			} else { 
                		$test[$value][$i] = null;
			}
               	} else {
	                $test[$value][$i]=floatval($chartData[$i][$value]);
		}

        	if ($test[$value][$i] != null || $test[$value][$i]==0) {
                	$emptyChart = 'false';
        	}

		if ($max < $chartData[$i][$value]) {
                	$max = $chartData[$i][$value];
		}
        }
}
}


if ($max == 0) {
	$max = 1;
}

include_once( 'php-ofc-library/open-flash-chart.php' );
$g = new open_flash_chart();
$title = new title( $title_string );
$g->set_title( $title );
$offset=false;

if ($emptyChart == 'false') {
	$line=array();
	$line_default_dot=array();
	$i = 0;
	foreach ($metrics as $value) {
		$line_default_dot[$i] = new dot();
		$line_default_dot[$i]->colour($colors[$i]);
		$line_default_dot[$i]->tooltip( "#x_label#<br>".$metrics[$i].": #val#<br>" );
		$line[$i] = new line();
		$line[$i]->set_default_dot_style($line_default_dot[$i]);
		$line[$i]->set_values( $test[$value] );
		$line[$i]->colour = $colors[$i];
		$line[$i]->set_width( sizeof($metrics)-$i );
		$line[$i]->set_key( $value, 11 );

		$g->add_element( $line[$i] );
		$i++;
	}

	$x_labels = new x_axis_labels();
	$x_labels->set_steps( $step );
	$x_labels->rotate(-30);
	$x_labels->set_labels( $test["date"] );

	include('chart_config.inc');
} else {
        include('chart_nodata.inc');
}

echo $g->toPrettyString();
?>
