import wx
from card_load_panel import CardLoadPanel
from logo_tabs_panel import LogoTabsPanel
from card_admin_panel import CardAdminPanel
from buttons_panel import ButtonsPanel
from wallet_connect_panel import WalletConnectPanel
from pubsub import pub

class NFT_CardManager_Frame(wx.Frame):

    def __init__(self, *args, **kw):
        super(NFT_CardManager_Frame,self).__init__(*args, **kw)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.card_load_panel = CardLoadPanel(self,-1)

        main_sizer.Add(LogoTabsPanel(self,-1),0,wx.EXPAND)
        main_sizer.Add(self.card_load_panel,0,wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(10)
        main_sizer.Add(ButtonsPanel(self,-1),0,wx.EXPAND)
        main_sizer.Add(WalletConnectPanel(self,-1),0,wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(10)
        main_sizer.Add(CardAdminPanel(self,-1),0,wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(10)

        self.Bind(wx.EVT_CLOSE,self.on_close)
        self.GetChildren()[3].Hide()
        self.GetChildren()[4].Hide()
        self.SetSizerAndFit(main_sizer)
        self.Show(1)

    def CardLoadTabPressed(self,event):
        self.GetChildren()[4].Hide()
        self.GetChildren()[2].Show()
        self.GetChildren()[3].Hide()
        self.GetChildren()[0].Show()
        self.Layout()

    def WalletConnectTabPressed(self,event):
        self.GetChildren()[4].Hide()
        self.GetChildren()[2].Hide()
        self.GetChildren()[3].Show()
        self.GetChildren()[0].Hide()
        self.Layout()

    def CardAdminTabPressed(self,event):
        print('CardAdminTabbed')
        self.GetChildren()[4].Show()
        self.GetChildren()[2].Hide()
        self.GetChildren()[3].Hide()
        self.GetChildren()[0].Hide()
        self.Layout()

    def on_close(self,event):
        print('Close')
        self.GetChildren()[2].check_card_run = False
        pub.sendMessage("pause_check_card")
        wx.CallLater(500,self.Destroy)

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