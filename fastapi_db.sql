-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 30, 2024 at 08:38 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fastapi_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `notifies`
--

CREATE TABLE `notifies` (
  `id` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `explain` varchar(255) DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `confirmed_at` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `notifies`
--

INSERT INTO `notifies` (`id`, `customer_id`, `title`, `content`, `explain`, `is_read`, `created_at`, `confirmed_at`, `user_id`) VALUES
(1, 100, 'Tiêu đề thông báo', 'Nội dung thông báo', 'Thằng sinh viên này ngu quá', 1, '2024-07-30 15:36:16', '2024-07-30 15:37:57', 8),
(2, 100, 'Tiêu đề thông báo 1', 'Nội dung thông báo', NULL, 0, '2024-07-30 15:36:22', NULL, NULL),
(3, 100, 'Tiêu đề thông báo 2', 'Nội dung thông báo', NULL, 0, '2024-07-30 15:36:25', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `notifies`
--
ALTER TABLE `notifies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_notifies_title` (`title`),
  ADD KEY `ix_notifies_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `notifies`
--
ALTER TABLE `notifies`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
