DROP TABLE IF EXISTS `keyword_en`;
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

DROP TABLE IF EXISTS `article_en`;
CREATE TABLE `article_en` (
  `article_id` bigint(20) NOT NULL auto_increment,
  `content_type` varchar(20) NOT NULL default '',
  `origin_id` varchar(40) NOT NULL default '0',
  `provider_id` int(4) NOT NULL default '0',
  `isEnglish` char(1) NOT NULL default '0',
  `target_id` bigint(20) default NULL,
  `action_type` char(1) default NULL,
  `status` int(2) default NULL,
  `keyword_id` bigint(20) default NULL,
  PRIMARY KEY  (`article_id`),
  KEY `keyword_id` (`keyword_id`),
  KEY `status` (`status`),
  KEY `origin_id` (`origin_id`,`provider_id`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk AUTO_INCREMENT=1 ;
