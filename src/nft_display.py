from threading import Thread
import wx
from pubsub import pub
import requests

class DownloadThread(Thread):
    def __init__(self,panel: wx.Panel, image_url: str):
        super(DownloadThread, self).__init__()
        self.panel = panel
        self.url: str = image_url
        print(self.url)
        self.panel.download_progress = 0
        self.start()

    def run(self):
        header = requests.head(self.url)
        self.file_size = int(int(header.headers["content-length"]) / 1024)
        wx.CallAfter(pub.sendMessage,"show_gauge",data=self.file_size)
        self.data = b""
        try:
            print(f'Starting download thread')
            req = requests.get(self.url, stream=True)
            total_size = 0
            for byte in req.iter_content(chunk_size=1024):
                if byte:
                    self.data += byte
                total_size += len(byte)
                if total_size/1024 <= self.file_size:
                    self.panel.download_progress = total_size/1024
                    self.panel.gauge.setValue(total_size/1024)
                    progress = ((total_size/1024)/self.file_size)*100
                    wx.CallAfter(pub.sendMessage, "update_gauge",data=progress)
            self.panel.gauge.setValue(0)
            wx.CallAfter(pub.sendMessage, "downloaded", data=self.data)
        except Exception as e:
            print(f'Exception in downloading: {e}')