<?php
include_once ("jpgraph/jpgraph.php");
include_once ("jpgraph/jpgraph_line.php");
include_once ("jpgraph/jpgraph_error.php");

$graph = new Graph(800,600);
$graph->SetMargin(50,50,40,100);
$graph->SetMarginColor('white');
$graph->SetScale('intlin');
$graph->xaxis->SetLabelAngle(90);
$graph->xaxis->title->Set("Time");

$test = array();
$p = array();
$pLB = array();
$variables = array();

if (sizeof($chartHWData) != 0) {
for ($i=0; $i<sizeof($chartHWData); $i++) {
        $test["date"][$i]=substr($chartHWData[$i]["date"], 5, -3);

	foreach ($customHW as $key => $value) {
		if (isset($customHW[$key])) {
			$test[$key][$i]=$chartHWData[$i][$key];
		}
	}

}
}

if (sizeof($chartServiceData) != 0) {
for ($i=0; $i<sizeof($chartServiceData); $i++) {
        $test["date"][$i]=substr($chartServiceData[$i]["date"], 5, -3);

        foreach ($customService as $key => $value) {
                if (isset($customService[$key])) {
                        $test[$key][$i]=$chartServiceData[$i][$key];
                }
        }

}
}

if (sizeof($chartJobData) != 0) {
for ($i=0; $i<sizeof($chartJobData); $i++) {

        foreach ($customJob as $key => $value) {
                if (isset($customJob[$key]) && !is_null($chartJobData[$i][$key])) {
	                      	$testLB[$key][$i]=floatval($chartJobData[$i][$key]/floatval($chartJobData[$i]['deltat']));
		}
        }
}
}

if (sizeof($chartMetricData) != 0) {
for ($i=0; $i<sizeof($chartMetricData); $i++) {
        $test["date"][$i]=substr($chartMetricData[$i]["date"], 5, -3);

        foreach ($customMetric as $key => $value) {
                if (isset($customMetric[$key])) {
                        $test[$key][$i]=$chartMetricData[$i][$key];
                }
        }

}
}

$graph->xaxis->SetTickLabels($test["date"]);

$colors = array('#d01f3c','#356aa0','#C79810','#32CD32','#FFA07A','#838B83','#EE799F','#9932CC','#8B6508','#404040','#FFFF00');

$i = 0;
foreach ($customHW as $key => $value) {
$p[$key] = new LinePlot($test[$key]);
$p[$key]->SetColor($colors[$i]);
$p[$key]->SetWeight(sizeof($customHW)+sizeof($customService)+sizeof($customJob)+sizeof($customMetric)-$i);
if ($key == 'Sandbox partition' || $key == '/var/log partition' || $key == '/var/lib/mysql part.' || $key == 'LB /var/lib/mysql') {
	$p[$key]->SetLegend($key." (%)");
} else {
	$p[$key]->SetLegend($key." (Number)");
}
$graph->Add($p[$key]);
$variables[$key]=$key;
$i++;
}

$j = 0;
foreach ($customService as $key => $value) {
$p[$key] = new LinePlot($test[$key]);
$p[$key]->SetColor($colors[$i+$j]);
$p[$key]->SetWeight(sizeof($customHW)+sizeof($customService)+sizeof($customJob)+sizeof($customMetric)-$j-$i);
$p[$key]->SetLegend($key." (Number)");
$graph->Add($p[$key]);
$variables[$key]=$key;
$j++;
}

$y = 0;
foreach ($customJob as $key => $value) {
$pLB[$key] = new LinePlot($testLB[$key]);
$pLB[$key]->SetColor($colors[$i+$j+$y]);
$pLB[$key]->SetWeight(sizeof($customHW)+sizeof($customService)+sizeof($customJob)+sizeof($customMetric)-$j-$i-$y);
$pLB[$key]->SetLegend($key." (Hz)");
if ($i!=0 || $j!=0) {
	$graph->AddY(0, $pLB[$key]);
} else {
	$graph->Add($pLB[$key]);
}
$variables[$key]=$key;
$y++;
}

$z = 0;
foreach ($customMetric as $key => $value) {
$p[$key] = new LinePlot($test[$key]);
$p[$key]->SetColor($colors[$i+$j+$y+$z]);
$p[$key]->SetWeight(sizeof($customHW)+sizeof($customService)+sizeof($customJob)+sizeof($customMetric)-$j-$i-$y-$z+1);
$p[$key]->SetLegend($key." (Number)");
$graph->Add($p[$key]);
$variables[$key]=$key;
$z++;
}

if (($i!=0 || $j!=0) && ($y!=0)) {
        $graph->SetYScale(0, 'lin');
        $graph->yaxis->title->Set("Number, %");
        $graph->ynaxis[0]->title->Set("Rate (Hz)");
        $graph->legend->Pos(0.08,0);
} else if (($i!=0 || $j!=0) && ($y==0)) {
        $graph->yaxis->title->Set("Number, %");
        $graph->legend->Pos(0,0);
} else if (($i==0 && $j==0) && ($y!=0)) {
        $graph->yaxis->title->Set("Rate (Hz)");
        $graph->legend->Pos(0,0);
}

//$graph->Stroke('jp_file.png');

//$filename = "";
$filename = "";
foreach ($variables as $key => $value) {
	$filename = $filename.$value."-";
}

//$filename = strtr($filename, " ", "");

$filename = str_replace(' ', '', $filename); 
$filename = str_replace('/', '-', $filename);
$filename = strtolower($filename);
$filename = $filename."from=".$startDate."-to=".$endDate;
$filename = $filename.".png";

$graph->Stroke('img/'.$filename);

echo "<div>";
//echo "<img src=\"jp_file.png\"></img>";

echo "<img src=\"img/".$filename."\"></img>";

echo "</div>";
?>
