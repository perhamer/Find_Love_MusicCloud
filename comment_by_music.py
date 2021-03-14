
import json
import math
import random
import time
from datetime import datetime
import logging
import requests
import sys
import sql
from chromedriver import user_agent_list

headers = {
    'Cookie': '',#更换为自己的cookie,登录网易云音乐pc版,F12里获取
    'Referer': 'http://music.163.com/',
    'User-Agent': random.choice(user_agent_list)
}

class Comment(object):
    def __init__(self, music_id, user_id, content, reply_id, reply_content, liked_count, comment_time):
        self.comment_time = comment_time
        self.liked_count = liked_count
        self.reply_content = reply_content
        self.reply_id = reply_id
        self.music_id = music_id
        self.user_id = user_id
        self.content = content


def get_comment_count(music_id):
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(music_id)
    response = requests.post(url, headers=headers)
    json_dict = json.loads(response.content)
    try:
        total = json_dict['total']
    except Exception :
        print(json_dict["message"])
        sys.exit(1)
    return total


def get_comment_by_music_id_and_user_id(music_id, user_id):
    total = get_comment_count(music_id)
    size = 100
    totalPages = math.ceil(total / size)
    i = 0
    for page in range(0, totalPages):
        if totalPages > 20 and (10 < page < totalPages - 10):
            continue
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(music_id) + '?offset=' + str(
            page * size) + '&limit=' + str(page * size + size)
        response = requests.get(url, headers=headers)
        json_dict = json.loads(response.content)
        try:
            comments = json_dict['comments']
        except Exception:
            print(json_dict["message"])
            sys.exit(1)
        for comment in comments:
            is_reply = 1 if len(comment['beReplied']) > 0 else 0
            if comment['user']['userId'] == user_id or (is_reply == 1
                                                        and comment['beReplied'][0]['user']['userId'] == user_id):
                c = Comment(music_id,
                            comment['user']['userId'],
                            comment['content'],
                            comment['beReplied'][0]['beRepliedCommentId'] if is_reply == 1 else '',
                            comment['beReplied'][0]['content'] if is_reply == 1 else '',
                            comment['likedCount'],
                            datetime.fromtimestamp(comment['time'] / 1000))
                logging.info(comment['content'])
                sql.insert_comment(c)
        i += 1
        print('\r查询成功，歌曲：' + str(music_id) + ',共' + str(total) + '条评论，进度：' + str(i) + '/' + str(
            totalPages if totalPages < 21 else 21),
              end='')
    print(str(music_id) + ",歌曲查找完毕")


def get_comment_by_user_musics(user_id):
    music_list = sql.get_musics_by_user(user_id)
    music_index = 0
    count = len(music_list)
    logging.info('获取成功，共' + str(count) + '首歌曲')
    for music in music_list:
        get_comment_by_music_id_and_user_id(music['music_id'], user_id)
        music_index += 1
        print('\r歌曲:' + str(music['music_id']) + '，查询完毕。进度：' + str(music_index) + '/' + str(count), end='')
        print()


if __name__ == "__main__":
    logging.basicConfig(filename="out.log", level=logging.INFO)
    start = time.time()
    get_comment_by_user_musics(111111)
    cost = (time.time() - start)
    print('耗时：' + str(cost) + '秒')
