<?php
$max_y = getYaxisMaxValue($max, 3, 1.00);
$x = new x_axis();
$x->set_offset( $offset );
$x->set_steps( $step );
$x->set_labels( $x_labels );

$y = new y_axis();
$y->set_range( 0, $max_y, $max_y/5);

$x_legend = new x_legend( $x_axis_legend );
$x_legend->set_style( '{font-size: 11px; color: #000000}' );

$y_legend = new y_legend( $y_axis_legend );
$y_legend->set_style( '{font-size: 11px; color: #000000}' );

$g->set_x_axis( $x );
$g->set_y_axis( $y );
$g->set_x_legend( $x_legend );
$g->set_y_legend( $y_legend );
$g->set_bg_colour( '#EEEEEE' );
?>
