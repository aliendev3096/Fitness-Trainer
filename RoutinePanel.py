import wx;

class RoutinePanel(wx.Panel):
    def __init__(self, parent):
        super(RoutinePanel, self).__init__(parent)
        lblList = ['Value X', 'Value Y', 'Value Z']
        rbox = wx.RadioBox(self, label='RadioBox', pos=(25, 10), choices=lblList,
                           majorDimension=1, style=wx.RA_SPECIFY_ROWS);