-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: flight_booking
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `flight_booking_booking`
--

DROP TABLE IF EXISTS `flight_booking_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_booking_booking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `number_of_tickets` int unsigned NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `ticket_code` varchar(6) NOT NULL,
  `number_of_tickets_economy` int unsigned NOT NULL,
  `number_of_tickets_first_class` int unsigned NOT NULL,
  `number_of_tickets_premium_economy` int unsigned NOT NULL,
  `ticket_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `flight_booking_booki_ticket_id_04cc18f7_fk_flight_bo` (`ticket_id`),
  CONSTRAINT `flight_booking_booki_ticket_id_04cc18f7_fk_flight_bo` FOREIGN KEY (`ticket_id`) REFERENCES `flight_booking_ticket` (`id`),
  CONSTRAINT `flight_booking_booking_chk_1` CHECK ((`number_of_tickets` >= 0)),
  CONSTRAINT `flight_booking_booking_chk_2` CHECK ((`number_of_tickets_economy` >= 0)),
  CONSTRAINT `flight_booking_booking_chk_3` CHECK ((`number_of_tickets_first_class` >= 0)),
  CONSTRAINT `flight_booking_booking_chk_4` CHECK ((`number_of_tickets_premium_economy` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_booking_booking`
--

LOCK TABLES `flight_booking_booking` WRITE;
/*!40000 ALTER TABLE `flight_booking_booking` DISABLE KEYS */;
INSERT INTO `flight_booking_booking` VALUES (1,'MATHEUS',17,1839.99,'4A7IBT',12,1,4,1),(2,'renata',11,1919.99,'ILJY4W',2,4,5,1),(3,'jhon doe',1,100.00,'O5GANX',1,0,0,1),(4,'jane doe',5,879.99,'ONGW66',0,1,4,1),(5,'Clay More',12,1679.99,'H5R1C4',7,4,1,1),(6,'wal',3,300.00,'R6WPFE',3,0,0,1),(7,'wal',6,1039.99,'VD3FM2',2,3,1,1),(9,'Sara',6,1119.99,'MEHU0L',1,3,2,1);
/*!40000 ALTER TABLE `flight_booking_booking` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-26  8:50:52
