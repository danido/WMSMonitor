<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
$chart_type = isset($_GET['chart_type']) ? $_GET['chart_type'] : 'current';
session_name($nameSession);
session_start();
if ($chart_type=='current') {
	$chartJobData = $_SESSION['chartJobData'];
	$customRates = $_SESSION['customRates'];
}
$step = $_SESSION['step'];
$customAll = $chart_type=='daily' ? $_SESSION['customDailyRates'] : $_SESSION['customAll'];
$chartAllData = $chart_type=='daily' ? $_SESSION['chartDailyData'] : $_SESSION['chartAllData'];

include "../common/functions.php";

$test = array();
$max = 0;
$min = 0;
$maxRates = 0;
$emptyChart = 'true';

if (sizeof($chartAllData) > 1) {
for ($i=0; $i<sizeof($chartAllData); $i++) {
        $test["date"][$i] = $chart_type=='daily' ? substr($chartAllData[$i]["date"], 5) : substr($chartAllData[$i]["date"], 5, -3);
        if (sizeof($customAll) != 0 && $customAll != '') {
        foreach ($customAll as $value) {
                $test[$value][$i]=floatval($chartAllData[$i][$value]);
                if ($max < $chartAllData[$i][$value]) {
                        $max = $chartAllData[$i][$value];
                }
		if ($test[$value][$i] != '' && $min > $test[$value][$i]) {
                        $min = $test[$value][$i];
                }
		if ($test[$value][$i] != 'null') {
         	       $emptyChart = 'false';
        	}
        }

	}
}
}

if (sizeof($chartJobData) > 1) {
for ($i=0; $i<sizeof($chartJobData); $i++) {
	if (sizeof($customRates) != 0 && $customRates != '') {
        foreach ($customRates as $value) {
                if (isset($value) && $value!='date') {
			if (isset($customRates[$i]['deltat'])) {
				if ((!(is_null($chartJobData[$i]['deltat']))) && (!(is_null($chartJobData[$i][$value]))) && ($chartJobData[$i]['deltat'] != 0)) {
                        		$testRates[$value][$i]=floatval($chartJobData[$i][$value])/floatval($chartJobData[$i]['deltat']);
                        	} else {
					$testRates[$value][$i] = 'null';
				}
			} else {
				if (!(is_null($chartJobData[$i][$value]))) {
					$testRates[$value][$i]=floatval($chartJobData[$i][$value]);
				} else {
					$testRates[$value][$i] = 'null';
				}	
			}
                }
                if (!(isset($chartJobData[$i]['deltat'])) || (($chartJobData[$i]['deltat'] != 0) && ($maxRates < $testRates[$value][$i]))) {
                       	$maxRates = $testRates[$value][$i];
               	}
        }
	
        if ($testRates[$value][$i] != 'null') {
                $emptyChart = 'false';
        }
	}
}
}

include_once( 'php-ofc-library/open-flash-chart.php' );

$g = new open_flash_chart();
$offset=false;

$colors = array('#d01f3c','#356aa0','#C79810','#32CD32','#FFA07A','#838B83','#EE799F','#9932CC','#8B6508','#404040','#FFFF00');

if ($emptyChart == 'false') {
//	$max_y = getYaxisMaxValue($max, 3, 1.00);
//	$maxRates_y = getYaxisMaxValue($maxRates, 3, 1.00);
//	$min_y = getYaxisMaxValue((-1*$min), 3, 1.00);
  //      $min_y = -1*$min_y;

	$line=array();
	$line_default_dot=array();

	$j = 0;
	if (sizeof($customAll) > 0) {
		$max_y = getYaxisMaxValue($max, 3, 1.00);
		$min_y = getYaxisMaxValue((-1*$min), 3, 1.00);
        	$min_y = -1*$min_y;
        	foreach ($customAll as $value) {
			$line_default_dot[$j] = new dot();
                	$line_default_dot[$j]->colour($colors[$j]);
			$line_default_dot[$j]->tooltip( "#x_label#<br>".$customAll[$j].": #val#<br>" );
			$line[$j] = new line();
			$line[$j]->set_default_dot_style($line_default_dot[$j]);
                	$line[$j]->set_values( $test[$value] );
			$line[$j]->colour = $colors[$j];
			$line[$j]->set_width( sizeof($customAll)+sizeof($customRates)-$j );
			if ($value == 'Sandbox partition' || $value == '/var/log partition' || $value == '/var/lib/mysql part.') {
                		$line[$j]->set_key( $value.'(Percentage)', 11 );
			} else {
				if ($chart_type=='current') {
					$line[$j]->set_key( $value.'(Number)', 11 );
				} else {
					$line[$j]->set_key( $value, 11 );
				}
			}
			$g->add_element( $line[$j] );
                	$j++;
        	}
	}

	$z = (sizeof($customAll) > 0) ? $j : 0;
	$k = 0;
//	if (sizeof($customRates) > 0) {
	if (sizeof($chartJobData) > 1) {
		$maxRates_y = getYaxisMaxValue($maxRates, 3, 1.00);
        	foreach ($customRates as $value) {
                	$line_default_dot[$z] = new dot();
                	$line_default_dot[$z]->colour($colors[$z]);
			$line_default_dot[$z]->tooltip( "#x_label#<br>".$customRates[$k].": #val#<br>" );
                	$line[$z] = new line();
                	$line[$z]->set_values( $testRates[$value] );
			$line[$z]->set_default_dot_style($line_default_dot[$z]);
                	$line[$z]->colour = $colors[$z];
			$line[$z]->set_width( sizeof($customAll)+sizeof($customRates)-$j-$k );
                	$line[$z]->set_key( $value.'(Hz)', 11 );
			if ($j != 0) {
				$line[$z]->attach_to_right_y_axis();
			}
                	$g->add_element( $line[$z] );
                	$k++;
                	$z++;
 		}
	}

	if ($j != 0 || ($j == 0 && $k != 0)) {
		$y = new y_axis();
		$g->set_y_axis( $y );
		$y->set_range( 0, $max_y, $max_y/5);
		$y_axis_legend = ($j!=0) ? $chart_type=='daily' ? 'Number' : 'Number - Percentage' : 'Rate (Hz)';
		$y_legend = new y_legend( $y_axis_legend );
		$y_legend->set_style( '{font-size: 11px; color: #000000}' );
		$g->set_y_legend( $y_legend );
	}

	if (sizeof($chartJobData) > 1) {
	if (($k != 0) && ($j != 0)) {
		$y2 = new y_axis_right();
                $g->set_y_axis_right( $y2 );
                $y2->set_range( 0, $maxRates_y, $maxRates_y/5);
		$y2->set_colour( '#3D5C56' );
		$y2_axis_legend = 'Rate (Hz)';
                $y2_legend = new y2_legend( $y2_axis_legend );
                $y2_legend->set_style( '{font-size: 11px; color: #000000}' );
                $g->set_y2_legend( $y2_legend );
	}
	}

	$x_labels = new x_axis_labels();
        $x_labels->set_steps( $step );
        $x_labels->rotate(-30);
        $x_labels->set_labels( $test["date"] );

	$x = new x_axis();
	$x->set_labels( $x_labels );
	$x->set_offset( $offset );
	$x->set_steps( $step );

	$x_legend = new x_legend( 'Time' );
	$x_legend->set_style( '{font-size: 11px; color: #000000}' );

	$g->set_x_axis( $x );
	$g->set_x_legend( $x_legend );

	$g->set_bg_colour( '#EEEEEE' );
} else {
	include('chart_nodata.inc');
}

echo $g->toPrettyString();
?>
