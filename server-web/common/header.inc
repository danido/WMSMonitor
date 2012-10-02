<?php
require_once "../common/functions.php";
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
        <head>
                <title>WMSMonitor</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <link href="../common/css/style.css" rel="stylesheet" type="text/css" media="screen"/>
		<link href="../common/css/dhtmlgoodies_calendar.css" rel="stylesheet" type="text/css" media="screen"/>
		<link rel="icon" type="image/png" href="../common/icon/favicon.png"/>

<style type="text/css">
<?php
	for ($i=0; $i<sizeof($selectedId); $i++){
		echo "a#".$selectedId[$i];
		if ($i != (sizeof($selectedId)-1)) {
			echo ", ";
		}
	}
?>
      {
      	background-color: #FFFFFF;
        color: #000066; 
      	cursor: default;
      }
</style>

		<script src="../common/js/mootools.js" type="text/javascript"></script>        
		<script src="../common/js/formTriggers.js" type="text/javascript"></script>
		<script src="../common/js/dhtmlgoodies_calendar.js" type="text/javascript"></script>
		<script src="../common/js/visibleMenu.js" type="text/javascript"></script>
		<script src="../common/js/partialHistogram.js" type="text/javascript"></script>
		<script src="../common/js/dashboard.js" type="text/javascript"></script>

		<script src="js/jquery-1.2.6.min.js" type="text/javascript"></script>
		<script type="text/javascript" src="js/swfobject.js"></script>

		<script type="text/javascript">
			window.addEvent('domready', function(){    
        			var tip = new Tips($$('table.main td[title]'), {});
				var tip = new Tips($$('table.main img[title]'), {}); 
			});

var global_wide = true;

function changeSize()
{
	this.o = document.getElementById("open_flash_chart");
	
	if( global_wide )
	{
		// fix an IE bug, use this.o:	
		this.o.style.height="285px";
		this.o.style.width="395px";
	}
	else
	{
		this.o.style.height="285px";
		this.o.style.width="395px";
	}
	
	global_wide = !global_wide;
}

var step = 0;
var width = 0;

function grow()
{
	if( global_wide )
		make_big();
	else
		make_small();
		
	global_wide = !global_wide;
}

function make_big()
{
	step = 200;
	width = 600;
	
	this.o = document.getElementById("open_flash_chart");
	var t = setTimeout("bigger()",30);
}

function bigger()
{
	this.o = document.getElementById("open_flash_chart");
	this.o.style.width = (width-step)+'px';
	this.o.style.height = (width-step)+'px';
	
	step /= 2;
	
	if( step > 0.5 )
		setTimeout("bigger()",30);
		
}

function make_small()
{
	step = 200;
	width = 285;
	
	this.o = document.getElementById("open_flash_chart");
	var t = setTimeout("smaller()",30);
}

function smaller()
{
	this.o = document.getElementById("open_flash_chart");
	this.o.style.width = (width+step)+'px';
	this.o.style.height = (width+step)+'px';
	
	step /= 2;
	
	if( step > 0.5 )
		setTimeout("smaller()",30);
		
}
		</script>
<script type="text/javascript"><!--//--><![CDATA[//><!--

sfHover = function() {
	var sfEls = document.getElementById("nav").getElementsByTagName("LI");
	for (var i=0; i<sfEls.length; i++) {
		sfEls[i].onmouseover=function() {
			this.className+=" sfhover";
		}
		sfEls[i].onmouseout=function() {
			this.className=this.className.replace(new RegExp(" sfhover\\b"), "");
		}
	}
}

function transparent() {
	var obj = document.getElementById("transparent");
//	if (document.getElementById("nav3").style.display == "list-item") {
		obj.style.visibility = "hidden";
//	}
}

//if (window.attachEvent) window.attachEvent("onload", sfHover);
//if (window.attachEvent) window.attachEvent("onload", transparent);

//--><!]]></script>



<script type="text/javascript">

OFC = {};

OFC.jquery = {
    name: "jQuery",
    version: function(src) { return $('#'+ src)[0].get_version() },
    rasterize: function (src, dst) { $('#'+ dst).replaceWith(OFC.jquery.image(src)) },
    image: function(src) { return "<img src='data:image/png;base64," + $('#'+src)[0].get_img_binary() + "' />"},
    popup: function(src) {
        var img_win = window.open('', 'Charts: Export as Image')
        with(img_win.document) {
            write('<html><head><title>Charts: Export as Image<\/title><\/head><body>' + OFC.jquery.image(src) + '<\/body><\/html>') }
                // stop the 'loading...' message
                img_win.document.close();
     }
}

// Using an object as namespaces is JS Best Practice. I like the Control.XXX style.
//if (!Control) {var Control = {}}
//if (typeof(Control == "undefined")) {var Control = {}}
if (typeof(Control == "undefined")) {var Control = {OFC: OFC.jquery}}

// This function is used by the png button
function change_format(div_list) {
	var items = change_format.arguments.length
        for(i=0; i<=items; i++) {
                OFC.jquery.rasterize(change_format.arguments[i], change_format.arguments[i])
        }
}

//This function is used by the right click of mouse on the flash frame
function save_image() { 
<?php
	echo "var items = ".sizeof($plot_names)."\n";
	foreach ($plot_names as $value) {	
		echo "OFC.jquery.popup('".$value."')\n";
	}
?>
}

function moo() { alert(99); };

</script>

	</head>
	<body>
