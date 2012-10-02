<?php
require_once "config.php";

function getDateInterval($interval, $endDate) {
	$date_int = array();
	$date_int["end"] = $endDate." 23:59:59";
	$date_end_epoch = mktime(intval(substr($date_int["end"], 11, 2)), intval(substr($date_int["end"], 14, 2)), intval(substr($date_int["end"], 17, 2)), intval(substr($date_int["end"], 5, 2)), intval(substr($date_int["end"], 8, 2)), intval(substr($date_int["end"], 0, 4)));
        if (date("Y-m-d") == $endDate) {
		$oneweekago = date("Y-m-d H:i:s", time()-604800);
        	$threedaysago = date("Y-m-d H:i:s", time()-259200);
        	$onedayago = date("Y-m-d H:i:s", time()-86400);
	} else {
		$oneweekago = date("Y-m-d H:i:s", $date_end_epoch-604800);
        	$threedaysago = date("Y-m-d H:i:s", $date_end_epoch-259200);
        	$onedayago = date("Y-m-d H:i:s", $date_end_epoch-86400);
	}

        switch ($interval) {
        case 'day':
                $date_int["start"] = $onedayago;
                break;
        case '3days':
                $date_int["start"] = $threedaysago;
                break;
        case 'week':
                $date_int["start"] = $oneweekago;
                break;
        }

	return $date_int;
}


function getXaxisSteps($interval) {
	switch ($interval) {
        case 'day':
                $step = 24;
                break;
        case '3days':
                $step = 48;
                break;
        case 'week':
                $step = 96;
                break;
        }

        return $step;
}

function getCustomXaxisSteps($startDate, $endDate) {

	$date_start = $startDate." 00:00:00";
	$date_end = $endDate." 23:59:59";
	$date_start_epoch = mktime(intval(substr($date_start, 11, 2)), intval(substr($date_start, 14, 2)), intval(substr($date_start, 17, 2)), intval(substr($date_start, 5, 2)), intval(substr($date_start, 8, 2)), intval(substr($date_start, 0, 4)));
	$date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));
	$num_days = ceil(($date_end_epoch-$date_start_epoch)/86400);

	$step = $num_days*24;

        return $step;
}

function getXaxisDailySteps($daily) {       
        switch ($daily) {
        case 'week':
                $step = 1;
                break;
        case '3weeks':
                $step = 1;
                break;
        case 'month':
                $step = 1;
                break;
        }

        return $step;
}


function getXaxisAggregatedSteps($startDate, $endDate) {
	$date_end = $endDate." 23:59:59";
        $date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));
        $date_start = $startDate." 23:59:59";
        $date_start_epoch = mktime(intval(substr($date_start, 11, 2)), intval(substr($date_start, 14, 2)), intval(substr($date_start, 17, 2)), intval(substr($date_start, 5, 2)), intval(substr($date_start, 8, 2)), intval(substr($date_start, 0, 4)));

        $num_days = ($date_end_epoch-$date_start_epoch)/86400;

	$step = ceil ($num_days/20);

        return $step;
}


function getYaxisMaxValue($max,$upper,$perc_upper) {
	if ($max==0) {
		$max_y=1.00;
	} else if (log10($max)>1) {
   		$max_temp=$max/pow(10, (floor(log10($max)-1)));
   		$max_y=ceil($perc_upper*$max_temp/$upper)*$upper;
   		$max_y=$max_y*pow(10, (floor(log10($max)-1)));
	} else {
   		$max_temp=$max*pow(10, ceil(-log10($max)+1));
   		$max_y=ceil($perc_upper*$max_temp/$upper)*$upper;
   		$max_y=$max_y*pow(10, floor(log10($max)-1));
	}

	return $max_y;
}


function getWmsCount() {
	global $config, $db;
	$result = array();	

        $sql="SELECT DISTINCT wms FROM wmssensor";

	$res=mysql_query($sql);

	while ($row = mysql_fetch_row($res)) {
		array_push($result, $row);
        }

	sort($result);
	return $result;
}


function getMainInfos($scope,$owner,$vo_group,$service_usage) {
        global $config, $db, $now;
	$result = array();
	$wmsList = array();
	$wmsList=getWMSList($scope,$owner,$vo_group,$service_usage);
	sort($wmsList);

	for ($i=0; $i<sizeof($wmsList); $i++) {
//		$sql="SELECT * FROM wms_sensor join hosts IGNORE INDEX (hostname) WHERE wms_sensor.idhost=hosts.idhost and hostname='".$wmsList[$i]."' ORDER BY measure_time DESC LIMIT 1";
		$sql="SELECT h.hostname, w.*, a.vo FROM wms_sensor as w join hosts as h IGNORE INDEX (hostname), admin_host_labels as a WHERE w.idhost=h.idhost and h.idhost=a.idhost and hostname='".$wmsList[$i]."' ORDER BY measure_time DESC LIMIT 1";
		$res=mysql_query($sql);
		while ($row = mysql_fetch_array($res)) {
			array_push($result, $row);
        	}
	}

	return $result;
}

function getMainLBInfos($owner) {
        global $config, $db, $now;
        $result = array();

	$lbList=getLBList($owner);
	sort($lbList);

	for ($i=0; $i<sizeof($lbList); $i++) {
//                $sql="SELECT * FROM lbsensor WHERE wms ='".$wmsList[$i]."' ORDER BY date DESC LIMIT 1";
//		$sql="SELECT * FROM lb_sensor join hosts IGNORE INDEX (hostname) WHERE lb_sensor.idhost=hosts.idhost and hostname='".$lbList[$i]."' ORDER BY measure_time DESC LIMIT 1";
		$sql="SELECT * FROM lb_sensor join hosts IGNORE INDEX (hostname) WHERE lb_sensor.idhost=hosts.idhost and hostname='".$lbList[$i]."' ORDER BY measure_time DESC LIMIT 1";
                $res=mysql_query($sql);
                while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                        array_push($result, $row);
                }
        }
        return $result;
}

