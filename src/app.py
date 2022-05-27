import wx
from card_load_panel import CardLoadPanel
from logo_tabs_panel import LogoTabsPanel

class NFT_CardManager_App(wx.App):

    def __init__(self):
        super(NFT_CardManager_App, self).__init__()
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.frame = wx.Frame(None, 1, "NFT CARD MANAGER",pos=((wx.DisplaySize()[0]/2)-600,(wx.DisplaySize()[1]/2)-525),size=(1200,1050))
        # self.frame.SetBackgroundColour('black')
        self.frame.SetForegroundColour('white')
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.logo_tabs_panel = LogoTabsPanel(self.frame,1)
        top_sizer.Add(self.logo_tabs_panel,1,wx.EXPAND)

        main_sizer.Add(top_sizer,1,wx.CENTER)

        panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel_sizer.Add(CardLoadPanel(self.frame,2),1,wx.EXPAND)
     
        main_sizer.Add(panel_sizer,2,wx.CENTER)  

        self.frame.SetSizerAndFit(main_sizer)
        self.frame.Show(1)
        self.MainLoop()

def main() -> None:
    app = NFT_CardManager_App()
    

if __name__ == '__main__':
    main()