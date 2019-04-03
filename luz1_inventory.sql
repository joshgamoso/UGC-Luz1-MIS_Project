-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 07, 2018 at 03:18 AM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 5.6.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `luz1_inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'S3cur1t4');

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_no` int(11) NOT NULL,
  `area` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  `des` varchar(100) NOT NULL,
  `sn` varchar(32) NOT NULL,
  `dop` varchar(11) NOT NULL,
  `qty` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_no`, `area`, `type`, `des`, `sn`, `dop`, `qty`) VALUES
(1, 'La Union', 'Desktop Set', 'HP win7 i5 2gb', 'HPD7P6XX', '2018-04-17', 1),
(2, 'La Union', 'Desktop Set', 'Intel coreduo winxp 2gb', 'N/A', '2018-04-17', 1),
(3, 'La Union', 'Desktop Set', 'Intel winxp pentium 2gb', 'N/A', '2018-04-17', 1),
(4, 'La Union', 'Desktop Set', 'AMD win10 Mini-PC 4gb', 'N/A', '2018-04-17', 1),
(5, 'Villasis', 'Router/Switch', 'Cisco 1900 series VPN', 'C4ICO687', '2018-04-18', 1),
(6, 'Calasiao', 'CCTV', 'Optic HD CAM set', 'OPH90896', '2018-04-18', 3),
(7, 'La Union', 'Laptop', 'HP Probook 4440s', '0PUK00XG', '2018-04-18', 1),
(8, 'Irisan', 'CCTV', 'Optic HD Cam set', 'OPH90909', '2018-04-18', 5),
(9, 'VIllasis', 'Monitor', 'Asus ProArt 1080p 21\"', 'N/A', '2018-04-19', 1),
(10, 'Isabela', 'Router/Switch', 'Cisco 1900 series VPN', 'N/A', '2018-04-19', 1),
(11, 'Isabela', 'Desktop Set', 'intel win 7 Pentium 4gb', 'N/A', '2018-04-19', 3),
(12, 'Isabela', 'Router/Switch', 'TP link router wr840n', 'N/A', '2018-04-19', 1),
(13, 'Isabela', 'Monitor', 'Acer R0 17\"', 'N/A', '2018-04-19', 2),
(14, 'Pampanga', 'Desktop Set', 'Intel win7 pentium 2gb', 'N/A', '2018-04-19', 1),
(15, 'La Union', 'Printer', 'HPlaserjet521', 'PH97LP0J', '2018-04-20', 1),
(16, 'La Union', 'Laptop', 'Lenovo Ideapad 100s', '0PUK0LIP', '2018-04-20', 1),
(17, 'Bantay', 'Desktop Set', 'Intel win7 pentium 2gb', 'N/A', '2018-04-20', 1),
(18, 'Bantay', 'CCTV', 'Optic DVI Cam set', 'OPD01X23', '2018-04-20', 4),
(19, 'Pampanga', 'Printer', 'Canon inkjet 2700', 'C44NI0K6', '2018-04-20', 1),
(20, 'Nueva Ecija', 'Desktop Set', 'Intel win7 pentium 2gb', 'N/A', '2018-04-20', 1),
(21, 'Nueva Ecija', 'Desktop Set', 'Intel win10 celeron 2gb', 'N/A', '2018-04-20', 1),
(22, 'VIllasis', 'Monitor', 'Asus MG series 32\"', 'RC69K68M', '2018-04-20', 1),
(23, 'La Union', 'RAM/Video Card', 'Radeon HD6570 2gb', '3GH4AM2G', '2018-04-20', 1),
(24, 'Bantay', 'Mouse/Keyboard', 'A4tech PS2 mouse+keyboard set', 'H4AS3CPS', '2018-04-20', 1),
(25, 'VIllasis', 'Router/Switch', 'Asus Router N300', '45U5T3K3', '2018-04-20', 1),
(26, 'Isabela', 'Laptop', 'HP PROBOOK 4440s', 'PH9X70V6', '2018-04-20', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `item_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
