var url = document.URL;

function hiddenChart(transparent) {
	if (url.match("ce_mm.php") || url.match("vo_details.php")) {
		var obj = document.getElementById(transparent);
        	obj.style.visibility = "hidden";
	} else {
                return false;
        }
}

function visibleChart(transparent) {
	if (url.match("ce_mm.php") || url.match("vo_details.php")) {
		var obj = document.getElementById(transparent);
        	obj.style.visibility = "visible";
	} else {
		return false;
	}
}
