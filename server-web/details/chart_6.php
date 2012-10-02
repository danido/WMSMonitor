<?php

$nameSession = isset($_GET['nameSession']) ? $_GET['nameSession'] : '';
session_name($nameSession);
session_start();
$chartData = $_SESSION['chartLBDailyData'];
$step = $_SESSION['stepDaily'];
$metrics = $_SESSION['metrics_6'];
$title_string = 'Job Final State';
$x_axis_legend = 'Time';
$y_axis_legend = '# Jobs';
$colors = array('#50CC33','#EE0000','#000080','#C79810');

include "chart_body.php";
?>
