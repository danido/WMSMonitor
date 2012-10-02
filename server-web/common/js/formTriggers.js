addLoadEvent(formTriggers);
addLoadEvent(formTriggers2);

function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    }
    else {
        window.onload = function() {
                func();
            }
    }
}

function formTriggers() {
    // Switching Roles
    if (!document.getElementById("inline")) return false;
    var role_box = document.getElementById("inline");
    var role_options = role_box.getElementsByTagName("option");
    var url = document.URL;
    role_box.onchange = function() {
        if (role_box.options[role_box.selectedIndex].value=="cms") {
            location.search = "?scope=cms";
        }
        else if (role_box.options[role_box.selectedIndex].value=="atlas") {
            location.search = "?scope=atlas";
        } 
        else if (role_box.options[role_box.selectedIndex].value=="cdf") {
            location.search = "?scope=cdf";
        }
        else {
            location.search = "?scope=all";
        }

        document.getElementById("searchbutton").disabled = true;
    }
}

function formTriggers2() {
    // Switching Roles
    if (!document.getElementById("volist_type_group")) return false;
    var role_box = document.getElementById("volist_type_group");
    var role_options = role_box.getElementsByTagName("option");
    var url = document.URL;
    if (role_box.options[role_box.selectedIndex].value=="custom") {
            document.getElementById("vochecklist").style.display = "inline";
    }
    role_box.onchange = function() {
        if (role_box.options[role_box.selectedIndex].value=="custom") {
            document.getElementById("vochecklist").style.display = "inline";
        }
	else {
            document.getElementById("vochecklist").style.display = "none";
	}

        document.getElementById("searchbutton").disabled = true;
    }
}
