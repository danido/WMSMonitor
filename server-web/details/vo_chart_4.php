<?php
$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartData'];
$step = $_SESSION['step'];

include "../common/functions.php";

$test = array();

$max = 0;

include_once( 'php-ofc-library/open-flash-chart.php' );

$line_1 = new line( 5, '#EE0000' );
$line_1->key( 'Jobs -> WMProxy', 10 );

$line_2 = new line( 2, '#000080' );
$line_2->key( 'Jobs -> Condor', 10 );

for ($i=sizeof($chartData); $i>=1; $i--) {
	$test["date"][$i]=substr(substr($chartData[$i][2], 5), 0, 5);
	$test["WMP_in"][$i]=$chartData[$i][3];
	$test["JC_out"][$i]=$chartData[$i][4];

	if (is_null($test["WMP_in"][$i])) {
                $test["WMP_in"][$i] = 0;
        }

        if (is_null($test["JC_out"][$i])) {
                $test["JC_out"][$i] = 0;
        }

	if ($max < $chartData[$i][3]) {   
                $max = $chartData[$i][3];
        }
        if ($max < $chartData[$i][4]) {
                $max = $chartData[$i][4];
        }

	$line_1->data[] = $test["WMP_in"][$i];
	$line_2->data[] = $test["JC_out"][$i];
}

$max_y = getYaxisMaxValue($max, 3, 1.00);

$g = new graph();
$g->title( 'Submitted vs Condor per day', '{font-size: 11px; color: #000000; margin: 2px 2 2px 2;}');

$g->data_sets[] = $line_1;
$g->data_sets[] = $line_2;

$g->set_x_labels( $test["date"] );
$g->set_y_legend( '# Jobs', 11, '#000000' );
$g->set_x_offset( false );


include('chart_config.inc');

echo $g->render();
?>
