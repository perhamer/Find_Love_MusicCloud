"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='cloudmusic',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# 获取用户所有歌单下的所有音乐
def get_musics_by_user(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT DISTINCT music_id FROM playlist_music p LEFT JOIN user_playlist u ON p.playlist_id = u.playlist_id WHERE u.user_id = %s and music_id > 5412259 ORDER BY music_id ASC"
        cursor.execute(sql, (user_id))
        return cursor.fetchall()


# 保存用户的playlists
def insert_user_playlist(user_id, playlist_id, playlist_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO user_playlist (`user_id`,`playlist_id`,playlist_name)  VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, playlist_id, playlist_name))
        connection.commit()


# 获取用户的playlists
def get_playlists(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT `playlist_id` FROM `user_playlist` WHERE user_id = %s"
        cursor.execute(sql, (user_id))
        return cursor.fetchall()


# 保存歌单的歌曲
def insert_playlist_music(playlist_id, musics):
    with connection.cursor() as cursor:
        sql = "INSERT INTO playlist_music (`playlist_id`,`music_id`)  VALUES (%s, %s)"
        for id in musics:
            cursor.execute(sql, (playlist_id, str(id)))
        connection.commit()


# 获取歌曲评论
def insert_comment(comment):
    with connection.cursor() as cursor:
        sql = "INSERT INTO comments (`music_id`, `user_id`,`content`, `reply_comment_id`, `reply_content`, `liked_count`, `comment_time`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            comment.music_id, comment.user_id, comment.content, comment.reply_id, comment.reply_content,
            comment.liked_count, comment.comment_time))
        connection.commit()


def dis_connect():
    connection.close()
