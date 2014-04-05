-- +----------+---------------+------+-----+---------+----------------+
-- | Field    | Type          | Null | Key | Default | Extra          |
-- +----------+---------------+------+-----+---------+----------------+
-- | id       | int(11)       | NO   | PRI | NULL    | auto_increment |
-- | word     | varchar(100)  | NO   | UNI | NULL    |                |
-- | meaning  | varchar(5000) | YES  |     | NULL    |                |
-- | sentence | varchar(5000) | YES  |     | NULL    |                |
-- | x        | int(11)       | YES  |     | NULL    |                |
-- | y        | int(11)       | YES  |     | NULL    |                |
-- | z        | int(11)       | YES  |     | NULL    |                |
-- +----------+---------------+------+-----+---------+----------------+


CREATE TABLE `nodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(100) NOT NULL,
  `meaning` varchar(5000) DEFAULT NULL,
  `sentence` varchar(5000) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `z` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

CREATE TABLE `edges` (
  `source` int(11) NOT NULL,
  `dest` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ;