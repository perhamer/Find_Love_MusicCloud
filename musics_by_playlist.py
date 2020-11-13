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
    'Cookie': 'mail_psc_fingerprint=498d14b7a8d9a9a0b34d0563228a16c9; _ntes_nuid=cf6d08772a7d965a71ea32fc0253160e; WM_TID=xxfBNToE6rpAQEQUFRM5bbXAL2A4Uot4; nts_mail_user=cxiaohei3@163.com:-1:1; P_INFO=d1135034979@163.com|1557229799|0|cbg|00&99|CN&1557200062&xyq#hen&410100#10#0#0|&0|xyq|d1135034979@163.com; _ga=GA1.2.1833807352.1564928031; vinfo_n_f_l_n3=896edd08aa545002.1.0.1570693739370.0.1570693771539; _iuqxldmzr_=32; ntes_kaola_ad=1; _ntes_nnid=cf6d08772a7d965a71ea32fc0253160e,1586997354536; WM_NI=GYRTWpY%2F9SMBG%2BvFZLCUiMPJ0euzbLdpcVjUPtOn6bisNw9vTtuNbjGivT%2FP%2Fny2kk2dg5ee6MHSnp95Pf%2B0hCfxc9pexpcU0VdZrlkoV7wsy9RnE6I9fSr19lor3mcbQXk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea3bb5bad9cf9afbb68ba968bb7d14e868e8baaf14fb186bf93b779a99bfca2ed2af0fea7c3b92a85879eb5d67c9bf1f7b4d04a85f5baa7d948818ba7aed342f4bbbb9be148a8b0adb7e95f94ac818fb56aabad8298bc7e98acbbafe16285b7bab5ae5cedb2b7d3ea61f2bca9d6e86ff69388b4ed7cfbeba087aa3cac9daa99e233b4bbb891e25ff48aacbbf168a9b19ad8f679bbe79e8fc83e8be7aab4f13bfbb4a193b267a1be9fb9ea37e2a3; JSESSIONID-WYYY=WMnvntZ9W5QB%2BSfddzPI0hbcitnRA69NFN5o%2BFp02WdzR70DoBrIFhNeG637Ptyrmf7bGgf9IiwvsMTKZCuQ0ZlcJb3PpFtD%2BoX%2Bwk7hXM46r3eHSEBuEz%5C%2BsoMH%2B%2BuOblxgtsb7sCr6R9bVfhd21B4OqhwmIKg4x%5CxKF2ZDbBX4Ck0D%3A1587399839919',
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