function getChartData($wms, $interval, $endDate) {
        global $config, $db;
 	$result = array();

	$date_int = getDateInterval($interval, $endDate);

//	$sql="SELECT running, idle, date, input_fl, queue_fl, dg20 FROM wmssensor WHERE wms = '".$wms."' and date > '".$date_int["start"]."' and date <= '".$date_int["end"]."' ORDER BY date";
	$sql="SELECT condor_running as 'Running condor', condor_idle as 'Idle condor', measure_time as date, wm_queue as 'WM queue', jc_queue as 'JC queue', lb_event as 'LB events queue', ice_queue as 'Ice queue', ice_running as 'Running ice', ice_idle as 'Idle ice' from wms_sensor join hosts IGNORE INDEX (hostname) WHERE wms_sensor.idhost=hosts.idhost and hostname='".$wms."' and measure_time > '".$date_int["start"]."' and measure_time <= '".$date_int["end"]."' ORDER BY date";
 
      $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

	return $result;
}





function getCustomAllData($wms, $startDate, $endDate, $allSensorFields) {
        global $config, $db;
        $result = array();
        $startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

	$sql="SELECT measure_time as `date`,";

	$i=1;
	foreach ($allSensorFields as $key => $value) {
		$sql=$sql.$key.' as `'.$value.'`';
		if ($i != sizeof($allSensorFields)) {
			$sql=$sql.", ";
		}
		$i++;		
	}

	$sql=$sql." FROM wms_sensor join hosts IGNORE INDEX (hostname) WHERE wms_sensor.idhost=hosts.idhost and hostname='".$wms."' and measure_time > '".$startDate."' and measure_time <= '".$endDate."' ORDER BY date";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}



function getChartLBData($wms, $interval, $endDate) {
        global $config, $db;
        $result = array();

	$date_int = getDateInterval($interval, $endDate);

        $sql="SELECT date, WMP_in, WM_in, WM_in_res, JC_in, JC_out, deltat, WMP_in_col FROM lbsensor WHERE wms = '".$wms."' and date > '".$date_int["start"]."' and date <= '".$date_int["end"]."' ORDER BY date";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_row($res)) {
                array_push($result, $row);
        }

        return $result;
}


function getMetricWMSList() {
        global $config, $db;
	$result = array();
	
	$sql="SELECT DISTINCT wms FROM wmsloadbalance";

        $res=mysql_query($sql);

	while ($row = mysql_fetch_array($res, MYSQL_NUM)) {
                array_push($result, $row);
        }

        return $result;
}




function getMetricData($wms, $startDate, $endDate) {
        global $config, $db;
        $result = array();
        $startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

//        $sql="SELECT date, wms, fload, ftraversaltime, MEMUSAGE FROM wmsloadbalance WHERE wms = '".$wms."' and date > '".$startDate."' and date <= '".$endDate."' ORDER BY date";


   	$sql="SELECT measure_time as date, wms_sensor.idhost, loadb_fload as `fload`, loadb_ftraversaltime as `ftraversaltime`, loadb_fmetric as `fmetric`, disk_sandbox as `disk`, loadb_memusage as `memusage`, cpu_load as `load`, wm_queue as `WM queue`, jc_queue as `JC queue`, lb_event as `LB events` FROM wms_sensor join hosts WHERE wms_sensor.idhost=hosts.idhost and hosts.hostname= '".$wms."' and measure_time > '".$startDate."' and measure_time <= '".$endDate."' ORDER BY measure_time";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}


function getVOMetricData($wms_list, $startDate, $endDate) {
	global $config, $db;
        $result = array();
	$startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

	foreach ($wms_list as $wms) {
		$result[$wms] = array();
        	$sql[$wms]="SELECT * FROM wmsloadbalance WHERE wms = '".$wms."' and date > '".$startDate."' and date <= '".$endDate."' ORDER BY date";

        	$res[$wms]=mysql_query($sql[$wms]);

        	while ($row[$wms] = mysql_fetch_array($res[$wms], MYSQL_ASSOC)) {
                	array_push($result[$wms], $row[$wms]);
        	}
	}

        return $result;
}


//function getCustomChartLBData($wms, $startDate, $endDate) {
function getCustomJobData($wms, $startDate, $endDate, $jobRatesFields) {
        global $config, $db;
        $result = array();
	$startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

	$sql="SELECT start_date as `date`, timestampdiff(SECOND, start_date, end_date) as `deltat`,";

        $i=1;
        foreach ($jobRatesFields as $key => $value) {
                $sql=$sql.$key.' as `'.$value.'`';
                if ($i != sizeof($jobRatesFields)) {
                        $sql=$sql.", ";
                }
                $i++;
        }

        $sql=$sql." FROM wms_rates join hosts IGNORE INDEX (hostname) WHERE wms_rates.idhost=hosts.idhost and hostname='".$wms."' and start_date > '".$startDate."' and start_date <= '".$endDate."'";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}



function getChartLBDailyData($wms, $daily, $endDate) {
        global $config, $db;
	$result = array();
	
	switch ($daily) {
        case 'week':
                $num_days = 7;
                break;
        case '2weeks':
                $num_days = 14;
                break;
        case 'month':
                $num_days = 30;
                break;
        }	

	$date_end = $endDate." 23:59:59";
	$date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));

        $date_start_epoch = $date_end_epoch-($num_days-1)*86400;
	$date_start = date("Y-m-d", $date_start_epoch);
	
	$sql="SELECT date(date), WMP_in, WM_in, WM_in_res, JC_in, JC_out, JOB_DONE, JOB_ABORTED, WMP_in_col FROM lbsensor_daily WHERE wms ='".$wms."' and date between '".$date_start."' and '".$date_end."' GROUP BY date ORDER BY date,ID_Rec DESC";
	$res=mysql_query($sql); 
	while ($row = mysql_fetch_array($res, MYSQL_NUM)) {
        	array_push($result, $row);
        }

        return $result;
}



