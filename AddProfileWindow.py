# GUI Window Class
# Author: Jeff Vang

import wx;


class ProfileWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 500));
        self.setupForm();

        self.Show(True);

    def setupForm(self):
        # Creating menus with event bindings
        fileTab = wx.Menu();




