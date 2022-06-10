from threading import Thread
import wx
from pubsub import pub
import cryptnoxpy as cp
import time

class CardCheckThread(Thread):
    def __init__(self,panel: wx.Panel, image_url: str):
        super(CardCheckThread, self).__init__()
        self.panel = panel
        self.start()

    def run(self):
        while self.panel.check_card_run:
            print('Check card running')
            if self.panel.check_card:
                print('Going in')
                try:
                    # if self.panel.check_card:
                    #     print('Check_card: Connection')
                    #     conn = cp.Connection()
                    # if self.panel.check_card:
                    #     print('Check_card: Card')
                    #     card_obj = cp.factory.get_card(conn)
                    if self.panel.check_card:
                        print('Check_card: Init')
                        # cp.factory.get_card(cp.Connection()).check_init()
                    # message = f'🟢 Card found: {card_obj.serial_number}'
                    message = f'Initialized card found'
                except Exception as e:
                    if 'initialized' in str(e):
                        message = '🔴 Uninitialized card found'
                    else:
                        message = '🔴 No card found in reader'
                    wx.CallAfter(pub.sendMessage, "update_status", data=message)
                    time.sleep(0.5)
                    continue
                if self.panel.check_card:
                    print('Check_card: Publish message')
                    wx.CallAfter(pub.sendMessage, "update_status", data=message)
                # print('Deleting check card')
                # del conn
                # del card_obj
                print('sleeping')
                time.sleep(0.5)
            else:
                print('SLEEPING')
                time.sleep(0.5)
        print('Card check end')