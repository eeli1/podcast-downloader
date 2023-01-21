import feedparser
import os
import sys


def downland(url, path, filename):
    if not os.path.isfile(os.path.join(path, filename)):
        os.system("cd {} && wget {} -O {}".format(path, url, filename))


def get_audio(url, path, title):
    filename = title.replace(' ', '_')+".mp3"
    filename = filename.replace("/", "")
    downland(url, path, filename)


def get_audio_url(links):
    for e in links:
        if "audio" in e["type"]:
            return e["href"]
    raise Exception("no audio found")


def download_rss(url, base_path):
    feed = feedparser.parse(url)
    title = feed["feed"]["title"]
    title = title.replace(' ', '_')
    title = title.replace("'", '')
    path = os.path.join(base_path, title)
    if not os.path.exists(path):
        os.mkdir(path)

    downland(url, path, "rss")

    image_url = feed["feed"]["image"]["href"]
    image_name = title.replace(' ', '_')+".jpg"
    downland(image_url, path, image_name)

    for e in feed["entries"]:
        audio_url = get_audio_url(e["links"])
        audio_title = e["title"]
        get_audio(audio_url, path, audio_title)


def main(argv):
    if len(argv) != 3:
        print("error:")
        print("\tpython3 podcast_downloader.py <urls> <podcast path>")
        print("\n\t<urls> is a file where all your rss urls are")
        print("\n\t<podcast path> is the directory where all the data gets downloaded into")
        return
    base_path = argv[2]
    file1 = open(argv[1], 'r')
    lines = file1.readlines()
    for url in lines:
        download_rss(url, base_path)


if __name__ == "__main__":
    main(sys.argv)
