function partialHistogram(bin, max, limit_to) {
	for (i=bin-1; i<=max; i=i+bin) {
		document.getElementById('partial'+i).style.display='none';
	}
	document.getElementById('partial'+limit_to).style.display='block';
	document.getElementById('ce_mm_subtitle').style.width='800px';

	document.getElementById('nav3_wms').onmouseover = function() {
		hiddenChart('partial'+limit_to);
	}

	document.getElementById('nav2_wms').onmouseover = function() {
                hiddenChart('partial'+limit_to);
        }

	document.getElementById('nav3_wms').onmouseout = function() {
                visibleChart('partial'+limit_to);
        }

	document.getElementById('nav2_wms').onmouseout = function() {
                visibleChart('partial'+limit_to);
        }

	document.getElementById('nav3_vo').onmouseover = function() {
                hiddenChart('partial'+limit_to);
        }

        document.getElementById('nav2_vo').onmouseover = function() {
                hiddenChart('partial'+limit_to);
        }

        document.getElementById('nav3_vo').onmouseout = function() {
                visibleChart('partial'+limit_to);
        }

        document.getElementById('nav2_vo').onmouseout = function() {
                visibleChart('partial'+limit_to);
        }
}
