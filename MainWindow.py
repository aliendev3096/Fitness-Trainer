# GUI Window Class
# Author: Jeff Vang

import wx;
import AddProfileWindow;

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 750));
        self.setupMenuBar();

        self.Show(True);

    def setupMenuBar(self):
        # Creating menus with event bindings
        fileTab = wx.Menu();
        fileSaveOption = fileTab.Append(wx.ID_FILE, "&Save Profile", "Save Profile");
        self.Bind(wx.EVT_MENU, self.OnSaveProfile, fileSaveOption);
        fileExportOption = fileTab.Append(wx.ID_FILE, "&Export", "Export Weekly Routine");
        self.Bind(wx.EVT_MENU, self.OnExport, fileExportOption);
        fileQuitOption = fileTab.Append(wx.ID_FILE, "&Quit", "Quit PyExFitness");
        self.Bind(wx.EVT_MENU, self.OnFileQuit, fileQuitOption);

        profileTab = wx.Menu();
        profileAddUser = profileTab.Append(wx.ID_ADD, "&Add Profile", "Add User Profile");
        self.Bind(wx.EVT_MENU, self.OnAddProfile, profileAddUser);

        windowMenuBar = wx.MenuBar();
        windowMenuBar.Append(fileTab, "File");
        windowMenuBar.Append(profileTab, "Profile");
        self.SetMenuBar(windowMenuBar);
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
        profileFrame = AddProfileWindow.ProfileWindow(self, "Add Profile");

