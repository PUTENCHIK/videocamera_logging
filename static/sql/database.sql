CREATE TABLE IF NOT EXISTS `types` (
	`id` int(10) AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(100) NOT NULL,
	`created_at` timestamp NOT NULL,
	`deleted_at` timestamp DEFAULT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `cameras` (
	`id` int(10) AUTO_INCREMENT NOT NULL UNIQUE,
	`login` varchar(255) NOT NULL,
	`ip` varchar(20),
	`password` varchar(255) NOT NULL,
	`port` int(10) NOT NULL,
	`created_at` timestamp NOT NULL,
	`deleted_at` timestamp DEFAULT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `images` (
	`id` int(10) AUTO_INCREMENT NOT NULL UNIQUE,
	`camera_id` int(10) NOT NULL,
	`created_at` timestamp NOT NULL,
	`deleted_at` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `objects` (
	`id` int(10) AUTO_INCREMENT NOT NULL UNIQUE,
	`image_id` int(10) NOT NULL,
	`type_id` int(10) NOT NULL,
	`created_at` timestamp NOT NULL,
	`deleted_at` timestamp DEFAULT NULL,
	PRIMARY KEY (`id`)
);



ALTER TABLE `images` ADD CONSTRAINT `images_fk1` FOREIGN KEY (`camera_id`) REFERENCES `cameras`(`id`);
ALTER TABLE `objects` ADD CONSTRAINT `objects_fk1` FOREIGN KEY (`image_id`) REFERENCES `images`(`id`);
ALTER TABLE `objects` ADD CONSTRAINT `objects_fk2` FOREIGN KEY (`type_id`) REFERENCES `types`(`id`);