function getCustomJobDailyData($wms, $startDate, $endDate, $jobRatesFields) {
        global $config, $db;
        $result = array();

//$date_start = $startDate." 00:00:00";
//$date_end = $endDate." 23:59:59";
//$date_start_epoch = mktime(intval(substr($date_start, 11, 2)), intval(substr($date_start, 14, 2)), intval(substr($date_start, 17, 2)), intval(substr($date_start, 5, 2)), intval(substr($date_start, 8, 2)), intval(substr($date_start, 0, 4)));
//$date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));
//$num_days = ceil(($date_end_epoch-$date_start_epoch)/86400);


        $startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";
        $sql="SELECT date(day) as `date`, ";
        $i=1;
        foreach ($jobRatesFields as $key => $value) {
                $sql=$sql.$key.' as `'.$value.'`';
                if ($i != sizeof($jobRatesFields)) {
                        $sql=$sql.", ";
                }
                $i++;
        }
        $sql=$sql." FROM wms_rates_daily join hosts IGNORE INDEX (hostname) WHERE wms_rates_daily.idhost=hosts.idhost and hostname='".$wms."' and date(day) > '".$startDate."' and date(day) <= '".$endDate."'";


//echo $sql;


//        $sql="SELECT date(date) as `date`, WMP_in as `Jobs -> WMProxy`, WM_in as `Jobs -> WM`, WM_in_res as `Jobs Resub -> WM`, JC_in as `Jobs -> JC`, JC_out as `Jobs JC -> Condor`, WMP_in_col as `Collections`, JOB_DONE as `Job done`, JOB_ABORTED as `Job aborted` FROM lbsensor_daily WHERE wms ='".$wms."' and date between '".$date_start."%' and '".$date_end."%' ORDER BY date";
        $res=mysql_query($sql);
        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}


function getAggregatedChartLBDailyDataByUsers($vo, $startDate, $endDate) {
	global $config, $db;

//        $date_end = $endDate." 23:59:59";
//        $date_start = $startDate." 00:00:00";

	$date_end = $endDate;
	$date_start = $startDate;

        $result = array();

//        $sql="select sum(job_done) as `JOB_DONE`, sum(job_aborted) as `JOB_ABORTED`, date(date) as date, SUM(WMP_in) as `WMP_in`, SUM(JC_out) as `JC_out`, SUM(WMP_in_col) as `WMP_in_col` from users where date between '".$date_start."' and '".$date_end."' and vo='".$vo."' group by date order by date desc";
	$sql="select sum(user_rates_daily.job_done) as `JOB_DONE`, sum(user_rates_daily.job_aborted) as `JOB_ABORTED`, user_rates_daily.day as `date`, SUM(user_rates_daily.WMP_in) as `WMP_in`, SUM(user_rates_daily.JC_out) as `JC_out`, SUM(user_rates_daily.WMP_in_col) as `WMP_in_col` from user_rates_daily join user_map on user_rates_daily.idusermap=user_map.idusermap where day between '".$date_start."' and '".$date_end."' and user_map.vo='".$vo."' group by date order by date";

        $res=mysql_query($sql);
        if (mysql_num_rows($res) > 0) {
                while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                        array_push($result, $row);
                }
        }
        return $result;

}


function getWMSUsageChartLBDailyDataByUsers($vo, $startDate, $endDate) {
        global $config, $db, $now;
        $result = array();

//        $endDate = $endDate." 23:59:59";
//        $startDate = $startDate." 00:00:00";

	$date_end = $endDate;
        $date_start = $startDate;

//	$sql="select wms, SUM(JOB_DONE) as `JOB_DONE`, SUM(JOB_ABORTED) as `JOB_ABORTED`, SUM(WMP_in) as `WMP_in`, SUM(JC_out) as `JC_out`, SUM(WMP_in_col) as `WMP_in_col`, date FROM users where date > '".$startDate."%' and date <= '".$endDate."%' and VO = '".$vo."' group by wms";
	$sql="select hosts.hostname as `wms`, SUM(user_rates_daily.JOB_DONE) as `JOB_DONE`, SUM(user_rates_daily.JOB_ABORTED) as `JOB_ABORTED`, SUM(user_rates_daily.WMP_in) as `WMP_in`, SUM(user_rates_daily.JC_in) as `JC_in`, SUM(user_rates_daily.JC_out) as `JC_out`, SUM(user_rates_daily.WMP_in_col) as `WMP_in_col`, day FROM user_rates_daily join user_map,hosts where user_rates_daily.idusermap=user_map.idusermap and hosts.idhost=user_rates_daily.idhost and day > '".$startDate."%' and day <= '".$endDate."%' and user_map.VO = '".$vo."' group by wms";

	$res=mysql_query($sql);
	while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
		array_push($result, $row);
        }

	return $result;
}


function orderBy($data, $field) {
	$code = "return strnatcmp(\$a['$field'], \$b['$field']);";
        usort($data, create_function('$a,$b', $code));
}


function getVOUsageLBDailyDataByUsers($scope, $startDate, $endDate, $volist_type, $custom_vos) {
        global $config, $db, $now;
        $result = array();
        $result1 = array();
        $volist=array();

//        $date_end = $endDate." 23:59:59";
	$date_end = $endDate;
        $date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));
//        $date_start = $startDate." 00:00:00";
	$date_start = $startDate;
        $date_start_epoch = mktime(intval(substr($date_start, 11, 2)), intval(substr($date_start, 14, 2)), intval(substr($date_start, 17, 2)), intval(substr($date_start, 5, 2)), intval(substr($date_start, 8, 2)), intval(substr($date_start, 0, 4)));


//Create an array with alla days between $date_start and $date_end
	$num_days = ($date_end_epoch-$date_start_epoch)/86400;
        $all_days=array();
        for ($j=0; $j<$num_days; $j++) {
        	array_push($all_days, date("Y-m-d", $date_end_epoch-(($num_days-$j)*86400)));
        }

