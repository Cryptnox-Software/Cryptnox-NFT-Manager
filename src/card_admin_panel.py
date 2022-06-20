import wx
from utils import get_cryptnox_card,ask,checksum_address
import cryptnoxpy
import json
import gzip
from pathlib import Path
import qrcode

class CardAdminPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(CardAdminPanel,self).__init__(*args, **kw)
        self.SetBackgroundColour('black')
        self.SetForegroundColour('white')
        font = wx.Font(11, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #PIN
        pin_sizer = wx.BoxSizer(wx.VERTICAL)
        
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_text = wx.StaticText(self,-1,label="PIN",size=(150,23),style=wx.ALIGN_CENTER)
        title_text.SetFont(font)
        test_pin = wx.Button(self,-1,label="Test PIN",size=(100,30))
        test_pin.Bind(wx.EVT_BUTTON,self.test_pin)
        change_pin = wx.Button(self,-1,label="Change PIN",size=(100,30))
        change_pin.Bind(wx.EVT_BUTTON,self.change_card_pin)
        row_sizer.Add(test_pin,0,wx.ALL,border=5)
        row_sizer.Add(change_pin,0,wx.ALL,border=5)
        
        pin_sizer.Add(title_text,0,wx.ALIGN_CENTER)
        pin_sizer.AddSpacer(30)
        pin_sizer.Add(row_sizer,0)


        main_sizer.Add(pin_sizer,0)
        main_sizer.AddSpacer(100)

        #PUK
        puk_sizer = wx.BoxSizer(wx.VERTICAL)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_text = wx.StaticText(self,-1,label="PUK",size=(150,23),style=wx.ALIGN_CENTER)
        title_text.SetFont(font)
        test_puk = wx.Button(self,-1,label="Test PUK",size=(100,30))
        test_puk.Bind(wx.EVT_BUTTON,self.test_puk)
        change_puk = wx.Button(self,-1,label="Change PUK",size=(100,30))
        change_puk.Bind(wx.EVT_BUTTON,self.change_card_puk)
        row_sizer.Add(test_puk,0,wx.ALL,border=5)
        row_sizer.Add(change_puk,0,wx.ALL,border=5)

        puk_sizer.Add(title_text,0,wx.ALIGN_CENTER)
        puk_sizer.AddSpacer(30)
        puk_sizer.Add(row_sizer,0)


        main_sizer.Add(puk_sizer,0)
        main_sizer.AddSpacer(100)


        #Export
        data_sizer = wx.BoxSizer(wx.VERTICAL)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_text = wx.StaticText(self,-1,label="Data",size=(150,23),style=wx.ALIGN_CENTER)
        title_text.SetFont(font)
        view_data = wx.Button(self,-1,label="View data",size=(100,30))
        view_data.Bind(wx.EVT_BUTTON,self.view_card_data)
        export_data = wx.Button(self,-1,label="Export data",size=(100,30))
        export_data.Bind(wx.EVT_BUTTON,self.export_card_data)
        row_sizer.Add(view_data,0,wx.ALL,border=5)
        row_sizer.Add(export_data,0,wx.ALL,border=5)

        data_sizer.Add(title_text,0,wx.ALIGN_CENTER)
        data_sizer.AddSpacer(30)
        data_sizer.Add(row_sizer,0)
    
        main_sizer.Add(data_sizer,0)

        self.SetSizerAndFit(main_sizer)

    def test_pin(self,event):
        print(f'Test pin')
        pin_result = ask(message='Please input PIN to test for validity:')
        if type(pin_result) != str:
            return
        try:
            int(pin_result)
            if len(pin_result) > 3 and len(pin_result) < 10:
                wx.MessageBox('The entered PIN is valid for use.')
            else:
                raise Exception('Invalid Length')
        except Exception as e:
            wx.MessageBox('The pin must have between 4 and 9 numeric characters')
        
        

    def test_puk(self,event):
        print(f'Test puk')
        puk_result = ask(message='Please input PUK to test for validity:')
        if type(puk_result) != str:
            return
        if len(puk_result) != 12:
            wx.MessageBox('The PUK must have 12 letters or number characters')
        else:
            wx.MessageBox('The entered PUK is valid for use')
        

    def change_card_pin(self,event):
        print(f'Change card pin')
        card = get_cryptnox_card()
        if card:
            try:
                card.check_init()
                pin_result = ask(message='Please input your card PIN:\nFor EASY MODE PIN\'000000000\', press enter.')
                if type(pin_result) != str:
                    return
                pin = '000000000' if pin_result == '' else pin_result
                card.verify_pin(pin)
                new_pin_result = ask(message='Please input new PIN:\nFor EASY MODE PIN\'000000000\', press enter.')
                if type(new_pin_result) != str:
                    return
                new_pin = '000000000' if new_pin_result == '' else new_pin_result
                card.change_pin(new_pin)
            except Exception as e:
                if 'initialized' in str(e):
                    wx.MessageBox("Card is not initialized\n\nPlease initialize the card for use.")
                elif 'Invalid PIN' in str(e):
                    wx.MessageBox("Invalid PIN code provided\n\n Please try again.")
                else:
                    wx.MessageBox(str(e))
                return
            wx.MessageBox('Card PIN has been changed successfully.')
        else:
            wx.MessageBox("Card not found\n\nPlease ensure device is properly connected.")

    def change_card_puk(self,event):
        print(f'Change card puk')
        card = get_cryptnox_card()
        if card:
            try:
                card.check_init()
                puk_result = ask(message='Please input your card PUK:\nFor EASY MODE PUK\'000000000000\', press enter.')
                if type(puk_result) != str:
                    return
                puk = '000000000000' if puk_result == '' else puk_result
                new_puk_result = ask(message='Please input new card PUK:\nFor EASY MODE PUK\'000000000000\', press enter.')
                if type(new_puk_result) != str:
                    return
                new_puk = '000000000000' if new_puk_result == '' else new_puk_result
                card.change_puk(puk,new_puk)
            except Exception as e:
                if 'initialized' in str(e):
                    wx.MessageBox("Card is not initialized\n\nPlease initialize the card for use.")
                else:
                    wx.MessageBox(str(e))
                return
            wx.MessageBox('Card PUK has been changed successfully.')
        else:
            wx.MessageBox("Card not found\n\nPlease ensure device is properly connected.")

    def view_card_data(self,event):
        print(f'View card data')
        card = get_cryptnox_card()
        if card:
            try:
                card.check_init()
                data = []
                for i in range(0,4):
                    data.append(gzip.decompress(card.user_data[i]))
                data = [json.loads(x.decode('UTF-8')) if x != b'' else '' for x in data]
                dialog_data = data[0]
                dialog_data['image'] = data[3]['image'] if 'image' in data[3].keys() else data[3]['image_url']
                dialog_data['serial'] = card.serial_number
                public_key = card.get_public_key()
                dialog_data['address'] = checksum_address(public_key)
                print(dialog_data)
                ViewDataDialog(self,'NFT Card Data',dialog_data)
            except Exception as e:
                if 'initialized' in str(e):
                    wx.MessageBox("Card is not initialized\n\nPlease initialize the card for use.")
                elif 'Connection' in str(e):
                    wx.MessageBox("Connection issue\n\nPlease ensure device is properly connected and/or try again.")
                else:
                    wx.MessageBox(str(e))
        else:
            wx.MessageBox("Card not found\n\nPlease ensure device is properly connected.")

    def export_card_data(self,event):
        print(f'Export card data')



class ViewDataDialog(wx.Dialog):
    def __init__(self, parent, title,view_data):
        super(ViewDataDialog,self).__init__(parent,title=title)
        self.SetBackgroundColour('white')
        self.SetForegroundColour('black')

        LK = {
            'Card serial':'serial',
            'Address':'address',
            'Contract address':'contract_address',
            'Endpoint':'endpoint',
            'Chain ID':'chain_id',
            'NFT ID':'nft_id',
            'Image':'image'
            }

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        path = Path(__file__).parent.joinpath("logo.png").absolute()
        img = wx.Image(str(path),wx.BITMAP_TYPE_PNG)
        img_size = (50,50)
        img = img.Scale(int(img_size[0]),int(img_size[1]),wx.IMAGE_QUALITY_HIGH)
        img = img.ConvertToBitmap()
        image = wx.StaticBitmap(self, wx.ID_ANY, img, (0,0))

        main_sizer.Add(image,0,wx.ALIGN_CENTER_HORIZONTAL)

        main_sizer.Add(wx.StaticLine(self,-1,style=wx.LI_HORIZONTAL),0)

        for k,v in LK.items():
            main_sizer.Add(wx.StaticText(self,-1,label=k),0,wx.LEFT,border=10)
            main_sizer.Add(wx.StaticText(self,-1,label=str(view_data[v])),0,wx.LEFT | wx.RIGHT,border=10)
            main_sizer.AddSpacer(10)
            if v == 'address':
                main_sizer.Add(wx.StaticText(self,-1,label="Address (QR Code)"),0,wx.LEFT,border=10)

                obj_qr = qrcode.QRCode(  
                    version = 1,  
                    error_correction = qrcode.constants.ERROR_CORRECT_L,  
                    box_size = 10,  
                    border = 4,  
                )
                obj_qr.add_data(view_data[v])
                obj_qr.make(fit = True)
                qr_img = obj_qr.make_image(fill_color = "black", back_color = "white").tobytes()
                img = wx.Image(size=(50,50),data=qr_img)
                print('converting to bitmap')
                img = img.ConvertToBitmap()
                image = wx.StaticBitmap(self, wx.ID_ANY, img, (0,0))

                main_sizer.Add(image,0,wx.LEFT,border=10)
                main_sizer.AddSpacer(10)

        self.SetSizerAndFit(main_sizer)
        self.ShowModal()
