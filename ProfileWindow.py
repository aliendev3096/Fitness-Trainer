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

        self.editname = wx.TextCtrl(panel)
        sizer.Add(self.editname, pos=(1, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        self.buttonOk = wx.Button(panel, label="Ok", size=(90, 28))
        self.buttonOk.Bind(wx.EVT_BUTTON, self.onSaveProfile);
        self.buttonClose = wx.Button(panel, label="Close", size=(90, 28))
        self.buttonClose.Bind(wx.EVT_BUTTON, self.onClose);
        sizer.Add(self.buttonOk, pos=(3, 3))
        sizer.Add(self.buttonClose, pos=(3, 4), flag=wx.RIGHT | wx.BOTTOM, border=10)

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

    def onClose(self, event=None):
        self.Close();

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
                json.dump("", dboutfile);

        except EnvironmentError:
            wx.MessageBox('Something went wrong. Could not create profile', 'Info', wx.OK | wx.ICON_INFORMATION);
        finally:
            mainWindow = self.GetParent()
            profileMenu = mainWindow.windowMenuBar.GetMenu(3)
            # Add new user to menu
            profileTab = profileMenu.Append(wx.NewId(), "&{}".format(self.editname.Value),
                "Change to Routine {}".format(self.editname.Value));
            mainWindow.Bind(wx.EVT_MENU, mainWindow.OnSwitchUser, profileTab);

            # Remove routine, new user would not have any
            mainWindow.windowMenuBar.Remove(4)

            profileMenu.SetTitle(self.editname.Value)
            mainWindow.active_user = self.editname.Value
            mainWindow.active_routine = []

            wx.MessageBox('Profile {} Created!'.format(self.editname.Value), 'Info', wx.OK | wx.ICON_INFORMATION);
            self.Close();

    def onDeleteProfile(self, event=None):

        try:
            os.remove('./profiles/{}.json'.format(self.nameToBeDeleted.Value))
            os.remove('./db/{}-notes.txt'.format(self.nameToBeDeleted.Value))

            mainWindow = self.GetParent()
            profileMenu = mainWindow.windowMenuBar.GetMenu(3)
            menuItems = profileMenu.GetMenuItems()
            for menuItem in menuItems:
                menuName = menuItem.GetItemLabel().replace("&", "")
                if menuName == self.nameToBeDeleted.Value:
                    profileMenu.Remove(menuItem)
                    nextExistingUser = menuItems[0].GetItemLabel().replace("&", "")
                    profileMenu.SetTitle(nextExistingUser)

                    # Load existing user
                    with open('./profiles/{}.json'.format(nextExistingUser), 'r') as userjson:
                        userData = json.load(userjson)
                        userData["Routines"];

                    mainWindow.active_user = nextExistingUser
                    mainWindow.active_routine = userData["Routines"][0]
            # Remove routines if there were any
            if len(mainWindow.windowMenuBar.GetMenus()) > 4:
                mainWindow.windowMenuBar.Remove(4);

        except EnvironmentError:
            wx.MessageBox('Something went wrong. Could not delete profile', 'Info', wx.OK | wx.ICON_INFORMATION);
        finally:
            wx.MessageBox('Profile {} Deleted!'.format(self.nameToBeDeleted.Value), 'Info', wx.OK | wx.ICON_INFORMATION);
            self.Close();