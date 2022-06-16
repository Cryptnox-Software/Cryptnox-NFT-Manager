import wx
from pywalletconnect import WCClient
from utils import *
import cryptnoxpy
from pyweb3 import Web3Client
import json

class WalletConnectPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(WalletConnectPanel,self).__init__(*args, **kw)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        self.GWEI_DECIMALS = 9
        self.GAZ_LIMIT_ERC_20_TX = 180000
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
                    'Mainnet':137,
                    'Ropsten':80001
                }
                         }
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
        text = wx.StaticText(self,label='Paste URL')
        text.SetFont(font)
        row_sizer.Add(text,1,wx.ALL,border=5)
        self.url_field = wx.TextCtrl(self,-1)
        row_sizer.Add(self.url_field,1,wx.ALL,border=5)
        
        main_sizer.Add(row_sizer,1,wx.EXPAND)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_text = wx.StaticText(self,label='🔴 Not connected')
        self.status_text.SetFont(font)

        row_sizer.Add(self.status_text,1,wx.ALL,border=5)

        main_sizer.Add(row_sizer,1,wx.EXPAND)
        
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        connect_btn = wx.Button(self,label='Connect',size=(150,40))
        connect_btn.Bind(wx.EVT_BUTTON,self.connect_dapp)

        row_sizer.Add(connect_btn,1,wx.ALL,border=5)

        self.disconnect_btn = wx.Button(self,label='Disconnect',size=(150,40))
        self.disconnect_btn.Bind(wx.EVT_BUTTON,self.disconnect_dapp)
        self.disconnect_btn.Disable()
        
        row_sizer.Add(self.disconnect_btn,1,wx.ALL,border=5)

        main_sizer.Add(row_sizer,1,wx.EXPAND)

        self.SetSizerAndFit(main_sizer)

    def blockchain_chosen(self,event):
        self.network_choice.SetItems(self.networks[self.blockchain_choice.GetStringSelection()])

    def erase_info(self):
        print('Erasing info')
        self.wc_client.close()
        self.wc_timer.Stop()
        del self.wc_client
        del self.wc_timer
        self.Parent.Refresh()
            

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
        print(f'SigningDataHex: {data_hex}')
        print(type(data_hex))
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
            print(self.card.get_public_key(hexed=False))
            return encode_datasign(hash_sign, der_signature,self.card.get_public_key(hexed=False))

    def get_messages(self):
        print(f'Getting messages')
        wc_message = self.wc_client.get_message()
        while wc_message[0] is not None:
            id_request = wc_message[0]
            method = wc_message[1]
            parameters = wc_message[2]
            try:
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
            except Exception as e:
                if 'Disconnected' in str(e):
                    self.erase_info()
                    self.status_text.SetLabel('🔴 Not connected')
                    self.status_text.SetForegroundColour('white')
                    self.disconnect_btn.Disable()
                    wx.MessageBox(f'WalletConnect session has been disconnected.')
                else:
                    wx.MessageBox(f'Something went wrong: {e}')

    def process_sign_typeddata(self, data_bin):
        print('ProcessSignTypeData')
        """Process a WalletConnect eth_signTypedData call"""
        EIP712_HEADER = b"\x19\x01"
        data_obj = json.loads(data_bin)
        chain_id = None
        if "domain" in data_obj and "chainId" in data_obj["domain"]:
            print('IFone')
            chain_id = data_obj["domain"]["chainId"]
            if isinstance(chain_id, str) and chain_id.startswith("eip155:"):
                chain_id = int(chain_id[7:])
        # Silent ignore when chain ids mismatch
        if chain_id is not None and self.chainID != data_obj["domain"]["chainId"]:
            print("Wrong chain id in signedTypedData")
            return None
        print('Prepare typed sign hash')
        hash_domain, hash_data = typed_sign_hash(data_obj)
        print('Preparing sign request')
        sign_request = (
            "WalletConnect signature request :\n\n"
            f"- Data to sign (typed) :\n"
            f"{print_text_query(data_obj)}"
            f"\n - Hash domain (hex) :\n"
            f" 0x{hash_domain.hex().upper()}\n"
            f"\n - Hash data (hex) :\n"
            f" 0x{hash_data.hex().upper()}\n"
        )
        sign_request += USER_SCREEN
        if confirm(self,sign_request) == 5100:
            hash_sign = sha3(EIP712_HEADER + hash_domain + hash_data)
            der_signature = self.card.sign(hash_sign,pin=self.pin)
            return self.encode_datasign(hash_sign, der_signature)

    def encode_datasign(self, datahash, signature_der):
        print('EncodeDataSign')
        """Encode a message signature from the DER sig."""
        # Signature decoding
        lenr = int(signature_der[3])
        lens = int(signature_der[5 + lenr])
        r = int.from_bytes(signature_der[4 : lenr + 4], "big")
        s = int.from_bytes(signature_der[lenr + 6 : lenr + 6 + lens], "big")
        # Parity recovery
        v = 27
        h = int.from_bytes(datahash, "big")
        print(self.pubkey)
        if public_key_recover(h, r, s, v) != self.pubkey:
            v += 1
        # Signature encoding
        return uint256(r) + uint256(s) + bytes([v])

    def broadcast_tx(self, txdata):
        """Broadcast and return the tx hash as 0xhhhhhhhh"""
        return self.send(txdata)

    def send(self, tx_hex):
        """Upload the tx"""
        return self.api.pushtx(tx_hex)

    def process_signtransaction(self, txdata):
        print('ProcessSignTransaction')
        """Build a signed tx, for WalletConnect eth_sendTransaction and eth_signTransaction call"""
        to_addr = txdata.get("to", "  New contract")[2:]
        value = txdata.get("value", 0)
        if value != 0:
            value = int(value, 16)
        gas_price = txdata.get("gasPrice", 0)
        if gas_price != 0:
            gas_price = int(gas_price, 16)
        else:
            gas_price = self.api.get_gasprice()
        gas_limit = txdata.get("gas", self.GAZ_LIMIT_ERC_20_TX)
        if gas_limit != self.GAZ_LIMIT_ERC_20_TX:
            gas_limit = int(gas_limit, 16)
        request_message = (
            "WalletConnect transaction request :\n\n"
            f" To    :  0x{to_addr}\n"
            f" Value :  {balance_string(value , self.decimals)} {self.blockchain_choice.GetStringSelection()}\n"
            f" Gas price  : {balance_string(gas_price, self.GWEI_DECIMALS)} Gwei\n"
            f" Gas limit  : {gas_limit}\n"
            f"Max fee cost: {balance_string(gas_limit*gas_price, self.decimals)} {self.blockchain_choice.GetStringSelection()}\n"
        )
        request_message += USER_SCREEN
        if confirm(self,request_message) == 5100:
            data_hex = txdata.get("data", "0x")
            data = bytearray.fromhex(data_hex[2:])
            return self.build_tx(value, gas_price, gas_limit, to_addr, data)

    def getbalance(self, native=True):
        print('Getbalance')
        BALANCEOF_FUNCTION = "70a08231"
        block_state = "latest"
        if native:
            # ETH native balance
            return self.api.get_balance(f"0x{self.eth_address}", block_state)
        # ERC20 token balance
        balraw = self.api.call(
            self.ERC20,
            BALANCEOF_FUNCTION,
            f"000000000000000000000000{self.address}",
            block_state,
        )
        if balraw == [] or balraw == "0x":
            return 0
        balance = int(balraw[2:], 16)
        return balance

    def getnonce(self):
        print('GetNonce')
        numtx = self.api.get_tx_num(self.eth_address, "pending")
        return numtx

    def prepare(self, toaddr, paymentvalue, gprice, glimit, data=bytearray(b"")):
        print('Prepare')
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
        tx_signature = self.card.sign(hash_to_sign,pin=self.pin)
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

    def disconnect_dapp(self,event):
        self.erase_info()
        self.status_text.SetLabel('🔴 Not connected')
        self.status_text.SetForegroundColour('white')
        self.disconnect_btn.Disable()
        wx.MessageBox('Walletconnect has been disconnected.')

    def connect_dapp(self,event):
        INFURA_KEY = 'ac389dd3ded74e4a85cc05c8927825e8'
        self.decimals = self.get_decimals()
        self.network = self.network_choice.GetStringSelection().lower().strip()
        print(self.network)
        self.chainID = self.chain_ids[self.blockchain_choice.GetStringSelection()][self.network_choice.GetStringSelection()]
        if self.blockchain_choice.GetStringSelection() == 'ETH':
            if self.network == 'mainnet':
                rpc_endpoint = f"https://rpc.ankr.com/eth/"
                self.explorer = "https://etherscan.io/address/0x"
            else:
                rpc_endpoint = f"https://{self.network}.infura.io/v3/{INFURA_KEY}"
                self.explorer = f"https://{self.network}.etherscan.io/address/0x"
        else:
            if self.network == 'mainnet':
                rpc_endpoint = "https://rpc.ankr.com/polygon/"
                self.explorer = "https://polygonscan.com/address/0x"
            else:
                rpc_endpoint = "https://matic-mumbai.chainstacklabs.com/"
                self.explorer = "https://mumbai.polygonscan.com/address/0x"
        WALLETCONNECT_PROJID = "5af34a5c60298f270f4281f8bae67f33"
        WALLET_DESCR = {
            "description": "A universal blockchain wallet for cryptos",
            "url": "https://uniblow.org",
            "icons": ["https://uniblow.org/img/uniblow_logo.png"],
            "name": "Uniblow",
        }
        wc_uri = self.url_field.GetValue().strip()
        try:
            pin_result = ask(message='Please input your card PIN:\nFor default PIN\'000000000\', press enter.')
            self.pin = '000000000' if pin_result == '' else pin_result
            self.card = cryptnoxpy.factory.get_card(cryptnoxpy.Connection())
            self.card.verify_pin(self.pin)
            self.pubkey = self.card.get_public_key(hexed=False)
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
        key_hash = sha3(self.pubkey[1:])
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
            self.wc_timer = wx.Timer()
            self.wc_timer.Notify = self.watch_messages
            self.wc_timer.Start(2500, oneShot=wx.TIMER_CONTINUOUS)
            self.status_text.SetLabel('🟢 Connected to DAPP')
            self.status_text.SetForegroundColour('green')
            self.url_field.SetValue('')
            self.disconnect_btn.Enable()
        else:
            self.wc_client.reject_session_request(req_id)
            self.wc_client.close()
            wx.MessageBox('Walletconnect request has been cancelled.')