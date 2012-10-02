<?php
$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartData'];
$step = $_SESSION['step'];
$variable = isset($_GET["variable"]) ? $_GET["variable"] : "JOB_DONE";

switch ($variable) {
        case 'JOB_DONE':
                $variableDisplay='Jobs Done';
                break;
	case 'JOB_ABORTED':
                $variableDisplay='Jobs Aborted';
                break;
	case 'WMP_in':
                $variableDisplay='Submitted Jobs';
                break;
	case 'JC_out':
                $variableDisplay='JSS Jobs';
                break;
}

include "../common/functions.php";

$test = array();

$max = 0;

include_once( 'php-ofc-library/open-flash-chart.php' );
$g = new open_flash_chart();
$title_string = $variableDisplay.' per day';
$title = new title( $title_string );
$g->set_title( $title );
$offset=false;

$colors = array('#d01f3c','#356aa0','#C79810','#32CD32','#FFA07A','#838B83','#EE799F','#9932CC','#8B6508','#404040','#FFFF00','#f00000','#356000','#C75000','#320000','#FFA000');

for ($i=0; $i<sizeof($chartData); $i++) { 
$test["date"][$i]=substr($chartData[$i][0]["date"], 5, 5);

	for ($j=0; $j<sizeof($chartData[$i]); $j++) {
        	$test[$variable][$j][$i]=intval($chartData[$i][$j][$variable]);

        	if ($max < $chartData[$i][$j][$variable]) {
                	$max = $chartData[$i][$j][$variable];
        	}
	}
}

for ($j=0; $j<sizeof($chartData[0]); $j++) {
	${"line_default_dot_".$j} = new dot();
        ${"line_default_dot_".$j}->colour($colors[$j]);
	${"line_default_dot_".$j}->tooltip( "#x_label#<br>".$variable." (".$chartData[0][$j]["VO"].")".": #val#<br>" );
	${"line_".$j} = new line();
	${"line_".$j}->set_key( $chartData[0][$j]["VO"], 11 );
	${"line_".$j}->set_default_dot_style(${"line_default_dot_".$j});
	${"line_".$j}->colour = $colors[$j];
	${"line_".$j}->set_width( 1 );
	${"line_".$j}->set_values( $test[$variable][$j] );
	$g->add_element( ${"line_".$j} );
}

$max_y = getYaxisMaxValue($max, 3, 1.00);

$x_labels = new x_axis_labels();
$x_labels->set_steps( $step );
$x_labels->rotate(-30);
$x_labels->set_labels( $test["date"] );

$x_axis_legend='Time';
$y_axis_legend='# Jobs';

include('chart_config.inc');

echo $g->toPrettyString();
?>
