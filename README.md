# Disaster backup xen disk file names on SR

## MySQL
```
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `xs_storage` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `xs_storage`;

CREATE TABLE `sr_file_name` (
  `uid` int(10) UNSIGNED NOT NULL,
  `file_uuid` char(36) NOT NULL COMMENT 'znamena nazev souboru na sr',
  `snapshot_of` char(36) NOT NULL,
  `file_name_description` varchar(255) NOT NULL,
  `file_name_label` varchar(255) NOT NULL COMMENT 'nazev disku v xs',
  `is_a_snapshot` varchar(255) NOT NULL,
  `snapshot_time` varchar(255) NOT NULL
  `created` datetime NOT NULL,
  `updated` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sr_list` (
  `uid` int(10) UNSIGNED NOT NULL,
  `sr_uuid` char(36) NOT NULL,
  `name_label` varchar(255) NOT NULL,
  `name_description` varchar(255) DEFAULT NULL,
  `created` datetime NOT NULL,
  `updated` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `vm_list` (
  `uid` int(10) UNSIGNED NOT NULL,
  `uid_sr_list` int(10) UNSIGNED NOT NULL,
  `uid_sr_file_name` int(10) UNSIGNED NOT NULL,
  `vm_uuid` char(36) NOT NULL,
  `vm_name_label` varchar(255) NOT NULL,
  `vdi_name_description` varchar(255) DEFAULT NULL,
  `device` varchar(255) NOT NULL,
  `bootable` varchar(255) NOT NULL
  `created` datetime NOT NULL,
  `updated` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `sr_file_name`
  ADD PRIMARY KEY (`uid`);

ALTER TABLE `sr_list`
  ADD PRIMARY KEY (`uid`);

ALTER TABLE `vm_list`
  ADD PRIMARY KEY (`uid`,`uid_sr_list`,`uid_sr_file_name`),
  ADD KEY `uid_sr_file_name` (`uid_sr_file_name`),
  ADD KEY `uid_sr_list` (`uid_sr_list`);

ALTER TABLE `sr_file_name`
  MODIFY `uid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `sr_list`
  MODIFY `uid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `vm_list`
  MODIFY `uid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `vm_list`
  ADD CONSTRAINT `vm_list_ibfk_1` FOREIGN KEY (`uid_sr_file_name`) REFERENCES `sr_file_name` (`uid`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `vm_list_ibfk_2` FOREIGN KEY (`uid_sr_list`) REFERENCES `sr_list` (`uid`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;
```