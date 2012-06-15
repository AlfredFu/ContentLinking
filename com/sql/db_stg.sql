DROP TABLE IF EXISTS `opr_load_status_en`;
CREATE TABLE `opr_load_status_en` (
  `opr_id` int(11) NOT NULL AUTO_INCREMENT,
  `content_type` varchar(20) NOT NULL DEFAULT '',
  `origin_id` varchar(40) NOT NULL DEFAULT '',
  `provider_id` int(4) NOT NULL DEFAULT '0',
  `is_english` char(1) NOT NULL DEFAULT '',
  `target_id` int(11) DEFAULT NULL,
  `action_type` char(1) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `dc_status_code` varchar(20) DEFAULT NULL,
  `dc_error_desc` text,
  `upd_time` datetime DEFAULT NULL,
  `infiledate` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`opr_id`),
  KEY `provider_id` (`provider_id`,`status`,`is_english`),
  KEY `target_id` (`target_id`),
  KEY `origin_id` (`origin_id`,`provider_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=gbk AUTO_INCREMENT=1 ;

#ALTER TABLE cross_ref_link CHANGE src_isenglish src_isenglish enum('N','Y') DEFAULT 'N', CHANGE des_isenglish des_isenglish enum('N','Y') DEFAULT 'N';
use newlaw;
CREATE TABLE IF NOT EXISTS `cross_ref_link_en` (
  `cross_ref_link_id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `src_article_id` int(8) unsigned NOT NULL DEFAULT '0',
  `keyword_id` int(8) unsigned NOT NULL DEFAULT '0',
  `des_article_id` int(8) unsigned NOT NULL DEFAULT '0',
  `des_item_id` smallint(4) NOT NULL,
  `des_attachment_id` smallint(6) NOT NULL,
  `src_content_type` enum('C','CO','CT','CTP','FL','HN','J','LB','LM','LOCP','LOEE','LOEP','LOFDI','LOTP','NL','PC','PNL','SUMMARY','T','T4','TR') NOT NULL,
  `src_origin_id` varchar(23) NOT NULL DEFAULT '0',
  `src_provider_id` enum('1','2','3','4','5','6') NOT NULL DEFAULT '1',
  `src_isenglish` enum('N','Y') DEFAULT 'N',
  `des_content_type` enum('T','T4') NOT NULL,
  `des_origin_id` varchar(23) NOT NULL DEFAULT '0',
  `des_provider_id` enum('1','2','3','4') NOT NULL DEFAULT '1',
  `des_isenglish` enum('N','Y') DEFAULT 'N',
  PRIMARY KEY (`cross_ref_link_id`),
  KEY `idx_article_id` (`src_article_id`),
  KEY `idx_oid_pid_src` (`src_origin_id`,`src_provider_id`),
  KEY `idx_oid_pid_des` (`des_origin_id`,`des_provider_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=gbk AUTO_INCREMENT=1 ;

