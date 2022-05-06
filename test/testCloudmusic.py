# author: HRH

# date: 2022/2/17

# PyCharm
import cloudmusic

if __name__ == '__main__':
    playlist = cloudmusic.getPlaylist(119713936)
    # for music in playlist:
    #     try:
    #         music.download(level="lossless")
    #     except:
    #         continue
    print(playlist.name)