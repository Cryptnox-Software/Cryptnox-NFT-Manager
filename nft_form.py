import requests
import wx
import cryptnoxpy
import gzip
from bs4 import BeautifulSoup
from pathlib import Path
from nft_display import DownloadThread
import filetype
import tempfile
from wx import media
from wx.lib.pubsub import pub

class Panel(wx.Panel):

    def __init__(self,parent,id):
        super(Panel,self).__init__(parent,id)
        self.columns = ['Field 1','Field 2','PIN','PUK','Chain Name and ID','Contract address','Token ID','Metadata']
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        self.ABI_modes = ['Automatic','ERC-721 Openzeppelin','ERC-1155 Openzeppelin','Manual']
        self.endpoints = ['Polygon','Ethereum']
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

        font = wx.Font(13, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        col_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(col_sizer,1,wx.ALIGN_LEFT)
        self.col_sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.col_sizer_2.AddSpacer(500)
        main_sizer.Add(self.col_sizer_2,1,wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

        #Cryptnox logo on top
        path = Path(__file__).parent.joinpath("cryptnox_transparent.png").absolute()
        img = wx.Image(str(path),wx.BITMAP_TYPE_PNG)
        img_size = (250,250)
        img = img.Scale(int(img_size[0]),int(img_size[1]),wx.IMAGE_QUALITY_HIGH)
        img = img.ConvertToBitmap()
        image = wx.StaticBitmap(self, wx.ID_ANY, img, (0,0))
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(image,1,wx.ALL)
        col_sizer.Add(row_sizer,1,wx.EXPAND)

        for x in range(0,4):
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            text = wx.StaticText(self,label=self.columns[x])
            text.SetFont(font)
            row_sizer.Add(text,1,wx.ALL,border=10)
            field = wx.TextCtrl(self,x+1)            
            row_sizer.Add(field,1,wx.ALL,border=10)
            col_sizer.Add(row_sizer,1,wx.EXPAND)

        #Input methods choice
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
        for x in range(4,len(self.columns)):
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            text = wx.StaticText(self,label=self.columns[x])
            text.SetFont(font)
            row_sizer.Add(text,1,wx.ALL,border=10)
            field = wx.TextCtrl(self,x+1)            
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

        

        #Reset card and Execute load buttons
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.reset_btn = wx.Button(self,-1,size=(0,40))
        self.reset_btn.SetFont(font)
        self.reset_btn.SetLabel('Reset card')

        self.reset_btn.Bind(wx.EVT_BUTTON,self.reset_card)

        row_sizer.Add(self.reset_btn,1,wx.ALL,border=30)

        self.execute_btn = wx.Button(self,-1,size=(250,40))
        self.execute_btn.SetFont(font)
        self.execute_btn.SetLabel('Execute load')

        self.execute_btn.Bind(wx.EVT_BUTTON,self.execute_load)

        row_sizer.Add(self.execute_btn,1,wx.ALL,border=30)

        col_sizer.Add(row_sizer,1,wx.EXPAND)


        self.SetSizerAndFit(main_sizer)

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
                field.Disable()
            self.manual_ABI.SetEditable(False)
            self.endpoint_choice.Disable()
            self.endpoint_choice.Clear()
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
                field.Disable()
            self.manual_ABI.SetEditable(False)
            self.endpoint_choice.Disable()
            self.endpoint_choice.Clear()
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
                    self.endpoint_choice.SetStringSelection('Ethereum')
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
        self.Parent.FindWindowById(5).SetValue(self.chains[endpoint]['name']+' '+self.chains[endpoint]['id'])
        self.Parent.FindWindowById(6).SetValue(contract_address)
        self.Parent.FindWindowById(7).SetValue(token_id)
        self.endpoint_choice.SetStringSelection(endpoint)
        self.endpoint_choice.Disable()

        try:
            ABI = self.fetch_ABI(self.abi_urls[endpoint],contract_address,self.api_keys[endpoint])
            self.ABI_chooser.SetStringSelection('Manual')
            self.manual_abi_sizer.Show(0)
            self.manual_abi_sizer.Show(1)
            self.Layout()
            self.manual_ABI.SetValue(ABI)
            response = requests.get(url)
            if response.status_code >= 400:
                raise
            soup = BeautifulSoup(response.text)
        except Exception as e:
            print(f'Exception fetching url: {e}')
            wx.MessageBox(f"Network error in fetching url, please continue input manually or try again.\n\n", "Error" ,wx.OK | wx.ICON_WARNING)
            self.Parent.FindWindowById(8).SetValue('')
            self.Parent.FindWindowById(8).Enable()
            self.Parent.FindWindowById(8).SetEditable(True)            
            return
        # with open('Goo.html') as fp:
        #     soup = BeautifulSoup(fp, 'html.parser')
        divs = soup.find_all("div",{'class':'Blockreact__Block-sc-1xf18x6-0 elqhCm'})
        spans = divs[1].find_all("span")
        metadata_url = spans[4].find_all("a")[0]['href']
        try:
            metadata = requests.get(metadata_url).json()
            self.Parent.FindWindowById(8).SetValue(str(metadata))
        except Exception as e:
            print(f'Exception fetching metadata: {e}')
            wx.MessageBox(f"Network error in fetching Metadata, please input manually or try again.\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_WARNING)
            self.Parent.FindWindowById(8).SetValue('')
            self.Parent.FindWindowById(8).SetEditable(True)

    def fetch_ABI(self,url,contract_address,api_key):
        try:
            response = requests.get(url+f'&address={contract_address}'+f'&apikey={api_key}')
            resp = response.json()['result']
            print(response.status_code)
            if response.status_code >= 400 or 'Invalid' in resp or 'verified' in resp:
                raise Exception('Source not verified or Invalid API key')
            self.manual_ABI.SetEditable(False)
            self.manual_ABI.Disable()
        except Exception as e:
            print(f'Exception fetching ABI: {e}')
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
        d['endpoint'] = self.endpoint_urls[self.endpoint_choice.GetStringSelection()]
        d['chain_id'] = self.chains[self.endpoint_choice.GetStringSelection()]['id']
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
        wx.MessageBox("Card has been loaded with the NFT, it can now be viewed with Cryptnox Gallery.", "Info" ,wx.OK | wx.ICON_INFORMATION)
        wx.CallAfter(self.Parent.Close)

    def get_card(self):
        return cryptnoxpy.factory.get_card(cryptnoxpy.Connection())
        
    
    def validate_fields(self):
        l = []
        for x in range(0,8):
            v = self.Parent.FindWindowById(x+1).GetValue()
            if v == '' or 'Please' in v:
                l.append(self.columns[x])
        if self.manual_ABI.GetValue() == '':
            l.append('ABI')
        if 5 > len(self.Parent.FindWindowById(3).GetValue()) < 9:
            wx.MessageBox("PIN must be more than 5 and less than 9 numeric values", "Error" ,wx.OK | wx.ICON_INFORMATION)
        if len(self.Parent.FindWindowById(4).GetValue()) <= 11:
            wx.MessageBox("PUK must be 12 alphanumeric value", "Error" ,wx.OK | wx.ICON_INFORMATION)
        return l

    def reset_card(self,event):
        try:
            card = self.get_card()
            puk = self.ask(message='Please input your PUK to reset:')
            if puk:
                card.reset(puk)
                wx.MessageBox(f"Card has been reset.", "Info" ,wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error resetting card:\n\nError Information:\n\n{e}", "Error" ,wx.OK | wx.ICON_INFORMATION)
            return

    def ask(parent=None, message=''):
        dlg = wx.TextEntryDialog(parent, message)
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        return result

    def metedata_changed(self,event):
        v = self.Parent.FindWindowById(8).GetValue()
        try:
            metadata_json = eval(v)
            image_url = metadata_json['image_url'] if 'image_url' in metadata_json.keys() else metadata_json['image']
            split_url = image_url.split('/')
            url = f"https://cf-ipfs.com/ipfs/{split_url[-2]}/{split_url[-1]}"
            self.fetch_nft(url)
        except Exception as e:  
            print('Not downloading NFT:{e}')
            pass

    def fetch_nft(self,url):
        print(f'Fetching NFT: {url}')
        header = requests.head(url)
        file_size = int(int(header.headers["content-length"]) / 1024)
        DownloadThread(self,url,file_size=file_size)

    def downloaded(self, data):
        try:
            print(f'Downloaded')
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
        self.Parent.SetSize(1200,1200)
        if nft_type == 'gif':
            ft = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
            ft.write(data)
            ft.flush()
            ft.close()
            self.anim = media.MediaCtrl(self,-1,style=wx.SIMPLE_BORDER,pos=(0,500), size=(500,500))
            self.anim.Bind(media.EVT_MEDIA_LOADED, self.on_media_loaded)
            self.anim.Bind(media.EVT_MEDIA_FINISHED,self.on_media_finished)
            self.anim.Load(ft.name)
            self.col_sizer_2.Add(self.anim, 0, wx.CENTER, 0)
            self.Layout()
        else:
            print('Not gif')
            
    def on_media_loaded(self, event):
        self.anim.Play()

    def on_media_finished(self,event: media.EVT_MEDIA_FINISHED):
        self.anim.Play()

class NFT_Form_App(wx.App):

    def __init__(self):
        super(NFT_Form_App, self).__init__()
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.frame = wx.Frame(None, -1, "NFT CARD MANAGER",pos=((wx.DisplaySize()[0]/2)-325,(wx.DisplaySize()[1]/2)-600),size=(650,1200))
        self.panel = Panel(self.frame, -1)
        self.frame.Show(1)
        self.MainLoop()

def main() -> None:
    app = NFT_Form_App()
    

if __name__ == '__main__':
    main()