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

ALTER TABLE cross_ref_link CHANGE src_isenglish src_isenglish enum('N','Y') DEFAULT 'N', CHANGE des_isenglish des_isenglish enum('N','Y') DEFAULT 'N';
