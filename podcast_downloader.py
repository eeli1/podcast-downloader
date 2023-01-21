import feedparser
import requests
import os
import sys

def downland(url,file_path ):
    if not os.exists(file_path):
        os.system("wget {} -O {}".format(url,file_path))
    
def get_audio(url, path, title):
    filename = title.replace(' ','_')+".mp3"
    filename = filename.replace("/","")
    file_path = os.path.join(path, filename)
    downland(url,file_path)
    
def get_audio_url(links):
    for e in links:
        if "audio" in e["type"]:
            return e["href"]
    raise Exception("no audio found")

def download_rss(url, base_path):
    feed = feedparser.parse(url)
    title = feed["feed"]["title"]
    path = os.path.join(base_path,title.replace(' ','_'))
    os.mkdir(path)

    downland(url,os.path.join(path,"rss"))

    image_url =  feed["feed"]["image"]["href"]
    image_name = title.replace(' ','_')+".jpg"
    image_path = os.path.join(path,image_name)
    downland(image_url,image_path)

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
        download_rss(url,base_path)

if __name__ == "__main__":
   main(sys.argv)
