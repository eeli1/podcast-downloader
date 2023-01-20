import feedparser
import requests
import os
import sys
    
def get_audio(url, path, title):
    filename = title.replace(' ','_')+".mp3"
    filename = filename.replace("/","")
    os.system("cd {} && wget {}".format(path,url))
    file_path = os.path.join(path, filename)
    os.rename(os.path.join(path,url.split("/")[-1]), file_path)

def download_rss(url, base_path):
    feed = feedparser.parse(url)
    title = feed["feed"]["title"]
    path = os.path.join(base_path,title.replace(' ','_'))
    os.mkdir(path)

    image_url =  feed["feed"]["image"]["href"]
    image_name = title.replace(' ','_')+".jpg"
    r = requests.get(image_url, allow_redirects=True)
    open(os.path.join(path,image_name), 'wb').write(r.content)

    for e in feed["entries"]:
        audio_url = e["links"][1]["href"]
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
        download_rss(url,base_path)

if __name__ == "__main__":
   main(sys.argv)
