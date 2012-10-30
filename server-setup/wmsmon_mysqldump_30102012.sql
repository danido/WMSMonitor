-- MySQL dump 10.13  Distrib 5.1.52, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: wmsmon
-- ------------------------------------------------------
-- Server version	5.1.52

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_host_labels`
--

DROP TABLE IF EXISTS `admin_host_labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_host_labels` (
  `idhostlabel` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `service` varchar(50) DEFAULT NULL,
  `vo` varchar(150) DEFAULT NULL,
  `vo_group` varchar(150) DEFAULT NULL,
  `service_usage` varchar(150) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `host_owner` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`idhostlabel`),
  UNIQUE KEY `idhost` (`idhost`,`service`),
  CONSTRAINT `admin_host_labels_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `admin_loadbalancing`
--

DROP TABLE IF EXISTS `admin_loadbalancing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_loadbalancing` (
  `idalias` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `enable_flag` tinyint(1) NOT NULL,
  `numout` int(11) NOT NULL,
  `subtest_enable` tinyint(1) NOT NULL,
  `alias_name` varchar(150) NOT NULL,
  PRIMARY KEY (`idalias`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `admin_web_users`
--

DROP TABLE IF EXISTS `admin_web_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_web_users` (
  `idwebuser` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dn` varchar(150) NOT NULL,
  `privileges` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`idwebuser`)
) ENGINE=InnoDB AUTO_INCREMENT=1355 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `admin_wms_alias_list`
--

DROP TABLE IF EXISTS `admin_wms_alias_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_wms_alias_list` (
  `idlist` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idalias` int(10) unsigned NOT NULL,
  `idwms` int(10) unsigned NOT NULL,
  `spare_label` tinyint(1) DEFAULT NULL,
  `test_url` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`idlist`),
  KEY `idalias` (`idalias`),
  KEY `idwms` (`idwms`),
  CONSTRAINT `admin_wms_alias_list_ibfk_1` FOREIGN KEY (`idalias`) REFERENCES `admin_loadbalancing` (`idalias`) ON DELETE CASCADE,
  CONSTRAINT `admin_wms_alias_list_ibfk_2` FOREIGN KEY (`idwms`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ce_mm`
--

DROP TABLE IF EXISTS `ce_mm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ce_mm` (
  `idcemm` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `day` date NOT NULL DEFAULT '0000-00-00',
  `num_ce` int(10) unsigned NOT NULL,
  `occurrences` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`idcemm`),
  KEY `idhost` (`idhost`),
  CONSTRAINT `ce_mm_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5385459 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ce_stats`
--

DROP TABLE IF EXISTS `ce_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ce_stats` (
  `idcestats` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idwms` int(10) unsigned NOT NULL,
  `measure_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `idcehost` int(10) unsigned NOT NULL,
  `idusermap` int(10) unsigned DEFAULT NULL,
  `occurrences` int(10) unsigned DEFAULT NULL,
  `last_mod_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idcestats`),
  KEY `idwms` (`idwms`),
  KEY `idcehost` (`idcehost`),
  KEY `idusermap` (`idusermap`),
  CONSTRAINT `ce_stats_ibfk_1` FOREIGN KEY (`idwms`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE,
  CONSTRAINT `ce_stats_ibfk_3` FOREIGN KEY (`idcehost`) REFERENCES `cehosts` (`idcehost`) ON DELETE CASCADE,
  CONSTRAINT `ce_stats_ibfk_4` FOREIGN KEY (`idusermap`) REFERENCES `user_map` (`idusermap`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3563839 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ce_stats_daily`
--

DROP TABLE IF EXISTS `ce_stats_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ce_stats_daily` (
  `idcestats` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idwms` int(10) unsigned NOT NULL,
  `day` date NOT NULL DEFAULT '0000-00-00',
  `idcehost` int(10) unsigned NOT NULL,
  `idusermap` int(10) unsigned DEFAULT NULL,
  `occurrences` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`idcestats`),
  UNIQUE KEY `day` (`day`,`idcehost`,`idwms`),
  KEY `idwms` (`idwms`),
  KEY `idcehost` (`idcehost`),
  KEY `idusermap` (`idusermap`),
  CONSTRAINT `ce_stats_daily_ibfk_1` FOREIGN KEY (`idwms`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE,
  CONSTRAINT `ce_stats_daily_ibfk_3` FOREIGN KEY (`idcehost`) REFERENCES `cehosts` (`idcehost`) ON DELETE CASCADE,
  CONSTRAINT `ce_stats_daily_ibfk_4` FOREIGN KEY (`idusermap`) REFERENCES `user_map` (`idusermap`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6068039 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cehosts`
--

DROP TABLE IF EXISTS `cehosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cehosts` (
  `idcehost` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostname` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`idcehost`)
) ENGINE=InnoDB AUTO_INCREMENT=6704 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `err_stats`
--

DROP TABLE IF EXISTS `err_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `err_stats` (
  `iderr` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `day` date NOT NULL DEFAULT '0000-00-00',
  `error_string` varchar(150) DEFAULT NULL,
  `occurrences` int(10) unsigned DEFAULT NULL,
  `err_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`iderr`),
  KEY `idhost` (`idhost`),
  CONSTRAINT `err_stats_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24382 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `host_usagetest`
--

DROP TABLE IF EXISTS `host_usagetest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_usagetest` (
  `idhostusagetest` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `t_lastcheck` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `test_vo` varchar(150) NOT NULL,
  `test_result` int(10) unsigned NOT NULL,
  PRIMARY KEY (`idhostusagetest`),
  KEY `idhost` (`idhost`),
  CONSTRAINT `host_usagetest_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hosts` (
  `idhost` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostname` varchar(150) NOT NULL,
  PRIMARY KEY (`idhost`),
  UNIQUE KEY `hostname` (`hostname`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lb_hist`
--

DROP TABLE IF EXISTS `lb_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_hist` (
  `idlbhist` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idwms` int(10) unsigned NOT NULL,
  `measure_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `idlb` int(10) unsigned NOT NULL,
  `occurrences` int(10) unsigned DEFAULT NULL,
  `last_mod_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idlbhist`),
  KEY `idwms` (`idwms`),
  KEY `idlb` (`idlb`),
  CONSTRAINT `lb_hist_ibfk_1` FOREIGN KEY (`idwms`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE,
  CONSTRAINT `lb_hist_ibfk_2` FOREIGN KEY (`idlb`) REFERENCES `lbhosts` (`idlbhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=328068 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lb_hist_daily`
--

DROP TABLE IF EXISTS `lb_hist_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_hist_daily` (
  `idlbhistdaily` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idwms` int(10) unsigned NOT NULL,
  `day` date NOT NULL DEFAULT '0000-00-00',
  `idlb` int(10) unsigned NOT NULL,
  `occurrences` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`idlbhistdaily`),
  UNIQUE KEY `idwms` (`idwms`,`day`,`idlb`),
  KEY `idlb` (`idlb`),
  CONSTRAINT `lb_hist_daily_ibfk_1` FOREIGN KEY (`idlb`) REFERENCES `lbhosts` (`idlbhost`) ON DELETE CASCADE,
  CONSTRAINT `lb_hist_daily_ibfk_2` FOREIGN KEY (`idwms`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=290727 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lb_sensor`
--

DROP TABLE IF EXISTS `lb_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_sensor` (
  `idlbsensor` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `measure_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `cpu_load` decimal(15,4) unsigned DEFAULT NULL,
  `disk_lb` int(10) unsigned DEFAULT NULL,
  `disk_varlibmysql` int(10) unsigned DEFAULT NULL,
  `lb_con` smallint(5) unsigned DEFAULT NULL,
  `daemon_lb` tinyint(1) unsigned DEFAULT NULL,
  `daemon_ll` tinyint(1) unsigned DEFAULT NULL,
  `daemon_NTPD` smallint(5) unsigned DEFAULT NULL,
  `last_mod_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idlbsensor`),
  KEY `idhost` (`idhost`),
  KEY `measure_time` (`measure_time`),
  CONSTRAINT `lb_sensor_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5447202 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lbhosts`
--

DROP TABLE IF EXISTS `lbhosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lbhosts` (
  `idlbhost` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostname` varchar(150) NOT NULL,
  PRIMARY KEY (`idlbhost`),
  UNIQUE KEY `hostname` (`hostname`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_map`
--

DROP TABLE IF EXISTS `user_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_map` (
  `idusermap` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `iduser` int(10) unsigned DEFAULT NULL,
  `vo` varchar(150) DEFAULT NULL,
  `voms_group` varchar(150) DEFAULT NULL,
  `role` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`idusermap`),
  UNIQUE KEY `iduser` (`iduser`,`vo`,`voms_group`,`role`),
  CONSTRAINT `user_map_ibfk_1` FOREIGN KEY (`iduser`) REFERENCES `users` (`iduser`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18382 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_rates`
--

DROP TABLE IF EXISTS `user_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_rates` (
  `iduserrates` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `idusermap` int(10) unsigned NOT NULL,
  `start_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `WMP_in` int(10) unsigned DEFAULT NULL,
  `WMP_in_col` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_min_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_max_nodes` int(10) unsigned DEFAULT NULL,
  `WM_in` int(10) unsigned DEFAULT NULL,
  `WM_in_res` int(10) unsigned DEFAULT NULL,
  `JC_in` int(10) unsigned DEFAULT NULL,
  `JC_out` int(10) unsigned DEFAULT NULL,
  `JOB_DONE` int(10) unsigned DEFAULT NULL,
  `JOB_ABORTED` int(10) unsigned DEFAULT NULL,
  `last_mod_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`iduserrates`),
  KEY `idhost` (`idhost`),
  KEY `idusermap` (`idusermap`),
  CONSTRAINT `user_rates_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE,
  CONSTRAINT `user_rates_ibfk_2` FOREIGN KEY (`idusermap`) REFERENCES `user_map` (`idusermap`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2705318 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_rates_daily`
--

DROP TABLE IF EXISTS `user_rates_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_rates_daily` (
  `iduserratesdaily` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `idusermap` int(10) unsigned NOT NULL,
  `day` date NOT NULL DEFAULT '0000-00-00',
  `WMP_in` int(10) unsigned DEFAULT NULL,
  `WMP_in_col` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_min_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_max_nodes` int(10) unsigned DEFAULT NULL,
  `WM_in` int(10) unsigned DEFAULT NULL,
  `WM_in_res` int(10) unsigned DEFAULT NULL,
  `JC_in` int(10) unsigned DEFAULT NULL,
  `JC_out` int(10) unsigned DEFAULT NULL,
  `JOB_DONE` int(10) unsigned DEFAULT NULL,
  `JOB_ABORTED` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`iduserratesdaily`),
  UNIQUE KEY `iduser` (`idusermap`,`day`,`idhost`),
  KEY `idhost` (`idhost`),
  KEY `idusermap` (`idusermap`),
  CONSTRAINT `user_rates_daily_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE,
  CONSTRAINT `user_rates_daily_ibfk_2` FOREIGN KEY (`idusermap`) REFERENCES `user_map` (`idusermap`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3099389 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `iduser` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dn` varchar(150) NOT NULL,
  PRIMARY KEY (`iduser`),
  UNIQUE KEY `dn` (`dn`)
) ENGINE=InnoDB AUTO_INCREMENT=10149 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wms_rates`
--

DROP TABLE IF EXISTS `wms_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wms_rates` (
  `idwmsrates` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `start_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `WMP_in` int(10) unsigned DEFAULT NULL,
  `WMP_in_col` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_min_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_max_nodes` int(10) unsigned DEFAULT NULL,
  `WM_in` int(10) unsigned DEFAULT NULL,
  `WM_in_res` int(10) unsigned DEFAULT NULL,
  `JC_in` int(10) unsigned DEFAULT NULL,
  `JC_out` int(10) unsigned DEFAULT NULL,
  `JOB_DONE` int(10) unsigned DEFAULT NULL,
  `JOB_ABORTED` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`idwmsrates`),
  KEY `idhost` (`idhost`),
  CONSTRAINT `wms_rates_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3213067 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wms_rates_daily`
--

DROP TABLE IF EXISTS `wms_rates_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wms_rates_daily` (
  `idwmsratesdaily` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `day` date NOT NULL DEFAULT '0000-00-00',
  `WMP_in` int(10) unsigned DEFAULT NULL,
  `WMP_in_col` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_min_nodes` int(10) unsigned DEFAULT NULL,
  `WMP_in_col_max_nodes` int(10) unsigned DEFAULT NULL,
  `WM_in` int(10) unsigned DEFAULT NULL,
  `WM_in_res` int(10) unsigned DEFAULT NULL,
  `JC_in` int(10) unsigned DEFAULT NULL,
  `JC_out` int(10) unsigned DEFAULT NULL,
  `JOB_DONE` int(10) unsigned DEFAULT NULL,
  `JOB_ABORTED` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`idwmsratesdaily`),
  UNIQUE KEY `iduser` (`day`,`idhost`),
  KEY `idhost` (`idhost`),
  CONSTRAINT `wms_rates_daily_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=755242 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wms_sensor`
--

DROP TABLE IF EXISTS `wms_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wms_sensor` (
  `idwmssensor` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `measure_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `condor_running` int(10) unsigned DEFAULT NULL,
  `condor_current` int(10) unsigned DEFAULT NULL,
  `condor_idle` int(10) unsigned DEFAULT NULL,
  `cpu_load` decimal(15,2) unsigned DEFAULT NULL,
  `wm_queue` int(10) unsigned DEFAULT NULL,
  `jc_queue` int(10) unsigned DEFAULT NULL,
  `lb_event` smallint(5) unsigned DEFAULT NULL,
  `ism_size` int(20) unsigned DEFAULT NULL,
  `ism_entries` int(20) unsigned DEFAULT NULL,
  `fd_wm` smallint(5) unsigned DEFAULT NULL,
  `fd_lm` smallint(5) unsigned DEFAULT NULL,
  `fd_jc` smallint(5) unsigned DEFAULT NULL,
  `fd_ll` smallint(5) unsigned DEFAULT NULL,
  `disk_sandbox` int(10) unsigned DEFAULT NULL,
  `disk_tmp` int(10) unsigned DEFAULT NULL,
  `disk_varlog` int(10) unsigned DEFAULT NULL,
  `disk_varlibmysql` int(10) unsigned DEFAULT NULL,
  `gftp_con` smallint(5) unsigned DEFAULT NULL,
  `daemon_wm` tinyint(1) unsigned DEFAULT NULL,
  `daemon_wmp` tinyint(1) unsigned DEFAULT NULL,
  `daemon_jc` tinyint(1) unsigned DEFAULT NULL,
  `daemon_px` tinyint(1) unsigned DEFAULT NULL,
  `daemon_lm` tinyint(1) unsigned DEFAULT NULL,
  `daemon_ll` tinyint(1) unsigned DEFAULT NULL,
  `daemon_lbpx` tinyint(1) unsigned DEFAULT NULL,
  `daemon_ftpd` tinyint(1) unsigned DEFAULT NULL,
  `daemon_ntpd` smallint(5) unsigned DEFAULT NULL,
  `loadb_fmetric` decimal(15,4) DEFAULT NULL,
  `loadb_memusage` decimal(15,4) DEFAULT NULL,
  `loadb_fdrain` int(10) DEFAULT NULL,
  `loadb_fload` decimal(15,4) DEFAULT NULL,
  `loadb_ftraversaltime` decimal(15,4) DEFAULT NULL,
  `ice_running` int(10) DEFAULT NULL,
  `ice_idle` int(10) DEFAULT NULL,
  `ice_pending` int(10) DEFAULT NULL,
  `daemon_bdii` smallint(5) unsigned DEFAULT NULL,
  `daemon_ice` smallint(5) unsigned DEFAULT NULL,
  `ice_queue` int(10) unsigned DEFAULT NULL,
  `ice_held` int(10) unsigned DEFAULT NULL,
  `last_mod_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idwmssensor`),
  KEY `idhost` (`idhost`),
  KEY `measure_time` (`measure_time`)
) ENGINE=MyISAM AUTO_INCREMENT=3559355 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wms_sensor_test`
--

DROP TABLE IF EXISTS `wms_sensor_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wms_sensor_test` (
  `idwmssensor` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idhost` int(10) unsigned NOT NULL,
  `measure_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `condor_running` int(10) unsigned DEFAULT NULL,
  `condor_current` int(10) unsigned DEFAULT NULL,
  `condor_idle` int(10) unsigned DEFAULT NULL,
  `cpu_load` decimal(15,4) unsigned DEFAULT NULL,
  `wm_queue` int(10) unsigned DEFAULT NULL,
  `jc_queue` int(10) unsigned DEFAULT NULL,
  `lb_event` smallint(5) unsigned DEFAULT NULL,
  `ism_size` int(20) unsigned DEFAULT NULL,
  `ism_entries` int(20) unsigned DEFAULT NULL,
  `fd_wm` smallint(5) unsigned DEFAULT NULL,
  `fd_lm` smallint(5) unsigned DEFAULT NULL,
  `fd_jc` smallint(5) unsigned DEFAULT NULL,
  `fd_ll` smallint(5) unsigned DEFAULT NULL,
  `disk_sandbox` int(10) unsigned DEFAULT NULL,
  `disk_tmp` int(10) unsigned DEFAULT NULL,
  `disk_varlog` int(10) unsigned DEFAULT NULL,
  `disk_varlibmysql` int(10) unsigned DEFAULT NULL,
  `gftp_con` smallint(5) unsigned DEFAULT NULL,
  `daemon_wm` tinyint(1) unsigned DEFAULT NULL,
  `daemon_wmp` tinyint(1) unsigned DEFAULT NULL,
  `daemon_jc` tinyint(1) unsigned DEFAULT NULL,
  `daemon_px` tinyint(1) unsigned DEFAULT NULL,
  `daemon_lm` tinyint(1) unsigned DEFAULT NULL,
  `daemon_ll` tinyint(1) unsigned DEFAULT NULL,
  `daemon_lbpx` tinyint(1) unsigned DEFAULT NULL,
  `daemon_ftpd` tinyint(1) unsigned DEFAULT NULL,
  `daemon_ntpd` smallint(5) unsigned DEFAULT NULL,
  `loadb_fmetric` decimal(15,4) DEFAULT NULL,
  `loadb_memusage` int(10) DEFAULT NULL,
  `loadb_fdrain` int(10) DEFAULT NULL,
  `loadb_fload` decimal(15,7) DEFAULT NULL,
  `loadb_ftraversaltime` decimal(15,4) DEFAULT NULL,
  `ice_running` int(10) DEFAULT NULL,
  `ice_idle` int(10) DEFAULT NULL,
  `ice_pending` int(10) DEFAULT NULL,
  `daemon_bdii` smallint(5) unsigned DEFAULT NULL,
  `daemon_ice` smallint(5) unsigned DEFAULT NULL,
  `ice_queue` int(10) unsigned DEFAULT NULL,
  `ice_held` int(10) unsigned DEFAULT NULL,
  `last_mod_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`idwmssensor`),
  KEY `idhost` (`idhost`),
  KEY `measure_time` (`measure_time`),
  CONSTRAINT `wms_sensor_test_ibfk_1` FOREIGN KEY (`idhost`) REFERENCES `hosts` (`idhost`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'wmsmon'
--
/*!50003 DROP PROCEDURE IF EXISTS `add_wmshost_to_ALIAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `add_wmshost_to_ALIAS`(IN hostnamewms varchar(150), IN alias_nameIN varchar(250), IN spare_label_flag tinyint, IN test_urlIN varchar(300))
mainblock: begin

if exists (select idhost from hosts where hostname=hostnamewms) then
    set @idhosttmp:= (select idhost from hosts where hostname=hostnamewms);
else 
    select 'WMS hostname not found in database'; 
    leave mainblock;
end if;

if exists (select idalias from admin_loadbalancing where alias_name=alias_nameIN) then
    set @idaliastmp:= (select idalias from admin_loadbalancing where alias_name=alias_nameIN);
else 
    select 'ALIAS not defined in database'; 
    leave mainblock;
end if;

if exists (select idwms from admin_wms_alias_list where idwms=@idhosttmp) then
    select 'WMS already associated to  ALIAS'; 
    leave mainblock;
else 
    INSERT INTO
    admin_wms_alias_list(idalias, idwms, spare_label, test_url)
    VALUES (@idaliastmp, @idhosttmp, spare_label_flag, test_urlIN);
end if;

end mainblock */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertCEHost` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertCEHost`(IN host_name varchar(150))
begin if not exists (select idcehost from cehosts where hostname = host_name) then insert into cehosts values ('',host_name); end if; end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertCEStatsDailyWithCEHostWithDummyUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertCEStatsDailyWithCEHostWithDummyUser`(IN day date, IN hostnamece varchar(250), IN hostnamewms varchar(250), IN vo varchar(250))
begin declare idcehosttmp, idwmshosttmp, idusertmp INT; set idcehosttmp= (select idcehost from cehosts where hostname=hostnamece), idwmshosttmp= (select idhost from hosts where hostname=hostnamewms), idusertmp= (select user_map.idusermap from user_map join users on user_map.iduser=users.iduser where users.dn like 'dummy_%' and user_map.vo=vo); INSERT INTO ce_stats_daily (idcestats,idwms,day,idcehost,idusermap,occurrences) VALUES('', idwmshosttmp, day, idcehosttmp, idusertmp, (select SUM(occurrences) from ce_stats where idcehost=idcehosttmp and idwms=idwmshosttmp and idusermap=idusertmp and measure_time like CONCAT(day,'%'))) ON DUPLICATE KEY UPDATE occurrences=(select SUM(occurrences) from ce_stats where idcehost=idcehosttmp and idwms=idwmshosttmp and idusermap=idusertmp and measure_time like CONCAT(day,'%')); end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertCEStatsWithCEHostWithDummyUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertCEStatsWithCEHostWithDummyUser`(IN measure_time datetime, IN hostnamece varchar(250), IN hostnamewms varchar(250), IN occ int(10), IN vo varchar(250))
begin call insertCEHost(hostnamece);
insert into ce_stats (idwms,measure_time,idcehost,idusermap,occurrences) values ((select idhost from hosts where hostname=hostnamewms), measure_time, (select idcehost from cehosts where hostname=hostnamece), (select user_map.idusermap from user_map join users on user_map.iduser=users.iduser where users.dn like 'dummy_%' and user_map.vo=vo), occ);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertDummyUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertDummyUser`(IN vo_name varchar(150))
begin
if not exists (select iduser from users where dn = CONCAT('dummy_',vo_name))
then
insert into users values ('', CONCAT('dummy_',vo_name));
insert into user_map values ('', (select iduser from users where dn =CONCAT('dummy_',vo_name)), vo_name, NULL, NULL);
end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertHost` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertHost`(IN host_name varchar(150))
begin
if not exists (select idhost from hosts where hostname = host_name)
then
insert into hosts values ('',host_name);
select 'SUCCESS: host inserted into TABLE hosts' as Message1;
else
select 'WARNING: host already registered into TABLE hosts' as Message1;
end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertHostLabels` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertHostLabels`(IN host_name varchar(150), IN service_name varchar(150), IN vo_name varchar(150), IN vo_group_name varchar(150), service_usage_name varchar(150), active_flag int, host_owner_name varchar(150))
begin
call insertHost(host_name);
if exists (select idhost from hosts where hostname = host_name)
then
insert into admin_host_labels values ('', (select idhost from hosts where hostname=host_name), service_name, vo_name, vo_group_name, service_usage_name, active_flag, host_owner_name);
select 'SUCCESS: labels inserted into TABLE admin_host_labels' as Message2;
call insertDummyUser(vo_name);
end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertLBHost` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertLBHost`(IN host_name varchar(150))
begin
if not exists (select idlbhost from lbhosts where hostname = host_name)
then
insert into lbhosts values ('',host_name);
end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertLB_hist` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertLB_hist`(IN datemeas datetime, IN hostnamewms varchar(250), IN hostnamelb varchar(150), IN occurrences int(10) unsigned)
begin
call insertLBHost(hostnamelb);
insert into lb_hist (idwms, measure_time, idlb, occurrences) values ((select idhost from hosts where hosts.hostname=hostnamewms), datemeas, (select idlbhost from lbhosts where lbhosts.hostname=hostnamelb), occurrences);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertLB_histDaily` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertLB_histDaily`(IN dateday date, IN hostnamelb varchar(250), IN hostnamewms varchar(150))
begin
declare idlbhosttmp, idwmshosttmp INT; set idlbhosttmp=(select idlbhost from lbhosts where hostname=hostnamelb), idwmshosttmp=(select idhost from hosts where hostname=hostnamewms);
INSERT INTO lb_hist_daily(idlbhistdaily, idwms, day, idlb, occurrences) VALUES ('', idwmshosttmp, dateday, idlbhosttmp, (select SUM(occurrences) from lb_hist where measure_time like CONCAT(dateday,'%') and idlb=idlbhosttmp and idwms=idwmshosttmp))
ON DUPLICATE KEY UPDATE occurrences=(select SUM(occurrences) from lb_hist where measure_time like CONCAT(dateday,'%') and idlb=idlbhosttmp and idwms=idwmshosttmp);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertUser`(IN cert varchar(150))
begin if not exists (select iduser from users where dn = cert) then insert into users values ('',cert); end if; end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertUserRateDailyWithMap` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertUserRateDailyWithMap`(IN day date, IN dn varchar(150), IN vo_name varchar(150), IN group_name varchar(150), IN role_name varchar(150), IN host_name varchar(150))
begin declare idusermaptmp, idhosttmp, wmp_in_tmp, wmp_in_col_tmp, wmp_in_col_nodes_tmp, wmp_in_col_min_nodes_tmp, wmp_in_col_max_nodes_tmp, wm_in_tmp, wm_in_res_tmp, jc_in_tmp, jc_out_tmp, job_done_tmp, job_aborted_tmp INT;
set idusermaptmp=(select idusermap from user_map join users on user_map.iduser=users.iduser where (CASE when dn is NULL then users.dn is NULL ELSE users.dn=dn END) and (CASE when vo_name is NULL then user_map.vo is NULL ELSE user_map.vo=vo_name END) and (CASE when group_name is NULL then user_map.voms_group is NULL ELSE user_map.voms_group=group_name END) and (CASE when role_name is NULL then user_map.role is NULL else user_map.role=role_name END));
set idhosttmp=(select idhost from hosts where hostname=host_name);
set wmp_in_tmp=(select sum(wmp_in) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), wmp_in_col_tmp=(select sum(wmp_in_col) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), wmp_in_col_nodes_tmp=(select sum(wmp_in_col_nodes) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), wmp_in_col_min_nodes_tmp=(select min(wmp_in_col_min_nodes) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), wmp_in_col_max_nodes_tmp=(select max(wmp_in_col_max_nodes) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), wm_in_tmp=(select sum(wm_in) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), wm_in_res_tmp=(select sum(wm_in_res) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), jc_in_tmp=(select sum(jc_in) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), jc_out_tmp=(select sum(jc_out) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), job_done_tmp=(select sum(job_done) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%')), job_aborted_tmp=(select sum(job_aborted) from user_rates where idusermap=idusermaptmp and idhost=idhosttmp and end_date like CONCAT(day,'%'));
INSERT INTO user_rates_daily (idhost,idusermap,day,wmp_in, wmp_in_col, wmp_in_col_nodes, wmp_in_col_min_nodes, wmp_in_col_max_nodes, wm_in, wm_in_res, jc_in, jc_out, job_done, job_aborted) VALUES (idhosttmp, idusermaptmp, day, wmp_in_tmp, wmp_in_col_tmp, wmp_in_col_nodes_tmp, wmp_in_col_min_nodes_tmp, wmp_in_col_max_nodes_tmp, wm_in_tmp, wm_in_res_tmp, jc_in_tmp, jc_out_tmp, job_done_tmp, job_aborted_tmp) ON DUPLICATE KEY UPDATE wmp_in=wmp_in_tmp, wmp_in_col=wmp_in_col_tmp, wmp_in_col_nodes=wmp_in_col_nodes_tmp, wmp_in_col_min_nodes=wmp_in_col_min_nodes_tmp, wmp_in_col_max_nodes=wmp_in_col_max_nodes_tmp, wm_in=wm_in_tmp, wm_in_res=wm_in_res_tmp, jc_in=jc_in_tmp, jc_out=jc_out_tmp, job_done=job_done_tmp, job_aborted=job_aborted;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertUserRateWithMap` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertUserRateWithMap`(IN dn varchar(150), IN vo_name varchar(150), IN group_name varchar(150) , IN role_name varchar(150) , IN startdate datetime, IN enddate datetime, IN hostname varchar(150), IN wmp_in int(10) unsigned, IN wmp_in_col int(10) unsigned, IN wmp_in_col_nodes int(10) unsigned, IN wmp_in_col_min_nodes int(10) unsigned, IN wmp_in_col_max_nodes int(10) unsigned, IN wm_in int(10) unsigned, IN wm_in_res int(10) unsigned,  IN jc_in int(10) unsigned, IN jc_out int(10) unsigned,  IN job_done int(10) unsigned, IN job_aborted int(10) unsigned)
begin call insertUserWithMap(dn,group_name,role_name,vo_name); insert into user_rates (idhost, idusermap, start_date, end_date, WMP_in, WMP_in_col, WMP_in_col_nodes, WMP_in_col_min_nodes, WMP_in_col_max_nodes, WM_in, WM_in_res, JC_in, JC_out, JOB_DONE, JOB_ABORTED) values ((select idhost from hosts where hosts.hostname=hostname), (select idusermap from user_map join users on user_map.iduser=users.iduser where (CASE when dn is NULL then users.dn is NULL ELSE users.dn=dn END) and (CASE when vo_name is NULL then user_map.vo is NULL ELSE user_map.vo=vo_name END) and (CASE when group_name is NULL then user_map.voms_group is NULL ELSE user_map.voms_group=group_name END) and (CASE when role_name is NULL then user_map.role is NULL else user_map.role=role_name END)),  startdate, enddate, WMP_in, WMP_in_col, WMP_in_col_nodes, wmp_in_col_min_nodes, wmp_in_col_max_nodes, WM_in, WM_in_res, JC_in, JC_out, JOB_DONE, JOB_ABORTED); end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertUserWithMap` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insertUserWithMap`(IN dn varchar(150), IN group_name varchar(150) , IN role_name varchar(150) , IN vo_name varchar(150) )
begin call insertUser(dn); if not exists (select idusermap from user_map join users on user_map.iduser=users.iduser where (CASE when dn is NULL then users.dn is NULL ELSE users.dn=dn END) and (CASE when vo_name is NULL then user_map.vo is NULL ELSE user_map.vo=vo_name END) and (CASE when group_name is NULL then user_map.voms_group is NULL ELSE user_map.voms_group=group_name END) and (CASE when role_name is NULL then user_map.role is NULL else user_map.role=role_name END) ) then insert into user_map values ('',(select iduser from users where users.dn=dn),vo_name,group_name,role_name); end if; end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_loadbalancing_ALIAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `insert_loadbalancing_ALIAS`(IN enable_flagIN tinyint, IN numoutIN int, IN subtest_enableIN tinyint, IN alias_nameIN varchar(250))
mainblock: begin
if exists (select idalias from admin_loadbalancing where alias_name=alias_nameIN) then
    select 'ALIAS already in database'; 
    leave mainblock;
else
   INSERT INTO
   admin_loadbalancing(idalias, enable_flag, numout, subtest_enable, alias_name)
   VALUES ('', enable_flagIN, numoutIN, subtest_enableIN, alias_nameIN);
end if; 
end mainblock */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `remove_loadbalancing_ALIAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `remove_loadbalancing_ALIAS`(IN alias_nameIN varchar(250))
mainblock: begin
if exists (select idalias from admin_loadbalancing where alias_name=alias_nameIN) then
    DELETE from admin_loadbalancing where alias_name=alias_nameIN;
else 
    select 'ALIAS not defined in database'; 
    leave mainblock;
end if;
end mainblock */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `remove_wmshost_from_ALIAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `remove_wmshost_from_ALIAS`(IN hostnamewms varchar(150), IN alias_nameIN varchar(250))
mainblock: begin

if exists (select idhost from hosts where hostname=hostnamewms) then
    set @idhosttmp:= (select idhost from hosts where hostname=hostnamewms);
else 
    select 'WMS hostname not found in database'; 
    leave mainblock;
end if;

if exists (select idalias from admin_loadbalancing where alias_name=alias_nameIN) then
    set @idaliastmp:= (select idalias from admin_loadbalancing where alias_name=alias_nameIN);
else 
    select 'ALIAS not defined in database'; 
    leave mainblock;
end if;
if exists (select idwms from admin_wms_alias_list where idwms=@idhosttmp) then
    DELETE from admin_wms_alias_list where idwms=@idhosttmp;
else 
    select 'WMS NOT associated to considered ALIAS'; 
    leave mainblock;
end if;

end mainblock */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `updateHostLabels` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`wmsmon`@`localhost`*/ /*!50003 PROCEDURE `updateHostLabels`(IN host_name varchar(150), IN service_name varchar(150), IN vo_name varchar(150), IN vo_group_name varchar(150), service_usage_name varchar(150), active_flag int, host_owner_name varchar(150))
begin
if exists (select idhostlabel from admin_host_labels where idhost=(select idhost from hosts where hostname=host_name) and service=service_name)
then
update admin_host_labels set vo=vo_name, vo_group=vo_group_name, service_usage=service_usage_name, active=active_flag, host_owner=host_owner_name where idhost=(select idhost from hosts where hostname = host_name) and service=service_name;
select 'SUCCESS: labels successfully updated into TABLE admin_host_labels for the desired host with the specified service name' as Message1;
call insertDummyUser(vo_name);
else
select 'ERROR: host not present into TABLE admin_host_labels with the specified service name. Please use the procedure insertHostLabels' as Message1;
end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-10-30 15:27:27
