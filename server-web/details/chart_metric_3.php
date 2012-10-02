<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartData'];
$step = $_SESSION['step'];
$metrics = array('WM queue', 'JC queue', 'LB events');
$title_string = 'Components Queues';
$x_axis_legend = 'Time';
$y_axis_legend = '# Jobs';
$colors = array('#50CC33','#EE0000','#000080','#C79810');
$chart_type = 'current';

include "chart_body.php";
?>
