# GUI Window Class
# Author: Jeff Vang

import wx;
import json;
import os;

class ProfileWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 250));
        self.setupForm();

        self.Show(True);

    def setupForm(self):
        # Creating menus with event bindings
         # pos(width, height)
        self.panel = wx.Panel(self)
        self.lblname = wx.StaticText(self.panel, pos=(50, 25), label="Enter your profile username: ");
        self.editname = wx.TextCtrl(self.panel, pos=(250, 25), size=(140, -1));
        self.saveButton = wx.Button(self.panel, label="Save Profile", pos=(200, 75));

        self.saveButton.Bind(wx.EVT_BUTTON, self.onSaveProfile);

    def onSaveProfile(self, event=None):
        initProfile = {};
        initProfile['Username'] = "{}".format(self.editname.Value);
        initProfile['Workouts'] = [];

        filename = "./profiles/{}.json".format(self.editname.Value);
        try:
            if not os.path.exists('./profiles'):
                os.makedirs('./profiles', 0o777)

            with open(filename, 'w') as outfile:
                json.dump(initProfile, outfile);
        except EnvironmentError:
            wx.MessageBox('Something went wrong. Could not create profile', 'Info', wx.OK | wx.ICON_INFORMATION);
        finally:
            wx.MessageBox('Profile {} Created!'.format(self.editname.Value), 'Info', wx.OK | wx.ICON_INFORMATION);
            self.Close();