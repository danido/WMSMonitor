<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartLBData'];
$step = $_SESSION['step'];
$metrics = $_SESSION['metrics_3'];
$title_string = 'Job Flow Rates';
$x_axis_legend = 'Time';
$y_axis_legend = 'Jobs Rates (Hz)';
$colors = array('#50CC33','#EE0000','#000080','#C79810');

include "chart_body_rates.php";
?>