//Create the VO list. 3 different kind: LHC, best 10 (by JOB_DONE), all vos and a customizable (by the web interface) set of VOs
if ($volist_type == 'lhc' || $volist_type == 'lhc-nonlhc') {
        $volist = array('alice', 'atlas', 'cms', 'lhcb');
} else if ($volist_type == 'best') {
//        $sql_volist="SELECT VO AS `VO`, SUM(JOB_DONE) as `JOB_DONE` from users WHERE date >= '".$date_start."' and date < '".$date_end."' and VO != '' GROUP BY VO ORDER BY JOB_DONE desc LIMIT 10";
	$sql_volist="SELECT user_map.vo AS `VO`, SUM(user_rates_daily.JOB_DONE) as `JOB_DONE` from user_rates_daily join user_map on user_rates_daily.idusermap=user_map.idusermap WHERE user_rates_daily.day >= '".$date_start."' and user_rates_daily.day < '".$date_end."' and VO != '' GROUP BY VO ORDER BY JOB_DONE desc LIMIT 10";

        $res_volist=mysql_query($sql_volist);

        while ($row = mysql_fetch_row($res_volist)) {
                array_push($volist, $row[0]);
        }

} else if ($volist_type == 'all') {
//        $sql_volist="SELECT DISTINCT(VO) AS `VO` from users WHERE date >= '".$date_start."' and date < '".$date_end."' and VO != '' ORDER BY VO asc";
	$sql_volist="SELECT DISTINCT(user_map.VO) AS `VO` from user_map join user_rates_daily on user_rates_daily.idusermap=user_map.idusermap WHERE user_rates_daily.day >= '".$date_start."' and user_rates_daily.day < '".$date_end."' and VO != '' ORDER BY VO asc";

        $res_volist=mysql_query($sql_volist);

        while ($row = mysql_fetch_row($res_volist)) {
                array_push($volist, $row[0]);
        }
} else {
        $volist = array_values($custom_vos);
}


//Execute a unique query to obtain all data to plot
//	 $sql="select VO as `VO`, SUM(JOB_DONE) as `JOB_DONE`, SUM(JOB_ABORTED) as `JOB_ABORTED`, SUM(WMP_in) as `WMP_in`, SUM(JC_out) as `JC_out`, SUM(WMP_in_col) as `WMP_in_col`, SUM(WM_in_res) as `WM_in_res`, date(date) as date FROM users where date between '".$date_start."' and '".$date_end."' and VO in (";
	$sql="select user_map.vo as `VO`, SUM(user_rates_daily.JOB_DONE) as `JOB_DONE`, SUM(user_rates_daily.JOB_ABORTED) as `JOB_ABORTED`, SUM(user_rates_daily.WMP_in) as `WMP_in`, SUM(user_rates_daily.JC_out) as `JC_out`, SUM(user_rates_daily.WMP_in_col) as `WMP_in_col`, SUM(user_rates_daily.WM_in_res) as `WM_in_res`, user_rates_daily.day as date FROM user_rates_daily join user_map on user_rates_daily.idusermap=user_map.idusermap where user_rates_daily.day between '".$date_start."' and '".$date_end."' and VO in (";
                        for ($i=0; $i<sizeof($volist)-1; $i++) {
                                $sql=$sql."'".$volist[$i]."', ";
                        }
                        $sql=$sql."'".$volist[$i]."'";
                        $sql=$sql.") group by date,VO";

                        $res=mysql_query($sql);

			$result = array();
                        $result2 = array();
			$days = array();

                        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
				array_push($days, $row['date']);
                                array_push($result2, $row);
	
                        }

			if ($volist_type == 'lhc-nonlhc') {
//        			$sql_nonlhc="select SUM(JOB_DONE) as `JOB_DONE`, SUM(JOB_ABORTED) as `JOB_ABORTED`, SUM(WMP_in) as `WMP_in`, SUM(JC_out) as `JC_out`, SUM(WMP_in_col) as `WMP_in_col`, SUM(WM_in_res) as `WM_in_res`, date(date) as date FROM users where date between '".$date_start."' and '".$date_end."' and VO not in (";
				$sql_nonlhc="select SUM(user_rates_daily.JOB_DONE) as `JOB_DONE`, SUM(user_rates_daily.JOB_ABORTED) as `JOB_ABORTED`, SUM(user_rates_daily.WMP_in) as `WMP_in`, SUM(user_rates_daily.JC_out) as `JC_out`, SUM(user_rates_daily.WMP_in_col) as `WMP_in_col`, SUM(user_rates_daily.WM_in_res) as `WM_in_res`, user_rates_daily.day as date FROM user_rates_daily join user_map on user_rates_daily.idusermap=user_map.idusermap where user_rates_daily.day between '".$date_start."' and '".$date_end."' and user_map.vo not in (";
				for ($i=0; $i<sizeof($volist)-1; $i++) {
                                	$sql_nonlhc=$sql_nonlhc."'".$volist[$i]."', ";
                        	}
                        	$sql_nonlhc=$sql_nonlhc."'".$volist[$i]."'";
                        	$sql_nonlhc=$sql_nonlhc.") group by date";
				$res_nonlhc=mysql_query($sql_nonlhc);
				while ($row = mysql_fetch_array($res_nonlhc, MYSQL_ASSOC)) {
					$row['VO']='non-LHC';
                                	array_push($result2, $row);
                        	}
				array_push($volist, 'non-LHC');
			}

			$days = array_values(array_unique($days));
			sort($volist);

			$i=0;
			//For each day in the $all_days array, we create the result array
			foreach ($all_days as $value) {
				//In order to have alla days plotted in the chart, not only days with not null values:
				//If for a specific day there are result from the query, push the result array
				if (in_array($value, $days)) {
					$not_null_index=array();
					foreach ($result2 as $value2) {
						if ($value2['date'] == $value) {
							$j=0;
							while ($j<sizeof($volist)) {
								if ($value2['VO'] == $volist[$j]) {
									$result[$i][$j] = $value2;
									$not_null_index[$j]=1;
                                                		} else {
									//Check if exist a row in the result array for that VO with not null values
									if (!isset($not_null_index[$j])) {
										$result[$i][$j] = array("VO" => $volist[$j], "JOB_DONE" => 0, "JOB_ABORTED" => 0, "WMP_in" => 0, "JC_out" => 0, "WMP_in_col" => 0, "WM_in_res" => 0, "date" => $value2['date']);	
									}
								}
								$j++;
							}
						}
					}

				//else push the result array with null values
				} else {
					$j=0;
					while ($j<sizeof($volist)) {
						$result[$i][$j] = array("VO" => $volist[$j], "JOB_DONE" => 0, "JOB_ABORTED" => 0, "WMP_in" => 0, "JC_out"=> 0, "WMP_in_col" => 0, "WM_in_res" => 0, "date" => $value);
						$j++;	
					}
				}
				$i++;
			}

                        return $result;
}


