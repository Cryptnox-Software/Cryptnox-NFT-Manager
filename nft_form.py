from lib2to3.pgen2 import token
from random import choices
from tkinter import E
import requests
import wx
import cryptnoxpy
import gzip
from bs4 import BeautifulSoup

class Panel(wx.Panel):

    def __init__(self,parent,id):
        super(Panel,self).__init__(parent,id)
        columns = ['Name','Email','PIN','PUK','Chain ID','Contract address','NFT ID','Metadata']
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        self.ABI_modes = ['Automatic','ERC721 Openzeppelin','ERC1155 Openzeppelin','Manual']
        self.endpoints = ['Polygon','Ethereum']
        self.api_keys = {
            'Polygon':'QQDEW4R8YBKBD1PZ3QCGHY8MKGP79MIR4M',
            'ethereum':'754G6AI3GKUYRHG7M493AR4Y2TCZZ8YAWY'
            }
        self.endpoint_urls = {
            'Polygon':'https://polygon-rpc.com',
            'ethereum':'https://cloudflare-eth.com',
            'gnosis':'https://rpc.gnosischain.com',
            'optimism':'https://mainnet.optimism.io',
            'arbitrum':'https://arb1.arbitrum.io/rpc'
            }
        self.chain_ids = {
            'Polygon':'137',
            'ethereum':'1',
            'gnosis':'100',
            'optimism':'10',
            'arbitrum':'42161'
        }
        self.abi_urls = {
            'Polygon':'https://api.polygonscan.com/api?module=contract&action=getabi',
            'Ethereum':''
        }

        font = wx.Font(13, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        col_sizer = wx.BoxSizer(wx.VERTICAL)
        col_sizer.Add((0, 0), 1, wx.EXPAND)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Please choose NFT data input method below:')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=10)
        col_sizer.Add(row_sizer,1,wx.EXPAND)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        rb1 = wx.RadioButton(self,label='URL',style=wx.RB_GROUP)
        rb2 = wx.RadioButton(self,label='File')
        rb3 = wx.RadioButton(self,label='Manual')
        row_sizer.Add(rb1,1,wx.ALL,border=10)
        row_sizer.Add(rb2,1,wx.ALL,border=10)
        row_sizer.Add(rb3,1,wx.ALL,border=10)
        col_sizer.Add(row_sizer,1,wx.EXPAND)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_choice)

        #File picker field
        self.file_picker_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='File')
        text.SetFont(font)
        self.file_picker_sizer.Add(text,1,wx.ALL,border=10)
        self.file_picker = wx.FilePickerCtrl(self)
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED,self.file_picked)
        self.file_picker_sizer.Add(self.file_picker,1,wx.ALL,border=10)
        col_sizer.Add(self.file_picker_sizer,1,wx.EXPAND)

        self.file_picker_sizer.Hide(0)
        self.file_picker_sizer.Hide(1)
        

        #URL field
        self.url_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='URL')
        text.SetFont(font)
        self.url_input_sizer.Add(text,1,wx.ALL,border=10)
        self.url_field = wx.TextCtrl(self)
        self.url_input_sizer.Add(self.url_field,1,wx.ALL,border=10)
        self.get_fields = wx.Button(self,-1,size=(50,22))
        self.get_fields.SetLabel('Get fields')
        self.get_fields.Bind(wx.EVT_BUTTON,self.get_fields_from_url)
        self.url_input_sizer.Add(self.get_fields,1,wx.TOP | wx.RIGHT,border=10)
        col_sizer.Add(self.url_input_sizer,1,wx.EXPAND)

        #NFT fields
        for each in columns:
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            text = wx.StaticText(self,label=each)
            text.SetFont(font)
            row_sizer.Add(text,1,wx.ALL,border=10)
            field = wx.TextCtrl(self,columns.index(each)+1)            
            row_sizer.Add(field,1,wx.ALL,border=10)
            col_sizer.Add(row_sizer,1,wx.EXPAND)
        
        

        #NFC Sign
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='NFC sign')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=10)
        self.NFC_choice = wx.CheckBox(self)
        row_sizer.Add(self.NFC_choice,1,wx.ALL,border=10)
        col_sizer.Add(row_sizer,1,wx.EXPAND)
        
        #ABI
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='ABI')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=10)
        self.ABI_chooser = wx.ListBox(self,choices=self.ABI_modes)
        self.ABI_chooser.Bind(wx.EVT_LISTBOX,self.ABI_chosen)
        row_sizer.Add(self.ABI_chooser,1,wx.ALL,border=10)
        col_sizer.Add(row_sizer,1,wx.EXPAND)

        #manual ABI
        self.manual_abi_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Manual ABI')
        text.SetFont(font)
        self.manual_abi_sizer.Add(text,1,wx.ALL,border=10)
        self.manual_ABI = wx.TextCtrl(self)            
        self.manual_abi_sizer.Add(self.manual_ABI,1,wx.ALL,border=10)
        col_sizer.Add(self.manual_abi_sizer,1,wx.EXPAND)
        self.manual_abi_sizer.Hide(0)
        self.manual_abi_sizer.Hide(1)

        #Endpoint URLs
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Endpoint')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=10)
        self.endpoint_choice = wx.Choice(self,choices=self.endpoints)
        row_sizer.Add(self.endpoint_choice,1,wx.ALL,border=10)
        col_sizer.Add(row_sizer,1,wx.EXPAND)

        

        #Execute load button
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.execute_btn = wx.Button(self,-1,size=(0,40))
        self.execute_btn.SetFont(font)
        self.execute_btn.SetLabel('Execute load')
        row_sizer.Add(self.execute_btn,1,wx.ALL,border=30)
        col_sizer.Add(row_sizer,1,wx.EXPAND)
        self.execute_btn.Bind(wx.EVT_BUTTON,self.execute_load)

        self.SetSizerAndFit(col_sizer)

        for x in range(5,9):
            field = self.Parent.FindWindowById(x)
            field.SetEditable(False)
            field.SetValue('<Please input URL above>')
        self.manual_ABI.SetEditable(False)

    def on_radio_choice(self,event):
        choice = event.GetEventObject().GetLabel()
        if 'URL' in choice:
            self.file_picker_sizer.Hide(0)
            self.file_picker_sizer.Hide(1)
            self.url_input_sizer.Show(0)
            self.url_input_sizer.Show(1)
            self.url_input_sizer.Show(2)
            for x in range(5,9):
                field = self.Parent.FindWindowById(x)
                field.SetEditable(False)
                field.SetValue('<Please input URL above>')
            self.manual_ABI.SetEditable(False)
        elif 'File' in choice:
            self.url_input_sizer.Hide(0)
            self.url_input_sizer.Hide(1)
            self.url_input_sizer.Hide(2)
            self.file_picker_sizer.Show(0)
            self.file_picker_sizer.Show(1)
            for x in range(5,9):
                field = self.Parent.FindWindowById(x)
                field.SetEditable(False)
                field.SetValue('<Please select file above>')
            self.manual_ABI.SetEditable(False)
        else:
            self.url_input_sizer.Hide(0)
            self.url_input_sizer.Hide(1)
            self.url_input_sizer.Hide(2)
            self.file_picker_sizer.Hide(0)
            self.file_picker_sizer.Hide(1)
            for x in range(5,9):
                field = self.Parent.FindWindowById(x)
                field.SetEditable(True)
                field.SetValue('')
            self.manual_ABI.SetEditable(True)
        self.Layout()

    def ABI_chosen(self,event: wx.EVT_LISTBOX):
        if self.ABI_chooser.GetString(self.ABI_chooser.GetSelection()) == 'Manual':
            self.manual_abi_sizer.Show(0)
            self.manual_abi_sizer.Show(1)
            self.Layout()
        else:
            self.manual_abi_sizer.Hide(0)
            self.manual_abi_sizer.Hide(1)
            self.Layout()

    def file_picked(self,event: wx.EVT_FILEPICKER_CHANGED):
        path_picked = self.file_picker.GetPath()
        print(path_picked[-3:])
        if path_picked[-3:] == 'txt' and 'NFT' in path_picked:
            try:
                with open(path_picked,'r') as file:
                    lines = file.readlines()
                if 'http' not in lines[0].strip():
                    raise Exception()
                l = []
                l.append(lines[6].strip()) #chain_id
                l.append(lines[9].strip()) #contract_address
                l.append(lines[13].strip()) #token_id
                l.append(lines[21].strip()) #metadata
                l.append(lines[3].strip()) #endpoint
                l.append(lines[18].strip()) #ABI
                if 'polygon' in l[-2]:
                    self.endpoint_choice.SetStringSelection('Polygon')
                elif 'ethereum' in l[-2]:
                    self.endpoint_choice.SetStringSelection('ethereum')
                else:
                    print(f'Unrecognized endpoint: {l[-2]}')
            except Exception as e:
                wx.MessageBox("Please select a valid txt file with NFT fields.", "Info" ,wx.OK | wx.ICON_WARNING)
                return
                
            for x in range (5,9):
                field = self.Parent.FindWindowById(x)
                field.SetValue(l[x-5])


            self.ABI_chooser.SetStringSelection('Manual')
            self.manual_abi_sizer.Show(0)
            self.manual_abi_sizer.Show(1)
            self.Layout()
            
            self.manual_ABI.SetValue(l[-1])
        else:
            wx.MessageBox("Please select a valid txt file with NFT fields.", "Info" ,wx.OK | wx.ICON_WARNING)

    def get_fields_from_url(self,event):
        url = self.url_field.GetValue()
        split = url.split('/')
        contract_address = split[-2]
        token_id = split[-1]
        response = requests.get(url)
        # soup = BeautifulSoup(response.text)
        with open('scrape_me.html') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        divs = soup.find_all("div",{'class':'Blockreact__Block-sc-1xf18x6-0 elqhCm'})
        spans = divs[1].find_all("span")
        endpoint = spans[3].text
        metadata_url = spans[4].find_all("a")[0]['href']
        metadata = requests.get(metadata_url).json()
        ABI = self.fetch_ABI(self.abi_urls[endpoint],contract_address,self.api_keys[endpoint])
        print(f'Got ABI: {len(ABI)}')
        l = [0,0,0,0,0,self.chain_ids[endpoint],contract_address,token_id,str(metadata)]
        for x in range(5,9):
            field = self.Parent.FindWindowById(x)
            field.SetValue(l[x])
        self.ABI_chooser.SetStringSelection('Manual')
        self.manual_abi_sizer.Show(0)
        self.manual_abi_sizer.Show(1)
        self.Layout()
        self.manual_ABI.SetValue(ABI)
        self.endpoint_choice.SetStringSelection(endpoint)

    def fetch_ABI(self,url,contract_address,api_key):
        try:
            resp = requests.get(url+f'&address={contract_address}'+f'&apikey={api_key}').json()['result']
        except Exception as e:
            print(f'Exception fetching ABI: {e}')
            resp = e
        return resp

    def execute_load(self,event):
        l = ['','Name','Mail','PIN','PUK']
        data = {}
        slot_data = []
        slots = []
        for x in range(1,5):
            field = self.Parent.FindWindowById(x)
            value = field.GetValue()
            data[l[x]]=value
        for x in range(5,9):
            field = self.Parent.FindWindowById(x)
            value = field.GetValue()
            slot_data.append(value)
        slot_data.append(self.manual_ABI.GetValue())
        d = {}
        d['endpoint'] = self.endpoint_urls[self.endpoint_choice.GetStringSelection()]
        d['chain_id'] = slot_data[0]
        d['contract_address'] = slot_data[1]
        d['token_id'] = slot_data[2]
        slots.append(d)
        slots.append('')
        d = {}
        d['ABI'] = slot_data[4]
        slots.append(d)
        slots.append(slot_data[3])
        slots[0] = str(slots[0])
        slots[2] = str(slots[2])
        meta_str = str(slots[3]).replace('\'','\"')
        meta = eval(meta_str)
        meta_url = meta['image_url'].split('/')
        image_url = f'https://cloudflare-ipfs.com/ipfs/{meta_url[-2]}/{meta_url[-1]}'
        meta['image_url'] = image_url
        slots[3] = str(meta).replace('\'','\"')
        print(data)
        print(slots[0])
        print(type(slots[0]))
        print(slots[3])
        connection = cryptnoxpy.Connection()
        card = cryptnoxpy.factory.get_card(connection)
        try:
            card.init(data['Name'],data['Mail'],data['PIN'],data['PUK'],nfc_sign=self.NFC_choice.GetValue())
        except Exception as e:
            print(f'Exception in init: {e}')
            wx.MessageBox("Card cannot be initialized, please reset using Cryptnoxpro.", "Info" ,wx.OK | wx.ICON_WARNING)
            return
        connection = cryptnoxpy.Connection()
        card = cryptnoxpy.factory.get_card(connection)
        for index,value in enumerate(slots):
            if value:
                card.user_data[index] = gzip.compress(value.encode("UTF-8"))
        print('Data written')
        wx.MessageBox("Card has been loaded with the NFT, it can now be viewed with Cryptnox Gallery.", "Info" ,wx.OK | wx.ICON_INFORMATION)
        wx.CallAfter(self.Parent.Close)
        


class NFT_Form_App(wx.App):

    def __init__(self):
        super(NFT_Form_App, self).__init__()
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.frame = wx.Frame(None, -1, "NFT Form",pos=((wx.DisplaySize()[0]/2)-250,(wx.DisplaySize()[1]/2)-500),size=(500,1000))
        self.panel = Panel(self.frame, -1)
        self.frame.Show(1)
        self.MainLoop()

def main() -> None:
    app = NFT_Form_App()
    

if __name__ == '__main__':
    main()