<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['ceStatsData'];
$best_limit = isset($_GET['best_limit']) ? $_GET['best_limit'] : 10;
$variable = isset($_GET["variable"]) ? $_GET["variable"] : "Jobs_done";

include "../common/functions.php";

$test = array();

$max = 0;
$emptyChart = 'true';

include_once( 'php-ofc-library/open-flash-chart.php' );

$title = $best_limit.' most active users - '.$variable;
$title = new title( $title );

$g = new open_flash_chart();
$g->set_title( $title );

$bar = new bar_sketch('#FFFF00','#8B6508',5);
$bar_values=array();

for ($i=0; $i<$best_limit; $i++) {
	if ($chartData[$i][$variable]!='') {
		$test[$variable][$i]=floatval($chartData[$i][$variable]);
	} else {
		$test[$variable][$i]=null;
	}
	$test["dn"][$i]=$chartData[$i]["dn"];
	$test["cn"][$i]=guess_name($test["dn"][$i]);       

	if (is_null($test["dn"][$i])) {
                $test["dn"][$i] = null;
        }
//        if ($test[$variable][$i]=='') {
  //              $test[$variable][$i] = 0;
    //    }

        if ($max < $test[$variable][$i]) {
                $max = $test[$variable][$i];
        }

        if ($test[$variable][$i] != null) {
                $emptyChart = 'false';
	}

	if (strlen($test["dn"][$i]) > 83) {
		$dn_1 = substr($test["dn"][$i], 0, 83);
		$dn_2 = substr($test["dn"][$i], 83, 80);
		$tip[$i] = $variable.': '.$test[$variable][$i].'<br>'.$dn_1.'<br>'.$dn_2;
	} else {
		$tip[$i] = $variable.': '.$test[$variable][$i].'<br>'.$test["dn"][$i];
	}

	$bar_values[$i] = new bar_value($test[$variable][$i]);
	$bar_values[$i]->set_tooltip( $tip[$i] );
}

//echo $max;

if ($emptyChart == 'false') {
	$bar->set_values( $bar_values );
	$bar->set_on_show(new bar_on_show('grow-up', 0.1, 0.1));
	$font_size = ($best_limit > 50) ? 8 : 12;
	$x_labels = new x_axis_labels();
        $x_labels->set_vertical();
        $x_labels->set_labels( $test["cn"] );
        $x_labels->set_size( $font_size );

	$offset=true;

	$y_axis_legend=$variable;

	$max_y = getYaxisMaxValue($max, 3, 1.00);
//	if ($max!=0) {
//		$max_y = getYaxisMaxValue($max, 3, 1.00);
//	} else {
//		$max_y = 0;
//	}

	$x = new x_axis();
	$x->set_offset( $offset );
	$x->set_labels( $x_labels );

	$y = new y_axis();
	$y->set_range( 0, $max_y, $max_y/5);

	$x_legend = new x_legend( 'User name' );
	$x_legend->set_style( '{font-size: 11px; color: #000000}' );

	$y_axis_legend=$variable;
	$y_legend = new y_legend( $y_axis_legend );
	$y_legend->set_style( '{font-size: 11px; color: #000000}' );

	$g->set_x_axis( $x );
	$g->set_y_axis( $y );
	$g->set_x_legend( $x_legend );
	$g->set_y_legend( $y_legend );
	$g->set_bg_colour( '#EEEEEE' );

} else {
	include('chart_nodata.inc');
}

$g->add_element( $bar );
echo $g->toPrettyString();
?>
