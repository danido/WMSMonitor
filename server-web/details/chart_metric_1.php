<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartData'];
$step = $_SESSION['step'];
$metrics = array('fload', 'ftraversaltime', 'fmetric');
$title_string = 'Metric functions';
$x_axis_legend = 'Time';
$y_axis_legend = 'Num';
$colors = array('#50CC33','#EE0000','#000080','#C79810');
$chart_type = 'current';

include "chart_body.php";
?>
