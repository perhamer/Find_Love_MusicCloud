"""
获取用户的歌单
"""
import sql

from chromedriver import get_driver


def save_playlist(id,driver):
    try:
        driver.get('https://music.163.com/user/home?id=' +str(id))
        driver.switch_to.frame('g_iframe')
        playlists = driver.find_elements_by_class_name('m-cvrlst li .tit')

        for playlist in playlists:
            link = playlist.get_attribute('href')
            playlist_id = link[str(link).find('=') + 1:]
            playlist_name = playlist.text
            sql.insert_user_playlist(id, playlist_id, playlist_name)
            print('插入成功：id:' + str(id) + ',list_id:' + playlist_id + ',playlist_name:' + playlist_name)

    except Exception as e:
        print(e)
        print(e.__context__)
        print(e.__cause__)
    finally:
        driver.quit()
        return


if __name__ == '__main__':
    driver = get_driver()
    save_playlist(11111,driver)
