# GUI Window Class
# Author: Jeff Vang

import wx;
import ProfileWindow;
import json;
import os;
import HomePanel;
import RoutinePanel;
import NotesPanel;
import SettingsPanel;

class MainWindow(wx.Frame):
    def __init__(self, parent, title, active_user, routines):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 750));
        self.active_user = active_user;
        self.routines = routines
        self.active_routine = routines[0] if len(routines) > 0 else None;

        self.setupMenuBar();

        self.createNoteBook();

        self.Show(True);

    def createNoteBook(self):
        self.nb = wx.Notebook(self)
        self.homePage = HomePanel.HomePanel(self.nb)
        self.nb.AddPage(self.homePage, "Home")
        self.routinePage = RoutinePanel.RoutinePanel(self.nb);
        self.nb.AddPage(self.routinePage, "Routines")
        self.notesPage = NotesPanel.NotesPanel(self.nb)
        self.nb.AddPage(self.notesPage, "Notes")
        self.settingsPage = SettingsPanel.SettingsPanel(self.nb)
        self.nb.AddPage(self.settingsPage, "Settings")

        # Binding method listener to set routine when note page has changed
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChangeListener, self.nb)

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

        # Create Routine Menus if any exists under set profile
        routineTab = wx.Menu();
        # if there is no active routine, there are no routines to iterate over
        if(type(self.active_routine) != type(None)):
            for routine in self.routines:
                routineOption = routineTab.Append(wx.NewId(), "&{}".format(routine["routineName"]), "Change to Routine {}".format(routine["routineName"]));
                self.Bind(wx.EVT_MENU, self.OnSwitchRoutine, routineOption);
            self.windowMenuBar.Append(routineTab, self.active_routine["routineName"]);

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
        self.active_user = obj.GetLabel(menuId).replace("&", "");
        self.windowMenuBar.SetMenuLabel(3, self.active_user);

        # Remove routines if there were any before we switch users
        if len(self.windowMenuBar.GetMenus()) > 4:
            self.windowMenuBar.Remove(4);

        # Get Home Page, we need to revalidate routine name if a user has entered a routine name
        homePage = self.nb.GetPage(0)
        homePage.routineName.SetValue("")
        # Load new user existing routines
        with open('./profiles/{}.json'.format(self.active_user), 'r') as userjson:
            userData = json.load(userjson)
            if(len(userData["Routines"]) > 0):
                self.routines = userData["Routines"]
                self.active_routine = self.routines[0]

                # Dyanmically generate new routines menu if routines exist for user
                routineTab = wx.Menu();
                for routine in self.routines:
                    routineOption = routineTab.Append(wx.NewId(), "&{}".format(routine["routineName"]),
                                                      "Change to Routine {}".format(routine["routineName"]));
                    self.Bind(wx.EVT_MENU, self.OnSwitchRoutine, routineOption);
                self.windowMenuBar.Append(routineTab, self.active_routine["routineName"]);

            else:
                # No routines, clear active statuses
                self.routines = []
                self.active_routine = None


    # Menu Event Handler
    def OnSwitchRoutine(self, event=None):
        # Switch Current Active Routine
        menuId = event.GetId()
        obj = event.GetEventObject()
        routineName = obj.GetLabel(menuId).replace("&", "");
        with open("profiles/{}.json".format(self.active_user), 'r') as outfile:
            userWorkouts = json.load(outfile);
            routines = userWorkouts["Routines"]
        workouts = []
        # Set active routine to routine object
        for routine in routines:
            if routine["routineName"] == routineName:
                self.active_routine = routine
                # Change Routine View
                sessions = self.active_routine["sessions"]
                for session in sessions:
                    workouts.extend(session["workouts"])
                self.routinePage.routineView.SetObjects(workouts)

        self.windowMenuBar.SetMenuLabel(4, routineName);


    # Menu Event Handler
    def onLightTheme(self, event=None):
        self.SetBackgroundColour(wx.Colour(255, 255, 255));

    # Menu Event Handler
    def onDarkTheme(self, event=None):
        self.SetBackgroundColour(wx.Colour(43, 45, 46));
        self.Update();
        self.Show(True);

    # Routine Event Handler
    def onPageChangeListener(self, event=None):
        page = event.GetEventObject()
        activePage = page.GetPageText(page.GetSelection())
        switch = {
            "Home": self.homePage,
            "Routines": self.routinePage,
            "Notes": self.notesPage,
            "Settings": self.settingsPage
        }
        listener = switch.get(activePage, lambda: "")
        listener.onPageChangeListener();


