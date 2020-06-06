-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 06, 2020 at 12:09 PM
-- Server version: 5.7.30-0ubuntu0.18.04.1
-- PHP Version: 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fishtanks_75planted`
--

-- --------------------------------------------------------

--
-- Table structure for table `airpump_status`
--

CREATE TABLE `airpump_status` (
  `ok` bit(1) NOT NULL,
  `alert_sent` bit(1) NOT NULL,
  `last_alert_sent_time` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `airpump_status`
--

INSERT INTO `airpump_status` (`ok`, `alert_sent`, `last_alert_sent_time`) VALUES
(b'1', b'0', 1582478762);

-- --------------------------------------------------------

--
-- Table structure for table `atlas_data`
--

CREATE TABLE `atlas_data` (
  `last_update_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `atlas_data`
--

INSERT INTO `atlas_data` (`last_update_time`) VALUES
(1591466822);

-- --------------------------------------------------------

--
-- Table structure for table `led_status`
--

CREATE TABLE `led_status` (
  `temp_status_low` bit(1) NOT NULL,
  `ph_status_low` bit(1) NOT NULL,
  `nh3_status` bit(1) NOT NULL,
  `nh4_status` bit(1) NOT NULL,
  `tank_overall_status_led` bit(1) NOT NULL,
  `temp_status_high` bit(1) NOT NULL,
  `tds_status` bit(1) NOT NULL,
  `fx6_status` bit(1) NOT NULL,
  `f406_status` bit(1) NOT NULL,
  `injecting_co2_led` bit(1) NOT NULL,
  `ph_status_high` bit(1) NOT NULL,
  `airpump_status` bit(1) NOT NULL,
  `uv_pump_status` bit(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `led_status`
--

INSERT INTO `led_status` (`temp_status_low`, `ph_status_low`, `nh3_status`, `nh4_status`, `tank_overall_status_led`, `temp_status_high`, `tds_status`, `fx6_status`, `f406_status`, `injecting_co2_led`, `ph_status_high`, `airpump_status`, `uv_pump_status`) VALUES
(b'0', b'0', b'0', b'1', b'0', b'0', b'0', b'1', b'1', b'1', b'0', b'0', b'0');

-- --------------------------------------------------------

--
-- Table structure for table `logging`
--

CREATE TABLE `logging` (
  `console` tinyint(1) NOT NULL,
  `system_logging` tinyint(1) NOT NULL,
  `log_level` varchar(8) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `logging`
--

INSERT INTO `logging` (`console`, `system_logging`, `log_level`) VALUES
(1, 1, 'DEBUG');

-- --------------------------------------------------------

--
-- Table structure for table `nh3_status`
--

CREATE TABLE `nh3_status` (
  `ok` bit(1) NOT NULL,
  `alert_sent` bit(1) NOT NULL,
  `last_alert_sent_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `nh3_status`
--

INSERT INTO `nh3_status` (`ok`, `alert_sent`, `last_alert_sent_time`) VALUES
(b'1', b'0', 1584211393);

-- --------------------------------------------------------

--
-- Table structure for table `nh4_status`
--

CREATE TABLE `nh4_status` (
  `ok` bit(1) NOT NULL,
  `alert_sent` bit(1) NOT NULL,
  `last_alert_sent_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `nh4_status`
--

INSERT INTO `nh4_status` (`ok`, `alert_sent`, `last_alert_sent_time`) VALUES
(b'0', b'1', 1591463281);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `system_wide` tinyint(1) NOT NULL,
  `edit_notifications` tinyint(1) NOT NULL,
  `ph_status_sms` tinyint(1) NOT NULL,
  `ph_status_pb` tinyint(1) NOT NULL,
  `ph_status_email` tinyint(1) NOT NULL,
  `fx6filter_status_sms` tinyint(1) NOT NULL,
  `fx6filter_status_pb` tinyint(1) NOT NULL,
  `fx6filter_status_email` tinyint(1) NOT NULL,
  `f406filter_status_sms` tinyint(1) NOT NULL,
  `f406filter_status_pb` tinyint(1) NOT NULL,
  `f406filter_status_email` tinyint(1) NOT NULL,
  `uv_status_sms` tinyint(1) NOT NULL,
  `uv_status_pb` tinyint(1) NOT NULL,
  `uv_status_email` tinyint(1) NOT NULL,
  `phcontroller_status_sms` tinyint(1) NOT NULL,
  `phcontroller_status_pb` tinyint(1) NOT NULL,
  `phcontroller_status_email` tinyint(1) NOT NULL,
  `airpump_status_sms` tinyint(1) NOT NULL,
  `airpump_status_pb` tinyint(1) NOT NULL,
  `airpump_status_email` tinyint(1) NOT NULL,
  `temp_status_sms` tinyint(1) NOT NULL,
  `temp_status_pb` tinyint(1) NOT NULL,
  `temp_status_email` tinyint(1) NOT NULL,
  `waterlevel_status_sms` tinyint(1) NOT NULL,
  `waterlevel_status_pb` tinyint(1) NOT NULL,
  `waterlevel_status_email` tinyint(1) NOT NULL,
  `nh3_status_sms` tinyint(1) NOT NULL,
  `nh3_status_pb` tinyint(1) NOT NULL,
  `nh3_status_email` tinyint(1) NOT NULL,
  `tds_status_sms` tinyint(1) NOT NULL,
  `tds_status_pb` tinyint(1) NOT NULL,
  `tds_status_email` tinyint(1) NOT NULL,
  `nh4_status_email` tinyint(1) NOT NULL,
  `nh4_status_sms` tinyint(1) NOT NULL,
  `nh4_status_pb` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`system_wide`, `edit_notifications`, `ph_status_sms`, `ph_status_pb`, `ph_status_email`, `fx6filter_status_sms`, `fx6filter_status_pb`, `fx6filter_status_email`, `f406filter_status_sms`, `f406filter_status_pb`, `f406filter_status_email`, `uv_status_sms`, `uv_status_pb`, `uv_status_email`, `phcontroller_status_sms`, `phcontroller_status_pb`, `phcontroller_status_email`, `airpump_status_sms`, `airpump_status_pb`, `airpump_status_email`, `temp_status_sms`, `temp_status_pb`, `temp_status_email`, `waterlevel_status_sms`, `waterlevel_status_pb`, `waterlevel_status_email`, `nh3_status_sms`, `nh3_status_pb`, `nh3_status_email`, `tds_status_sms`, `tds_status_pb`, `tds_status_email`, `nh4_status_email`, `nh4_status_sms`, `nh4_status_pb`) VALUES
(1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `o2_status`
--

CREATE TABLE `o2_status` (
  `ok` bit(1) NOT NULL,
  `alert_sent` bit(1) NOT NULL,
  `last_alert_sent_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `o2_status`
--

INSERT INTO `o2_status` (`ok`, `alert_sent`, `last_alert_sent_time`) VALUES
(b'1', b'0', 1582514736);

-- --------------------------------------------------------

--
-- Table structure for table `ph_status`
--

CREATE TABLE `ph_status` (
  `ok` bit(1) NOT NULL,
  `alert_sent` bit(1) NOT NULL,
  `last_alert_sent_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `ph_status`
--

INSERT INTO `ph_status` (`ok`, `alert_sent`, `last_alert_sent_time`) VALUES
(b'1', b'0', 1591321441);

-- --------------------------------------------------------

--
-- Table structure for table `power_solar`
--

CREATE TABLE `power_solar` (
  `total_current_power_utilization` smallint(5) NOT NULL,
  `total_current_power_import` smallint(5) NOT NULL,
  `total_current_solar_production` smallint(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `power_solar`
--

INSERT INTO `power_solar` (`total_current_power_utilization`, `total_current_power_import`, `total_current_solar_production`) VALUES
(2961, 1283, 1678);

-- --------------------------------------------------------

--
-- Table structure for table `seneye_data`
--

CREATE TABLE `seneye_data` (
  `last_update_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `seneye_data`
--

INSERT INTO `seneye_data` (`last_update_time`) VALUES
(1591466462);

-- --------------------------------------------------------

--
-- Table structure for table `system_status`
--

CREATE TABLE `system_status` (
  `pool_level_batt_percentage` tinyint(3) NOT NULL,
  `current_military_time` varchar(35) COLLATE utf8_unicode_ci NOT NULL,
  `pool_temp_batt_percentage` tinyint(3) NOT NULL,
  `garage_temp_batt_percentage` tinyint(3) NOT NULL,
  `attic_temp_batt_percentage` tinyint(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `system_status`
--

INSERT INTO `system_status` (`pool_level_batt_percentage`, `current_military_time`, `pool_temp_batt_percentage`, `garage_temp_batt_percentage`, `attic_temp_batt_percentage`) VALUES
(100, 'Saturday Jun 06, 2020  11:09:02', 100, 87, 100);

-- --------------------------------------------------------

--
-- Table structure for table `tds_status`
--

CREATE TABLE `tds_status` (
  `ok` bit(1) NOT NULL,
  `alert_sent` bit(1) NOT NULL,
  `last_alert_sent_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `tds_status`
--

INSERT INTO `tds_status` (`ok`, `alert_sent`, `last_alert_sent_time`) VALUES
(b'1', b'0', 1584130625);

-- --------------------------------------------------------

--
-- Table structure for table `temp_status`
--

CREATE TABLE `temp_status` (
  `ok` bit(1) NOT NULL,
  `alert_sent` bit(1) NOT NULL,
  `last_alert_sent_time` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `temp_status`
--

INSERT INTO `temp_status` (`ok`, `alert_sent`, `last_alert_sent_time`) VALUES
(b'1', b'0', 1591347842);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airpump_status`
--
ALTER TABLE `airpump_status`
  ADD PRIMARY KEY (`ok`);

--
-- Indexes for table `atlas_data`
--
ALTER TABLE `atlas_data`
  ADD PRIMARY KEY (`last_update_time`);

--
-- Indexes for table `led_status`
--
ALTER TABLE `led_status`
  ADD UNIQUE KEY `sprinkler_run_led` (`temp_status_low`);

--
-- Indexes for table `logging`
--
ALTER TABLE `logging`
  ADD UNIQUE KEY `console` (`console`);

--
-- Indexes for table `nh3_status`
--
ALTER TABLE `nh3_status`
  ADD PRIMARY KEY (`ok`);

--
-- Indexes for table `nh4_status`
--
ALTER TABLE `nh4_status`
  ADD PRIMARY KEY (`ok`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`system_wide`);

--
-- Indexes for table `o2_status`
--
ALTER TABLE `o2_status`
  ADD PRIMARY KEY (`ok`);

--
-- Indexes for table `ph_status`
--
ALTER TABLE `ph_status`
  ADD PRIMARY KEY (`ok`);

--
-- Indexes for table `power_solar`
--
ALTER TABLE `power_solar`
  ADD UNIQUE KEY `total_current_power_utilization` (`total_current_power_utilization`);

--
-- Indexes for table `seneye_data`
--
ALTER TABLE `seneye_data`
  ADD PRIMARY KEY (`last_update_time`);

--
-- Indexes for table `system_status`
--
ALTER TABLE `system_status`
  ADD PRIMARY KEY (`current_military_time`);

--
-- Indexes for table `tds_status`
--
ALTER TABLE `tds_status`
  ADD PRIMARY KEY (`ok`);

--
-- Indexes for table `temp_status`
--
ALTER TABLE `temp_status`
  ADD PRIMARY KEY (`ok`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
