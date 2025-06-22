-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: Adyukinn.mysql.pythonanywhere-services.com    Database: Adyukinn$default
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `event_date` date NOT NULL,
  `location` varchar(255) NOT NULL,
  `required_volunteers` int NOT NULL,
  `image_filename` varchar(255) NOT NULL,
  `organizer_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `organizer_id` (`organizer_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`organizer_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'Экологический субботник','Уборка территории городского парка','2026-04-20','Центральный парк',15,'eco_cleanup.jpg',1,'2025-06-22 07:59:02'),(2,'Благотворительный марафон','Забег в поддержку детей с особенностями развития','2024-05-15','Набережная реки',20,'charity_run.jpg',1,'2025-06-22 07:59:02'),(3,'Фестиваль волонтерства','Праздник для волонтеров города','2026-06-01','Городская площадь',10,'volunteer_fest.jpg',2,'2025-06-22 07:59:02'),(4,'Помощь приюту','Уход за животными в городском приюте','2026-04-25','Приют \"Добрый дом\"',8,'animal_shelter.jpg',3,'2025-06-22 07:59:02'),(5,'День донора','Акция по сдаче крови','2024-05-10','Городская больница',12,'blood_donation.jpg',4,'2025-06-22 07:59:02'),(6,'Помощь пожилым','Помощь по хозяйству пожилым людям','2026-04-22','Центр социальной помощи',10,'elderly_help.jpg',2,'2025-06-22 07:59:02'),(7,'Субботник в школе','Уборка территории школы №5','2026-05-05','Школа №5',15,'school_cleanup.jpg',3,'2025-06-22 07:59:02'),(8,'Помощь библиотеке','Организация книжного фонда','2026-05-20','Городская библиотека',8,'library_help.jpg',4,'2025-06-22 07:59:02'),(9,'Экологическая акция','Сбор макулатуры и пластика','2026-06-10','Торговый центр \"Меридиан\"',20,'eco_action.jpg',1,'2025-06-22 07:59:02'),(10,'Помощь детскому дому','Проведение мастер-классов','2026-05-25','Детский дом \"Радуга\"',12,'orphanage_help.jpg',2,'2025-06-22 07:59:02'),(11,'Спортивный праздник','Спортивные соревнования для детей','2026-06-15','Стадион \"Олимпийский\"',15,'sport_event.jpg',3,'2025-06-22 07:59:02'),(12,'Помощь бездомным','Раздача горячей пищи','2026-04-30','Центр помощи бездомным',10,'homeless_help.jpg',4,'2025-06-22 07:59:02'),(13,'Экскурсия для детей','Познавательная экскурсия по городу','2026-05-18','Городской музей',8,'city_tour.jpg',1,'2025-06-22 07:59:02'),(14,'Помощь в больнице','Помощь в организации работы','2026-06-05','Городская клиническая больница',15,'hospital_help.jpg',2,'2025-06-22 07:59:02'),(15,'Праздник двора','Организация праздника для жителей','2026-05-28','Дворовая площадка',12,'yard_party.jpg',3,'2025-06-22 07:59:02'),(16,'Помощь в приюте','Уборка и ремонт помещений','2026-06-12','Приют для бездомных животных',10,'shelter_help.jpg',4,'2025-06-22 07:59:02'),(17,'Экологический квест','Интерактивная игра по экологии','2026-05-22','Городской парк',15,'eco_quest.jpg',1,'2025-06-22 07:59:02'),(18,'Помощь в детском саду','Проведение развивающих занятий','2026-06-08','Детский сад \"Солнышко\"',8,'kindergarten_help.jpg',2,'2025-06-22 07:59:02'),(19,'Спортивный марафон','Благотворительный забег','2026-05-30','Городской стадион',20,'sport_marathon.jpg',3,'2025-06-22 07:59:02'),(20,'Помощь в музее','Помощь в организации выставки','2026-06-18','Художественный музей',10,'museum_help.jpg',4,'2025-06-22 07:59:02');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'administrator','Superuser with full access to the system, including creating and deleting events'),(2,'moderator','Can edit event data and moderate registrations'),(3,'user','Can view information and register for events');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `role_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','Admin','System',NULL,1,'2025-06-22 07:58:53'),(2,'moderator','09fbcc458fb3430db7ec54ee95635e7fbc06ccfd982b49c55ec53ab8ac2397e7','Moderator','Test',NULL,2,'2025-06-22 07:58:53'),(3,'ivanov','9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c','Иванов','Иван','Иванович',3,'2025-06-22 07:58:53'),(4,'petrov','9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c','Петров','Петр','Петрович',3,'2025-06-22 07:58:53'),(5,'sidorov','9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c','Сидоров','Алексей','Сергеевич',3,'2025-06-22 07:58:53'),(6,'smirnova','9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c','Смирнова','Анна','Павловна',2,'2025-06-22 07:58:53'),(7,'kuznetsov','9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c','Кузнецов','Дмитрий','Александрович',2,'2025-06-22 07:58:53');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer_registrations`
--

DROP TABLE IF EXISTS `volunteer_registrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `volunteer_registrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `volunteer_id` int NOT NULL,
  `contact_info` varchar(255) NOT NULL,
  `registration_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`id`),
  KEY `event_id` (`event_id`),
  KEY `volunteer_id` (`volunteer_id`),
  CONSTRAINT `volunteer_registrations_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE,
  CONSTRAINT `volunteer_registrations_ibfk_2` FOREIGN KEY (`volunteer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer_registrations`
--

LOCK TABLES `volunteer_registrations` WRITE;
/*!40000 ALTER TABLE `volunteer_registrations` DISABLE KEYS */;
INSERT INTO `volunteer_registrations` VALUES (1,1,2,'+7 (999) 123-45-67','2025-06-22 07:59:02','accepted'),(2,1,3,'+7 (999) 234-56-78','2025-06-22 07:59:02','pending'),(3,2,2,'+7 (999) 345-67-89','2025-06-22 07:59:02','accepted'),(4,2,4,'+7 (999) 456-78-90','2025-06-22 07:59:02','rejected'),(5,3,3,'+7 (999) 567-89-01','2025-06-22 07:59:02','accepted'),(6,3,4,'+7 (999) 678-90-12','2025-06-22 07:59:02','pending'),(7,4,2,'+7 (999) 789-01-23','2025-06-22 07:59:02','accepted'),(8,4,3,'+7 (999) 890-12-34','2025-06-22 07:59:02','pending'),(9,5,4,'+7 (999) 901-23-45','2025-06-22 07:59:02','accepted'),(10,5,2,'+7 (999) 012-34-56','2025-06-22 07:59:02','pending');
/*!40000 ALTER TABLE `volunteer_registrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-22  8:41:09
