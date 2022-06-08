import requests
import wx
import cryptnoxpy
import gzip
from bs4 import BeautifulSoup
from nft_display import DownloadThread
import filetype
import tempfile
from wx import media
import io
from pubsub import pub
from eth_utils.curried import keccak
from web3 import Web3
import utils
import json
from wx.lib.scrolledpanel import ScrolledPanel



class CardLoadPanel(ScrolledPanel):

    def __init__(self,parent,id):
        super(CardLoadPanel,self).__init__(parent,id)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        self.mode = 'URL'
        self.field_placeholders = {
            'URL':'<Please input URL above>',
            'File':'<Please select file above>',
            'Manual':''
        }
        self.opensea_apikey = '31e9b4471d30479186e089c36268e35e'
        self.columns = ['Field 1','Field 2','PIN','PUK','Chain Name and ID','Contract address','Token ID','Metadata']
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        self.ABI_modes = ['Automatic','ERC-721 Openzeppelin','ERC-1155 Openzeppelin','Manual']
        self.endpoints = ['Polygon','Ethereum']
        self.metadata_apikeys = {
            'nftport':'b15abe1b-2545-4e1e-b07c-5da11cec6950'
        }
        self.api_keys = {
            'Polygon':'QQDEW4R8YBKBD1PZ3QCGHY8MKGP79MIR4M',
            'Ethereum':'754G6AI3GKUYRHG7M493AR4Y2TCZZ8YAWY'
            }
        self.endpoint_urls = {
            'Polygon':'https://polygon-rpc.com',
            'Ethereum':'https://cloudflare-eth.com',
            'Gnosis':'https://rpc.gnosischain.com',
            'Optimism':'https://mainnet.optimism.io',
            'Arbitrum':'https://arb1.arbitrum.io/rpc'
            }
        self.chains = {
            'Polygon':{'name':'Polygon Mainnet','id':'137'},
            'Ethereum':{'name':'Ethereum Mainnet','id':'1'},
            'Gnosis':{'name':'Gnosis Chain','id':'100'},
            'Optimism':{'name':'Optimism','id':'10'},
            'Arbitrum':{'name':'Arbitrum One','id':'42161'}
        }
        self.abi_urls = {
            'Polygon':'https://api.polygonscan.com/api?module=contract&action=getabi',
            'Ethereum':'https://api.etherscan.io/api?module=contract&action=getabi'
        }
        self._SEED_SOURCE_TRANSLATION = {
            cryptnoxpy.SeedSource.NO_SEED: "No seed",
            cryptnoxpy.SeedSource.INTERNAL: "Single card",
            cryptnoxpy.SeedSource.DUAL: "Dual card",
        }

        font = wx.Font(10, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        col_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(col_sizer,1,wx.ALIGN_LEFT)
        self.col_sizer_2 = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.col_sizer_2,1,wx.EXPAND)

        
        for x in range(0,4):
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            text = wx.StaticText(self,label=self.columns[x])
            text.SetFont(font)
            row_sizer.Add(text,1,wx.ALL,border=5)
            field = wx.TextCtrl(self,x+1)            
            row_sizer.Add(field,1,wx.ALL,border=5)
            col_sizer.Add(row_sizer,0,wx.EXPAND)

        #Input methods choice
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Please choose NFT data input method below:')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)

        self.clear_fields_btn = wx.Button(self,-1,label='Reset all fields',size=(100,30))
        self.clear_fields_btn.SetFont(font)
        self.clear_fields_btn.SetBackgroundColour('gray')
        self.clear_fields_btn.Bind(wx.EVT_BUTTON,self.clear_fields)
        # row_sizer.AddSpacer(100)
        row_sizer.Add(self.clear_fields_btn,1,wx.ALL,border=5)

        self.col_sizer_2.Add(row_sizer,0,wx.EXPAND)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        rb1 = wx.RadioButton(self,label='URL',style=wx.RB_GROUP)
        rb2 = wx.RadioButton(self,label='File')
        rb3 = wx.RadioButton(self,label='Manual')
        row_sizer.Add(rb1,1,wx.ALL,border=15)
        row_sizer.Add(rb2,1,wx.ALL,border=15)
        row_sizer.Add(rb3,1,wx.ALL,border=15)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_choice)

        self.col_sizer_2.Add(row_sizer,0,wx.EXPAND)

    
        #File picker field
        self.file_picker_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='File')
        text.SetFont(font)
        self.file_picker_sizer.Add(text,1,wx.ALL,border=5)
        self.file_picker = wx.FilePickerCtrl(self)
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED,self.file_picked)
        self.file_picker_sizer.Add(self.file_picker,1,wx.ALL,border=5)

        self.col_sizer_2.Add(self.file_picker_sizer,0,wx.EXPAND)

        self.file_picker_sizer.Hide(0)
        self.file_picker_sizer.Hide(1)
        

        #URL field
        self.url_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='URL')
        text.SetFont(font)
        self.url_input_sizer.Add(text,1,wx.ALL,border=5)
        self.url_field = wx.TextCtrl(self,size=(250,23))
        self.url_input_sizer.Add(self.url_field,0,wx.ALL,border=5)
        self.get_fields = wx.Button(self,-1,size=(80,22))
        self.get_fields.SetLabel('Get fields')
        self.get_fields.Bind(wx.EVT_BUTTON,self.get_fields_from_url)
        self.url_input_sizer.Add(self.get_fields,0,wx.TOP | wx.RIGHT,border=5)

        self.col_sizer_2.Add(self.url_input_sizer,0,wx.EXPAND)

        #NFT fields
        for x in range(4,len(self.columns)):
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            if x == 7:
                self.metedata_label = wx.StaticText(self,label=self.columns[x])
                self.metedata_label.SetFont(font)
                row_sizer.Add(self.metedata_label,1,wx.ALL,border=5)
            else:
                text = wx.StaticText(self,label=self.columns[x])
                text.SetFont(font)
                row_sizer.Add(text,1,wx.ALL,border=5)
            field = wx.TextCtrl(self,x+1)            
            row_sizer.Add(field,1,wx.ALL,border=5)
            self.col_sizer_2.Add(row_sizer,0,wx.EXPAND)
        
        self.preview_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.col_sizer_2.Add(self.preview_sizer)

        #NFC Sign
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='NFC sign')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)
        self.NFC_choice = wx.CheckBox(self)
        row_sizer.Add(self.NFC_choice,1,wx.ALL,border=5)
        col_sizer.Add(row_sizer,0,wx.EXPAND)
        
        #ABI
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='ABI Mode')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)
        self.ABI_chooser = wx.ListBox(self,choices=self.ABI_modes)
        self.ABI_chooser.SetStringSelection(self.ABI_modes[0])
        self.ABI_chooser.Bind(wx.EVT_LISTBOX,self.ABI_chosen)
        row_sizer.Add(self.ABI_chooser,1,wx.ALL,border=5)
        col_sizer.Add(row_sizer,0,wx.EXPAND)

        #manual ABI
        self.manual_abi_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='ABI Value')
        text.SetFont(font)
        self.manual_abi_sizer.Add(text,1,wx.ALL,border=5)
        self.manual_ABI = wx.TextCtrl(self)            
        self.manual_abi_sizer.Add(self.manual_ABI,1,wx.ALL,border=5)
        col_sizer.Add(self.manual_abi_sizer,0,wx.EXPAND)

        #Endpoint URLs
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Endpoint')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)
        self.endpoint_choice = wx.Choice(self,choices=[f'{key}: {value}' for key,value in self.endpoint_urls.items()])
        row_sizer.Add(self.endpoint_choice,1,wx.ALL,border=5)
        col_sizer.Add(row_sizer,0,wx.EXPAND)

        
        col_sizer.AddSpacer(100)

        #Reset card and Execute load buttons
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.reset_btn = wx.Button(self,11,size=(150,40))
        self.reset_btn.SetFont(font)
        self.reset_btn.SetLabel('Card reset')

        self.reset_btn.Bind(wx.EVT_BUTTON,self.reset_card)

        left_sizer.Add(self.reset_btn,0,wx.RIGHT,border=20)

        self.info_btn = wx.Button(self,12,size=(150,40))
        self.info_btn.SetFont(font)
        self.info_btn.SetLabel('Card Info')

        self.info_btn.Bind(wx.EVT_BUTTON,self.info_card)

        left_sizer.Add(self.info_btn,0,wx.ALL,border=0)

        self.execute_btn = wx.Button(self,13,size=(250,40))
        self.execute_btn.SetFont(font)
        self.execute_btn.SetLabel('Execute load')

        self.execute_btn.Bind(wx.EVT_BUTTON,self.execute_load)

        row_sizer.Add(left_sizer,1,wx.ALL,border=30)
        row_sizer.Add(self.execute_btn,0,wx.ALL,border=30)

        col_sizer.Add(row_sizer,0,wx.EXPAND)


        self.SetSizerAndFit(main_sizer)
        self.manual_abi_sizer.Hide(0)
        self.manual_abi_sizer.Hide(1)

        for x in range(5,9):
            field = self.Parent.FindWindowById(x)
            field.SetEditable(False)
            field.SetValue('<Please input URL above>')
            field.Disable()
        self.endpoint_choice.Disable()
        self.manual_ABI.Disable()
        self.Parent.FindWindowById(3).SetValue('000000000')
        self.Parent.FindWindowById(4).SetValue('000000000000')

        pub.subscribe(self.downloaded, "downloaded")

        self.Parent.FindWindowById(8).Bind(wx.EVT_TEXT,self.metedata_changed)

    def clear_fields(self,event):
        for i in range(1,len(self.columns)+1):
            field = self.FindWindowById(i)
            if 'Please' in field.GetValue():
                pass
            elif i in [3,4]:
                if i == 3:
                    field.SetValue('000000000')
                else:
                    field.SetValue('000000000000')
            else:
                if i in [5,6,7,8]:
                    print(f'Clearing field {i}, {field.GetValue()}')
                    field.SetValue(self.field_placeholders[self.mode])
                else:
                    field.SetValue('')
            self.endpoint_choice.Clear()
            self.endpoint_choice.SetItems([f'{key}: {value}' for key,value in self.endpoint_urls.items()])
            self.endpoint_choice.Enable()
            self.manual_ABI.SetValue('')
            self.manual_abi_sizer.Hide(0)
            self.manual_abi_sizer.Hide(1)
            self.manual_ABI.SetEditable(False)
            self.ABI_chooser.Enable()
            self.Layout()
            self.ABI_chooser.SetStringSelection('Automatic')
            self.url_field.SetValue('')
            self.preview_sizer.Clear(1)

        
        
    def info_card(self,event='',message=''):
        try:
            card = self.get_card()
        except Exception as e:
            wx.MessageBox(f"Card or reader not found, please ensure device is connected.\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_WARNING)
            return
        slots = []
        try:
            for i in range(0,4):
                slots.append(gzip.decompress(card.user_data[i]))
            slot0 = json.loads(slots[0].decode('UTF-8'))
            abi = slots[2].decode("UTF8")
            # message+='----------------------------------------------'
            seed_source = card.seed_source
            message+=f'{self._SEED_SOURCE_TRANSLATION[seed_source]}'
            # message+='\n----------------------------------------------'
            public_key = card.get_public_key()
            # message+=f'\nPublic key: \n{public_key}'
            # message+='\n----------------------------------------------'
            result = utils._private_key_check(card,bytes.fromhex(public_key))
            message+=f'\nPrivate key check: \n{result}'
            # message+='\n----------------------------------------------'
            result = utils._history_counter(card)
            message+=f'\n{result}'
            # message+='\n----------------------------------------------'
            address = self.checksum_address(public_key)
            message+=f'\nYour card address: \n{address}'
            # message+='\n----------------------------------------------'
            message+=f'\nChecking owner on contract'
            result = utils._owner(slot0['endpoint'], slot0['contract_address'], abi, address, slot0['nft_id'])
            message+=f'\n{result}'
            # message+='\n----------------------------------------------'
            result = utils._balance(slot0['endpoint'], address)
            message+=f'\n{result}'
            # message+='\n----------------------------------------------'
            message+=f"\nEndpoint: {slot0['endpoint']}"
            # message+="\n----------------------------------------------"
            message+=f"\nChain ID: {slot0['chain_id']}"
            # message+="\n----------------------------------------------"
            message+=f"\nNFT Contract address: {slot0['contract_address']}"
            # message+="\n----------------------------------------------"
            message+=f"\nNFT Token ID: {slot0['nft_id']}"
            # message+="\n----------------------------------------------"
            metadata = slots[3].decode("UTF8").replace("\n", "")
            message+=f"\nmetadata: {metadata}"
            # message+="\n----------------------------------------------"
            result = utils._url(metadata)
            message+=f'\n{result}'
            # wx.MessageBox(message, "Info" ,wx.OK | wx.ICON_WARNING)
            MessageBox(self,'Card info',message)
        except Exception as e:
            print(f'Error getting card info: {e}')
            wx.MessageBox(f"Could not get info from card, please ensure card is initialized.", "Error" ,wx.OK | wx.ICON_WARNING)

        

    def on_radio_choice(self,event):
        choice = event.GetEventObject().GetLabel()
        if 'URL' in choice:
            self.mode = 'URL'
            self.file_picker_sizer.Hide(0)
            self.file_picker_sizer.Hide(1)
            self.url_input_sizer.Show(0)
            self.url_input_sizer.Show(1)
            self.url_input_sizer.Show(2)
            for x in range(5,9):
                field = self.Parent.FindWindowById(x)
                field.SetEditable(False)
                field.SetValue('<Please input URL above>')
                field.Disable()
            self.manual_ABI.SetEditable(False)
            self.endpoint_choice.Disable()
            self.endpoint_choice.Clear()
            self.endpoint_choice.SetItems([f'{key}: {value}' for key,value in self.endpoint_urls.items()])
        elif 'File' in choice:
            self.mode = 'File'
            self.url_input_sizer.Hide(0)
            self.url_input_sizer.Hide(1)
            self.url_input_sizer.Hide(2)
            self.file_picker_sizer.Show(0)
            self.file_picker_sizer.Show(1)
            for x in range(5,9):
                field = self.Parent.FindWindowById(x)
                field.SetEditable(False)
                field.SetValue('<Please select file above>')
                field.Disable()
            self.manual_ABI.SetEditable(False)
            self.endpoint_choice.Disable()
            self.endpoint_choice.Clear()
            self.endpoint_choice.SetItems([f'{key}: {value}' for key,value in self.endpoint_urls.items()])
        else:
            self.mode = 'Manual'
            self.url_input_sizer.Hide(0)
            self.url_input_sizer.Hide(1)
            self.url_input_sizer.Hide(2)
            self.file_picker_sizer.Hide(0)
            self.file_picker_sizer.Hide(1)
            for x in range(5,9):
                field = self.Parent.FindWindowById(x)
                field.SetEditable(True)
                field.SetValue('')
                field.Enable()
            self.manual_ABI.SetEditable(True)
            self.manual_ABI.Enable()
            self.manual_ABI.SetValue('')
            self.endpoint_choice.Enable()
        self.Parent.FindWindowById(3).SetValue('000000000')
        self.Parent.FindWindowById(4).SetValue('000000000000')
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
                    self.endpoint_choice.SetStringSelection(f'Polygon: {self.endpoint_urls["Polygon"]}')
                elif 'ethereum' in l[-2]:
                    self.endpoint_choice.SetStringSelection(f'Ethereum: {self.endpoint_urls["Ethereum"]}')
                else:
                    wx.MessageBox("Unrecognized endpoint, please contact developer", "Info" ,wx.OK | wx.ICON_WARNING)
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
            self.manual_ABI.Disable()
        else:
            wx.MessageBox("Please select a valid txt file with NFT fields.", "Info" ,wx.OK | wx.ICON_WARNING)

    def get_fields_from_url(self,event):
        try:
            url = self.url_field.GetValue()
            split = url.split('/')
            contract_address = split[-2]
            token_id = split[-1]
            endpoint = 'Polygon' if 'matic' in url else 'Ethereum'
        except Exception as e:
            print(f'Exception parsing url: {e}')
            wx.MessageBox(f"Invalid URL, please try again.\n\n", "Error" ,wx.OK | wx.ICON_WARNING)
            return
        self.Parent.FindWindowById(5).SetValue(self.chains[endpoint]['id']+' ('+self.chains[endpoint]['name']+')')
        self.Parent.FindWindowById(6).SetValue(contract_address)
        self.Parent.FindWindowById(7).SetValue(token_id)
        self.endpoint_choice.SetStringSelection(f'{endpoint}: {self.endpoint_urls[endpoint]}')
        self.endpoint_choice.Disable()
        self.Parent.FindWindowById(8).SetValue('')

        ABI = self.fetch_ABI(self.abi_urls[endpoint],contract_address,self.api_keys[endpoint])
        self.ABI_chooser.SetStringSelection('Automatic')
        self.ABI_chooser.Disable()
        self.manual_abi_sizer.Show(0)
        self.manual_abi_sizer.Show(1)
        self.Layout()
        self.manual_ABI.SetValue(ABI)
        metadata = False
        try:
            nftport_url = f"https://api.nftport.xyz/v0/nfts/{contract_address}/{token_id}"
            print(nftport_url)
            querystring = {"chain":endpoint.lower(),"refresh_metadata":"false"}
            headers = {
                'Content-Type': "application/json",
                'Authorization': self.metadata_apikeys['nftport']
            }
            nftport_response = requests.request("GET",nftport_url,headers=headers,params=querystring)
            print(nftport_response.text)
            metadata = nftport_response.json()['nft']['metadata']
            self.Parent.FindWindowById(8).SetValue(str(metadata))
        except Exception as e:
            print(f'Error fetching metadata: {e}')
            self.Parent.FindWindowById(8).Enable()
            self.Parent.FindWindowById(8).SetEditable(True)

        try:
            if not metadata:
                response = requests.get(url)
                if response.status_code >= 400:
                    raise
                soup = BeautifulSoup(response.text)
            else:
                return
        except Exception as e:
            print(f'Exception fetching url: {e}')
            wx.MessageBox(f"Metadata not found in database, please continue input manually.\n\n", "Info" ,wx.OK | wx.ICON_WARNING)
            self.Parent.FindWindowById(8).Enable()
            self.Parent.FindWindowById(8).SetEditable(True)   
            return
        divs = soup.find_all("div",{'class':'Blockreact__Block-sc-1xf18x6-0 elqhCm'})
        spans = divs[1].find_all("span")
        metadata_url = spans[4].find_all("a")[0]['href']
        try:
            metadata = requests.get(metadata_url).json()
            self.Parent.FindWindowById(8).SetValue(str(metadata))
        except Exception as e:
            print(f'Exception fetching metadata: {e}')
            wx.MessageBox(f"Network error in fetching Metadata, please input manually or try again.\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_WARNING)
            self.Parent.FindWindowById(8).SetEditable(True)

    def fetch_ABI(self,url,contract_address,api_key):
        try:
            response = requests.get(url+f'&address={contract_address}'+f'&apikey={api_key}')
            print(url+f'&address={contract_address}'+f'&apikey={api_key}')
            resp = response.json()['result']            
            print(response.status_code)
            if response.status_code >= 400 or 'Invalid' in resp or 'verified' in resp:
                raise Exception(resp)
            self.manual_ABI.SetEditable(False)
            self.manual_ABI.Disable()
        except Exception as e:
            print(f'Exception fetching ABI: {e}')
            if 'Invalid' in str(e) or 'verified' in str(e):
                wx.MessageBox(f"ABI could not be fetched, please input manually or try again.\n\nInfo:\n\n{e}", "Info" ,wx.OK | wx.ICON_WARNING)
            else:
                wx.MessageBox(f"Network error in fetching ABI, please input manually or try again.\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_WARNING)
            self.manual_ABI.SetEditable(True)
            self.manual_ABI.Enable()
            resp = ''
        return resp

    def execute_load(self,event):
        unfilled_list = self.validate_fields()
        if len(unfilled_list) > 0:
            empty_fields = []
            message = 'Please fill the following fields:'
            for each in unfilled_list:
                message+=(f'\n-{each}')
            wx.MessageBox(message, "Error" ,wx.OK | wx.ICON_WARNING)
            return
        try:
            card = self.get_card()
        except Exception as e:
            print(f'Exception getting card object: {e}')
            wx.MessageBox(f"Card or reader not found, please ensure device is connected.\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_WARNING)
            return
        l = ['','Name','Mail','PIN','PUK']
        data = {}
        slot_data = []
        slots = []
        for x in range(1,5):
            field = self.Parent.FindWindowById(x)
            value = field.GetValue()
            data[l[x]]=value
        if data['Name'] == '':
            data['Name'] = 'EASY MODE'
        if data['Mail'] == '':
            data['Mail'] = 'EASY MODE'
        if data['PIN'] == '':
            data['PIN'] = '000000000'
        if data['PUK'] == '':
            data['PUK'] = '000000000000'
        for x in range(5,9):
            field = self.Parent.FindWindowById(x)
            value = field.GetValue()
            slot_data.append(value)
        slot_data.append(self.manual_ABI.GetValue())
        d = {}
        d['endpoint'] = self.endpoint_urls[self.endpoint_choice.GetStringSelection().split(':')[0]]
        d['chain_id'] = self.chains[self.endpoint_choice.GetStringSelection().split(':')[0]]['id']
        print(d['chain_id'])
        d['contract_address'] = Web3.toChecksumAddress(slot_data[1])
        d['token_id'] = slot_data[2]
        slots.append(d)
        slots.append('')
        d = {}
        if slot_data[4] == '':
            print(f'Getting ABI')
            endpoint = self.endpoint_choice.GetStringSelection()
            contract_address = slot_data[1]
            ABI_resp = self.fetch_ABI(self.abi_urls[endpoint],contract_address,self.api_keys[endpoint])
            if ABI_resp == '':
                print('No ABI')
                return
            d['ABI'] = ABI_resp
        else:
            d['ABI'] = slot_data[4]
        slots.append(slot_data[4])
        slots.append(slot_data[3])
        slots[0] = str(slots[0]).replace('\'','\"').replace('token_id','nft_id')
        slots[2] = str(slots[2]).replace('\'','\"')
        meta_str = str(slots[3]).replace('\'','\"')
        meta = eval(meta_str)
        meta_url = meta['image_url'].split('/')
        image_url = f'https://cloudflare-ipfs.com/ipfs/{meta_url[-2]}/{meta_url[-1]}'
        meta['image_url'] = image_url
        slots[3] = str(meta).replace('\'','\"')
        try:
            card.init(data['Name'],data['Mail'],data['PIN'],data['PUK'],nfc_sign=self.NFC_choice.GetValue())
        except Exception as e:
            print(f'Exception in init: {e}')
            wx.MessageBox(f"Card cannot be initialized, please reset the card.\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_WARNING)
            return
        try:
            card = self.get_card()
        except Exception as e:
            wx.MessageBox(f"Card or reader not found, please ensure device is connected.\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_WARNING)
            return
        try:
            for index,value in enumerate(slots):
                if value:
                    card.user_data[index] = gzip.compress(value.encode("UTF-8"))
        except Exception as e:
            print(f'Error writing data to card: {e}')
            wx.MessageBox(f"Error writing data to card.\n\n {e}", "Error" ,wx.OK | wx.ICON_WARNING)
            return
        print('Data written')
        print("Generating seed...")
        card.generate_seed(data["PIN"])
        print("Seed generated")
        message = f"Card has been loaded with the NFT, it can now be viewed with Cryptnox Gallery.\nTransfer tokens to it to complete the initialization process.\n"
        self.info_card(message=message)

    def get_card(self):
        return cryptnoxpy.factory.get_card(cryptnoxpy.Connection())
        
    
    def validate_fields(self):
        l = []
        for x in range(2,8):
            v = self.Parent.FindWindowById(x+1).GetValue()
            if v == '' or 'Please' in v:
                l.append(self.columns[x])
        if self.manual_ABI.GetValue() == '':
            if self.ABI_chooser.GetStringSelection() == 'Manual':
                l.append('ABI')
        if 5 > len(self.Parent.FindWindowById(3).GetValue()) < 9:
            wx.MessageBox("PIN must be more than 5 and less than 9 numeric values", "Error" ,wx.OK | wx.ICON_INFORMATION)
        if len(self.Parent.FindWindowById(4).GetValue()) <= 11:
            wx.MessageBox("PUK must be 12 alphanumeric value", "Error" ,wx.OK | wx.ICON_INFORMATION)
        if self.endpoint_choice.GetStringSelection() == '':
            l.append('Endpoint')
        return l

    def reset_card(self,event):
        try:
            card = self.get_card()
            puk = utils.ask(message='Please input your PUK to reset:')
            if puk:
                confirm = utils.confirm(message='This will reset the card, are you sure ?')
                if confirm == 5100:
                    card.reset(puk)
                    wx.MessageBox(f"Card has been reset.", "Info" ,wx.OK | wx.ICON_INFORMATION)
                else:
                    return
        except Exception as e:
            wx.MessageBox(f"Error resetting card:\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_INFORMATION)
            return


    def metedata_changed(self,event):
        v = self.Parent.FindWindowById(8).GetValue()
        try:
            metadata_json = eval(v)
            image_url = metadata_json['image_url'] if 'image_url' in metadata_json.keys() else metadata_json['image']
            split_url = image_url.split('/')
            url = f"https://cf-ipfs.com/ipfs/{split_url[-2]}/{split_url[-1]}"
            self.fetch_nft(url)
        except Exception as e:  
            print(f'Not downloading NFT:{e}')
            pass

    def fetch_nft(self,url):
        print(f'Fetching NFT: {url}')
        self.metedata_label.SetLabel('Metadata (Loading preview...)')
        DownloadThread(self,url)
        # self.preview_text.SetLabel('Loading preview')
        # wx.MessageBox(f"NFT preview will be available shortly.", "Error" ,wx.OK | wx.ICON_INFORMATION)

    def downloaded(self, data):
        try:
            print(f'Downloaded')
            self.metedata_label.SetLabel('Metadata')
            file_type = filetype.guess(data).mime
            if not file_type.startswith('image'):
                wx.MessageBox(f"File format not recognized, preview unavailable", "Error" ,wx.OK | wx.ICON_INFORMATION)
                return
            if file_type.endswith('gif'):
                self.show_nft('gif',data)
            else:
                self.show_nft('image',data)
        except Exception as e:
            print(f'Exception in downloaded: {e}')

    def show_nft(self,nft_type,data):
        self.preview_sizer.Clear(1)
        if nft_type == 'gif':
            ft = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
            ft.write(data)
            ft.flush()
            ft.close()
            self.anim = media.MediaCtrl(self,-1,style=wx.SIMPLE_BORDER,pos=(0,300), size=(500,500))
            # print(self.col_sizer_2.GetSize())
            self.anim.Bind(media.EVT_MEDIA_LOADED, self.on_media_loaded)
            self.anim.Bind(media.EVT_MEDIA_FINISHED,self.on_media_finished)
            self.anim.Load(ft.name)
            self.preview_sizer.Add(self.anim, 0, wx.CENTER, 0)
            self.Layout()
        else:
            print('Not gif')
            img = wx.Image(io.BytesIO(data)).ConvertToBitmap()
            img = self.scale_bitmap(img, 500, img.GetHeight())
            nft = wx.StaticBitmap(self, -1, img, (0,500))
            self.preview_sizer.Add(nft,0,wx.CENTER,0)
            self.Layout()

    def scale_bitmap(self,bitmap, width, height):
        image = bitmap.ConvertToImage()
        rescale_height = ((bitmap.GetWidth()-500)/bitmap.GetWidth())*bitmap.GetHeight()
        height_rescaled = bitmap.GetHeight()-rescale_height
        image = image.Scale(width, height_rescaled, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result
            
    def on_media_loaded(self, event):
        self.anim.Play()

    def on_media_finished(self,event: media.EVT_MEDIA_FINISHED):
        self.anim.Play()

    def address(self,public_key: str) -> str:
        return keccak(hexstr=("0x" + public_key[2:]))[-20:].hex()


    def checksum_address(self,public_key: str) -> str:
        return Web3.toChecksumAddress(self.address(public_key))


class MessageBox(wx.Dialog):
    def __init__(self, parent, title, message):
        wx.Dialog.__init__(self, parent, title=title)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        window = wx.ScrolledWindow(self,-1,size=(600,600))
        main_sizer.Add(window,1,wx.EXPAND)
        print(message.split('\n'))
        height = 0
        for each in message.split('\n'):
            text = wx.TextCtrl(window, style=wx.TE_READONLY|wx.BORDER_NONE,pos=(30,height),size=(1000,23))
            text.SetValue(each)
            # window.AddChild(text)
            height+=23
        window.SetVirtualSize(600,height)
        print(window.GetSize())
        window.SetScrollRate(15,15)
        self.SetSizerAndFit(main_sizer)
        self.ShowModal()