from numpy import broadcast_arrays
import wx
from pathlib import Path


class LogoTabsPanel(wx.Panel):

    def __init__(self,parent,id):
        super(LogoTabsPanel,self).__init__(parent,id)        
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        font = wx.Font(11, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        top_sizer = wx.BoxSizer(wx.VERTICAL)

        #Cryptnox logo on top
        path = Path(__file__).parent.joinpath("cryptnox_transparent.png").absolute()
        img = wx.Image(str(path),wx.BITMAP_TYPE_PNG)
        img_size = (250,250)
        img = img.Scale(int(img_size[0]),int(img_size[1]),wx.IMAGE_QUALITY_HIGH)
        img = img.GetSubImage(wx.Rect((225,200)))
        img = img.ConvertToBitmap()
        image = wx.StaticBitmap(self, wx.ID_ANY, img, (0,0))

        top_sizer.Add(image,0,wx.CENTER)

        self.CardLoadTab = wx.Button(self,21,label='Initialize NFT card',size=(150,30))
        self.CardLoadTab.SetFont(font)
        self.CardLoadTab.Bind(wx.EVT_BUTTON,self.GetParent().CardLoadTabPressed)
        self.WalletConnectTab = wx.Button(self,22,label='Wallet Connect',size=(150,30))
        self.WalletConnectTab.SetFont(font)
        self.WalletConnectTab.Bind(wx.EVT_BUTTON,self.GetParent().WalletConnectTabPressed)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(self.CardLoadTab,1,wx.ALL,border=10)
        row_sizer.Add(self.WalletConnectTab,1,wx.ALL,border=10)
        
        top_sizer.Add(row_sizer,0,wx.EXPAND)
        top_sizer.AddSpacer(25)
        
        self.SetSizerAndFit(top_sizer)
