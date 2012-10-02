<?php
include "../common/functions.php";

//$chart_type = $_SESSION['chart_type'];
$test = array();
$max = 0;
$emptyChart = 'true';


include_once( 'php-ofc-library/open-flash-chart.php' );

$title = new title( $title_string );

$g = new open_flash_chart();
$g->set_title( $title );


$line=array();
$line_default_dot=array();
$data=array();

if (sizeof($chartData) != 0) {
for ($i=0; $i<sizeof($chartData); $i++) {
        $test["date"][$i]=substr($chartData[$i]["date"], 5, -3);

        foreach ($metrics as $value) {
                if ($chartData[$i][$value]/$chartData[$i]['delta_t'] == '') {
			$test[$value][$i] = null;
			$label[$value][$i] = 'unknown';
			$absolute[$value][$i] = 'unknown';
		} else {
			$test[$value][$i]=number_format(floatval($chartData[$i][$value])/floatval($chartData[$i]['delta_t']), 3, '.', '');
			$label[$value][$i] = number_format(floatval($chartData[$i][$value])/floatval($chartData[$i]['delta_t']), 3, '.', '');
                        $absolute[$value][$i]=floatval($chartData[$i][$value]);
                }
                if ($max < floatval($chartData[$i][$value]/$chartData[$i]['delta_t'])) {
                        $max = floatval($chartData[$i][$value]/$chartData[$i]['delta_t']);
                }

        	if ($test[$value][$i] != null || $test[$value][$i]==0) {
                	$emptyChart = 'false';
        	}

		$d[$i] = new dot(floatval($test[$value][$i]));
//	        $data[$value][$i] = $d[$i]->tooltip("#x_label#<br>Rate: #val#<br>Collections#: ".$chartData[$i]['WMP_in_col']."<br>".$value.": ".$absolute[$value][$i]."<br>Since: ".substr($chartData[$i]['start_date'], 5, -3));
		$data[$value][$i] = $d[$i]->tooltip("#x_label#<br>Rate: ".$label[$value][$i]."<br>Collections#: ".$chartData[$i]['WMP_in_col']."<br>".$value.": ".$absolute[$value][$i]."<br>Since: ".substr($chartData[$i]['start_date'], 5, -3));

	}

//	if ($max < $chartData[$i][$value]/$chartData[$i]['delta_t']) {
  //              $max = $chartData[$i][$value]/$chartData[$i]['delta_t'];
    //    }

}
}

$offset=false;

$i = 0;
if ($emptyChart == 'false') {
	$line=array();
	$line_default_dot=array();
	$i = 0;
	foreach ($metrics as $value) {
//		$line_default_dot[$i] = new dot();
//		$line_default_dot[$i]->colour($colors[$i]);
//		$line_default_dot[$i]->tooltip( "#x_label#<br>Rate: #val#<br>".$metrics[$i].": ".$prova[$value] );
		$line[$i] = new line();
//		$line[$i]->set_default_dot_style($line_default_dot[$i]);
//		$line[$i]->set_values( $test[$value] );
		$line[$i]->set_values( $data[$value] );
		$line[$i]->colour = $colors[$i];
		$line[$i]->set_width( sizeof($metrics)-$i );
		$line[$i]->set_key( $value, 11 );

		$g->add_element( $line[$i] );
		$i++;
	}

	$x_labels = new x_axis_labels();
	$x_labels->set_steps( $step );
	$x_labels->rotate(-30);
	$x_labels->set_labels( $test["date"] );

	$g->set_number_format(3, false, true, true );

	include('chart_config.inc');
} else {
        include('chart_nodata.inc');
}

echo $g->toPrettyString();
?>
