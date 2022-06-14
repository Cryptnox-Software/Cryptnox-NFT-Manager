import wx
from card_check import CardCheckThread
from pubsub import pub

class ButtonsPanel(wx.Panel):

    def __init__(self,parent,id):
        super(ButtonsPanel,self).__init__(parent,id)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        font = wx.Font(11, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)
        self.check_card_run = True
        self.check_card = True

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.AddSpacer(10)

        #Reset card
        self.reset_btn = wx.Button(self,11,size=(100,40))
        self.reset_btn.SetFont(font)
        self.reset_btn.SetLabel('Card reset')

        self.reset_btn.Bind(wx.EVT_BUTTON,self.GetParent().card_load_panel.reset_card)

        main_sizer.Add(self.reset_btn,0,wx.LEFT,border=60)

        #Card info
        self.info_btn = wx.Button(self,12,size=(100,40))
        self.info_btn.SetFont(font)
        self.info_btn.SetLabel('Card Info')

        self.info_btn.Bind(wx.EVT_BUTTON,self.GetParent().card_load_panel.info_card)

        main_sizer.Add(self.info_btn,0,wx.LEFT | wx.RIGHT,border=20)

        #Execute load
        self.execute_btn = wx.Button(self,13,size=(150,40))
        self.execute_btn.SetFont(font)
        self.execute_btn.SetLabel('Execute load')

        self.execute_btn.Bind(wx.EVT_BUTTON,self.GetParent().card_load_panel.execute_load)

        main_sizer.Add(self.execute_btn,0,wx.LEFT,border=130)

        self.status_label = wx.StaticText(self,label='')

        main_sizer.AddSpacer(200)
        main_sizer.Add(self.status_label,0,wx.TOP,border=10)

        # CardCheckThread(self,-1)
        pub.subscribe(self.update_status, "update_status")
        pub.subscribe(self.pause_check_card,"pause_check_card")
        pub.subscribe(self.start_check_card,"start_check_card")

        self.SetSizerAndFit(main_sizer)

    def update_status(self,data):
        self.status_label.SetLabel(data)

    def pause_check_card(self):
        print('Pausing check card')
        self.check_card = False

    def start_check_card(self):
        print('Starting check card')
        self.check_card = True