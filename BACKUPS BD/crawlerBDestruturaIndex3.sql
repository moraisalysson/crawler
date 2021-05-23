-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: index3
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `noticias_score`
--

DROP TABLE IF EXISTS `noticias_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `noticias_score` (
  `id_noticia_score` int NOT NULL AUTO_INCREMENT,
  `id_url` int NOT NULL,
  `score_LIWC` int DEFAULT NULL,
  `score_OpLexicon` int DEFAULT NULL,
  `score_ReLiLex` int DEFAULT NULL,
  `score_Sentilex` int DEFAULT NULL,
  `score_WordnetBr` int DEFAULT NULL,
  `polaridade_LIWC` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `polaridade_OpLexicon` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `polaridade_ReLiLex` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `polaridade_Sentilex` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `polaridade_WordnetBr` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_noticia_score`),
  KEY `idx_noticia_score` (`id_url`),
  CONSTRAINT `fK_noticia_score_id_url` FOREIGN KEY (`id_url`) REFERENCES `urls` (`idurl`)
) ENGINE=InnoDB AUTO_INCREMENT=6657 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `palavra_localizacao`
--

DROP TABLE IF EXISTS `palavra_localizacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `palavra_localizacao` (
  `idpalavra_localizacao` int NOT NULL AUTO_INCREMENT,
  `idurl` int NOT NULL,
  `idpalavra` int NOT NULL,
  `localizacao` int DEFAULT NULL,
  PRIMARY KEY (`idpalavra_localizacao`),
  KEY `fk_palavra_localizcao_idurl` (`idurl`),
  KEY `idx_palavra_localizacao_idpalavra` (`idpalavra`),
  CONSTRAINT `fk_palavra_localizcao_idpalavra` FOREIGN KEY (`idpalavra`) REFERENCES `palavras` (`idpalavra`),
  CONSTRAINT `fk_palavra_localizcao_idurl` FOREIGN KEY (`idurl`) REFERENCES `urls` (`idurl`)
) ENGINE=InnoDB AUTO_INCREMENT=2619651 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `palavra_polaridade`
--

DROP TABLE IF EXISTS `palavra_polaridade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `palavra_polaridade` (
  `idpalavra_polaridade` int NOT NULL AUTO_INCREMENT,
  `idpalavra` int NOT NULL,
  `polaridade_LIWC` int DEFAULT NULL,
  `polaridade_OpLexicon` int DEFAULT NULL,
  `polaridade_ReLiLex` int DEFAULT NULL,
  `polaridade_Sentilex` int DEFAULT NULL,
  `polaridade_WordnetBr` int DEFAULT NULL,
  PRIMARY KEY (`idpalavra_polaridade`),
  KEY `idx_palavra_polaridade` (`idpalavra`),
  CONSTRAINT `fK_palavra_polaridade_idpalavra` FOREIGN KEY (`idpalavra`) REFERENCES `palavras` (`idpalavra`)
) ENGINE=InnoDB AUTO_INCREMENT=12821 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `palavras`
--

DROP TABLE IF EXISTS `palavras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `palavras` (
  `idpalavra` int NOT NULL AUTO_INCREMENT,
  `palavra` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`idpalavra`),
  KEY `idx_palavras_palavra` (`palavra`)
) ENGINE=InnoDB AUTO_INCREMENT=59466 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `urls`
--

DROP TABLE IF EXISTS `urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `urls` (
  `idurl` int NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL,
  `autor` varchar(100) DEFAULT NULL,
  `dia` int DEFAULT NULL,
  `mes` varchar(10) DEFAULT NULL,
  `ano` int DEFAULT NULL,
  PRIMARY KEY (`idurl`)
) ENGINE=InnoDB AUTO_INCREMENT=6657 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'index3'
--

--
-- Dumping routines for database 'index3'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-12 21:35:55
