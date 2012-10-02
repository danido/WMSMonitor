<?php

include "/var/www/html/wmsmon/common/functions.php";
$chartData=getChartData($_GET['wms'], $_GET['interval']);
$step=getXaxisSteps($_GET['interval']);

$test = array();
$a = array();
$date1 = array();
$date1_epoch = array();

$max = 0;

for ($i=0; $i<sizeof($chartData); $i++) {
	$test["date"][$i]=$chartData[$i][2];
	$test["running"][$i]=$chartData[$i][0];
	$test["current"][$i]=$chartData[$i][1];
	if ($test["running"][$i] == '') {
		$test["running"][$i] = 'null';
	}
	if ($test["current"][$i] == '') {
                $test["current"][$i] = 'null';
        }
	
	if ($max < $chartData[$i][0]) { 
		$max = $chartData[$i][0];
	}
	if ($max < $chartData[$i][1]) {
                $max = $chartData[$i][1];
        }
}

//$max_y = ceil($max/1000)*1000;

$upper=3;
$perc_upper=1.00;
if (log10($max)>1) {
   $max_temp=$max/pow(10, (floor(log10($max)-1)));
   $max_y=ceil($perc_upper*$max_temp/$upper)*$upper;
   $max_y=$max_y*pow(10, (floor(log10($max)-1)));
} else {
   $max_temp=$max*pow(10, ceil(-log10($max)+1));
   $max_y=ceil($perc_upper*$max_temp/$upper)*$upper;
   $max_y=$max_y*pow(10, floor(log10($max)-1));
}

include_once( 'php-ofc-library/open-flash-chart.php' );

for ($i=0; $i<sizeof($chartData); $i++) {
$date1[$i]=$test["date"][$i];
$date1_epoch[$i] = mktime(intval(substr($date1[$i], 11, 2)), intval(substr($date1[$i], 14, 2)), intval(substr($date1[$i], 17, 2)), intval(substr($date1[$i], 5, 2)), intval(substr($date1[$i], 8, 2)), intval(substr($date1[$i], 0, 4)));
       $a[] = new point(intval($date1_epoch[$i]/10),$test["running"][$i],1);
//	$a[] = new point(2,3,4);
}

$g = new graph();

//$g->set_data( $test["running"] );
//$g->line( 3, '#9933CC', 'Running jobs', 10 );

//$g->set_data( $test["current"] );
//$g->line( 2, '#50CC33', 'Current jobs', 10 );

$g->scatter( $a, 3, '#736AFF', 'My Dots', 12 );


//if ($max != 0) {
//        $g->set_y_max( $max_y );
//} else {
//        $g->set_y_max( 1 );
//}
//$g->y_label_steps( 3 );
//$g->set_y_label_style( 9, '#000000' );

//$g->set_x_labels( $test["date"] );
//$g->set_x_axis_steps( $step );
//$g->set_x_label_style( 9, '#000000', 2, $step );

//$g->set_x_legend( 'Time', 9, '#000000' );

$g->set_tool_tip( 'x:#x_label#<br>y:#val#' );
//
//

//$g->set_x_offset( false );

$g->set_y_label_style( 10, '#9933CC' );
$g->y_label_steps(10);

$g->set_x_label_style( 10, '#9933CC', 2, 800 );
$g->set_x_axis_steps(800);

//$g->set_x_legend( '中文,中文&-%-"-£-+-=' );

$g->set_y_min( 0 );
$g->set_y_max( 3000 );
/*
$g->set_x_min( mktime(intval(substr($test["date"][0], 11, 2)), intval(substr($test["date"][0], 14, 2)), intval(substr($test["date"][0], 17, 2)), intval(substr($test["date"][0], 5, 2)), intval(substr($test["date"][0], 8, 2)), intval(substr($test["date"][0], 0, 4))) );
$g->set_x_max( mktime(intval(substr($test["date"][sizeof($chartData)], 11, 2)), intval(substr($test["date"][sizeof($chartData)], 14, 2)), intval(substr($test["date"][sizeof($chartData)], 17, 2)), intval(substr($test["date"][sizeof($chartData)], 5, 2)), intval(substr($test["date"][sizeof($chartData)], 8, 2)), intval(substr($test["date"][sizeof($chartData)], 0, 4))) );
*/
$g->set_x_min( 120031000 );
$g->set_x_max( 120042000 );

echo $g->render();
?>
