<?php
$wms = isset($_GET['wms']) ? $_GET['wms'] : '';
$wmsRepl = str_replace(".", "-", $wms);
$selectedId = array("WMS_view","Single_instance","Details","Details-".$wmsRepl);
$endDate = isset($_GET['endDate']) ? $_GET['endDate'] : date("Y-m-d");
//$startDate = isset($_GET['startDate']) ? $_GET['startDate'] : date("Y-m-d");
$interval = isset($_GET['interval']) ? $_GET['interval'] : 'day';
$jss_jobs = isset($_GET['jss_jobs']) ? $_GET['jss_jobs'] : 'all';
$nameSession = 'details'.$wmsRepl.$interval.$endDate;

session_name($nameSession);
session_start();

include "../common/header.inc";
include "../common/banner.inc";
$detailsWMSData=getDetailsWMSData($wms);
$detailsLBData=getDetailsLBHist($wms); 
$detailsWMSRates=getDetailsWMSRates($wms);
$detailsLBSensorData=getDetailsLBSensor($wms);

$i=0;
foreach ($detailsLBData as $item) {
	foreach ($item as $key => $value) {
		$detailsLBAll[$i][$key] = $value;
		foreach ($detailsLBSensorData as $item2) {
			foreach ($item2 as $key2 => $value2) {
				if ($item2['hostname']==$item['hostname']) {
					if ($key2!='hostname') {
						$detailsLBAll[$i][$key2] = $value2;
					}
				} else {
					if ($key2!='hostname') {
                                                $detailsLBAll[$i][$key2] = 100;
                                        }
				}
			}
		}			
        }
	$i++;
}

//print_r($detailsLBSensorData);
//print_r($detailsLBData);
//print_r($detailsLBAll);

$field_WMS = array();
$field_LB = array();
$td_string_WMS = array();
$td_string_LB = array();

