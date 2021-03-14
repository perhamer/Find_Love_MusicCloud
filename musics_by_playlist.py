# 获取用户所有歌单的音乐
import json
import time
import requests
import sql
from Crypto.Cipher import AES
from chromedriver import get_driver
import random
import base64
from chromedriver import user_agent_list

headers = {
    'Cookie': '',#更换为自己的cookie,登录网易云音乐pc版,F12里获取
    'Referer': 'http://music.163.com/',
    'User-Agent': random.choice(user_agent_list)
}

encSecKey = '257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c'
first_key = '0CoJUm6Qyw8W8jud'
iv = '0102030405060708'


def get_encrypt_params(playlist_id,offset, limit, total):
    param = '{id:"'+str(playlist_id)+'", offset:"' + str(offset) + '", total:"' + total + '",limit:"' + str(
        limit) + '", csrf_token:""}'
    second_key = 16 * 'F'
    h_encText = AES_encrypt(param, first_key, iv)
    h_encText = AES_encrypt(str(h_encText, 'utf-8'), second_key, iv)
    return h_encText


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text += pad * chr(pad)
    encryptor = AES.new(key.encode('UTF-8'), AES.MODE_CBC, iv.encode('UTF-8'))
    encrypt_text = encryptor.encrypt(text.encode('UTF-8'))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def save_musics_by_playlist(playlist_id, driver):
    try:
        url = 'https://music.163.com/weapi/v6/playlist/detail?csrf_token='
        param = get_encrypt_params(playlist_id, 0, 100, 'true')
        data = {
            "params": param,
            "encSecKey": encSecKey
        }
        response = requests.post(url, headers=headers, data=data)
        json_dict = json.loads(response.content)
        tracks = json_dict['playlist']['trackIds']
        musics = []
        for track in tracks:
            musics.append(str(track['id']))
        sql.insert_playlist_music(playlist_id, musics)
        print('保存歌单成功：playlist_id:' + str(playlist_id)+',共'+str(len(musics))+'首歌曲')


    except Exception as e:
        print(e)
        driver.quit()
        return


def get_musics_by_user(user_id):
    driver = get_driver()
    playlist_id_list = sql.get_playlists(user_id)
    for playlist_id in playlist_id_list:
        save_musics_by_playlist(playlist_id['playlist_id'], driver)
    print('所有歌单保存完毕,user:' + str(user_id))


if __name__ == '__main__':
    start = time.time()
    get_musics_by_user(11111)
    cost = (time.time() - start)
    print('耗时：' + str(cost) + '秒')
