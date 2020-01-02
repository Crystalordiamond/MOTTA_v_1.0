-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: MOTTA_data
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.18.04.4

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
-- Table structure for table `tb_user`
--

DROP TABLE IF EXISTS `tb_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `u_phone` varchar(32) NOT NULL,
  `u_backup` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (1,'123456',NULL,0,'chenjun','','','luochenxi163@163.com',0,1,'2019-12-25 11:47:33.373657','13651416330','Administrator'),(2,'123456',NULL,0,'chenjun1','','','luochenxi163@163.com',0,1,'2019-12-25 11:48:06.654979','13651416330','Manager'),(3,'123456',NULL,0,'chenjun2','','','luochenxi163@163.com',0,1,'2019-12-25 11:48:30.710932','13651416330','Visitor');
/*!40000 ALTER TABLE `tb_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_divices`
--

DROP TABLE IF EXISTS `tb_divices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_divices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `divice_ip` varchar(50) NOT NULL,
  `divice_location` varchar(50) DEFAULT NULL,
  `divice_site` varchar(50) DEFAULT NULL,
  `divice_communication` varchar(50) DEFAULT NULL,
  `divice_type` varchar(50) DEFAULT NULL,
  `divice_serial` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `divice_ip` (`divice_ip`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_divices`
--

LOCK TABLES `tb_divices` WRITE;
/*!40000 ALTER TABLE `tb_divices` DISABLE KEYS */;
INSERT INTO `tb_divices` VALUES (1,'192.168.1.30','China','MDC30','Modbus-TCP','ATM-06E','100101011'),(2,'192.168.1.175','China','MDC175','Modbus-TCP','ATM-06E','100101011');
/*!40000 ALTER TABLE `tb_divices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_warningconfig`
--

DROP TABLE IF EXISTS `tb_warningconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_warningconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `con_server` varchar(20) NOT NULL,
  `con_port` varchar(20) NOT NULL,
  `con_method` varchar(20) NOT NULL,
  `con_account` varchar(50) NOT NULL,
  `con_password` varchar(20) NOT NULL,
  `con_phone` varchar(20) NOT NULL,
  `con_ip` varchar(20) NOT NULL,
  `con_other` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_warningconfig`
--

LOCK TABLES `tb_warningconfig` WRITE;
/*!40000 ALTER TABLE `tb_warningconfig` DISABLE KEYS */;
INSERT INTO `tb_warningconfig` VALUES (1,'smtp.163.com','25','SSL','luochenxi163@163.com','1234abcd','','','Administrator');
/*!40000 ALTER TABLE `tb_warningconfig` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-27 12:12:43