function getVOUsageLBDailyDataByUsersOldStyle($scope, $startDate, $endDate) {
        global $config, $db, $now;
        $result = array();
        $result1 = array();
        $volist=array();

        $date_end = $endDate." 23:59:59";
        $date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));
        $date_start = $startDate." 00:00:00";
        $date_start_epoch = mktime(intval(substr($date_start, 11, 2)), intval(substr($date_start, 14, 2)), intval(substr($date_start, 17, 2)), intval(substr($date_start, 5, 2)), intval(substr($date_start, 8, 2)), intval(substr($date_start, 0, 4)));

        $sql_volist="SELECT DISTINCT(VO) AS `VO` from lbsensor_daily WHERE date >= '".$date_start."' and date < '".$date_end."' and VO != '' and VO != 'devel' and VO != 'multi' ORDER BY VO asc";
      $res_volist=mysql_query($sql_volist);

        while ($row = mysql_fetch_row($res_volist)) {
                array_push($volist, $row[0]);
        }

        $num_days = ($date_end_epoch-$date_start_epoch)/86400;
for ($j=0; $j<$num_days; $j++) {
                        $today1 = date("Y-m-d", $date_end_epoch-(($num_days-$j)*86400));

$sql="select VO as `VO`, SUM(JOB_DONE) as `JOB_DONE`, SUM(JOB_ABORTED) as `JOB_ABORTED`, SUM(WMP_in) as `WMP_in`, SUM(JC_out) as `JC_out`, SUM(WMP_in_col) as `WMP_in_col`, SUM(WM_in_res) as `WM_in_res`, date FROM lbsensor_daily where date like '".$today1."%' and VO != ''  and VO != 'devel' and VO != 'multi' group by VO";

                        $sql2="SELECT DISTINCT(VO) AS `VO`  from lbsensor_daily WHERE date like '".$today1."%' and VO != ''  and VO != 'devel' and VO != 'multi' ORDER BY VO asc";

                        $res=mysql_query($sql);

                        $result[$j] = array();
                        $result1[$j] = array();

                        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                                array_push($result[$j], $row);
                        }

                        $result2 = array();
                        $res2=mysql_query($sql2);
                        while ($row2 = mysql_fetch_row($res2)) {
                                array_push($result2, $row2[0]);
                        }

$y=0;
                        for ($i=0; $i<sizeof($volist); $i++) {
                                if (!(in_array($volist[$i], $result2))) {
                                        $result1[$j][$i] = array("VO" => $volist[$i], "JOB_DONE" => 0, "JOB_ABORTED" => 0, "WMP_in" => 0, "JC_out" => 0, "WMP_in_col" => 0, "WM_in_res" => 0);
                                } else {
                                        $result1[$j][$i] = $result[$j][$y];
                                        $y++;
                                }
                        }
              }
        return $result1;
}


function getDetailsWMSData($wms) {
        global $config, $db;
        $result = array();

//        $sql="SELECT * FROM wmssensor WHERE wms = '".$wms."' ORDER BY date DESC LIMIT 1";

//	$sql="SELECT * FROM wms_sensor join hosts IGNORE INDEX (hostname) WHERE wms_sensor.idhost=hosts.idhost and hostname='".$wms."' ORDER BY measure_time DESC LIMIT 1";
  
	$sql="SELECT * FROM wms_sensor join hosts WHERE wms_sensor.idhost=hosts.idhost and hostname='".$wms."' and timestampdiff(SECOND, wms_sensor.measure_time, (select max(end_date) from wms_rates join hosts on wms_rates.idhost=hosts.idhost and hosts.hostname='".$wms."')) between -300 and 300";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}


function getDetailsLBData($wms) {
        global $config, $db;
        $result = array();

        $sql="SELECT * FROM lbsensor WHERE wms = '".$wms."' ORDER BY date DESC LIMIT 1";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}


function getDetailsLBDailyData($wms) {
        global $config, $db;
        $result = array();

        $sql="SELECT * FROM lbsensor_daily WHERE wms = '".$wms."' ORDER BY date DESC LIMIT 1";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getCEMMWMSData($wms, $startDate, $endDate) {
        global $config, $db;
        $result = array();
//        $startDate = $startDate." 00:00:00";
//        $endDate = $endDate." 23:59:59";

//	$sql="SELECT cehosts.hostname as ce, sum(occurrences) as `occurrence` FROM ce_stats join cehosts, hosts where ce_stats.idcehost=cehosts.idcehost and hosts.idhost=ce_stats.idwms and hosts.hostname = '".$wms."' and measure_time > '".$startDate."' and measure_time <= '".$endDate."' GROUP BY ce ORDER BY occurrence desc";

//        $sql="SELECT num_ce, sum(occurrence) as `occurrence` FROM ce_mm WHERE wms = '".$wms."' and date > '".$startDate."' and date <= '".$endDate."' GROUP BY num_ce ORDER BY num_ce";

	$sql="SELECT num_ce, sum(occurrences) as `occurrence` FROM ce_mm join hosts WHERE hosts.idhost=ce_mm.idhost and hosts.hostname = '".$wms."' and day >= '".$startDate."' and day <= '".$endDate."' GROUP BY num_ce ORDER BY num_ce";

        $res=mysql_query($sql);
	$max_num_ce = 0;

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
		$result[$row["num_ce"]] = $row["occurrence"];
		if ($max_num_ce < $row["num_ce"]) {
                	$max_num_ce = $row["num_ce"];
        	}
        }

	for ($i=0; $i<$max_num_ce; $i++) {
	if (!isset($result[$i])) {
		$result[$i]=0;
	}
	}

        return $result;
}

