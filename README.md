# Disaster backup of xenserver (XCP-NG) VDIs disk file names on NFS SR

```
-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 01, 2022 at 04:58 PM
-- Server version: 10.3.34-MariaDB-0ubuntu0.20.04.1
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `xs_storage`
--

-- --------------------------------------------------------

--
-- Table structure for table `storages`
--

CREATE TABLE `storages` (
  `id` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `uuid` varchar(36) NOT NULL,
  `name_label` varchar(255) NOT NULL,
  `name_description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `vdi`
--

CREATE TABLE `vdi` (
  `id` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `vm` int(11) NOT NULL,
  `storage` int(11) NOT NULL,
  `uuid` varchar(36) NOT NULL,
  `name_label` varchar(255) NOT NULL,
  `snapshot` varchar(255) NOT NULL,
  `vbd_device` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `version`
--

CREATE TABLE `version` (
  `id` int(11) NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `vm`
--

CREATE TABLE `vm` (
  `id` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `uuid` varchar(36) NOT NULL,
  `name_label` varchar(255) NOT NULL,
  `name_description` varchar(255) NOT NULL,
  `snapshot` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `storages`
--
ALTER TABLE `storages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `version` (`version`);

--
-- Indexes for table `vdi`
--
ALTER TABLE `vdi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `version` (`version`),
  ADD KEY `vm` (`vm`),
  ADD KEY `storage` (`storage`);

--
-- Indexes for table `version`
--
ALTER TABLE `version`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `vm`
--
ALTER TABLE `vm`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `version` (`version`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `storages`
--
ALTER TABLE `storages`
  ADD CONSTRAINT `storages_ibfk_1` FOREIGN KEY (`version`) REFERENCES `version` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `vdi`
--
ALTER TABLE `vdi`
  ADD CONSTRAINT `vdi_ibfk_1` FOREIGN KEY (`version`) REFERENCES `version` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `vdi_ibfk_2` FOREIGN KEY (`vm`) REFERENCES `vm` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `vdi_ibfk_3` FOREIGN KEY (`storage`) REFERENCES `storages` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `vm`
--
ALTER TABLE `vm`
  ADD CONSTRAINT `vm_ibfk_1` FOREIGN KEY (`version`) REFERENCES `version` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;
```