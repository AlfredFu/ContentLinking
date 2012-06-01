CREATE TABLE IF NOT EXISTS `keyword_en` (
  `keyword_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `keyword` text,
  `status` varchar(3) DEFAULT NULL,
  `type` char(1) DEFAULT NULL,
  `full_title_keyword_id` bigint(20) DEFAULT NULL,
  `removed_record_id` bigint(20) DEFAULT NULL,
  `isenabling` char(1) DEFAULT NULL,
  PRIMARY KEY (`keyword_id`),
  KEY `full_title_keyword_id_index` (`full_title_keyword_id`),
  KEY `keyword_index` (`keyword`(60))
) ENGINE=InnoDB  DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC AUTO_INCREMENT=1;
