import wx
from pathlib import Path


class LogoTabsPanel(wx.Panel):

    def __init__(self,parent,id):
        super(LogoTabsPanel,self).__init__(parent,id)        
        self.SetBackgroundColour('blue')
        self.SetForegroundColour('white')
        font = wx.Font(11, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        top_sizer = wx.BoxSizer(wx.VERTICAL)

        #Cryptnox logo on top
        path = Path(__file__).parent.joinpath("cryptnox_transparent.png").absolute()
        img = wx.Image(str(path),wx.BITMAP_TYPE_PNG)
        img_size = (250,250)
        img = img.Scale(int(img_size[0]),int(img_size[1]),wx.IMAGE_QUALITY_HIGH)
        img = img.ConvertToBitmap()
        image = wx.StaticBitmap(self, wx.ID_ANY, img, (0,0))

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(image,1,wx.CENTER)

        top_sizer.Add(row_sizer,1,wx.CENTER)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CardLoadTab = wx.Button(self,1,label='Initialize NFT card',size=(150,50))
        self.CardLoadTab.SetFont(font)
        row_sizer.Add(self.CardLoadTab,2,wx.ALL,border=10)
        # self.WalletConnect = wx.Button(self,2,label='WalletConnect',size=(150,50))
        # self.WalletConnect.SetFont(font)
        # row_sizer.Add(self.WalletConnect,3,wx.TOP | wx.BOTTOM,border=10)

        top_sizer.Add(row_sizer,2,wx.CENTER)
        

        self.SetSizerAndFit(top_sizer)
        self.Layout()
