DROP DATABASE IF EXISTS doubanBook;
CREATE DATABASE doubanBook;
USE doubanBook;


DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键；自增长ID',
  `category` varchar(255) DEFAULT NULL COMMENT '分类',
  `tag` varchar(255) DEFAULT NULL COMMENT '标签',
  `url` varchar(255) DEFAULT NULL COMMENT '每个标签的连接',
  `num` varchar(255) DEFAULT NULL COMMENT '书籍数量',
  PRIMARY KEY (`id`),
  UNIQUE KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 COMMENT='书籍分类';


DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键；自增长ID',
  `tag` varchar(255) DEFAULT NULL COMMENT '所属标签',
  `title` varchar(255) DEFAULT NULL COMMENT '书名',
  `book_id` varchar(100) DEFAULT NULL COMMENT '书籍ID',
  `book_url` varchar(255) DEFAULT NULL COMMENT '书籍链接',
  `author` varchar(255) DEFAULT NULL COMMENT '作者',
  `author_url` varchar(255) DEFAULT NULL COMMENT '作者url',
  `publish_company` varchar(255) DEFAULT NULL COMMENT '出版社',
  `subtitle` varchar(255) DEFAULT NULL COMMENT '副标题',
  `original_name` varchar(255) DEFAULT NULL COMMENT '原作名',
  `translator` varchar(255) DEFAULT NULL COMMENT '译者',
  `translator_url` varchar(255) DEFAULT NULL COMMENT '译者url',
  `publish_year` varchar(255) DEFAULT NULL COMMENT '出版年',
  `pages` varchar(255) DEFAULT NULL COMMENT '页数',
  `price` varchar(100) DEFAULT NULL COMMENT '定价',
  `binding` varchar(255) DEFAULT NULL COMMENT '装帧',
  `series` varchar(255) DEFAULT NULL COMMENT '丛书',
  `series_url` varchar(255) DEFAULT NULL COMMENT '丛书url',
  `ISBN` varchar(255) DEFAULT NULL COMMENT '书号',
  `comment_score` varchar(255) DEFAULT NULL COMMENT '评分',
  `comment_quantity` varchar(255) DEFAULT NULL COMMENT '评论数量',
  `summary` text DEFAULT NULL COMMENT '简介',
  PRIMARY KEY (`id`),
  UNIQUE KEY (`tag`, `book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 COMMENT='书籍信息';

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键；自增长ID',
  `title` varchar(255) DEFAULT NULL COMMENT '书名',
  `book_id` varchar(255) DEFAULT NULL COMMENT '书籍ID',
  `comment_score` varchar(255) DEFAULT NULL COMMENT '评分',
  `comment_quantity` varchar(255) DEFAULT NULL COMMENT '评论数量',
  `recommend_strongly` varchar(255) DEFAULT NULL COMMENT '力荐',
  `recommend` varchar(255) DEFAULT NULL COMMENT '推荐',
  `just_so_so` varchar(255) DEFAULT NULL COMMENT '还行',
  `a_little_bad` varchar(255) DEFAULT NULL COMMENT '有点差',
  `so_bad` varchar(255) DEFAULT NULL COMMENT '很差',
  `already_read` varchar(255) DEFAULT NULL COMMENT '已读',
  `reading_now` varchar(255) DEFAULT NULL COMMENT '在读',
  `wish_read` varchar(255) DEFAULT NULL COMMENT '想读',
  PRIMARY KEY (`id`),
  UNIQUE KEY (`tag`, `book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 COMMENT='评论信息';
