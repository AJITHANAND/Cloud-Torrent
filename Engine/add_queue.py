import os
import qbittorrentapi
import json

link = "magnet:?xt=urn:btih:e3c00a07ef1fc244f8fcfadc71455a54a02bfbfd&dn=www.TamilBlasters.autos%20-%20Padavettu%20(2022)%20%5bMalayalam%20-%20HQ%20HDRip%20-%20x264%20-%20AAC%20-%20750MB%20-%20ESub%5d.mkv&tr=udp%3a%2f%2fdownload.nerocloud.me%3a6969%2fannounce&tr=udp%3a%2f%2fcutscloud.duckdns.org%3a6969%2fannounce&tr=udp%3a%2f%2fconcen.org%3a6969%2fannounce&tr=udp%3a%2f%2fchouchou.top%3a8080%2fannounce&tr=udp%3a%2f%2fcarr.codes%3a6969%2fannounce&tr=udp%3a%2f%2fbuddyfly.top%3a6969%2fannounce&tr=udp%3a%2f%2fbt.ktrackers.com%3a6666%2fannounce&tr=udp%3a%2f%2fblack-bird.ynh.fr%3a6969%2fannounce&tr=udp%3a%2f%2fben.kerbertools.xyz%3a6969%2fannounce&tr=udp%3a%2f%2fastrr.ru%3a6969%2fannounce&tr=udp%3a%2f%2fadmin.52ywp.com%3a6969%2fannounce&tr=udp%3a%2f%2faarsen.me%3a6969%2fannounce"


def last_update(arr: list):
    pass


def delete_torrrent(torrent, hash: str):
    torrent.delete(torrent_hashes=hash)
    return True


def get_info_hash(link: str):
    return link[20:60]


def add_to_queue(torrent: qbittorrentapi.torrents, magnet: str):
    locaiton = '/home/dh12/PycharmProjects/Cloud_Torrent/downloads'
    hash = get_info_hash(magnet)
    torrent.add(magnet, use_download_path=locaiton)
    return hash


# def status(client, hash):
#     return client.torrents_info(torrent_hashes=hash)
def get_status(torrent, hash):
    print(hash)
    data = torrent.info.all(torrent_hashes=hash)
    return data[0]


client = qbittorrentapi.Client(
    host='localhost',
    port=8080,
    username=os.environ.get("torrent_user"),
    password=os.environ.get("torrent_pass")

)


def get_client():
    try:
        client.auth_log_in()
        torrent = client.torrents
        return torrent
    except qbittorrentapi.exceptions.APIConnectionError as e:
        print(e)
        return None


def main():
    client.auth_log_in()
    torrent = client.torrents
    # val = torrent.delete(torrent_hashes="e3c00a07ef1fc244f8fcfadc71455a54a02bfbfd")
    # print(val)
    # print(client.torrents_info(torrent_hashes="98cd5d90252265f1c59ab47330ff4c39f48ccc78"))
    # add_to_queue(torrent, link)
    # info = add_to_queue(torrent, link)
    # torrent.add()
    # print(info)
    # item = torrent.info.all(torrent_hashes="e3c00a07ef1fc244f8fcfadc71455a54a02bfbfd")
    # print(item)
    # print(item[0])
    # print(json.dumps(*item, indent=4))
    # print(status(client,"e0d9af6671db5bc4fc77ab5462c50e2f3545dad9"))
    # status(client,None)
if __name__ == "__main__":
    main()
