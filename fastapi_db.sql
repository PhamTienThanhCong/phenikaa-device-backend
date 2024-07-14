-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 14, 2024 at 07:16 AM
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
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int NOT NULL,
  `role` int DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `birth_date` varchar(20) DEFAULT NULL,
  `gender` int DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `card_id` varchar(20) DEFAULT NULL,
  `date_start` varchar(20) DEFAULT NULL,
  `expired` tinyint(1) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `status` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `role`, `email`, `full_name`, `avatar`, `birth_date`, `gender`, `address`, `phone_number`, `card_id`, `date_start`, `expired`, `department`, `status`) VALUES
(100, 1, 'user@example.com', 'stringasdasd', 'string', 'string', 0, 'string', 'string', 'string', 'string', 0, 'string', 1),
(101, 1, 'user@example.com', 'string', 'string', 'string', 0, 'string', 'string', 'string', 'string', 0, 'string', 1),
(120, 1, 'user@example.com', 'string', 'string', 'string', 0, 'string', 'string', 'string', 'string', 0, 'string', 1);

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `presigned_url` varchar(255) DEFAULT NULL,
  `information` varchar(255) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `total` int DEFAULT NULL,
  `total_used` int DEFAULT NULL,
  `total_maintenance` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `devices`
--

INSERT INTO `devices` (`id`, `name`, `category`, `image`, `presigned_url`, `information`, `note`, `total`, `total_used`, `total_maintenance`, `is_active`) VALUES
(1, 'string', 'string', '', '8f1a8a96-6e4e-4827-a306-82803ac0c946', 'string', 'string', 0, 0, 0, 1),
(2, 'str123ing', 'string', '', '7ba5cb00-79ea-4b1f-975a-63f263c3666e', 'string', 'string', 0, 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `profiles`
--

CREATE TABLE `profiles` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `birth_date` varchar(20) DEFAULT NULL,
  `gender` int DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `card_id` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `profiles`
--

INSERT INTO `profiles` (`id`, `user_id`, `full_name`, `avatar`, `birth_date`, `gender`, `address`, `phone_number`, `card_id`) VALUES
(5, 8, 'string_edit', 'string', 'string', 0, 'string', 'string', 'string'),
(6, 9, 'string', 'string', 'string', 0, 'string', 'string', 'string'),
(7, 10, 'string', 'string', 'string', 0, 'string', 'string', 'string');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `full_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(250) DEFAULT NULL,
  `role` int DEFAULT NULL,
  `is_active` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `password`, `role`, `is_active`) VALUES
(8, 'string_edit', 'user@example.com', '$2b$12$iXNr0S74aEoucGU1CihgpOJtN3bxolZvuvuEaT6YSLv0VtSNLaOUu', 1, 0),
(9, 'string', 'use3r@example.com', '$2b$12$WFIR/UyMLuVEj76D60RmE.xQOHWrcNo3jU8L8JbTqczhVQoIO8fGi', 1, 0),
(10, 'string', 'user2@example.com', '$2b$12$PAVBcwtsdeiU917R9lVMnuEUQDLIuq.6KStkAC5xDHjLtIx5rCEPC', 1, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_customers_status` (`status`),
  ADD KEY `ix_customers_gender` (`gender`),
  ADD KEY `ix_customers_phone_number` (`phone_number`),
  ADD KEY `ix_customers_avatar` (`avatar`),
  ADD KEY `ix_customers_department` (`department`),
  ADD KEY `ix_customers_email` (`email`),
  ADD KEY `ix_customers_role` (`role`),
  ADD KEY `ix_customers_birth_date` (`birth_date`),
  ADD KEY `ix_customers_address` (`address`),
  ADD KEY `ix_customers_card_id` (`card_id`),
  ADD KEY `ix_customers_date_start` (`date_start`),
  ADD KEY `ix_customers_full_name` (`full_name`);

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_devices_category` (`category`),
  ADD KEY `ix_devices_name` (`name`),
  ADD KEY `ix_devices_note` (`note`),
  ADD KEY `ix_devices_information` (`information`);

--
-- Indexes for table `profiles`
--
ALTER TABLE `profiles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_profiles_user_id` (`user_id`),
  ADD KEY `ix_profiles_card_id` (`card_id`),
  ADD KEY `ix_profiles_full_name` (`full_name`),
  ADD KEY `ix_profiles_birth_date` (`birth_date`),
  ADD KEY `ix_profiles_gender` (`gender`),
  ADD KEY `ix_profiles_phone_number` (`phone_number`),
  ADD KEY `ix_profiles_avatar` (`avatar`),
  ADD KEY `ix_profiles_address` (`address`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT for table `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `profiles`
--
ALTER TABLE `profiles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `profiles`
--
ALTER TABLE `profiles`
  ADD CONSTRAINT `profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
