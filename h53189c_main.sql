-- phpMyAdmin SQL Dump
-- version 4.9.11
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Час створення: Бер 05 2023 р., 16:47
-- Версія сервера: 5.6.51
-- Версія PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База даних: `h53189c_main`
--

-- --------------------------------------------------------

--
-- Структура таблиці `abit_request`
--

CREATE TABLE `abit_request` (
  `AM` varchar(32) DEFAULT NULL,
  `PI` varchar(32) DEFAULT NULL,
  `CS` varchar(32) DEFAULT NULL,
  `SA` varchar(32) DEFAULT NULL,
  `date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `emoji_guard`
--

CREATE TABLE `emoji_guard` (
  `chat_user_id` varchar(64) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `right_answer` varchar(20) DEFAULT NULL,
  `answer_shit` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `guard`
--

CREATE TABLE `guard` (
  `chat_id` varchar(32) NOT NULL,
  `guard_status` tinyint(4) NOT NULL DEFAULT '0',
  `autodelete` tinyint(1) NOT NULL DEFAULT '1',
  `join_info` varchar(20) DEFAULT NULL,
  `personal` tinyint(1) NOT NULL DEFAULT '0',
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `log`
--

CREATE TABLE `log` (
  `chat_id` varchar(32) DEFAULT NULL,
  `user_id` varchar(32) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `time_stamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `penguin`
--

CREATE TABLE `penguin` (
  `chat_id` varchar(32) DEFAULT NULL,
  `user_id` varchar(32) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `need_penguin` tinyint(1) DEFAULT '1',
  `give_name` varchar(100) DEFAULT NULL,
  `give_id` varchar(32) DEFAULT NULL,
  `time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Структура таблиці `users`
--

CREATE TABLE `users` (
  `user_id` varchar(32) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Індекси збережених таблиць
--

--
-- Індекси таблиці `abit_request`
--
ALTER TABLE `abit_request`
  ADD UNIQUE KEY `date` (`date`);

--
-- Індекси таблиці `emoji_guard`
--
ALTER TABLE `emoji_guard`
  ADD UNIQUE KEY `chat_user_id` (`chat_user_id`);

--
-- Індекси таблиці `guard`
--
ALTER TABLE `guard`
  ADD UNIQUE KEY `chat_id` (`chat_id`);

--
-- Індекси таблиці `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `user_id` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
