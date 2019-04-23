-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.24-0ubuntu0.16.04.1 - (Ubuntu)
-- Server OS:                    Linux
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for autohome-dev
DROP DATABASE IF EXISTS `autohome-dev`;
CREATE DATABASE IF NOT EXISTS `autohome-dev` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `autohome-dev`;

-- Dumping structure for table autohome-dev.device
DROP TABLE IF EXISTS `device`;
CREATE TABLE IF NOT EXISTS `device` (
  `device_id` int(10) unsigned NOT NULL,
  `device_name` varchar(64) NOT NULL,
  `device_io` int(1) unsigned NOT NULL,
  `device_couple` int(10) unsigned DEFAULT NULL,
  `device_status` int(1) unsigned NOT NULL DEFAULT '0',
  `registration_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`device_id`),
  UNIQUE KEY `device_name` (`device_name`),
  KEY `FK_device_device_status` (`device_status`),
  KEY `FK_device_device` (`device_couple`),
  CONSTRAINT `FK_device_device_status` FOREIGN KEY (`device_status`) REFERENCES `device_status` (`status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table autohome-dev.device: ~0 rows (approximately)
DELETE FROM `device`;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
/*!40000 ALTER TABLE `device` ENABLE KEYS */;

-- Dumping structure for table autohome-dev.device_activity
DROP TABLE IF EXISTS `device_activity`;
CREATE TABLE IF NOT EXISTS `device_activity` (
  `activity_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_id` int(10) unsigned NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `event_type` int(10) unsigned NOT NULL,
  PRIMARY KEY (`activity_id`),
  KEY `FK_device_event_device` (`device_id`),
  KEY `FK_device_activity_device_event` (`event_type`),
  CONSTRAINT `FK_device_activity_device` FOREIGN KEY (`device_id`) REFERENCES `device` (`device_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_device_activity_device_event` FOREIGN KEY (`event_type`) REFERENCES `device_event` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table autohome-dev.device_activity: ~0 rows (approximately)
DELETE FROM `device_activity`;
/*!40000 ALTER TABLE `device_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_activity` ENABLE KEYS */;

-- Dumping structure for table autohome-dev.device_event
DROP TABLE IF EXISTS `device_event`;
CREATE TABLE IF NOT EXISTS `device_event` (
  `event_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_name` varchar(50) NOT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Dumping data for table autohome-dev.device_event: ~3 rows (approximately)
DELETE FROM `device_event`;
/*!40000 ALTER TABLE `device_event` DISABLE KEYS */;
INSERT INTO `device_event` (`event_id`, `event_name`) VALUES
	(0, 'DEVICE_OFF'),
	(1, 'DEVICE_ON'),
	(3, 'DEVICE_REGISTRATION');
/*!40000 ALTER TABLE `device_event` ENABLE KEYS */;

-- Dumping structure for table autohome-dev.device_status
DROP TABLE IF EXISTS `device_status`;
CREATE TABLE IF NOT EXISTS `device_status` (
  `status_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Dumping data for table autohome-dev.device_status: ~2 rows (approximately)
DELETE FROM `device_status`;
/*!40000 ALTER TABLE `device_status` DISABLE KEYS */;
INSERT INTO `device_status` (`status_id`, `status_name`) VALUES
	(0, 'OFF'),
	(1, 'ON');
/*!40000 ALTER TABLE `device_status` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
