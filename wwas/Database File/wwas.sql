-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 09, 2022 at 07:02 AM
-- Server version: 5.6.41-84.1
-- PHP Version: 7.3.32

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wwas`
--
CREATE DATABASE IF NOT EXISTS `wwas` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `wwas`;

DELIMITER $$
--
-- Procedures
--
DROP PROCEDURE IF EXISTS `createRequestMessage`$$
CREATE PROCEDURE `createRequestMessage` (IN `p1` BIGINT, IN `p2` TEXT, IN `p3` TEXT, IN `p4` ENUM('MESSAGE','FILE','IMAGE'))  NO SQL
    DETERMINISTIC
BEGIN
	INSERT INTO `msgs` (`userID`, `phone`, `message`, `type`) VALUES (p1, p2, p3, p4);
END$$

DROP PROCEDURE IF EXISTS `requestMessages`$$
CREATE PROCEDURE `requestMessages` (IN `p1` BIGINT)  NO SQL
    DETERMINISTIC
BEGIN
	SELECT `phone`, `message`, `type` FROM `msgs` WHERE `userID` = p1 AND `status` = 'WAITING';
    UPDATE `msgs` SET `status` = 'DONE' WHERE `userID` = p1;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `msgs`
--

DROP TABLE IF EXISTS `msgs`;
CREATE TABLE IF NOT EXISTS `msgs` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `userID` bigint(20) NOT NULL,
  `phone` text COLLATE utf8_unicode_ci NOT NULL,
  `message` text COLLATE utf8_unicode_ci NOT NULL,
  `type` enum('MESSAGE','FILE','IMAGE') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'MESSAGE',
  `status` enum('WAITING','DONE') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'WAITING',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='This table will store messages.';

--
-- Dumping data for table `msgs`
--

INSERT INTO `msgs` (`id`, `userID`, `phone`, `message`, `type`, `status`, `created`) VALUES
(1, 1, '445123456789', 'This is a test message.', 'MESSAGE', 'DONE', '2022-02-08 12:41:15'),
(2, 1, '445123456789', 'http://www.africau.edu/images/default/sample.pdf', 'FILE', 'DONE', '2022-02-08 12:43:27'),
(3, 1, '445123456789', 'https://i.pinimg.com/564x/63/f7/e9/63f7e99d2bdb21c005ce2debca4c3a9e.jpg', 'IMAGE', 'DONE', '2022-02-09 08:33:01');
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
