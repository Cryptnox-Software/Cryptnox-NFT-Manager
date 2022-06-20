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
        img_size = (200,200)
        img = img.Scale(int(img_size[0]),int(img_size[1]),wx.IMAGE_QUALITY_HIGH)
        img = img.GetSubImage(wx.Rect(pos=(20,43),size=(160,110)))
        img = img.ConvertToBitmap()
        image = wx.StaticBitmap(self, wx.ID_ANY, img, (0,0))

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(image,1)

        top_sizer.Add(row_sizer,0,wx.EXPAND)

        self.CardLoadTab = wx.Button(self,21,label='Initialize NFT card',size=(150,25))
        self.CardLoadTab.SetFont(font)
        self.CardLoadTab.SetForegroundColour('white')
        self.CardLoadTab.SetBackgroundColour('black')
        self.CardLoadTab.Bind(wx.EVT_ENTER_WINDOW,self.card_load_on_mouse_over)
        self.CardLoadTab.Bind(wx.EVT_LEAVE_WINDOW,self.card_load_on_mouse_leave)
        self.CardLoadTab.Bind(wx.EVT_BUTTON,self.card_load_tabbed)

        self.WalletConnectTab = wx.Button(self,22,label='Wallet Connect',size=(150,25))
        self.WalletConnectTab.SetFont(font)
        self.WalletConnectTab.SetForegroundColour('white')
        self.WalletConnectTab.SetBackgroundColour('black')
        self.WalletConnectTab.Bind(wx.EVT_ENTER_WINDOW,self.wallet_connect_on_mouse_over)
        self.WalletConnectTab.Bind(wx.EVT_LEAVE_WINDOW,self.wallet_connect_on_mouse_leave)
        self.WalletConnectTab.Bind(wx.EVT_BUTTON,self.wallet_connect_tabbed)
        
        self.CardAdminTab = wx.Button(self,23,label='Card Administration',size=(150,25))
        self.CardAdminTab.SetFont(font)
        self.CardAdminTab.SetForegroundColour('white')
        self.CardAdminTab.SetBackgroundColour('black')
        self.CardAdminTab.Bind(wx.EVT_ENTER_WINDOW,self.card_admin_on_mouse_over)
        self.CardAdminTab.Bind(wx.EVT_LEAVE_WINDOW,self.card_admin_on_mouse_leave)
        self.CardAdminTab.Bind(wx.EVT_BUTTON,self.card_admin_tabbed)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(self.CardLoadTab,0,wx.ALL,border=10)
        row_sizer.Add(self.WalletConnectTab,0,wx.ALL,border=10)
        row_sizer.Add(self.CardAdminTab,0,wx.ALL,border=10)
        
        top_sizer.Add(row_sizer,0,wx.ALIGN_CENTER_HORIZONTAL)
        
        self.SetSizerAndFit(top_sizer)

    def card_load_tabbed(self,event):
        self.CardLoadTab.SetBackgroundColour(wx.Colour(75,75,75,255))
        self.WalletConnectTab.SetBackgroundColour('black')
        self.CardAdminTab.SetBackgroundColour('black')
        self.GetParent().CardLoadTabPressed(event)

    def wallet_connect_tabbed(self,event):
        self.WalletConnectTab.SetBackgroundColour(wx.Colour(75,75,75,255))
        self.CardLoadTab.SetBackgroundColour('black')
        self.CardAdminTab.SetBackgroundColour('black')
        self.GetParent().WalletConnectTabPressed(event)

    def card_admin_tabbed(self,event):
        self.CardAdminTab.SetBackgroundColour(wx.Colour(75,75,75,255))
        self.CardLoadTab.SetBackgroundColour('black')
        self.WalletConnectTab.SetBackgroundColour('black')
        self.GetParent().CardAdminTabPressed(event)

    def card_load_on_mouse_over(self,event):
        self.CardLoadTab.SetForegroundColour('black')

    def card_load_on_mouse_leave(self,event):
        self.CardLoadTab.SetForegroundColour('white')

    def wallet_connect_on_mouse_over(self,event):
        self.WalletConnectTab.SetForegroundColour('black')

    def wallet_connect_on_mouse_leave(self,event):
        self.WalletConnectTab.SetForegroundColour('white')

    def card_admin_on_mouse_over(self,event):
        self.CardAdminTab.SetForegroundColour('black')

    def card_admin_on_mouse_leave(self,event):
        self.CardAdminTab.SetForegroundColour('white')