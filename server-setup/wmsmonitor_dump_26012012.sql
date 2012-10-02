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
-- Current Database: `wmsmon`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `wmsmon` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `wmsmon`;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-01-26 16:20:34
