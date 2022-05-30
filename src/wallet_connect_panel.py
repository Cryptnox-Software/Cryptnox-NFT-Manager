import wx
from pywalletconnect import WCClient
from utils import confirm,format_checksum_address
import cryptnoxpy
import sha3 as keccak

class WalletConnectPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(WalletConnectPanel,self).__init__(*args, **kw)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        font = wx.Font(13, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        self.blockchains = ['ETH','MATIC']
        self.networks = {
            'ETH':['Mainnet','Rinkeby','Ropsten','Kovan','Goerli'],
            'MATIC':['Mainnet','Mumbai']
        }
        self.account_types = ['Standard','ERC20','Walletconnect']

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Blockchain')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)
        self.blockchain_choice = wx.Choice(self,choices=self.blockchains)
        self.blockchain_choice.Bind(wx.EVT_CHOICE,self.blockchain_chosen)
        row_sizer.Add(self.blockchain_choice,1,wx.ALL,border=5)        

        main_sizer.Add(row_sizer,1,wx.EXPAND)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Network')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5) 
        self.network_choice = wx.Choice(self,choices=[])            
        row_sizer.Add(self.network_choice,1,wx.ALL,border=5)

        main_sizer.Add(row_sizer,1,wx.EXPAND)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Account type')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)
        field = wx.Choice(self,choices=self.account_types)            
        row_sizer.Add(field,1,wx.ALL,border=5)

        main_sizer.Add(row_sizer,1,wx.EXPAND)
        
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self,label='Paste URL')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)
        self.url_field = wx.TextCtrl(self,-1)
        row_sizer.Add(self.url_field,1,wx.ALL,border=5)
        
        main_sizer.Add(row_sizer,1,wx.EXPAND)
        
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        connect_btn = wx.Button(self,label='Connect',size=(150,40))
        connect_btn.Bind(wx.EVT_BUTTON,self.connect_dapp)
        row_sizer.Add(connect_btn,1,wx.ALL,border=5)

        main_sizer.Add(row_sizer,1,wx.EXPAND)

        self.SetSizerAndFit(main_sizer)

    def blockchain_chosen(self,event):
        self.network_choice.SetItems(self.networks[self.blockchain_choice.GetStringSelection()])

    def get_account(self):
        return 

    def connect_dapp(self,event):
        rpc_endpoint = "https://rpc.ankr.com/eth/"
        explorer = "https://etherscan.io/address/0x"
        WALLETCONNECT_PROJID = "5af34a5c60298f270f4281f8bae67f33"
        WALLET_DESCR = {
            "description": "A universal blockchain wallet for cryptos",
            "url": "https://uniblow.org",
            "icons": ["https://uniblow.org/img/uniblow_logo.png"],
            "name": "Uniblow",
        }
        wc_uri = self.url_field.GetValue().strip()
        try:
            card = cryptnoxpy.factory.get_card(cryptnoxpy.Connection())
            pubkey = card.get_public_key().encode('UTF-8')
        except Exception as e:
            print(f'Error getting card: {e}')
            return
        print(pubkey)
        print(pubkey[1:])
        key_hash = keccak.keccak_256(pubkey[1:]).digest()
        eth_address = format_checksum_address(key_hash.hex()[-40:])
        try:
            WCClient.set_wallet_metadata(WALLET_DESCR)
            WCClient.set_project_id(WALLETCONNECT_PROJID)
            self.wc_client = WCClient.from_wc_uri(wc_uri)
            req_id, req_chain_id, request_info = self.wc_client.open_session()
            relay = self.wc_client.get_relay_url()
        except Exception as e:
            print(f'Exception initializing WCClient: \n{e}')
        request_message = f"WalletConnect request from :\n\n{request_info['name']}\n\nwebsite  :  {request_info['url']}\nRelay URL : {relay}\n"
        approve = confirm(self,request_message)
        if approve:
            self.wc_client.reply_session_request(req_id, 1, f"0x{eth_address}")
            wx.MessageBox('Wallet has been connected, please continue transaction in DAPP.')
        else:
            self.wc_client.reject_session_request(req_id)
            self.wc_client.close()
            wx.MessageBox('Walletconnect request has been cancelled.')