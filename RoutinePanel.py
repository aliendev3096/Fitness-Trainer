import wx;
from ObjectListView import ObjectListView, ColumnDefn

class RoutinePanel(wx.Panel):
    def __init__(self, parent):
        super(RoutinePanel, self).__init__(parent)
        # Set Sizers
        self.routineViewSizer = wx.BoxSizer(wx.VERTICAL)

        self.active_routine = self.GetParent().GetParent().active_routine

        if self.active_routine is not None:
            self.sessions = self.active_routine["sessions"]
        else:
            self.sessions = []

        self.routineView = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        self.routineView.SetColumns([
            ColumnDefn("Workout Name", "left", 220, "workoutName"),
            ColumnDefn("Target", "left", 200, "muscleGroup"),
            ColumnDefn("Weight", "left", 180, "weight"),
            ColumnDefn("Variations", "left", 180, "variations"),
            ColumnDefn("Sets", "right", 100, "sets"),
            ColumnDefn("Reps", "left", 180, "reps")
        ])

        self.routineView.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

        self.routineViewSizer.Add(self.routineView, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.routineViewSizer)
        self.routineView.Show()

    # Routine Event Handler
    def onPageChangeListener(self, event=None):
        # Clear the routines
        self.sessions = []
        self.active_routine = self.GetParent().GetParent().active_routine
        # if active routine is set, generate list
        if self.active_routine is not None:
            sessions = self.active_routine["sessions"]

            # For each session, append the workouts
            for session in sessions:
                self.sessions.extend(session["workouts"])

            self.routineView.SetObjects(self.sessions)


