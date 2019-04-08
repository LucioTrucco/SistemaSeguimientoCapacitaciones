CREATE DATABASE  IF NOT EXISTS `capacitaciones` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `capacitaciones`;
-- MySQL dump 10.13  Distrib 5.6.24, for Win32 (x86)
--
-- Host: localhost    Database: capacitaciones
-- ------------------------------------------------------
-- Server version	5.7.11-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `topics` varchar(64) DEFAULT NULL,
  `topicsNext` varchar(64) DEFAULT NULL,
  `comments` varchar(64) DEFAULT NULL,
  `training_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `training_id` (`training_id`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`training_id`) REFERENCES `training` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (4,1,'1900-11-11 00:00:00','1','1','1',NULL),(14,2,'2019-04-03 00:00:00','Prender horno','prender microondas','11',NULL),(15,1,'2019-04-11 00:00:00','Presentacion','-','a',NULL);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'Admin'),(2,'Capacitador'),(3,'Direccion');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` int(11) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `surname` varchar(120) DEFAULT NULL,
  `name` varchar(120) DEFAULT NULL,
  `degree` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `file` (`file`),
  UNIQUE KEY `ix_student_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (32,21,'agrabb5@si.edu','Grabb','Adelbert','LWD'),(33,22,'acarrett6@tuttocitta.it','Carrett','Andi','Sales Tax'),(34,23,'bkinavan7@netscape.com','Kinavan','Beltran','Revenue Cycle Management'),(35,24,'tgipps8@guardian.co.uk','Gipps','Tori','Partnership Taxation'),(36,25,'gcrichmer9@omniture.com','Crichmer','Genia','Dog Training'),(37,26,'wcolliholea@yelp.com','Collihole','Wileen','HCS 2000'),(38,27,'mdjorvicb@weather.com','Djorvic','Markus','Successful Business Owner'),(39,28,'ghughesc@mit.edu','Hughes','Gabriel','FBA'),(40,29,'cmallordd@bbb.org','Mallord','Cloe','Video Games');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `training`
--

DROP TABLE IF EXISTS `training`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `training` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `start` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `finalizada` tinyint(1) DEFAULT NULL,
  `description` varchar(64) DEFAULT NULL,
  `comments` varchar(120) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `times` int(11) DEFAULT NULL,
  `department` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `training_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `training`
--

LOCK TABLES `training` WRITE;
/*!40000 ALTER TABLE `training` DISABLE KEYS */;
INSERT INTO `training` VALUES (9,'Aula virtual','2019-04-25 10:51:00','2019-04-19 10:51:00',0,'-','-',14,1,1),(10,'Campus Virtual','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',10,2,1),(11,'Knee','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',11,3,1),(12,'Jet Fuel','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',12,1,1),(13,'Rational DOORS','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',13,2,1),(14,'MSDS','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',14,3,2),(15,'NFPA','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',10,1,2),(16,'TCO reduction','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',11,2,2),(17,'xUnit','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',12,3,2),(18,'LynxOS','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',13,1,2),(19,'PCI Standards','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',14,2,3),(20,'UCM','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',10,3,3),(21,'Mystery Shopping','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',11,1,3),(22,'NRP','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',12,2,3),(23,'Governmental Affairs','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',13,3,3),(24,'Counseling Psychology','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',14,1,4),(25,'VSAM','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',10,2,4),(26,'BBP','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',11,3,4),(27,'SAP Business ByDesign','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',12,1,4),(28,'iPhone Support','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',13,2,1),(29,'Nylon','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',14,3,2),(30,'RSA Tokens','2019-04-08 14:00:00','2019-04-12 15:00:00',0,'-','-',10,1,3),(31,'Nylon Sup','2019-04-08 14:00:00','2019-04-12 15:00:00',1,'-','-',11,2,4);
/*!40000 ALTER TABLE `training` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `training_students`
--

DROP TABLE IF EXISTS `training_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `training_students` (
  `training_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  KEY `training_id` (`training_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `training_students_ibfk_1` FOREIGN KEY (`training_id`) REFERENCES `training` (`id`),
  CONSTRAINT `training_students_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `training_students`
--

LOCK TABLES `training_students` WRITE;
/*!40000 ALTER TABLE `training_students` DISABLE KEYS */;
INSERT INTO `training_students` VALUES (9,40),(9,39),(9,37),(9,35);
/*!40000 ALTER TABLE `training_students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  UNIQUE KEY `ix_user_username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'capacitador','cap@cap.com','pbkdf2:sha256:50000$GgKpUr9V$adc6331cf660d69da65e6c203696e7fd07b30b95bc6f167ef881a81e539bfdf7',1),(3,'admin','adm@adm.com','pbkdf2:sha256:50000$2sJACpSj$814edd7b8efb3276504fc4900a08613efcc308c21a90f4718e809977b9d45dcc',NULL),(7,'director','dir@dir.com','pbkdf2:sha256:50000$92oYmVNd$5ef50e8a6b5d3459e93326cc34aeeb86950b4dffedab52bd429a5659f241dcff',3),(10,'carlos','carlos@gmail.com','pbkdf2:sha256:50000$iY8OSArG$54bfedcaadbf9d8552aeae40a31de2e7b1f31ba922ea91a4966daf90422613da',NULL),(11,'Agustin','agustin@gmail.com','pbkdf2:sha256:50000$dgnAUAOM$930705483c062202d23abd6e1e45af6842062f8508ed47d5b0be4470978e31bd',NULL),(12,'Belen','belen@gmail.com','pbkdf2:sha256:50000$EYXFv8jP$3fa474bfabd7d89926482abfdf6327ac23c9c0bc9ae89c094e3103678e38e20c',NULL),(13,'Leandro','leandro@gmail.com','pbkdf2:sha256:50000$xtxk1T80$58fcfe7a7cabeab01b26e77887e04950cc2db19bf633fe50648e7558fc51315e',NULL),(14,'Lucio','trucco.lucioj@gmail.com','pbkdf2:sha256:50000$5Pd3DfUp$b3ae6254393080b7f085554038204bddb4fd06c5ac30c4f12f8f2922923c86a7',2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'capacitaciones'
--

--
-- Dumping routines for database 'capacitaciones'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-08 12:01:16
