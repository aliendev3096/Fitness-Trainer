# GUI Window Class
# Author: Jeff Vang

import wx;
import ProfileWindow;
import json;
import os;

class MainWindow(wx.Frame):
    def __init__(self, parent, title, active_user):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 750));
        self.panel = wx.Panel(self)
        self.active_user = active_user;
        self.setupMenuBar();

        self.Show(True);

    def setupMenuBar(self):
        # Creating menus with event bindings
        # Create File Menu
        fileTab = wx.Menu();
        fileExportOption = fileTab.Append(wx.NewId(), "&Export", "Export Weekly Routine");
        self.Bind(wx.EVT_MENU, self.OnExport, fileExportOption);
        fileQuitOption = fileTab.Append(wx.NewId(), "&Quit", "Quit PyExFitness");
        self.Bind(wx.EVT_MENU, self.OnFileQuit, fileQuitOption);

        # Create Profile Menu
        profileTab = wx.Menu();
        profileAddUser = profileTab.Append(wx.NewId(), "&Add Profile", "Add User Profile");
        profileDeleteUser = profileTab.Append(wx.NewId(), "&Delete Profile", "Delete User Profile");
        self.Bind(wx.EVT_MENU, self.OnAddProfile, profileAddUser);
        self.Bind(wx.EVT_MENU, self.OnDeleteProfile, profileDeleteUser);

        # Create Theme Menu
        themeTab = wx.Menu();
        lightTheme = themeTab.Append(wx.NewId(), "&Light Theme", "Light Theme");
        darkTheme = themeTab.Append(wx.NewId(), "&Dark Theme", "Dark Theme");
        self.Bind(wx.EVT_MENU, self.onLightTheme, lightTheme);
        self.Bind(wx.EVT_MENU, self.onDarkTheme, darkTheme);

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
        self.windowMenuBar.Append(themeTab, "Theme");
        self.windowMenuBar.Append(userTab, self.active_user);
        self.SetMenuBar(self.windowMenuBar);

    # Menu Event Handler
    def OnFileQuit(self, event=None):
        self.Close();

    # Menu Event Handler
    def OnExport(self, event=None):
        self.Close();

    # Menu Event Handler
    def OnAddProfile(self, event=None):
        # Open New Sub Window to Add Profile
        profileFrame = ProfileWindow.ProfileWindow(self, "Add Profile");
        profileFrame.OpenAddProfileScreen();
    # Menu Event Handler
    def OnDeleteProfile(self, event=None):
        # Open New Sub Window to Delete Profile
        profileFrame = ProfileWindow.ProfileWindow(self, "Delete Profile");
        profileFrame.OpenDeleteProfileScreen();

    # Menu Event Handler
    def OnSwitchUser(self, event=None):
        # Switch Current Active User
        menuId = event.GetId()
        obj = event.GetEventObject()
        self.active_user = obj.GetLabel(menuId);
        self.windowMenuBar.SetMenuLabel(3, self.active_user);

    # Menu Event Handler
    def onLightTheme(self, event=None):
        self.SetBackgroundColour(wx.Colour(255, 255, 255));

    # Menu Event Handler
    def onDarkTheme(self, event=None):
        self.SetBackgroundColour(wx.Colour(43, 45, 46));
        self.Update();
        self.Show(True);

