-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 28, 2022 at 05:28 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_farming`
--

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `id` int(11) NOT NULL,
  `comment` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `ticked` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`id`, `comment`, `user_id`, `post_id`, `created_at`, `ticked`) VALUES
(1, 'They don’t usually just rot unless you leave them along for too long. \r\nBut if they’re rotting before or as they ripen, you have some problem. If it’s on the end, it’s blossom-end rot. \r\nThat’s a result of the calcium levels in the soil and the water or l', 3, 1, '2022-02-26 13:20:28', 'on'),
(2, 'Why are they rotting? If it’s leaving them there too long, pic faster. However, there are several other \r\nreasons. If they develop a black spot on the base\r\n (opposite the stem) you have blossom-end rot which is a combination of lots of sun in hot weather', 3, 1, '2022-02-26 11:50:35', 'checked');

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `disease` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`id`, `disease`, `user_id`, `image`, `created_at`) VALUES
(3, 'Tomato___Bacterial_spot', 2, '0a64655c-4052-4e5f-a696-2a6cf25d10c9___GCREC_Bact.Sp_6017.JPG', '2022-02-26 10:09:06'),
(4, 'Tomato___Bacterial_spot', 2, '00a7c269-3476-4d25-b744-44d6353cd921___GCREC_Bact.Sp_5807.JPG', '2022-02-26 10:20:08'),
(5, 'Tomato___Late_blight', 2, '0ad88d7a-c14a-4ac9-8520-c11a0ade3a8f___UF.GRC_BS_Lab_Leaf_0996.JPG', '2022-02-26 10:20:19'),
(16, 'Tomato___healthy', 3, '1af0bfe1-4bcf-4b8b-be66-5d0953eb647e___GH_HL_Leaf_482.2.JPG', '2022-02-28 13:21:38'),
(17, 'Tomato___Spider_mites Two-spotted_spider_mite', 3, '0d831ad9-bc2a-4168-bbf2-6030f3f886f2___Com.G_SpM_FL_9419.JPG', '2022-02-28 13:21:44'),
(18, 'Tomato___Leaf_Mold', 3, '9ef0e7b7-ce38-4829-aad9-23b954a26000___PSU_CG_2324.JPG', '2022-02-28 13:22:57'),
(19, 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 3, '0d07c65d-0a4f-4a0b-8e5a-ade16407928a___UF.GRC_YLCV_Lab_02450.JPG', '2022-02-28 13:23:05'),
(20, 'Tomato___Septoria_leaf_spot', 3, '0a5edec2-e297-4a25-86fc-78f03772c100___JR_Sept.L.S_8468.JPG', '2022-02-28 13:23:13');

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `id` int(11) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`id`, `street`, `city`, `country`, `user_id`, `created_at`) VALUES
(1, '8663 Zimre Park', 'Harare', 'Zimbabwe', 2, '2022-02-26 08:43:40'),
(2, '676 Zata Chitungwiza ', 'harare', 'Zimbabwe', 3, '2022-02-26 08:53:32');

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

CREATE TABLE `post` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `body` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `post`
--

INSERT INTO `post` (`id`, `title`, `body`, `user_id`, `created_at`) VALUES
(1, 'What should I do to stop tomatoes from rotting on the vine?', '                    They don’t usually just rot unless you leave them along for too long. \r\nBut if they’re rotting before or as they ripen, you have some problem. If it’s on the end, it’s blossom-end rot.\r\n That’s a result of the calcium levels in the soi', 2, '2022-02-26 08:51:27');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(80) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`id`, `name`, `description`) VALUES
(1, 'farmer', NULL),
(2, 'admin', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `roles_users`
--

CREATE TABLE `roles_users` (
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `roles_users`
--

INSERT INTO `roles_users` (`user_id`, `role_id`) VALUES
(1, 2),
(2, 1),
(3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `confirmed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `phone`, `active`, `created_at`, `confirmed_at`) VALUES
(1, 'admin', 'admin@smartfarming.com', '$2b$12$gGR4n0oj89wmaKvIvXhwAO/qnj442P37hbjuU08tJpa2HMibVeOJW', '0777547547', 1, '2022-02-26 13:02:16', NULL),
(2, 'samuel', 'samuelfaindani@gmail.com', '$2b$12$eZg14VbzvB5aNNSpVYUrG.21n0dmCq1YioTys7.i4osqzS31oabA6', NULL, 1, '2022-02-26 08:43:40', NULL),
(3, 'mk', 'mk@gmail.com', '$2b$12$o.MV/BklXm/yLdnRLDWBTOPA9zwGu7u8EPWSNmqxn7Z.JRsdO2gBy', NULL, 1, '2022-02-26 08:53:32', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `post_id` (`post_id`);

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `roles_users`
--
ALTER TABLE `roles_users`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `role_id` (`role_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comment`
--
ALTER TABLE `comment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`);

--
-- Constraints for table `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT `history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `location`
--
ALTER TABLE `location`
  ADD CONSTRAINT `location_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `post`
--
ALTER TABLE `post`
  ADD CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `roles_users`
--
ALTER TABLE `roles_users`
  ADD CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `roles_users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
