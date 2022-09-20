import tempfile
import wx
from utils import get_cryptnox_card,ask,checksum_address
import cryptnoxpy
import json
import gzip
from pathlib import Path
import time
import config

class SettingsPanel(wx.Panel):
    
    gateways = [
        "https://cloudflare-ipfs.com/ipfs",
        "https://opengateway.mypinata.cloud/ipfs"
    ]

    def __init__(self, *args, **kw):
        super(SettingsPanel,self).__init__(*args, **kw)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        font = wx.Font(11, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        settings_sizer = wx.BoxSizer(wx.VERTICAL)
        

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Current IPFS gateway:',size=(100,16))
        text.SetFont(font)
        row_sizer.Add(text,0,wx.ALL,border=5)
        self.gateway_text = wx.StaticText(self,label=config.GATEWAY_URL,size=(200,16))
        self.gateway_text.SetFont(font)
        row_sizer.Add(self.gateway_text,0,wx.ALL,border=5)

        settings_sizer.Add(row_sizer,0,wx.ALIGN_LEFT)
        settings_sizer.AddSpacer(20)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='IPFS gateway',size=(100,16))
        text.SetFont(font)
        row_sizer.Add(text,0,wx.ALL,border=5)
        self.gateway_choice = wx.Choice(self,choices=[x for x in self.gateways])
        self.gateway_choice.Bind(wx.EVT_CHOICE,self.gateway_chosen)
        row_sizer.Add(self.gateway_choice,0,wx.ALL,border=5)

        settings_sizer.Add(row_sizer,0,wx.ALIGN_LEFT)
        settings_sizer.AddSpacer(20)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label="Manual gateway",size=(100,16))
        text.SetFont(font)
        row_sizer.Add(text,0,wx.ALL,border=5)
        self.gateway_field = wx.TextCtrl(self,size=(158,23))    
        self.set_gateway_button = wx.Button(self,-1,size=(75,23))
        self.set_gateway_button.SetLabel('Set')
        self.set_gateway_button.Bind(wx.EVT_BUTTON,self.set_gateway)        
        row_sizer.Add(self.gateway_field,0,wx.ALL,border=5)
        row_sizer.Add(self.set_gateway_button,0,wx.TOP | wx.RIGHT,border=5)

        settings_sizer.Add(row_sizer,0,wx.ALIGN_LEFT)

        self.SetSizerAndFit(settings_sizer)

    def gateway_chosen(self,event):
        config.GATEWAY_URL = self.gateway_choice.GetStringSelection()
        self.gateway_text.SetLabel(self.gateway_choice.GetStringSelection())

    def set_gateway(self,event):
        config.GATEWAY_URL = self.gateway_field.Value
        self.gateway_text.SetLabel(self.gateway_field.Value)