import os
import qbittorrentapi
import json

link = "https://releases.ubuntu.com/20.04/ubuntu-20.04.5-desktop-amd64.iso.torrent"


def add_to_queue(torrent: qbittorrentapi.torrents, magnet: str):
    torrent.add(magnet)


def status(client, hash):
    data = client.torrents_info(torrent_hashes=hash)
    print(json.dumps(*data, indent=4))


client = qbittorrentapi.Client(
    host='localhost',
    port=8080,
    username=os.environ.get("torrent_user"),
    password=os.environ.get("torrent_pass")
)


def main():
    client.auth_log_in()
    torrent = client.torrents
    # print(client.torrents_info(torrent_hashes="98cd5d90252265f1c59ab47330ff4c39f48ccc78"))
    # add_to_queue(torrent, link)
    torrent.add("https://releases.ubuntu.com/20.04/ubuntu-20.04.5-desktop-amd64.iso.torrent",
                infohash_v2="va0qtm5kyiia95m9386qqbhgbomfammtiz64vysl")
    item = torrent.info.all(infohash_v2="va0qtm5kyiia95m9386qqbhgbomfammtiz64vysl")
    print(json.dumps(*item, indent=4))
    # print(status(client,"e0d9af6671db5bc4fc77ab5462c50e2f3545dad9"))
    # status(client,None)


if __name__ == "__main__":
    main()
