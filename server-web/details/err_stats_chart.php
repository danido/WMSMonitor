<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['ceStatsData'];
//$step = $_SESSION['step'];
$best_limit = isset($_GET['best_limit']) ? $_GET['best_limit'] : 10;

include "../common/functions.php";

$test = array();

$max = 0;
$emptyChart = 'true';



include_once( 'php-ofc-library/open-flash-chart.php' );

$title = $best_limit.' most frequent errors';
$title = new title( $title );

$g = new open_flash_chart();
$g->set_title( $title );

$bar = new bar_sketch('#FFFF00','#8B6508',5);
$bar_values=array();

for ($i=0; $i<$best_limit; $i++) {
	$test["occurrence"][$i]=$chartData[$i]["occurrence"];
	$test["error_string_long"][$i]=$chartData[$i]["error_string"];
	$test["error_string"][$i]=substr($test["error_string_long"][$i], 0, 70);
	$test["error_string_remaining"][$i]=substr($test["error_string_long"][$i], 70);
 
	if (is_null($test["error_string"][$i])) {
                $test["error_string"][$i] = 'null';
        }
        if (is_null($test["occurrence"][$i])) {
                $test["occurrence"][$i] = 'null';
        }

        if ($max < $test["occurrence"][$i]) {
                $max = $test["occurrence"][$i];
        }

        if ($test["error_string"][$i] != 'null' || $test["occurrence"][$i] != 'null') {
                $emptyChart = 'false';
        }

	$tip[$i] = $test["occurrence"][$i].' occurrences<br>'.$test["error_string"][$i].'<br>'.$test["error_string_remaining"][$i];
	$bar_values[$i] = new bar_value($test["occurrence"][$i]);
        $bar_values[$i]->set_tooltip( $tip[$i] );

}

$bar->set_values( $bar_values );
$bar->set_on_show(new bar_on_show('grow-up', 0.1, 0.1));


if ($emptyChart == 'false') {
        $font_size = ($best_limit > 50) ? 8 : 12;
        $x_labels = new x_axis_labels();
        $x_labels->set_vertical();
        $x_labels->set_labels( $test["error_string"] );
        $x_labels->set_size( $font_size );

        $offset=true;

        $max_y = getYaxisMaxValue($max, 3, 1.00);

        $x = new x_axis();
        $x->set_offset( $offset );
        $x->set_labels( $x_labels );

        $y = new y_axis();
        $y->set_range( 0, $max_y, $max_y/5);

        $x_legend = new x_legend( 'Error' );
        $x_legend->set_style( '{font-size: 11px; color: #000000}' );

        $y_axis_legend='Occurrences';
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
