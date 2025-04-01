CREATE DATABASE  IF NOT EXISTS `parkingv2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `parkingv2`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: parkingv2
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `parkingslots`
--

DROP TABLE IF EXISTS `parkingslots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parkingslots` (
  `ParkingSlotID` int NOT NULL AUTO_INCREMENT,
  `SlotNumber` varchar(50) NOT NULL,
  `IsOccupied` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ParkingSlotID`),
  UNIQUE KEY `SlotNumber` (`SlotNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parkingslots`
--

LOCK TABLES `parkingslots` WRITE;
/*!40000 ALTER TABLE `parkingslots` DISABLE KEYS */;
INSERT INTO `parkingslots` VALUES (1,'A1',1),(2,'A2',0),(3,'A3',0),(4,'A4',0),(5,'A5',0),(6,'B1',0),(7,'B2',0),(8,'B3',0),(9,'B4',0),(10,'B5',0),(11,'C1',0),(12,'C2',0),(13,'C3',0),(14,'C4',0),(15,'C5',0),(16,'D1',0),(17,'D2',0),(18,'D3',0),(19,'D4',0),(20,'D5',0);
/*!40000 ALTER TABLE `parkingslots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parkingtransactions`
--

DROP TABLE IF EXISTS `parkingtransactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parkingtransactions` (
  `TransactionID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `VehicleID` int NOT NULL,
  `ParkingSlotID` int NOT NULL,
  `EntryTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `ExitTime` datetime DEFAULT NULL,
  `PaymentAmount` decimal(10,2) DEFAULT '0.00',
  `PaymentMethod` varchar(50) DEFAULT NULL,
  `DiscountRate` decimal(3,2) DEFAULT '0.00',
  PRIMARY KEY (`TransactionID`),
  KEY `UserID` (`UserID`),
  KEY `VehicleID` (`VehicleID`),
  KEY `ParkingSlotID` (`ParkingSlotID`),
  CONSTRAINT `parkingtransactions_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  CONSTRAINT `parkingtransactions_ibfk_2` FOREIGN KEY (`VehicleID`) REFERENCES `vehicles` (`VehicleID`) ON DELETE CASCADE,
  CONSTRAINT `parkingtransactions_ibfk_3` FOREIGN KEY (`ParkingSlotID`) REFERENCES `parkingslots` (`ParkingSlotID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parkingtransactions`
--

LOCK TABLES `parkingtransactions` WRITE;
/*!40000 ALTER TABLE `parkingtransactions` DISABLE KEYS */;
INSERT INTO `parkingtransactions` VALUES (1,1,1,1,'2025-04-01 08:56:00','2025-04-01 08:57:11',18.00,'Cash',0.10),(2,3,3,1,'2025-04-01 01:00:00',NULL,16.00,'Cash',0.20);
/*!40000 ALTER TABLE `parkingtransactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `UserType` enum('Student','Faculty','Visitor','Admin') NOT NULL,
  `FirstName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `PhoneNumber` varchar(20) DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `PhoneNumber` (`PhoneNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Student','Benedict','Elnar','Benedictelnar@gmail.com','09569127137','$2b$12$DMIXam/Z/ij2zMTTZ4K5VeqTjbqun6DH2Koo/ZdrLbwUpZK96GgqG'),(2,'Admin','System','Administrator','adminMe@gmail.com','09928731885','$2b$12$y4lD5ixqfoCbWWTkjfZJJOJfYSnl0iJU3be3hWWfGH9K9i/tHKaqm'),(3,'Student','me','you','us@gmail.com','0857219281','$2b$12$98qNIMjx1e35pmbIpbgoqOlZbGNdxbxvMeUbiIQeSf0.FvePErIFm');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicles` (
  `VehicleID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `VehicleType` varchar(50) NOT NULL,
  `LicensePlate` varchar(20) NOT NULL,
  `Make` varchar(255) NOT NULL,
  `Model` varchar(255) NOT NULL,
  `Color` varchar(50) NOT NULL,
  PRIMARY KEY (`VehicleID`),
  UNIQUE KEY `LicensePlate` (`LicensePlate`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles`
--

LOCK TABLES `vehicles` WRITE;
/*!40000 ALTER TABLE `vehicles` DISABLE KEYS */;
INSERT INTO `vehicles` VALUES (1,1,'Car','MQDDQW','Toyota','Mk4','orange'),(2,1,'Car','DQFQWFV','BMW','335','black'),(3,3,'Car','DQCQ12C','Toyota','MK3','brown');
/*!40000 ALTER TABLE `vehicles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-01  9:32:27
