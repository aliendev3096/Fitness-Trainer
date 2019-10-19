# GUI Window Class
# Author: Jeff Vang

import wx;
import AddProfileWindow;
import json;
import os;

class MainWindow(wx.Frame):
    def __init__(self, parent, title, active_user):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 750));
        # Need to create this despite it being created in for loop below. Unsure Why. Not a guarentee it will be created.
        self.active_user = active_user;
        self.setupMenuBar();

        self.Show(True);

    def setupMenuBar(self):
        # Creating menus with event bindings
        # Create File Menu
        fileTab = wx.Menu();
        fileSaveOption = fileTab.Append(wx.NewId(), "&Save Profile", "Save Profile");
        self.Bind(wx.EVT_MENU, self.OnSaveProfile, fileSaveOption);
        fileExportOption = fileTab.Append(wx.NewId(), "&Export", "Export Weekly Routine");
        self.Bind(wx.EVT_MENU, self.OnExport, fileExportOption);
        fileQuitOption = fileTab.Append(wx.NewId(), "&Quit", "Quit PyExFitness");
        self.Bind(wx.EVT_MENU, self.OnFileQuit, fileQuitOption);

        # Create Profile Menu
        profileTab = wx.Menu();
        profileAddUser = profileTab.Append(wx.NewId(), "&Add Profile", "Add User Profile");
        self.Bind(wx.EVT_MENU, self.OnAddProfile, profileAddUser);

        # Create User Menu
        userTab = wx.Menu();
        userProfiles = os.listdir('./profiles');
        for profile in userProfiles:
            username = profile.replace('.json', '');
            usernameOption = userTab.Append(wx.NewId(), "&{}".format(username), "Change to User {}".format(username));
            self.Bind(wx.EVT_MENU, self.OnSwitchUser, usernameOption);

        # Create Full Menu Bar
        self.windowMenuBar = wx.MenuBar();
        self.windowMenuBar.Append(fileTab, "File");
        self.windowMenuBar.Append(profileTab, "Profile");
        self.windowMenuBar.Append(userTab, self.active_user);
        self.SetMenuBar(self.windowMenuBar);

    # Menu Event Handler
    def OnFileQuit(self, event=None):
        self.Close();

    # Menu Event Handler
    def OnSaveProfile(self, event=None):
        self.Close();

    # Menu Event Handler
    def OnExport(self, event=None):
        self.Close();

    # Menu Event Handler
    def OnAddProfile(self, event=None):
        # Open New Sub Window to Add Profile
        print("Adding Profile")
        profileFrame = AddProfileWindow.ProfileWindow(self, "Add Profile");
        profileFrame.Open();

    # Menu Event Handler
    def OnSwitchUser(self, event=None):
        # Switch Current Active User
        menuId = event.GetId()
        obj = event.GetEventObject()
        self.active_user = obj.GetLabel(menuId);
        self.windowMenuBar.SetMenuLabel(2, self.active_user);

