var url = document.URL;

function visibleColumns(service) {
	var anchors = document.getElementsByTagName("td");
	for (var i=0; i<anchors.length; i++) {
		var anchor = anchors[i];
		if (anchor.getAttribute("class") && (anchor.getAttribute("class") == "hide_show_"+service || anchor.getAttribute("class") == "not_available hide_show_"+service)) {
			anchor.style.display = "table-cell";
		}
	}
	if (service == 'wms') {
		document.getElementById('main_lb').style.display = "none";
		document.getElementById('expand_lb').style.display = "none";
	} else {
		document.getElementById('main_wms').style.display = "none";
		document.getElementById('expand_wms').style.display = "none";
	}
	document.getElementById('cont_'+service).style.width = "100%";
	document.getElementById('expand_'+service).firstChild.nodeValue='Collapse '+service+' summary';
	document.getElementById('expand_'+service).attributes['onclick'].value="hiddenColumns('"+service+"')";


/*
	if (document.getElementByTagName(th)) {
		var obj = document.getElementById(className);
        	obj.style.display = "none";
	} else {
                return false;
        }
*/
}

function hiddenColumns(service) {
	var anchors = document.getElementsByTagName("td");
        for (var i=0; i<anchors.length; i++) {
                var anchor = anchors[i];
                if (anchor.getAttribute("class") && (anchor.getAttribute("class") == "hide_show_"+service || anchor.getAttribute("class") == "not_available hide_show_"+service)) {
                        anchor.style.display = "none";
                }
        }
	if (service == 'wms') {
                document.getElementById('main_lb').style.display = "table";
		document.getElementById('expand_lb').style.display = "block";
		document.getElementById('cont_'+service).style.width = "58%";
        } else {
                document.getElementById('main_wms').style.display = "table";
		document.getElementById('expand_wms').style.display = "block";
		document.getElementById('cont_'+service).style.width = "38%";
        }
	document.getElementById('expand_'+service).firstChild.nodeValue='Expand '+service+' summary';
        document.getElementById('expand_'+service).attributes['onclick'].value="visibleColumns('"+service+"')";
/*
	if (document.getElementById(className)) {
		var obj = document.getElementById(className);
        	obj.style.display = "table-cell";
	} else {
		return false;
	}
*/
}
