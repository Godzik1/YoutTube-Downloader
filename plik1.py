import pytube
from tkinter import filedialog
from tkinter import *


class YoutubeDownloader:
    def __init__(self , link):
        self.link = link
        self.yt = pytube.YouTube(str(self.link))

    def video_audio(self):
        x = self.yt.streams.filter(progressive=True)
        poss = []
        for i in x:
            try:
                poss.append([i.itag , i.mime_type , i.resolution , i.fps])
            except:
                poss.append([i.itag, i.mime_type, i.resolution])

        z = self.yt.streams.filter(type="audio")
        for i in z:
            try:
                poss.append([i.itag , i.mime_type , i.resolution , i.fps])
            except:
                poss.append([i.itag, i.mime_type, i.resolution])

        for i in range(len(poss)):
            temp = round(self.yt.streams.get_by_itag(poss[i][0]).filesize_mb,2)
            poss[i].append(str(temp) + 'MB')

        for i in range(len(poss)):
            if "video" in poss[i][1]:
                poss[i][3] = str(poss[i][3]) + ' fps'

        final_poss = []
        for i in range(len(poss)):
            temp = []
            for j in poss[i]:
                if j != None:
                    temp.append(j)
            final_poss.append(temp)

        return final_poss


    def set_path(self):
        root = Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory()
        return folder_selected

    def download(self , choice):

        destination = self.set_path()
        temp = self.video_audio()

        itag = temp[choice][0]

        dwnl = self.yt.streams.get_by_itag(itag)

        dwnl.download(r"{}".format(destination))

    def get_thumbnail_url(self):
        return self.yt.thumbnail_url

    def other_information(self):
        auth = self.yt.author
        tit = auth + " - " + self.yt.title + " | "

        sum = self.yt.length
        finally_length = str(sum // 60) + ":" + str(sum % 60)

        return tit + finally_length