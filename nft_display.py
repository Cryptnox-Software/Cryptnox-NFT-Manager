from threading import Thread
import wx
from wx.lib.pubsub import pub
import requests

class DownloadThread(Thread):
    def __init__(self,panel: wx.Panel, image_url: str):
        super(DownloadThread, self).__init__()
        self.panel = panel
        self.url: str = image_url
        header = requests.head(self.url)
        self.file_size = int(int(header.headers["content-length"]) / 1024)

        self.data = b""
        self.start()

    def run(self):
        try:
            print(f'Starting download thread')
            req = requests.get(self.url, stream=True)
            total_size = 0
            for byte in req.iter_content(chunk_size=1024):
                if byte:
                    self.data += byte
                total_size += len(byte)
                if total_size/1024 < self.file_size:
                    download_progress = total_size/1024
                    total_file_size = self.file_size/1024
                    # print(f'Downloading: {(download_progress/total_file_size)*100}')
            wx.CallAfter(pub.sendMessage, "downloaded", data=self.data)
        except Exception as e:
            print(f'Exception in downloading: {e}')