foreach ($detailsWMSData[0] as $key => $value) {
$field_WMS[$key] = $detailsWMSData[0][$key] == '' ? 'N/A' : $detailsWMSData[0][$key];
$td_string_WMS[$key] = $detailsWMSData[0][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$field_WMS[$key] : "<td>".$field_WMS[$key];
}

foreach ($detailsLBData[0] as $key => $value) {
$field_LB[$key] = $detailsLBData[0][$key] == '' ? 'N/A' : $detailsLBData[0][$key];
$td_string_LB[$key] = $detailsLBData[0][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$field_LB[$key] : "<td>".$field_LB[$key];
}

foreach ($detailsWMSRates[0] as $key => $value) {
$field_WMS_rates[$key] = $detailsWMSRates[0][$key] == '' ? 'N/A' : $detailsWMSRates[0][$key];
$td_string_WMS_rates[$key] = $detailsWMSRates[0][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$field_WMS_rates[$key] : "<td>".$field_WMS_rates[$key];
}

$date1 = $detailsWMSRates[0]["end_date"];
$unix_now = mktime(intval(substr($date1, 11, 2)), intval(substr($date1, 14, 2)), intval(substr($date1, 17, 2)), intval(substr($date1, 5, 2)), intval(substr($date1, 8, 2)), intval(substr($date1, 0, 4)));
$unix_previous = $unix_now - $detailsLBData[0]["deltat"];
//$date_previous = date("Y-m-d H:i:s", $unix_previous);
$date_previous = $detailsWMSRates[0]["start_date"];
$dateLB  = $field_WMS["measure_time"];
$unix_LB = mktime(intval(substr($dateLB, 11, 2)), intval(substr($dateLB, 14, 2)), intval(substr($dateLB, 17, 2)), intval(substr($dateLB, 5, 2)), intval(substr($dateLB, 8, 2)), intval(substr($dateLB, 0, 4)));

if ((time() - $unix_now) > 3600) {
        $row_details = 'row_error';
        $title = 'Date older than 1 hour ago';
} else if ((time() - $unix_now) > 1800) {
        $row_details = 'row_warning';
        $title = 'Date older than 30 minutes ago';
} else {
        $row_details = '';
        $title = 'Date of the last measure';
}
?>

<div class="breadcrumb">
<a title="Click to go to the main page" href="../main/main.php">WMSMonitor</a> >> WMS view >> Single instance >> Details::<?php echo $wms; ?>
</div>

<table class="main_container">
	<tr>
		<td id="detailed_table">

			<table class="details">
				<tr class="supertitle">
					<td>
						Component Details
						<?php
						echo "<span class=\"undersupertitle\">from ".$date_previous."</span>";

						if ((time() - $unix_now) > 3600) {
        						$row_details = 'row_error';
        						$title = 'Date older than 1 hour ago';
						} else if ((time() - $unix_now) > 1800) {
        						$row_details = 'row_warning';
        						$title = 'Date older than 30 minutes ago';
						} else {
        						$row_details = '';
        						$title = 'Date of the last measure';
						}
						echo "<span title=\"".$title."\" class=\"undersupertitle ".$row_details."\">to ".$date1."</span>";

						?>
					</td>
				</tr>
			</table>

			<table class="details">
				<tr class="title">
					<?php
						if (isset($detailsWMSData[0]["daemon_wmp"])) {
							$status_icon = $detailsWMSData[0]["daemon_wmp"] == 0 ? 'check16.png' : 'error16.png';
							$title = "WMP daemon = ".$detailsWMSData[0]["daemon_wmp"];
						} else {
							$status_icon = 'documenterror16.png';
							$title = "No data about WMP daemon";
						}
						echo "<td>WM Proxy</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td>";
						echo "</tr><tr title=\"Number of jobs submitted to WMProxy server from UI in past ".$detailsLBData[0]["deltat"]." sec\">";
						echo "<td>Jobs -> WMProxy</td>".$td_string_WMS_rates["WMP_in"]."</td>";
						echo "</tr><tr title=\"Number of job collections  submitted in past ".$detailsLBData[0]["deltat"]." sec\">";
						echo "<td>Collections submitted</td>".$td_string_WMS_rates["WMP_in_col"]."</td>";
						echo "</tr><tr title=\"Minimum number of nodes in job collections submitted in past ".$detailsLBData[0]["deltat"]." sec\">";
						echo "<td>Min nodes per coll.</td>".$td_string_WMS_rates["WMP_in_col_min_nodes"]."</td>";
						echo "</tr><tr title=\"Maximum number of nodes in collections submitted in past ".$detailsLBData[0]["deltat"]." sec\">";
						echo "<td>Max nodes per coll.</td>".$td_string_WMS_rates["WMP_in_col_max_nodes"]."</td>";
					?>
				</tr>
			</table>

			<table class="details">
				<tr class="title">
					<?php
						if (isset($detailsWMSData[0]["daemon_px"])) {
							$status_icon = $detailsWMSData[0]["daemon_px"] == 0 ? 'check16.png' : 'error16.png';
							$title = "PX daemon = ".$detailsWMSData[0]["daemon_px"];
						} else {
        						$status_icon = 'documenterror16.png';
							$title = "No data about PX daemon";
						}
						echo "<td>Proxy Reneval</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td></td>";
					?>
				</tr>
			</table>

			<table class="details">
				<tr class="title">
					<?php
						if (isset($detailsWMSData[0]["daemon_wm"])) {
	$status_icon = $detailsWMSData[0]["daemon_wm"] == 0 ? 'check16.png' : 'error16.png';
	$title = "WM daemon = ".$detailsWMSData[0]["daemon_wm"];
} else {
        $status_icon = 'documenterror16.png';
	$title = "No data about WM daemon";
}

echo "<td>Workload Manager</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td>";
if ($detailsWMSData[0]["FD_WM"] > 900) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["FD_WM"] > 700) {
        $row_details = 'row_warning';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Number of file descriptors opened by process Workload Manager\">";
echo "<td>WM file descriptors</td>".$td_string_WMS["fd_wm"]."</td>";
if ($detailsWMSData[0]["input_fl"] > 500) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["input_fl"] > 250) {
        $row_details = 'row_warning';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Number of unprocessed entries in WM /var/glite/workload_manager/input.fl\">";
echo "<td>WM queue</td>".$td_string_WMS["wm_queue"]."</td>";
echo "</tr><tr title=\"Number of jobs enqueued to WorkLoad Manager in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs -> WM</td>".$td_string_WMS_rates["WM_in"]."</td>";
echo "</tr><tr title=\"Number of jobs enqueued after resub to WorkLoad Manager in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs Resub -> WM</td>".$td_string_WMS_rates["WM_in_res"]."</td>";
echo "</tr><tr title=\"Number of VO Views entries in the Information Super Market\">";
echo "<td>VO Views</td>".$td_string_WMS["ism_entries"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_lm"])) {
	$status_icon = $detailsWMSData[0]["daemon_lm"] == 0 ? 'check16.png' : 'error16.png';
	$title = "LM daemon = ".$detailsWMSData[0]["daemon_lm"];
} else {
	$status_icon = 'documenterror16.png';
	$title = "No data about LM daemon";
}

echo "<td>Log Monitor</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td>";
if ($detailsWMSData[0]["fd_lm"] > 900) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["fd_lm"] > 700) {
        $row_details = 'row_warning';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Number of file descriptors opened by process Log Monitor\">";
echo "<td>LM file descriptors</td>".$td_string_WMS["fd_lm"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_jc"])) {
	$status_icon = $detailsWMSData[0]["daemon_jc"] == 0 ? 'check16.png' : 'error16.png';
	$title = "JC daemon = ".$detailsWMSData[0]["daemon_jc"];
} else {
        $status_icon = 'documenterror16.png';
	$title = "No data about JC daemon";
}
echo "<td>Job Controller</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td>";
if ($detailsWMSData[0]["jc_queue"] > 500) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["jc_queue"] > 250) {
        $row_details = 'row_warning';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Number of entries in file /var/glite/jobcontrol/queue.fl (Job Controller)\">";
echo "<td>JC queue</td>".$td_string_WMS["jc_queue"]."</td>";
if ($detailsWMSData[0]["fd_jc"] > 900) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["fd_jc"] > 700) {
        $row_details = 'row_warning';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Number of file descriptors opened by process Job Controller\">";
echo "<td>JC file descriptor</td>".$td_string_WMS["fd_jc"]."</td>";
echo "</tr><tr title=\"Number of jobs enqueued to Job Controller in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs -> JC</td>".$td_string_WMS_rates["JC_in"]."</td>";
echo "</tr><tr title=\"Number of jobs processed from Job Controller in past ".$detailsLBData[0]["deltat"]." sec\">";
echo "<td>Jobs JC -> Condor</td>".$td_string_WMS_rates["JC_out"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_ll"])) {
	$status_icon = $detailsWMSData[0]["daemon_ll"] == 0 ? 'check16.png' : 'error16.png';
	$title = "LL daemon = ".$detailsWMSData[0]["daemon_ll"];
} else {
        $status_icon = 'documenterror16.png';
	$title = "No data about LL daemon";
}
echo "<td>Local Logger</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td>";
if ($detailsWMSData[0]["lb_event"] > 1000) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["lb_event"] > 500) {
        $row_details = 'row_warning'; 
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"dg20logd_* files num in /var/glite/log (Events not yet transferred to the LB)\">";
echo "<td>LB events queue</td>".$td_string_WMS["lb_event"]."</td>";
if ($detailsWMSData[0]["fd_ll"] > 900) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["fd_ll"] > 700) {
        $row_details = 'row_warning';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Number of file descriptors opened by process Local Logger\">";
echo "<td>LL file descriptor</td>".$td_string_WMS["fd_ll"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_lbpx"])) {
        $status_icon = $detailsWMSData[0]["daemon_lbpx"] == 0 ? 'check16.png' : 'error16.png';
	$title = "LBPX daemon = ".$detailsWMSData[0]["daemon_lbpx"];
} else {
        $status_icon = 'documenterror16.png';
	$title = "No data about LBPX daemon";
}
echo "<td>LB Proxy</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td></td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_ftpd"])) {
	$status_icon = $detailsWMSData[0]["daemon_ftpd"] == 0 ? 'check16.png' : 'error16.png';
	$title = "FTPD daemon = ".$detailsWMSData[0]["daemon_ftpd"];
} else {
        $status_icon = 'documenterror16.png';
	$title = "No data about FTPD daemon";
}
echo "<td>Transfers</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td></td>";
echo "</tr><tr title=\"Number of gridftp sessions on WMS\">";
echo "<td>gftp</td>".$td_string_WMS["gftp_con"]."</td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_ntpd"])) {
        $status_icon = $detailsWMSData[0]["daemon_ntpd"] == 0 ? 'check16.png' : 'error16.png';
        $title = "LBPX daemon = ".$detailsWMSData[0]["daemon_ntpd"];
} else {
        $status_icon = 'documenterror16.png';
        $title = "No data about NTPD daemon";
}
echo "<td>NTPD</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td></td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_bdii"])) {
        $status_icon = $detailsWMSData[0]["daemon_bdii"] == 0 ? 'check16.png' : 'error16.png';
        $title = "BDII daemon = ".$detailsWMSData[0]["daemon_bdii"];
} else {
        $status_icon = 'documenterror16.png';
        $title = "No data about BDII daemon";
}
echo "<td>BDII</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td></td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">
<?php
if (isset($detailsWMSData[0]["daemon_ice"])) {
        $status_icon = $detailsWMSData[0]["daemon_ice"] == 0 ? 'check16.png' : 'error16.png';
        $title = "ICE daemon = ".$detailsWMSData[0]["daemon_ice"];
} else {
        $status_icon = 'documenterror16.png';
        $title = "No data about ICE daemon";
}
echo "<td>ICE</td><td><img src=\"../common/icon/".$status_icon."\" title=\"$title\"></img></td></td>";
?>
</tr>
</table>

