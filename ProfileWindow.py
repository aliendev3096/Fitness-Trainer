# GUI Window Class
# Author: Jeff Vang

import wx;
import json;
import os;


class ProfileWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 150));

    def OpenAddProfileScreen(self):
        self.setupAddForm();
        self.Show(True);

    def OpenDeleteProfileScreen(self):
        self.setupRemoveForm();
        self.Show(True);

    def setupAddForm(self):
        # Creating menus with event bindings
         # pos(width, height)
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(4, 4)

        text = wx.StaticText(panel, label="Add Profile")
        sizer.Add(text, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        tc = wx.TextCtrl(panel)
        sizer.Add(tc, pos=(1, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        buttonOk = wx.Button(panel, label="Ok", size=(90, 28))
        buttonClose = wx.Button(panel, label="Close", size=(90, 28))
        sizer.Add(buttonOk, pos=(3, 3))
        sizer.Add(buttonClose, pos=(3, 4), flag=wx.RIGHT | wx.BOTTOM, border=10)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        panel.SetSizer(sizer)

    def setupRemoveForm(self):
        # Creating menus with event bindings
        # pos(width, height)
        self.panel = wx.Panel(self)
        self.lblname = wx.StaticText(self.panel, pos=(50, 25), label="Enter your profile username: ");
        self.nameToBeDeleted = wx.TextCtrl(self.panel, pos=(250, 25), size=(140, -1));
        self.deleteButton = wx.Button(self.panel, label="Delete Profile", pos=(200, 75));

        self.deleteButton.Bind(wx.EVT_BUTTON, self.onDeleteProfile);

    def onSaveProfile(self, event=None):
        initProfile = {};
        initProfile['Username'] = "{}".format(self.editname.Value);
        initProfile['Routines'] = [];

        filename = "./profiles/{}.json".format(self.editname.Value);
        dbfilename = "./db/{}-notes.txt".format(self.editname.Value)
        try:
            if not os.path.exists('./profiles'):
                os.makedirs('./profiles', 0o777)

            with open(filename, 'w') as outfile:
                json.dump(initProfile, outfile);

            # Generate User Notes
            with open(dbfilename, 'w') as dboutfile:
                json.dump({}, dboutfile);

        except EnvironmentError:
            wx.MessageBox('Something went wrong. Could not create profile', 'Info', wx.OK | wx.ICON_INFORMATION);
        finally:
            wx.MessageBox('Profile {} Created!'.format(self.editname.Value), 'Info', wx.OK | wx.ICON_INFORMATION);
            self.Close();

    def onDeleteProfile(self, event=None):

        try:
            os.remove('./profiles/{}.json'.format(self.nameToBeDeleted.Value))
        except EnvironmentError:
            wx.MessageBox('Something went wrong. Could not delete profile', 'Info', wx.OK | wx.ICON_INFORMATION);
        finally:
            wx.MessageBox('Profile {} Deleted!'.format(self.nameToBeDeleted.Value), 'Info', wx.OK | wx.ICON_INFORMATION);
            self.Close();