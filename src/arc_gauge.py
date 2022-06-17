import wx
import math

class ArcGauge(wx.Gauge):

    def __init__(self,*args, **kwargs):
        super(ArcGauge, self).__init__(*args, **kwargs)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.lineWidth = 0
        self.min = 0
        self.max = 360
        self._value = 0
        self.setText = '100%'
        self.position = wx.Rect()  # self.position.Set(x, y, width, height)
        self.startPoint = math.radians(90)
        self.endPoint = math.radians(450)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetForegroundColour('white')

    def setRange(self, min, max):
        self.min = min
        self.max = max
        if self._value < self.min:
            self._value = self.min
        elif self._value > self.max:
            self._value = self.max
        self.Refresh(False)

    def setValue(self, val):
        if self._value != val:
            if val < self.min:
                self._value = self.min
            elif val > self.max:
                self._value = self.max
            else:
                self._value = val
        else:
            print('Not value')
        self.Refresh()

    def OnPaint(self, event=None):
        dc = wx.AutoBufferedPaintDC(self)
        self.DrawText(dc)
        gc = self.MakeGC(dc)
        self.Draw(gc)
        # text_dc = wx.AutoBufferedPaintDC(self)
        # self.DrawText(text_dc)

    def MakeGC(self, dc):
        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            dc.DrawText("This build of wxPython does not support the wx.GraphicsContext "
                        "family of classes.",
                        25, 25)
            return None
        return gc

    def DrawText(self,text_dc):
        #percentage text
        brush = wx.Brush('black')
        text_dc.SetBackground(brush)
        text_dc.Clear()
        text = f"{round((self._value/self.max)*100)}%"
        font = wx.Font(15,wx.ROMAN,wx.NORMAL,wx.NORMAL)
        text_dc.SetFont(font)
        text_dc.DrawText(text, ((self.Size[0]/2)-10),  ((self.Size[1]/2)-5))

    def Draw(self, gc):
        
        #middle progressbar line
        radStart = math.radians(90)
        radEnd = math.radians(450)
        path = gc.CreatePath()
        path.AddArc(80, 80, 50, radStart, radEnd, True)
        pen = wx.Pen('#696969', 15)
        pen.SetCap(wx.CAP_BUTT)
        gc.SetPen(pen)
        gc.SetBrush(wx.Brush('#000000', wx.TRANSPARENT))
        gc.DrawPath(path)

        #progress bar
        start = math.radians(90)
        #r = math.radians(270)
        arcStep = (360 / (self.max - self.min) * self._value)+90
        end = math.radians(arcStep)
        path = gc.CreatePath()
        path.AddArc(80, 80, 50, start, end, True)
        pen = wx.Pen('#FFFFFF', 15)
        pen.SetCap(wx.CAP_BUTT)
        gc.SetPen(pen)
        gc.SetBrush(wx.Brush('#000000', wx.TRANSPARENT))
        gc.DrawPath(path)
        
        gc.SetPen(wx.Pen('#FFFFFF',1))

        