-- MySQL dump 10.13  Distrib 8.3.0, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: Stairs_of_Acropolis
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `Acropolis_Questions_System`
--

DROP TABLE IF EXISTS `Acropolis_Questions_System`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Acropolis_Questions_System` (
  `question_id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `specialty` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `question` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `question_type` varchar(31) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `optionA` varchar(255) DEFAULT NULL,
  `optionB` varchar(255) DEFAULT NULL,
  `optionC` varchar(255) DEFAULT NULL,
  `optionD` varchar(255) DEFAULT NULL,
  `correct_answer` varchar(255) NOT NULL,
  `explanation` varchar(255) DEFAULT NULL,
  `difficulty` varchar(31) NOT NULL,
  PRIMARY KEY (`question_id`),
  CONSTRAINT `acropolis_questions_system_chk_1` CHECK ((`question_type` in (_utf8mb4'Gorgo',_utf8mb4'Sparta'))),
  CONSTRAINT `acropolis_questions_system_chk_2` CHECK ((`difficulty` in (_utf8mb4'BEGINNER',_utf8mb4'EASY',_utf8mb4'INTERMEDIATE',_utf8mb4'HARD',_utf8mb4'EXPERT'))),
  CONSTRAINT `acropolis_questions_system_chk_3` CHECK ((((`question_type` = _utf8mb4'Sparta') and (`optionA` is null) and (`optionB` is null) and (`optionC` is null) and (`optionD` is null)) or (`question_type` = _utf8mb4'Gorgo')))
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Acropolis_Questions_System`
--

/*!40000 ALTER TABLE `Acropolis_Questions_System` DISABLE KEYS */;
INSERT INTO `Acropolis_Questions_System` VALUES (1,'Mathematics','Which country was the famous mathematician Fibonacci born?','Gorgo','United States','France','Spain','Italy','Italy','Fibonacci was born in the town of Pisa, where the world-renown Leaning Tower of Pisa was placed.  ','BEGINNER'),(2,'Mathematics','Which civillization had found the most commonly used numeral system?','Gorgo','Egypt','India','Mesopotamia','China','India','Ancient Indian people had invented the Arabic numeral system whose numbers were indicated from 0 to 9, which became the most commonly used symbols for writing numbers until present and from now on.','BEGINNER'),(11,'Mathematics','Which famous theorem illustrates the relationship between three sides of a right triangle?','Gorgo','Pythagorean theorem','Thales\' theorem','Heron\'s theorem','Euler\'s theorem','Pythagorean theorem','Pythagorean theorem proposes that a squared value of hypotenuse is equal to the sum of two squared values of two legs of a right triangle.','BEGINNER'),(12,'Mathematics','How many diagonal lines of a rectangle?','Sparta',NULL,NULL,NULL,NULL,'2','For all kinds of quadrilateral, there are two diagonal lines formed by two pairs of opposite edges.','BEGINNER'),(13,'Mathematics','Calculate the next number in this sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34,...','Sparta',NULL,NULL,NULL,NULL,'56','The given sequence is a Fibonacci sequence whose rule proposes that the sum of two previous number equal to the number next to them. ','BEGINNER'),(14,'Mathematics','Which mathematical table illustrates the multiplication between the numbers from 1 to 9 and is commonly used for elementary teaching?','Sparta',NULL,NULL,NULL,NULL,'Multiplication table',NULL,'BEGINNER'),(15,'Mathematics','The graph of function y = |x| bears the resemblance to which letter?','Gorgo','Letter A','Letter V','Letter U','Letter C','Letter V','As y = x is illustrated as a line crossing over the root of coordinate system, y = |x| whose values are always positive, so even x is negative, y = |x| always returns positive value.','EASY'),(16,'Mathematics','How many hours in a week?','Gorgo','168','144','192','240','168','24 hours per day. Therefore, a week has 24*7 = 168 hours.','EASY'),(17,'Mathematics','To identify a rectangle, we firstly need to identify how many points in two-dimensional coordinate system?? ','Gorgo','Four points','Three points','Two points','One point','Two points','As a rectangle has its own particular features such as two pairs of parallel and equal sides, four right angles, we only need to identify two points on Oxy coordinate system.','EASY'),(18,'Mathematics','Find the two-digit number which satisfies this given condition: \"If I delete the tens-digit of this number, the new number is 1/3 of it.\"','Sparta',NULL,NULL,NULL,NULL,'15','As we delete the tens-digit of 15 (the digit 1), we have number 5. And 5 is 1/3 of 15, so the answer is 15.','EASY'),(19,'Mathematics','How about seconds make up two hours?','Sparta',NULL,NULL,NULL,NULL,'7200','60 seconds per minute and 60 minutes per hour, therefore leading to the result that 3600 seconds per hour. As such, 2 hours make up 3600*2 = 7200 seconds.','EASY'),(20,'Mathematics','A car runs 50km/h from A to B which is 150km away. A bicycle runs 10km/h from C which is between A and B. As a car and a bicycle starts running at the same time and a car meets a bicycle after 30 minutes. How far is C away from A?','Sparta',NULL,NULL,NULL,NULL,'65km','As we denote that the distance from A to C is x km, then the distance from B to C is (150 - x) km. After 30 minutes, we have an equation 150 - x - 0.5*50 = x - 0.5*5, and the solution x = 65, which is the final answer ','EASY'),(21,'Physics','Which physicist implemented an experiment of free fall at Leaning Tower of Pisa? ','Gorgo','Isaac Newton','Nicolas Copernicus','Galileo Galilei','Thomas Young','Galileo Galilei',NULL,'BEGINNER'),(22,'Physics','How many planets in the Solar System?','Gorgo','9','8','10','7','8','Since 2009, the scientists have approved that there are 8 planets in the Solar System, and recognized the Pluto as a dwarf planet.','BEGINNER'),(23,'Physics','Which measurement is used to evaluate whether an object is moving fast or slowly in a specific time?','Gorgo','Velocity','Distance','Speed','Acceleration','Acceleration','Acceleration is either positive or zero or negative. It will be 0 if the object moves normally and consistently, positive when it moves fast and negative when it moves slowly.','BEGINNER'),(24,'Physics','Which physicist has this famous quote: \"Give me a place to stand and I shall move the Earth\"?','Sparta',NULL,NULL,NULL,NULL,'Archimedes','Archimedes has this famous quote as an expression for how powerful lever is, and also for how far human is able to do if they have a chance or a stand.','BEGINNER'),(25,'Physics','Which force holds the planets in a specific distance together, holds the planets towards the Sun, and holds the Moon towards the Earth?','Sparta',NULL,NULL,NULL,NULL,'Gravity','According to Newton\'s universal law of gravitation, every object with enormous mass owns a gravity to hold a distance towards the others.','BEGINNER'),(26,'Physics','Which electrical device is used to store energy in eletric field?','Sparta',NULL,NULL,NULL,NULL,'Capacitor','Capacitor has capacitance, which measures how much energy of electrical field is stored. ','BEGINNER'),(27,'Physics','Which law given is not a law of Physics?','Gorgo','Conservation of energy','Conservation of momentum','Conservation of eletrical charges','Conservation of mass','Conservation of mass','Conservation of mass is a basic law of Chemistry in which the total mass before and after a chemical reaction is always a constant.','EASY'),(28,'Physics','Which value given below is approximately correctly indicated for speed of light?','Gorgo','3*10^6 km/s','3*10^6 km/h','3*10^6 m/s','3*10^3 km/h','3*10^6 m/s','Speed of light is indicated approximately 3 million metres per second, which is the biggest value to c','EASY'),(29,'Physics','An object is dropped from altitude of 15m. Supposing that there is no drag of air during the fall, and gravitational acceleration is 9.8m/s^2, how long does it take when the object hits the ground? Find the option closest to the value of time.','Gorgo','1.5 seconds','2 seconds','1.75 seconds','1.8 seconds','1.75 seconds','As the free fall formula for distance: s = 1/2*g*t^2, we calculate that t = sqrt(2gs) and it approximately 1.75 seconds. ','EASY'),(30,'Physics','Which physical game is played as two teams conflict face-to-face by pulling ropes as strong as possible to win against the opponent team?','Sparta',NULL,NULL,NULL,NULL,'Tug of war','Tug of war is played as two team pull a rope to fall the opponent of each other.','EASY'),(31,'Physics','What is the first invention ever made by human in history?','Sparta',NULL,NULL,NULL,NULL,'Fire','Fire is a product of combustion from kinetic friction between two surfaces at high temperature,  ','EASY'),(32,'Physics','In idealized harmonic oscillation, which measurement is considered constant during oscillation of an object and evaluate the maximum energy of an oscillating object?','Sparta',NULL,NULL,NULL,NULL,'Amplitude','Amplitude is the maximum distance of an object to oscillate from equilibrium position. It also evaluates the potential energy of an object, which leads to kinetic energy afterwards.','EASY'),(33,'Chemistry','Which chemical element takes the biggest proportion in the Earth\'s crust?','Gorgo','Oxygen','Silicon','Iron','Carbon','Oxygen','Oxygen takes about a half of proportion in compounds that form Earth\'s crust.','BEGINNER'),(34,'Chemistry','Which elements make up a molecule of water?','Gorgo','Nitrogen and Oxygen','Hydrogen and Oxygen','Sulfur and Oxygen','Nitrogen and Hydrogen','Hydrogen and Oxygen','Water\'s chemical formula is H2O, where two atoms of hydrogen bond with an atom of oxygen.','BEGINNER'),(35,'Chemistry','In order to examine whether a chemical is acidic or basic, which following tool does not apply?','Gorgo','pH indicator','Litmus','Phenolphtalein','Salt','Salt','Salt itself is a group of chemical compounds which is either acidic or neutral or basic, so we cannot use salt to testify whether a chemical is acidic or basic.','BEGINNER'),(36,'Chemistry','What is the name of the most famous explosive which became the signature invention of world-renown chemist Alfred Nobel?','Sparta',NULL,NULL,NULL,NULL,'Dynamite','Dynamite is an explosive with nitroglycerin as the main component, and it was invented by Alfred Nobel for road and building construction.','BEGINNER'),(37,'Chemistry','Which metal is at liquid state in normal temperature?','Sparta',NULL,NULL,NULL,NULL,'Mercury','Mercury (Hg) is a high-toxic metallic element which appears knowingly in liquid state. It is used for mercury-in-glass thermometer, which is the most used thermometer in the world nowadays.','BEGINNER'),(38,'Chemistry','France\'s world-renown Eiffel Tower is made by which material?','Sparta',NULL,NULL,NULL,NULL,'Steel','Eiffel Tower in Paris is considered the highest steel-made refrastructure ever built, and it became one of the cultural symbol of France.','BEGINNER'),(39,'Chemistry','Which chemical compound is considered the pillar of Alchemy and the foundation of modern chemical industry?','Gorgo','Sodium hydroxide (NaOH)','Calcium carbonate (CaCO3)','Sulfuric acid (H2SO4)','Methane (CH4)','Sulfuric acid (H2SO4)',NULL,'EASY'),(40,'Chemistry','What is the approximate atomic mass of iron (Fe)?','Gorgo','56','31','27','54','56','Atomic mass of Iron in Dalton measurement is approximately 56.','EASY'),(41,'Chemistry','Which following expression is not an use of Calcium carbonate (CaCO3)?','Gorgo','Material for construction','Material for deacidification of crops','Material for making soaps','Material for making baking soda','Material for making baking soda','Baking soda is made by sodium bicarbonate NaHCO3, which is totally not related to CaCO3.','EASY'),(42,'Chemistry','Which scientist had discovered the radioactive metallic element Radium (Ra) and built a steady thesis of radioactivity?','Sparta',NULL,NULL,NULL,NULL,'Marie Curie','World-renown female scientist Marie Curie discovered Radium and Polonium in 1911, which resulted in her Nobel Prize of Chemistry.','EASY'),(43,'Chemistry','Sodium hydroxide and Javel water are products of Sodium chlorite (salt water) through which method?','Sparta',NULL,NULL,NULL,NULL,'Electrolysis','Sodium hydroxide is produced via membrane-having electrolysis, whereas sodium hypochlorite is produced via membraneless electrolysis.','EASY'),(44,'Chemistry','Which chemical compound is the main component of black explosive used to make gunpowder?','Sparta',NULL,NULL,NULL,NULL,'Potassium nitrate','Potassium nitrate (KNO3) is the main component of black explosive, useful at making gunpowder.','EASY');
/*!40000 ALTER TABLE `Acropolis_Questions_System` ENABLE KEYS */;

--
-- Table structure for table `Player`
--

DROP TABLE IF EXISTS `Player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Player` (
  `PlayerID` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` int NOT NULL,
  `place_of_living` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `hobby` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `points` int DEFAULT '0',
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'NOT NULL',
  `gameturn` int DEFAULT NULL,
  `stop_level` varchar(255) DEFAULT NULL,
  `question_number` int DEFAULT NULL,
  PRIMARY KEY (`PlayerID`),
  UNIQUE KEY `UK_Player_User` (`username`),
  CONSTRAINT `player_chk_1` CHECK ((`gender` in (_utf8mb4'Men',_utf8mb4'Women'))),
  CONSTRAINT `player_chk_2` CHECK ((`question_number` <= 25))
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Player`
--

/*!40000 ALTER TABLE `Player` DISABLE KEYS */;
INSERT INTO `Player` VALUES (29,'Hizawa Satozaki',17,'Kyoto, Japan','Chemical experiment',0,'Women',NULL,NULL,NULL),(32,'Koshikawa Shibunagi',17,'Hadano, Kanagawa, Japan','Communicating with birds',0,'Men',NULL,NULL,NULL),(38,'Watanabe Masami',17,'Odawara, Kanagawa, Japan','Making inventions and Makeup',0,'Women',NULL,NULL,NULL),(39,'Yukawa Manabu',38,'Sapporo, Hokkaido, Japan','Researching Physics and Science',0,'Men',NULL,NULL,NULL),(40,'Leonardo DiCaprio',50,'Beverly Hills, California','Swimming, Photographing',0,'Men',NULL,NULL,NULL),(41,'Michael Jackson',39,'Beverly Hills, California','Singing and traveling',0,'Men',NULL,NULL,NULL),(42,'Jonathan Wiles',20,'London, United Kingdom','Photographing',0,'Men',NULL,NULL,NULL),(43,'James Nguyen',17,'Ninh Hoa, Khanh Hoa','Photographing',0,'Men',NULL,NULL,NULL),(44,'Nguyen Manh Tuan',19,'Nha Trang, Khanh Hoa','Writing ',0,'Men',NULL,NULL,NULL),(45,'Dorothy McCallins',28,'New York City, United States','Visiting monuments',0,'Women',NULL,NULL,NULL);
/*!40000 ALTER TABLE `Player` ENABLE KEYS */;

--
-- Dumping routines for database 'Stairs_of_Acropolis'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-18 21:26:56