<table class="details">
<tr class="title">

<?php
echo "<td colspan=\"2\">Load balancing</td><td></td>";
echo "</tr><tr title=\"".$title."\">";
if ($detailsWMSData[0]["loadb_fmetric"] >= 2 || $detailsWMSData[0]["loadb_fmetric"] < 0) {
        $row_details = 'row_error';
} else if ($detailsWMSData[0]["loadb_fmetric"] >= 1) {
        $row_details = 'row_warning';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Load balancing metric value\">";
echo "<td>Metric</td>".$td_string_WMS["loadb_fmetric"]."</td>";

if ($detailsWMSData[0]["loadb_fdrain"] == -1) {
        $row_details = 'row_error';
} else {
        $row_details = '';
}
echo "</tr><tr class=\"".$row_details."\" title=\"Drain flag (if -1 the WMS is in drain)\">";
echo "<td>Drain flag</td>".$td_string_WMS["loadb_fdrain"]."</td>";
?>
</tr>
</table>
</td>














		<td>
			<table class="upper_container">
				<tr>

					<td class="separator"></td>

					<td class="general_info">
						<table class="general">
							<tr class="supertitle">
								<td>
									General Info
									<span class="weight_normal">at
									<?php

									$field_WMS = array();
									$field_LB = array();
									$td_string_WMS = array();
									$td_string_LB = array();

									foreach ($detailsWMSData[0] as $key => $value) {
										$field_WMS[$key] = $detailsWMSData[0][$key] == '' ? 'N/A' : $detailsWMSData[0][$key];
										$td_string_WMS[$key] = $detailsWMSData[0][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$field_WMS[$key] : "<td>".$field_WMS[$key];
									}

									foreach ($detailsLBData[0] as $key => $value) {
										$field_LB[$key] = $detailsLBData[0][$key] == '' ? 'N/A' : $detailsLBData[0][$key];
										$td_string_LB[$key] = $detailsLBData[0][$key] == '' ? "<td class=\"not_available\" title=\"Not Available\">".$field_LB[$key] : "<td>".$field_LB[$key];
									}

									if ((time() - $unix_LB) > 3600) {
                                                        			$row_details = 'row_error';
                                                        			$title = 'Date older than 1 hour ago';
                                                			} else if ((time() - $unix_LB) > 1800) {
                                                        			$row_details = 'row_warning';
                                                        			$title = 'Date older than 30 minutes ago';
                                                			} else {
                                                        			$row_details = '';
                                                        			$title = 'Date of the last measure';
                                                			}

									echo "<span title=\"".$title."\" class=\"".$row_details."\">".$field_WMS["measure_time"]."</span>";
								
if (substr($wms, -10) == 'ba.infn.it') {
	echo "</span></td><td title=\"Click to see ganglia monitoring for ".$wms."\"><a href=\"".$config->bariURL.$wms."\">Ganglia</a></td>";
} else {
			
									if ($config->lemonLink == 1) {
									echo "</span></td><td title=\"Click to see lemon monitoring for ".$wms."\"><a href=\"".$config->lemonURL.$wms."\">Lemon</a></td>";
}

}
									?>
								</td>
							</tr>
						</table>

						<table class="details external">
							<tr class="title">
								<?php
									echo "<td>WMS HW Status</td><td></td>";
									if ($detailsWMSData[0]["disk_sandbox"] > 90) {
        									$row_details = 'row_error';
									} else if ($detailsWMSData[0]["disk_sandbox"] > 80) {
        									$row_details = 'row_warning';
									} else {
        									$row_details = '';
									}
									echo "</tr><tr class=\"".$row_details."\" title=\"Occupancy of directory /var/glite/SandboxDir\">";
									echo "<td>Sandbox partition</td>".$td_string_WMS["disk_sandbox"]."%</td>";
									if ($detailsWMSData[0]["tmp"] > 90) {
        									$row_details = 'row_error';
									} else if ($detailsWMSData[0]["tmp"] > 80) {
        									$row_details = 'row_warning';
									} else {
        									$row_details = '';
									}
									echo "</tr><tr class=\"".$row_details."\" title=\"Occupancy of directory /tmp\">";
									echo "<td>/tmp partition</td>".$td_string_WMS["disk_tmp"]."%</td>";
									if ($detailsWMSData[0]["cpu_load"] > 20) {
        									$row_details = 'row_error';
									} else if ($detailsWMSData[0]["cpu_load"] > 10) {
        									$row_details = 'row_warning';
									} else {
        									$row_details = '';
									}
									echo "</tr><tr class=\"".$row_details."\" title=\"Average CPU load during the past 15 min\">";
									echo "<td>CPU load</td>".$td_string_WMS["cpu_load"]."</td>";
									if ($detailsWMSData[0]["disk_varlog"] > 90) {
                                                                                $row_details = 'row_error';
                                                                        } else if ($detailsWMSData[0]["disk_varlog"] > 80) {
                                                                                $row_details = 'row_warning';
                                                                        } else {
                                                                                $row_details = '';
                                                                        }
									echo "</tr><tr class=\"".$row_details."\" title=\"Occupancy of directory /var/log\">";
									echo "<td>/var/log partition</td>".$td_string_WMS["disk_varlog"]."%</td>";
									if ($detailsWMSData[0]["disk_varlibmysql"] > 90) {
                                                                                $row_details = 'row_error';
                                                                        } else if ($detailsWMSData[0]["disk_varlibmysql"] > 80) {
                                                                                $row_details = 'row_warning';
                                                                        } else {
                                                                                $row_details = '';
                                                                        }
									echo "</tr><tr class=\"".$row_details."\" title=\"Occupancy of directory /var/lib/mysql\">";
									echo "<td>/var/lib/mysql partition</td>".$td_string_WMS["disk_varlibmysql"]."%</td>";

								?>
							</tr>
						</table>

						<table class="details external right">
							<tr class="title">
								<?php
									$status_icon = $detailsWMSData[0]["WMP"] == 0 ? 'check16.png' : 'error16.png';
									echo "<td>Job Stats (JSS)</td><td></td>";
									echo "</tr><tr title=\"Number of jobs in 'Running' state in the condor queue\">";
									echo "<td>Running Condor jobs</td>".$td_string_WMS["condor_running"]."</td>";
									echo "</tr><tr title=\"Number of jobs in 'Idle' state in the condor queue\">";
									echo "<td>Idle Condor jobs</td>".$td_string_WMS["condor_idle"]."</td>";

//									echo "</tr><tr title=\"Number of jobs in 'Running', 'Idle' or 'Held' state in the condor queue\">";
//									echo "<td>Total Condor jobs</td>".$td_string_WMS["condor_current"]."</td>";

									echo "</tr><tr title=\"Number of jobs in 'Running' state in the ICE queue\">";
                                                                        echo "<td>Running ICE jobs</td>".$td_string_WMS["ice_running"]."</td>";
                                                                        echo "</tr><tr title=\"Number of jobs in 'Idle' state in the ICE queue\">";
                                                                        echo "<td>Idle ICE jobs</td>".$td_string_WMS["ice_idle"]."</td>";
									
								?>
							</tr>
						</table>
					</td>


					<td class="separator"></td>

					<td class="general_info lb">
						<table class="general lb">
							<tr class="supertitle">
									<?php
										echo "<td title='List of LBs used by ".$wms." during this time interval'>";	

										echo "Info from LBs <span class=\"weight_normal\">from ".$date_previous."</span><span class=\"undersupertitle\"> to ".$date1."</span>";
										echo "</td>";
//										echo $detailsLBData[0]["lbserver"];
									?>
									<?php

//if (substr($wms, -10) == 'ba.infn.it') {
//        echo "</span></td><td title=\"Click to see ganglia monitoring for ".$wms."\"><a href=\"".$config->bariURL.$wms."\">Ganglia</a></td>";
//} else {
//										if ($config->lemonLink == 1) {
//											echo "<td title=\"Click to see lemon monitoring for ".$detailsLBData[0]["lbserver"]."\"><a href=\"".$config->lemonURL.$detailsLBData[0]["lbserver"]."\">Lemon</a></td>";
//										}

//}
									?>
							</tr>
						</table>

						<table class="details">
								<?php
									if (sizeof($detailsLBAll)==0) {
                                                                        	echo "<tr><td>No LB found in this time interval</td><td></td><td></td><tr>";
                                                                        } else {
	
                        							echo "<thead>";
											echo "<tr class='title'>";
												echo "<td class='cell1'>Hostname</td>";
												echo "<td class='cell2'>Submitted</td>";
												echo "<td class='cell3'></td>";
											echo "</tr>";
										echo "</thead>";

										echo "<tbody><tr><td colspan=\"3\"><div class=\"scroll\"><table class=\"inner_scroll\">";
										$status_icon=array();
										$title=array();
										$y=0;
										foreach ($detailsLBAll as $item) {
											echo "<tr>";

											if (!isset($item['daemon_ll']) && !isset($item['daemon_lb']) && !isset($item['daemon_NTPD'])) {
												$status_icon[$y] = 'documenterror16.png';
                                                                                                $title[$y] = 'No info about daemons status of this LB in this time interval';

											} else if ($item['daemon_ll'] != 100 && $item["daemon_lb"] != 100 && $item['daemon_NTPD'] != 100) {
												$status_icon[$y] = ($item['daemon_ll'] == 0 && $item["daemon_lb"] == 0 && $item['daemon_NTPD'] == 0) ? 'check16.png' : 'error16.png';

												$title[$y] = "LB daemon = ".$item['daemon_lb']." & LL daemon = ".$item['daemon_ll']." & NTPD daemon = ".$item['daemon_NTPD'];
											} else {
												$status_icon[$y] = 'documenterror16.png';
												$title[$y] = 'LB not monitored - no info about its daemon status';
											}
											
											$i=1;
											foreach ($item as $key => $value) {
												if ($key=='hostname') {
													echo "<td class=\"cell".$i."\">".$value."</td>";
													$i++;
												} else if ($key=='occurrences') {
													echo "<td class=\"cell".$i."\" title=\"Number of jobs sumbitted from ".$date_previous." to ".$date1."\">".$value."</td>";
                                                                                                        $i++;
												}
											}
											echo "<td><img src=\"../common/icon/".$status_icon[$y]."\" title=\"$title[$y]\"></img></td></tr>";
											$y++;
										}

										echo "</table>";
										echo "</div>";
										echo "</td>";
                                                                        	echo "</tr>";
										echo "</tbody>";
									}
								?>
						</table>
					</td>
				</tr>

				<tr>
					<td class="separator"></td><td colspan="3">

						<table>
							<br />
							<tr>
									<div id="tabcontainer">
										<ul class="tabbedvoice">
<?php
include 'php-ofc-library/open-flash-chart-object.php';
$chart_type = isset($_GET['chart_type']) ? $_GET['chart_type'] : 'current';
$daily = isset($_GET['daily']) ? $_GET['daily'] : 'week';
$deltat_mins = ceil($detailsLBData[0]["deltat"]/60);

if ($chart_type == 'current') {
echo "<li class=\"tabbedvoiceUP\">Detailed View</li>";
echo "<li class=\"tabbedvoiceDOWN\"><a href=\"details.php?chart_type=daily&wms=".$wms."&interval=".$interval."&daily=".$daily."\">Daily Report</a></li>";
} else {
echo "<li class=\"tabbedvoiceDOWN\"><a href=\"details.php?chart_type=current&wms=".$wms."&interval=".$interval."&daily=".$daily."\">Detailed View</a></li>";
echo "<li class=\"tabbedvoiceUP\">Daily Report</li>";
}
?>
										</ul>
									</div>
							</tr>
						</table>







						<table class="details charts">

<?php
echo "<tr class=\"supertitle chart_form\">";
echo "<td class=\"form_subtitle\" colspan=\"2\">";

if ($chart_type == 'current') {

echo "<form class=\"inline\" action=\"details.php\" method=\"get\" name=\"chartForm\">";
echo "<input type=\"hidden\" name=\"daily\" value=\"".$daily."\"/>";
echo "<input type=\"hidden\" name=\"chart_type\" value=\"".$chart_type."\"/>";
$wmsList = getWMSList('all','all','all','all');
echo "WMS:";
echo "<select name=\"wms\">";
for ($i=0; $i<sizeof($wmsList); $i++) {
        echo "<option value=\"".$wmsList[$i]."\" ";
        if ($wmsList[$i] == $wms) {echo "selected=selected";}
        echo ">".$wmsList[$i]."</option>";
}
echo "</select>";
echo "    Plot a period of ";
echo "<select name=\"interval\">";
echo "<option value=\"day\" ";
if ($interval == 'day') {echo "selected=selected";}
echo ">1 day</option>";
echo "<option value=\"3days\" ";
if ($interval == '3days') {echo "selected=selected";}
echo ">3 days</option>";
echo "<option value=\"week\" ";
if ($interval == 'week') {echo "selected=selected";}
echo ">1 week</option>";
echo "</select>";
echo " ending on ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "<input type=button OnClick=\"change_format('details_chart','chart_2','chart_3','chart_4');\" value=\"png version\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";

echo "<tr><td>";
echo "<form class=\"inline\" action=\"details.php\" method=\"get\" name=\"chartForm3\">";
echo "<input type=\"hidden\" name=\"daily\" value=\"".$daily."\"/>";
echo "<input type=\"hidden\" name=\"chart_type\" value=\"".$chart_type."\"/>";
echo "<input type=\"hidden\" name=\"interval\" value=\"".$interval."\"/>";
echo "<input type=\"hidden\" name=\"endDate\" value=\"".$endDate."\"/>";
echo "<input type=\"hidden\" name=\"wms\" value=\"".$wms."\"/>";
echo "Select JSS: ";
echo "<select name=\"jss_jobs\" onchange=\"this.form.submit()\">";
echo "<option value=\"all\" ";
if ($jss_jobs == 'all') {echo "selected=selected";}
echo ">All</option>";
echo "<option value=\"condor\" ";
if ($jss_jobs == 'condor') {echo "selected=selected";}
echo ">Condor</option>";
echo "<option value=\"ice\" ";
if ($jss_jobs == 'ice') {echo "selected=selected";}
echo ">ICE</option>";
echo "</select>";
echo "</form>";
echo "</td></tr>";

$file_name = "details_chart.php?wms=".$wms."&interval=".$interval."&endDate=".$endDate."&nameSession=".$nameSession;

if ($jss_jobs=='condor') {
        $metrics_1=array("Running condor","Idle condor");
} else if ($jss_jobs=='ice') {
        $metrics_1=array("Running ice","Idle ice");
} else {
        $metrics_1=array("Running condor","Idle condor","Running ice","Idle ice");
}

$metrics_2=array("WM queue","JC queue","LB events queue","Ice queue");
$metrics_3=array("Jobs -> WMProxy","Jobs -> WM","Jobs Resub -> WM");
$metrics_4=array("Total Jobs -> WM","Jobs -> JC","Jobs -> Condor");

$_SESSION['chartData'] = getChartData($wms, $interval, $endDate);

$_SESSION['step'] = getXaxisSteps($interval);
$_SESSION['chart_type'] = $chart_type;

$_SESSION['chartLBData'] = getChartRatesData($wms, $interval, $endDate);

$_SESSION['metrics_1'] = $metrics_1;
$_SESSION['metrics_2'] = $metrics_2;
$_SESSION['metrics_3'] = $metrics_3;
$_SESSION['metrics_4'] = $metrics_4;

$url_parameters='wms='.$wms.'%26interval='.$interval.'%26endDate='.$endDate.'%26nameSession='.$nameSession;
$url_1='details_chart.php?'.$url_parameters;
$url_2='chart_2.php?'.$url_parameters;
$url_3='chart_3.php?'.$url_parameters;
$url_4='chart_4.php?'.$url_parameters;
?>

<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "details_chart",
  "395", "285", "9.0.0", "expressInstall.swf",
	{"data-file":"<?php echo $url_1;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_2",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_2;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_3",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_3;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_4",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_4;?>"} );
</script>

<tr><td><div id="details_chart"></div></td>
<td><div id="chart_2"></div></td></tr>
<tr><td><div id="chart_3"></div></td>
<td><div id="chart_4"></div></td></tr>

<?php

} else {

echo "<form class=\"inline\" action=\"details.php\" method=\"get\" name=\"chartForm2\">";
echo "<input type=\"hidden\" name=\"wms\" value=\"".$wms."\"/>";
echo "<input type=\"hidden\" name=\"interval\" value=\"".$interval."\"/>";
echo "<input type=\"hidden\" name=\"chart_type\" value=\"".$chart_type."\"/>";
$wmsList = getWMSList('all','all','all','all');
echo "WMS:";
echo "<select name=\"wms\">";
for ($i=0; $i<sizeof($wmsList); $i++) {
        echo "<option value=\"".$wmsList[$i]."\" ";
        if ($wmsList[$i] == $wms) {echo "selected=selected";}
        echo ">".$wmsList[$i]."</option>";
}
echo "</select>";
echo "    Plot a period of ";
echo "<select name=\"daily\">";
echo "<option value=\"week\" ";
if ($daily == 'week') {echo "selected=selected";}
echo ">1 week</option>";
echo "<option value=\"2weeks\" ";
if ($daily == '2weeks') {echo "selected=selected";}
echo ">2 weeks</option>";
echo "<option value=\"month\" ";
if ($daily == 'month') {echo "selected=selected";}
echo ">1 month</option>";
echo "</select>";
echo " ending in ";
echo "<input type=\"text\" size=\"10\" value=\"".$endDate."\" readonly name=\"endDate\"/>";
echo "<img title=\"Date calendar\" src='../common/icon/calendar.gif' border='0' id='calendar_icon' onclick=\"displayCalendar(document.forms[0].endDate,'yyyy-mm-dd',this)\">";
echo "<input type=\"submit\" value=\"Submit\"/>";
echo "<input type=button OnClick=\"change_format('chart_5','chart_6','chart_7');\" value=\"png version\"/>";
echo "</form>";
echo "</td>";
echo "</tr>";
echo "<tr><td>";

$_SESSION['chartLBDailyData'] = getChartWMSRatesDailyData($wms, $daily, $endDate);
$_SESSION['stepDaily'] = getXaxisDailySteps($daily);
$_SESSION['chart_type'] = $chart_type;

$metrics_5=array("Jobs -> WMProxy", "Jobs -> WM", "Jobs Resub -> WM");
$metrics_6=array("JOB_DONE", "JOB_ABORTED");
$metrics_7=array("Total Jobs -> WM", "Jobs -> JC", "Jobs -> Condor");

$_SESSION['metrics_5'] = $metrics_5;
$_SESSION['metrics_6'] = $metrics_6;
$_SESSION['metrics_7'] = $metrics_7;

$url_parameters_daily='wms='.$wms.'%26daily='.$daily.'%26endDate='.$endDate.'%26nameSession='.$nameSession;
$url_5='chart_5.php?'.$url_parameters_daily;
$url_6='chart_6.php?'.$url_parameters_daily;
$url_7='chart_7.php?'.$url_parameters_daily;
?>


<script type="text/javascript">

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_5",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_5;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_6",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_6;?>"} );

swfobject.embedSWF(
  "open-flash-chart.swf", "chart_7",
  "395", "285", "9.0.0", "expressInstall.swf",
        {"data-file":"<?php echo $url_7;?>"} );
</script>


<tr><td><div id="chart_5"></div></td>
<td><div id="chart_6"></div></td></tr>
<tr><td><div id="chart_7"></div></td>
<td></td></tr>

<?php
}
?>
						</table>

					</td>
				</tr>
			</table>
		</td>
	</tr>
</table>


</body>
</html>
