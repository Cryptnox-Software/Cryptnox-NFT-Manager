import wx
from pywalletconnect import WCClient
from utils import *
import cryptnoxpy
from pyweb3 import Web3Client

class WalletConnectPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(WalletConnectPanel,self).__init__(*args, **kw)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        font = wx.Font(13, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        self.ERC20 = None
        self.blockchains = ['ETH','MATIC']
        self.networks = {
            'ETH':['Mainnet','Rinkeby','Ropsten','Kovan','Goerli'],
            'MATIC':['Mainnet','Mumbai']
        }
        self.chain_ids = {
            'ETH':
                {
                    'Mainnet':1,
                    'Ropsten':3,
                    'Rinkeby':4,
                    'Goerli':5,
                    'Kovan':42
                },
            'MATIC':
                {
                    'Mainnet':1,
                    'Ropsten':3,
                    'Rinkeby':4,
                    'Goerli':5,
                    'Kovan':42
                }
                         }
        self.account_types = ['Standard','ERC20','Walletconnect']
        self.wc_timer = None

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

    def erase_info(self):
        if self.wc_timer:
            self.wc_client.close()
            self.wc_timer.Stop()

    def watch_messages(self):
        try:
            self.get_messages()
        except Exception as e:
            print(f'Exception watching messages: {e}')

    def process_sign_message(self, data_hex):
        print('Gonna Process sign message')
        MESSAGE_HEADER = b"\x19Ethereum Signed Message:\n"
        """Process a WalletConnect personal_sign and eth_sign call"""
        # sign(keccak256("\x19Ethereum Signed Message:\n" + len(message) + message)))
        data_bin = bytes.fromhex(data_hex[2:])
        msg_header = MESSAGE_HEADER + str(len(data_bin)).encode("ascii")
        sign_request = (
            "WalletConnect signature request :\n\n"
            f"- Data to sign (hex) :\n"
            f"- {data_hex}\n"
            f"\n Data to sign (ASCII/UTF8) :\n"
        )
        try:
            sign_request += f" {data_bin.decode('utf8')}\n"
        except UnicodeDecodeError:
            sign_request += " <can't decode sign data to text>"
        hash2_data = sha2(data_bin).hex().upper()
        sign_request += f"\n Hash data to sign (hex) :\n {hash2_data}\n"
        sign_request += USER_SCREEN
        if confirm(self,sign_request) == 5100:
            hash_sign = sha3(msg_header + data_bin)
            print(hash_sign)
            der_signature = self.card.sign(hash_sign,pin=self.pin)
            print(der_signature)
            print(self.card.get_public_key().encode('UTF-8'))
            return encode_datasign(hash_sign, der_signature,self.card.get_public_key().encode('UTF-8'))

    def get_messages(self):
        print(f'Getting messages')
        wc_message = self.wc_client.get_message()
        while wc_message[0] is not None:
            id_request = wc_message[0]
            method = wc_message[1]
            parameters = wc_message[2]
            print(f"WC request id: {id_request}, method: {method}, params: {parameters}")
            if method == "wc_sessionPayload":
                # Read if WCv2 and extract to v1
                print("WCv2 request")
                if parameters.get("request"):
                    print("request decoding")
                    method = parameters["request"].get("method")
                    parameters = parameters["request"].get("params")
                    print(f"Actual method: {method}, params: {parameters}")
            if method == "wc_sessionUpdate":
                if parameters[0].get("approved") is False:
                    raise Exception("Disconnected by the web app service.")
            if method == "wc_sessionDelete":
                if parameters.get("reason"):
                    raise Exception(
                        "Disconnected by the web app service.\n"
                        f"Reason : {parameters['reason']['message']}"
                    )
            elif method == "personal_sign" and len(parameters) > 1:
                if compare_eth_addresses(parameters[1], self.get_account()):
                    signature = self.process_sign_message(parameters[0])
                    if signature is not None:
                        self.wc_client.reply(id_request, f"0x{signature.hex()}")
            elif method == "eth_sign" and len(parameters) > 1:
                if compare_eth_addresses(parameters[0], self.get_account()):
                    signature = self.process_sign_message(parameters[1])
                    if signature is not None:
                        self.wc_client.reply(id_request, f"0x{signature.hex()}")
            elif method == "eth_signTypedData" and len(parameters) > 1:
                if compare_eth_addresses(parameters[0], self.get_account()):
                    signature = self.process_sign_typeddata(parameters[1])
                    if signature is not None:
                        self.wc_client.reply(id_request, f"0x{signature.hex()}")
            elif method == "eth_sendTransaction" and len(parameters) > 0:
                # sign and sendRaw
                tx_obj_tosign = parameters[0]
                if compare_eth_addresses(tx_obj_tosign["from"], self.get_account()):
                    tx_signed = self.process_signtransaction(tx_obj_tosign)
                    if tx_signed is not None:
                        tx_hash = self.broadcast_tx(tx_signed)
                        self.wc_client.reply(id_request, tx_hash)
            elif method == "eth_signTransaction" and len(parameters) > 0:
                tx_obj_tosign = parameters[0]
                if compare_eth_addresses(tx_obj_tosign["from"], self.get_account()):
                    tx_signed = self.process_signtransaction(tx_obj_tosign)
                    if tx_signed is not None:
                        self.wc_client.reply(id_request, f"0x{tx_signed}")
            elif method == "eth_sendRawTransaction" and len(parameters) > 0:
                tx_data = parameters[0]
                tx_hash = self.broadcast_tx(tx_data)
                self.wc_client.reply(id_request, tx_hash)
            print("WC command processing finished, now reading next available message.")
            wc_message = self.wc_client.get_message()

    def process_signtransaction(self, txdata):
        GWEI_DECIMALS = 9
        GAZ_LIMIT_ERC_20_TX = 180000
        """Build a signed tx, for WalletConnect eth_sendTransaction and eth_signTransaction call"""
        to_addr = txdata.get("to", "  New contract")[2:]
        value = txdata.get("value", 0)
        if value != 0:
            value = int(value, 16)
        gas_price = txdata.get("gasPrice", 0)
        if gas_price != 0:
            gas_price = int(gas_price, 16)
        else:
            gas_price = self.eth.api.get_gasprice()
        gas_limit = txdata.get("gas", GAZ_LIMIT_ERC_20_TX)
        if gas_limit != GAZ_LIMIT_ERC_20_TX:
            gas_limit = int(gas_limit, 16)
        request_message = (
            "WalletConnect transaction request :\n\n"
            f" To    :  0x{to_addr}\n"
            f" Value :  {balance_string(value , self.eth.decimals)} {self.coin}\n"
            f" Gas price  : {balance_string(gas_price, GWEI_DECIMALS)} Gwei\n"
            f" Gas limit  : {gas_limit}\n"
            f"Max fee cost: {balance_string(gas_limit*gas_price, self.eth.decimals)} {self.coin}\n"
        )
        request_message += USER_SCREEN
        if confirm(self,request_message) == 5100:
            data_hex = txdata.get("data", "0x")
            data = bytearray.fromhex(data_hex[2:])
            return self.build_tx(value, gas_price, gas_limit, to_addr, data)

    def prepare(self, toaddr, paymentvalue, gprice, glimit, data=bytearray(b"")):
        """Build a transaction to be signed.
        toaddr in hex without 0x
        value in wei, gprice in Wei
        """
        if self.ERC20:
            maxspendable = self.getbalance(False)
            balance_eth = self.getbalance()
            if balance_eth < (gprice * glimit):
                raise Exception("Not enough native ETH funding for the tx fee")
        else:
            maxspendable = self.getbalance() - (gprice * glimit)
        if paymentvalue > maxspendable or paymentvalue < 0:
            if self.ERC20:
                sym = self.token_symbol
            else:
                sym = "native ETH"
            raise Exception(f"Not enough {sym} tokens for the tx")
        self.nonce = int2bytearray(self.getnonce())
        self.gasprice = int2bytearray(gprice)
        self.startgas = int2bytearray(glimit)
        if self.ERC20:
            self.to = bytearray.fromhex(self.ERC20[2:])
            self.value = int2bytearray(int(0))
            self.data = bytearray.fromhex(TRANSFERT_FUNCTION + "00" * 12 + toaddr) + uint256(
                paymentvalue
            )
        else:
            self.to = bytearray.fromhex(toaddr)
            self.value = int2bytearray(int(paymentvalue))
            self.data = data
        v = int2bytearray(self.chainID)
        r = int2bytearray(0)
        s = int2bytearray(0)
        signing_tx = rlp_encode(
            [
                self.nonce,
                self.gasprice,
                self.startgas,
                self.to,
                self.value,
                self.data,
                v,
                r,
                s,
            ]
        )
        self.datahash = sha3(signing_tx)
        return (signing_tx, self.datahash)

    def build_tx(self, amount, gazprice, ethgazlimit, account, data=None):
        """Build and sign a transaction.
        Used to transfer tokens native or ERC20 with the given parameters.
        """
        if data is None:
            data = bytearray(b"")
        tx_bin, hash_to_sign = self.prepare(account, amount, gazprice, ethgazlimit, data)
        if self.current_device.has_screen:
            if self.ERC20 and self.ledger_tokens_compat:
                # Token known by Ledger ?
                ledger_info = self.ledger_tokens.get(self.eth.ERC20)
                if ledger_info:
                    # Known token : provide the trusted info to the device
                    name = ledger_info["ticker"]
                    data_sig = ledger_info["signature"]
                    self.card.register_token(
                        name, self.ERC20[2:], self.decimals, self.chainID, data_sig
                    )
            vrs = self.card.sign(tx_bin)
            return add_vrs(vrs)
        tx_signature = self.card.sign(hash_to_sign)
        return add_signature(tx_signature)

    def get_decimals(self):
        if self.ERC20:
            balraw = self.api.call(self.ERC20, DECIMALS_FUNCTION)
            if balraw == [] or balraw == "0x":
                return 1
            return int(balraw[2:], 16)
        return ETH_DECIMALS

    def get_account(self):
        return f"0x{self.eth_address}"

    def connect_dapp(self,event):
        INFURA_KEY = 'ac389dd3ded74e4a85cc05c8927825e8'
        self.decimals = self.get_decimals()
        self.network = self.network_choice.GetStringSelection().lower().strip()
        print(self.network)
        self.chainID = self.chain_ids[self.blockchain_choice.GetStringSelection()][self.network_choice.GetStringSelection()]
        if self.network == 'mainnet':
            rpc_endpoint = "https://rpc.ankr.com/eth/"
            explorer = "https://etherscan.io/address/0x"
        else:
            rpc_endpoint = f"https://{self.network}.infura.io/v3/{INFURA_KEY}"
            explorer = f"https://{self.network}.etherscan.io/address/0x"
        WALLETCONNECT_PROJID = "5af34a5c60298f270f4281f8bae67f33"
        WALLET_DESCR = {
            "description": "A universal blockchain wallet for cryptos",
            "url": "https://uniblow.org",
            "icons": ["https://uniblow.org/img/uniblow_logo.png"],
            "name": "Uniblow",
        }
        wc_uri = self.url_field.GetValue().strip()
        try:
            self.pin = ask(message='Please input your card PIN:')
            self.card = cryptnoxpy.factory.get_card(cryptnoxpy.Connection())
            self.card.verify_pin(self.pin)
            pubkey = self.card.get_public_key().encode('UTF-8')
            print(rpc_endpoint)
            self.api = Web3Client(rpc_endpoint, "Uniblow/1")
        except cryptnoxpy.exceptions.PinException:
            print(f'Invalid PIN')
            wx.MessageBox('The PIN entered was incorrect, please try again.')
            return
        except Exception as e:
            print(f'Error getting card: {e}')
            wx.MessageBox(f'Error getting card, please ensure device is connected.\n{e}')
            return
        print(pubkey)
        print(pubkey[1:])
        key_hash = sha3(pubkey[1:])
        self.eth_address = format_checksum_address(key_hash.hex()[-40:])
        try:
            WCClient.set_wallet_metadata(WALLET_DESCR)
            WCClient.set_project_id(WALLETCONNECT_PROJID)
            self.wc_client = WCClient.from_wc_uri(wc_uri)
            req_id, req_chain_id, request_info = self.wc_client.open_session()
        except Exception as e:
            print(f'Exception opening session: {e}')
            if 'timeout' in str(e):
                wx.MessageBox('Session timeout, please try again.')
            else:
                wx.MessageBox(f'WC Network exception: \n{e}\nPlease try again.')
            return
        relay = self.wc_client.get_relay_url()
        request_message = f"WalletConnect request from :\n\n{request_info['name']}\n\nwebsite  :  {request_info['url']}\nRelay URL : {relay}\n"
        approve = confirm(self,request_message)
        if approve:
            self.wc_client.reply_session_request(req_id, self.chainID, f"0x{self.eth_address}")
            wx.MessageBox('Wallet has been connected, please continue transaction in DAPP.')
            self.erase_info()
            self.wc_timer = wx.Timer()
            self.wc_timer.Notify = self.watch_messages
            self.wc_timer.Start(2500, oneShot=wx.TIMER_CONTINUOUS)
        else:
            self.wc_client.reject_session_request(req_id)
            self.wc_client.close()
            wx.MessageBox('Walletconnect request has been cancelled.')