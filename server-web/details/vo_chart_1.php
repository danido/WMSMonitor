<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartData'];
$step = $_SESSION['step'];
$variable = isset($_GET['variable']) ? $_GET['variable'] : 'final_state';
$x_axis_legend = 'Time';
$y_axis_legend = '# Jobs';
$colors = array('#50CC33','#EE0000','#000080','#C79810');

switch ($variable) {
        case 'final_state':
                $metrics=array('JOB_DONE','JOB_ABORTED');
		$title_string = 'Job Final State per day';
                break;
        case 'sub_jss':
                $metrics=array('WMP_in','JC_out');
		$title_string = 'Submitted vs JSS per day';
                break;
}

include "chart_body.php";
?>
