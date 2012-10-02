<?php
include_once ("jpgraph/jpgraph.php");
include_once ("jpgraph/jpgraph_line.php");
include_once ("jpgraph/jpgraph_error.php");
include_once ("include/functions.php");

$graph = new Graph(800,600);
$graph->SetMargin(40,30,40,100);
$graph->SetMarginColor('white');
$graph->SetScale('intlin');
$graph->xaxis->SetLabelAngle(90);
$graph->xaxis->title->Set("Time");
$graph->yaxis->title->Set("Number");
$graph->legend->Pos(0,0); 

$test = array();
$p = array();

for ($i=0; $i<sizeof($chartDailyData); $i++) {
        $test["date"][$i]=substr($chartDailyData[$i]["date"], 5, 5);

	foreach ($customDaily as $key => $value) {
		if (isset($customDaily[$key])) {
			$test[$key][$i]=$chartDailyData[$i][$key];
		}
	}
}

$graph->xaxis->SetTickLabels($test["date"]);

$colors = array('#d01f3c','#356aa0','#C79810','#CD7F32','#32CD32','#FFA07A','#838B83','#EE799F','#9932CC','#8B6508','#404040','#FFFF00');

$i = 0;
foreach ($customDaily as $key => $value) {
$p[$key] = new LinePlot($test[$key]);
$p[$key]->SetColor($colors[$i]);
$p[$key]->SetLegend($key);
$graph->Add($p[$key]);
$i++;
}

$graph->Stroke('jp_file.png');

echo "<div>";
echo "<img src=\"jp_file.png\"></img>";
echo "</div>";
?>
