--Login Database Schema

CREATE TABLE `Login` (
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `email_UNIQUE` (`email`)
);

--password == 12345

INSERT INTO Login (
email, password) VALUES(
bennylim,
pbkdf2:sha256:260000$Lxi3sCxRpTn8XSAl$265f70573f0fa5900b97c34e59003090ff033b41f887f28d0b2b6a16e06dd5ad);

