/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : cov

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 04/04/2020 18:01:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
-- ----------------------------
-- Table structure for dayinfo
-- ----------------------------
DROP TABLE IF EXISTS `dayinfo`;
CREATE TABLE `dayinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day_time` datetime(0) NULL DEFAULT NULL,
  `city` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `now_confirm` int(11) NULL DEFAULT NULL,
  `confirm_add` int(11) NULL DEFAULT NULL,
  `heal` int(11) NULL DEFAULT NULL,
  `dead` int(11) NULL DEFAULT NULL,
  `zero` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for details
-- ----------------------------
DROP TABLE IF EXISTS `details`;
CREATE TABLE `details`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `province` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `city` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `confirm` int(11) NULL DEFAULT NULL,
  `confirm_add` int(11) NULL DEFAULT NULL,
  `heal` int(11) NULL DEFAULT NULL,
  `dead` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 431 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for history
-- ----------------------------
DROP TABLE IF EXISTS `history`;
CREATE TABLE `history`  (
  `ds` datetime(5) NOT NULL COMMENT '日期',
  `confirm` int(11) NULL DEFAULT NULL COMMENT '累积确诊',
  `confirm_add` int(11) NULL DEFAULT NULL,
  `nowConfirm` int(11) NULL DEFAULT NULL COMMENT '现存确诊',
  `suspect` int(11) NULL DEFAULT NULL,
  `suspect_add` int(11) NULL DEFAULT NULL,
  `heal` int(11) NULL DEFAULT NULL,
  `heal_add` int(11) NULL DEFAULT NULL,
  `dead` int(11) NULL DEFAULT NULL,
  `dead_add` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`ds`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for hotsearch
-- ----------------------------
DROP TABLE IF EXISTS `hotsearch`;
CREATE TABLE `hotsearch`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt` datetime(0) NOT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `dt`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

