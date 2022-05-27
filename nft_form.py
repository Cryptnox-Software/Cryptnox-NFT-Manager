import wx
from card_load_panel import CardLoadPanel


class NFT_Form_App(wx.App):

    def __init__(self):
        super(NFT_Form_App, self).__init__()
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.frame = wx.Frame(None, -1, "NFT CARD MANAGER",pos=((wx.DisplaySize()[0]/2)-600,(wx.DisplaySize()[1]/2)-525),size=(1200,1050))
        self.panel = CardLoadPanel(self.frame, -1)
        self.frame.Show(1)
        self.MainLoop()

def main() -> None:
    app = NFT_Form_App()
    

if __name__ == '__main__':
    main()