function getCEMMVOData($vo, $startDate, $endDate) {
        global $config, $db;
        $result = array();
        $startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

        $sql="SELECT num_ce, sum(occurrence) as `occurrence` FROM ce_mm WHERE vo = '".$vo."' and date >= '".$startDate."' and date <= '".$endDate."' GROUP BY num_ce ORDER BY num_ce";

        $res=mysql_query($sql);
        $max_num_ce = 0;

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                $result[$row["num_ce"]] = $row["occurrence"];
                if ($max_num_ce < $row["num_ce"]) {
                        $max_num_ce = $row["num_ce"];
                }
        }

        for ($i=0; $i<$max_num_ce; $i++) {
        if (!isset($result[$i])) {
                $result[$i]=0;
        }
        }

        return $result;
}

function getCEStatsWMSData($wms, $startDate, $endDate) {
        global $config, $db;
        $result = array();
        $startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

//        $sql="SELECT ce, sum(occ) as `occurrence` FROM ce_stats WHERE wms = '".$wms."' and date > '".$startDate."' and date <= '".$endDate."' GROUP BY ce ORDER BY occurrence desc";

	$sql="SELECT cehosts.hostname as ce, sum(occurrences) as `occurrence` FROM ce_stats_daily join cehosts, hosts where ce_stats_daily.idcehost=cehosts.idcehost and hosts.idhost=ce_stats_daily.idwms and hosts.hostname = '".$wms."' and day >= '".$startDate."' and day <= '".$endDate."' GROUP BY ce ORDER BY occurrence desc";

	$res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getCEStatsVOData($vo, $startDate, $endDate) {
        global $config, $db;
        $result = array();
        $startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

//        $sql="SELECT ce, sum(occ) as `occurrence` FROM ce_stats_daily WHERE vo = '".$vo."' and date > '".$startDate."' and date <= '".$endDate."' GROUP BY ce ORDER BY occurrence desc";

	$sql="SELECT hostname as `ce`, sum(occurrences) as `occurrence` FROM ce_stats_daily join cehosts, user_map where ce_stats_daily.idcehost=cehosts.idcehost and user_map.idusermap=ce_stats_daily.idusermap  and vo = '".$vo."' and day > '".$startDate."' and day <= '".$endDate."' GROUP BY hostname ORDER BY occurrence desc";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getWMSList($scope,$owner,$vo_group,$service_usage) {
	global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT(hostname) FROM hosts join admin_host_labels on hosts.idhost=admin_host_labels.idhost WHERE service = 'WMS' and active=1"; 
	if ($scope!='all') {
		$sql.=" and vo='".$scope."'";
	}
	if ($owner!='all') {
                $sql.=" and host_owner='".$owner."'";
        }
	if ($vo_group!='all') {
                $sql.=" and vo_group='".$vo_group."'";
        }
        if ($service_usage!='all') {
                $sql.=" and service_usage='".$service_usage."'";
        }
 	$sql.=" ORDER BY hostname asc";

	$res=mysql_query($sql);

        while ($row = mysql_fetch_array($res)) {
                array_push($result, $row[0]);
        }

        return $result;
}


function getWMSListCEStats() {
	global $config, $db;
        $result = array();

//        $sql="SELECT DISTINCT(wms) FROM ce_stats ORDER BY wms asc";

	$sql="SELECT DISTINCT(hosts.hostname) as wms FROM hosts join ce_stats_daily on hosts.idhost=ce_stats_daily.idwms ORDER BY wms asc";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getUsersStatsWMSData($wms, $startDate, $endDate, $orderedBy) {
        global $config, $db;
        $result = array();
//        $startDate = $startDate." 00:00:00";
//       $endDate = $endDate." 23:59:59";

//	$sql="SELECT dn, sum(WMP_in) as `Jobs submitted`, sum(JOB_DONE) as `Jobs done`, sum(JOB_ABORTED) as `Jobs aborted` FROM users WHERE wms = '".$wms."' and date > '".$startDate."' and date <= '".$endDate."' GROUP BY dn ORDER BY `".$orderedBy."` desc";
	$sql="SELECT (CASE users.dn WHEN '' THEN 'Unknown_DN' ELSE users.dn END) as dn, sum(WMP_in) as `Jobs_submitted`, sum(JOB_DONE) as `Jobs_done`, sum(JOB_ABORTED) as `Jobs_aborted` FROM user_rates_daily join user_map, hosts, users WHERE user_map.idusermap=user_rates_daily.idusermap and hosts.idhost=user_rates_daily.idhost and user_map.iduser=users.iduser and hosts.hostname = '".$wms."' and user_rates_daily.day >= '".$startDate."' and user_rates_daily.day <= '".$endDate."' GROUP BY dn ORDER BY `".$orderedBy."` desc";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getUsersStatsVOData($vo, $startDate, $endDate, $orderedBy) {
        global $config, $db;
        $result = array();
//       $startDate = $startDate." 00:00:00";
//        $endDate = $endDate." 23:59:59";

//        $sql="SELECT dn, sum(WMP_in) as `Jobs submitted`, sum(JOB_DONE) as `Jobs done`, sum(JOB_ABORTED) as `Jobs aborted` FROM users WHERE vo = '".$vo."' and date > '".$startDate."' and date <= '".$endDate."' GROUP BY dn ORDER BY `".$orderedBy."` desc";

	$sql="SELECT (CASE users.dn WHEN '' THEN 'Unknown_DN' ELSE users.dn END) as dn, sum(WMP_in) as `Jobs_submitted`, sum(JOB_DONE) as `Jobs_done`, sum(JOB_ABORTED) as `Jobs_aborted` FROM user_rates_daily join user_map, users WHERE user_map.idusermap=user_rates_daily.idusermap  and user_map.iduser=users.iduser and user_map.vo = '".$vo."' and user_rates_daily.day >= '".$startDate."' and user_rates_daily.day <= '".$endDate."' GROUP BY dn ORDER BY `".$orderedBy."` desc";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function guess_name($dn) {
        $cnA=explode("CN=",$dn);
        $cn=$cnA[count($cnA)-1];
        $cnA=explode("/",$cn);
        $cn=$cnA[0];
        $cn=trim($cn,"0123456789 ");
        $cn=ucsmart($cn);
        return $cn;
}

function ucsmart($text, $tolower=1) {
        if($tolower) $text=strtolower($text);
        $text=str_replace("- ","-",str_replace("' ","'",ucwords(str_replace("'","' ",str_replace("-","- ",$text)))));
        return $text;
}

function getVOList() {
        global $config, $db;
        $result = array();

	$sql="SELECT DISTINCT(vo) FROM user_map where vo != '' order by vo";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_NUM)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getVOListCEStats() {
        global $config, $db;
        $result = array();

	$sql="SELECT DISTINCT(user_map.vo) FROM user_map join ce_stats_daily on user_map.idusermap=ce_stats_daily.idusermap where user_map.vo != '' order by vo;";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_NUM)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function isThereCertificate() {
	$dn=$_SERVER['SSL_CLIENT_S_DN'];
	if($dn=="") return "no_certificate";
}

function getServiceUsageList($scope) {
        global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT(service_usage) FROM admin_host_labels where service='WMS' and active=1";

	if ($scope!='all') {
                $sql.=" and vo='".$scope."'";
        }

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getVOGroupList($scope) {
        global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT(vo_group) FROM admin_host_labels where service='WMS' and active=1";

	if ($scope!='all') {
                $sql.=" and vo='".$scope."'";
        }

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getHostOwnerList($scope) {
        global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT(host_owner) FROM admin_host_labels where service='WMS' and active=1";

	if ($scope!='all') {
		$sql.=" and vo='".$scope."'";
	}

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getLBOwnerList() {
        global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT(host_owner) FROM admin_host_labels where service='LB' and active=1";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getLBList($owner) {
        global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT(hostname) FROM hosts join admin_host_labels on hosts.idhost=admin_host_labels.idhost WHERE service = 'LB' and active=1";
	if ($owner!='all') {
                $sql.=" and host_owner='".$owner."'";
        }
	$sql.=" ORDER BY hostname asc";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getStaticVOList() {
        global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT(vo) FROM admin_host_labels where service = 'WMS' and active=1 order by vo";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_NUM)) {
                array_push($result, $row[0]);
        }

        return $result;
}

function getDetailsWMSRates($wms) {
        global $config, $db;
        $result = array();

//        $sql="SELECT * FROM wmssensor WHERE wms = '".$wms."' ORDER BY date DESC LIMIT 1";

        $sql="SELECT * FROM wms_rates join hosts WHERE wms_rates.idhost=hosts.idhost and hostname='".$wms."' ORDER BY end_date DESC LIMIT 1";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getDetailsLBHist($wms) {
        global $config, $db;
        $result = array();

#	$sql="SELECT lbhosts.hostname, occurrences FROM lb_hist join hosts, lbhosts WHERE lb_hist.idlb=lbhosts.idlbhost and lb_hist.idwms=hosts.idhost and hosts.hostname = '".$wms."' and timestampdiff(SECOND, lb_hist.measure_time, (select max(measure_time) from wms_sensor join hosts on wms_sensor.idhost=hosts.idhost where hosts.hostname = '".$wms."')) between -10 and 10 and timestampdiff(SECOND, lb_hist.measure_time, (select max(measure_time) from lb_hist)) between -10 and 10 ORDER BY lb_hist.measure_time DESC";

	$sql="SELECT lbhosts.hostname, occurrences FROM lb_hist join hosts, lbhosts WHERE lb_hist.idlb=lbhosts.idlbhost and lb_hist.idwms=hosts.idhost and hosts.hostname = '".$wms."' and lb_hist.measure_time = (select max(end_date) from wms_rates join hosts where wms_rates.idhost=hosts.idhost and hosts.hostname = '".$wms."') ORDER BY lb_hist.measure_time DESC";

#	$sql="SELECT hosts.hostname, occurrences FROM lb_hist join hosts WHERE lb_hist.idlb=hosts.idhost and lb_hist.idwms=(select idhost from hosts where hostname = '".$wms."') and lb_hist.measure_time = (select max(end_date) from wms_rates join hosts where wms_rates.idhost=hosts.idhost and hosts.hostname = '".$wms."') ORDER BY lb_hist.measure_time DESC";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}


function getDetailsLBSensor($wms) {
        global $config, $db;
        $result = array();

#	$sql="SELECT hosts.hostname, daemon_lb, daemon_ll, daemon_NTPD FROM lb_sensor join hosts ON lb_sensor.idhost=hosts.idhost WHERE lb_sensor.idhost=(select idhost from hosts where hostname in (SELECT lbhosts.hostname FROM lb_hist join hosts, lbhosts WHERE lb_hist.idlb=lbhosts.idlbhost and lb_hist.idwms=hosts.idhost and hosts.hostname = '".$wms."' and timestampdiff(SECOND, lb_hist.measure_time, (select max(measure_time) from wms_sensor join hosts on wms_sensor.idhost=hosts.idhost where hosts.hostname = '".$wms."')) between -10 and 10 and timestampdiff(SECOND, lb_hist.measure_time, (select max(measure_time) from lb_hist)) between -10 and 10 ORDER BY lb_hist.measure_time DESC)) and  timestampdiff(SECOND, lb_sensor.measure_time, (select max(measure_time) from wms_sensor join hosts on wms_sensor.idhost=hosts.idhost where hosts.hostname = '".$wms."')) between -10 and 10 ORDER BY lb_sensor.measure_time DESC";

	$sql="SELECT hosts.hostname, daemon_lb, daemon_ll, daemon_NTPD FROM lb_sensor join hosts ON lb_sensor.idhost=hosts.idhost WHERE lb_sensor.idhost=(select idhost from hosts where hostname in (SELECT lbhosts.hostname FROM lb_hist join hosts, lbhosts WHERE lb_hist.idlb=lbhosts.idlbhost and lb_hist.idwms=hosts.idhost and hosts.hostname = '".$wms."' and lb_hist.measure_time = (select max(end_date) from wms_rates join hosts on wms_rates.idhost=hosts.idhost where hosts.hostname = '".$wms."'))) and  timestampdiff(SECOND, lb_sensor.measure_time, (select max(end_date) from wms_rates join hosts on wms_rates.idhost=hosts.idhost where hosts.hostname = '".$wms."')) between -300 and 300 ORDER BY lb_sensor.measure_time DESC";

#	$sql="SELECT hosts.hostname, daemon_lb, daemon_ll, daemon_NTPD FROM lb_sensor join hosts ON lb_sensor.idhost=hosts.idhost WHERE lb_sensor.idhost=(select idhost from hosts where hostname in (SELECT hosts.hostname FROM lb_hist join hosts WHERE lb_hist.idlb=hosts.idhost and lb_hist.idwms=(select idhost from hosts where hostname = '".$wms."') and lb_hist.measure_time = (select max(end_date) from wms_rates join hosts on wms_rates.idhost=hosts.idhost where hosts.hostname = '".$wms."'))) and  timestampdiff(SECOND, lb_sensor.measure_time, (select max(end_date) from wms_rates join hosts on wms_rates.idhost=hosts.idhost where hosts.hostname = '".$wms."')) between -300 and 300 ORDER BY lb_sensor.measure_time DESC";

	$res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}



function getChartRatesData($wms, $interval, $endDate) {
        global $config, $db;
        $result = array();

        $date_int = getDateInterval($interval, $endDate);

        $sql="SELECT end_date as date, WMP_in as 'Jobs -> WMProxy', WM_in as 'Jobs -> WM', WM_in_res as 'Jobs Resub -> WM', JC_in as 'Jobs -> JC', JC_out as 'Jobs -> Condor', start_date, WMP_in_col, (WM_in+WM_in_res) as 'Total Jobs -> WM', timestampdiff(second, start_date, end_date) as 'delta_t' FROM wms_rates join hosts IGNORE INDEX (hostname) WHERE wms_rates.idhost=hosts.idhost and hostname = '".$wms."' and end_date > '".$date_int["start"]."' and end_date <= '".$date_int["end"]."' ORDER BY date";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getChartWMSRatesDailyData($wms, $daily, $endDate) {
        global $config, $db;
        $result = array();

        switch ($daily) {
        case 'week':
                $num_days = 7;
                break;
        case '2weeks':
                $num_days = 14;
                break;
        case 'month':
                $num_days = 30;
                break;
        }

        $date_end = $endDate." 23:59:59";
        $date_end_epoch = mktime(intval(substr($date_end, 11, 2)), intval(substr($date_end, 14, 2)), intval(substr($date_end, 17, 2)), intval(substr($date_end, 5, 2)), intval(substr($date_end, 8, 2)), intval(substr($date_end, 0, 4)));

        $date_start_epoch = $date_end_epoch-($num_days-1)*86400;
        $date_start = date("Y-m-d", $date_start_epoch);

        $sql="SELECT day as date, WMP_in as 'Jobs -> WMProxy', WM_in as 'Jobs -> WM', WM_in_res as 'Jobs Resub -> WM', JC_in as 'Jobs -> JC', JC_out as 'Jobs -> Condor', JOB_DONE, JOB_ABORTED, WMP_in_col, (WM_in+WM_in_res) as 'Total Jobs -> WM' FROM wms_rates_daily join hosts on wms_rates_daily.idhost=hosts.idhost where hostname ='".$wms."' and day between '".$date_start."' and '".$date_end."' GROUP BY day ORDER BY day,idwmsratesdaily DESC";
        $res=mysql_query($sql);
        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getErrStatsWMSData($wms, $startDate, $endDate) {
        global $config, $db;
        $result = array();
//        $startDate = $startDate." 00:00:00";
//        $endDate = $endDate." 23:59:59";

//        $sql="SELECT errstr, sum(occ) as `occurrence` FROM globuserr_stats WHERE wms = '".$wms."' and date > '".$startDate."' and date <= '".$endDate."' GROUP BY errstr ORDER BY occurrence desc";

	$sql="SELECT error_string, sum(occurrences) as `occurrence` FROM err_stats join hosts on hosts.idhost=err_stats.idhost WHERE hostname = '".$wms."' and day >= '".$startDate."' and day <= '".$endDate."' GROUP BY error_string ORDER BY occurrence desc";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getErrStatsVOData($vo, $startDate, $endDate) {
        global $config, $db;
        $result = array();
        $startDate = $startDate." 00:00:00";
        $endDate = $endDate." 23:59:59";

        $sql="SELECT errstr, sum(occ) as `occurrence` FROM globuserr_stats WHERE vo = '".$vo."' and date > '".$startDate."' and date <= '".$endDate."' GROUP BY errstr ORDER BY occurrence desc";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_ASSOC)) {
                array_push($result, $row);
        }

        return $result;
}

function getDNEnabledList() {
        global $config, $db;
        $result = array();

        $sql="SELECT DISTINCT dn FROM admin_web_users where privileges in ('admin','read')";

        $res=mysql_query($sql);

        while ($row = mysql_fetch_array($res, MYSQL_NUM)) {
                array_push($result, $row);
        }

        return $result;
}
?>
