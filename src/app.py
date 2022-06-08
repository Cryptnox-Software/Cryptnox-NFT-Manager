import wx
from card_load_panel import CardLoadPanel
from logo_tabs_panel import LogoTabsPanel
from wallet_connect_panel import WalletConnectPanel

class NFT_CardManager_Frame(wx.Frame):

    def __init__(self, *args, **kw):
        super(NFT_CardManager_Frame,self).__init__(*args, **kw)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(LogoTabsPanel(self,-1),0,wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.Add(CardLoadPanel(self,-1),0,wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.Add(WalletConnectPanel(self,-1),0,wx.ALIGN_CENTER_HORIZONTAL)

        self.GetChildren()[2].Hide()
        self.SetSizerAndFit(main_sizer)
        self.Show(1)

    def CardLoadTabPressed(self,event):
        print('CardLoabTabbed')
        self.GetChildren()[2].Hide()
        self.GetChildren()[1].Show()
        self.Layout()

    def WalletConnectTabPressed(self,event):
        print('WalletConnectTabbed')
        self.GetChildren()[1].Hide()
        self.GetChildren()[2].Show()
        self.Layout()

class NFT_CardManager_App(wx.App):

    def __init__(self):
        super(NFT_CardManager_App, self).__init__()
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        print(wx.DisplaySize())
        self.frame = NFT_CardManager_Frame(None, -1, "NFT CARD MANAGER")
        frame_position = ((wx.DisplaySize()[0]-self.frame.GetSize()[0])/2,(wx.DisplaySize()[1]-self.frame.GetSize()[1])/2)
        self.frame.SetPosition(frame_position)
        print(self.frame.GetSize())
        self.MainLoop()


def main() -> None:
    app = NFT_CardManager_App()
    

if __name__ == '__main__':
    main()