# Find_Love_MusicCloud
这是一个然并卵的项目。
可以查找Ta在网易云音乐评论，通过用户收藏和创建的歌单下所有歌曲的评论中查找到TA的评论。可以尽情满足我们的窥探欲望，从而使我们心有戚戚，立即升仙。
使用本源码造成的任何感情伤害概不负责。

This project is useless.
you can find his/her commones on MusicCloud By his/her playlists and its songs。So you are a pussy。
This Source is not to harm ,but make the world a better place. 

示例：


![image](https://user-images.githubusercontent.com/37055923/109450531-1915d680-7a86-11eb-8ef7-ec5c0a500789.png)


# musicCloud获取用户评论

#####原理：获取指定用户新建、收藏的所有歌单，获取其中所有歌曲，查询每首歌曲下的评论是否有目标用户的评论
	

# 执行顺序
#####1、下载chromeDriver.exe
	    https://sites.google.com/a/chromium.org/chromedriver/downloads
	    需要与自己Chrome浏览器版本匹配
#####2、将chromedriver.exe放到python安装目录下
#####3、执行sql init 初始化数据库
#####4、PC端打开目标网易云主页如:
        https://music.163.com/#/user/home?id=123123123
        123123123就是目标的id
#####5、执行playlist_by_user.py 输入用户ID查找用户创建的、收藏的歌单
    
#####6、执行musics_by_playlist.py 获取上一步获取到的歌单下的所有歌曲
    
#####7、执行comment_by_music.py 获取上一步获取到的歌曲下的所有评论，命中则存库
    
    
# sql init:


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `music_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reply_comment_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '回复的评论id',
  `reply_content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `liked_count` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `comment_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
-- Table structure for playlist_music
-- ----------------------------
DROP TABLE IF EXISTS `playlist_music`;
CREATE TABLE `playlist_music`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `playlist_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `music_id` bigint(255) NOT NULL,
  PRIMARY KEY (`id`, `playlist_id`, `music_id`) USING BTREE,
  INDEX `playlist_id`(`playlist_id`, `music_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1949 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;


-- ----------------------------
-- Table structure for user_playlist
-- ----------------------------
DROP TABLE IF EXISTS `user_playlist`;
CREATE TABLE `user_playlist`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `playlist_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `playlist_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `user_id`, `playlist_id`) USING BTREE,
  INDEX `user_id`(`user_id`, `playlist_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 62 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
