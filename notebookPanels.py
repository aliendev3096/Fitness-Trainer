import wx;
import wx.adv;

class HomePanel(wx.Panel):
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL);

        # Intro Text
        self.welcomeBox = wx.BoxSizer(wx.HORIZONTAL);
        self.welcomeText = wx.StaticText(self, label="Welcome to Fitness-Trainer", pos=(20,60));
        self.welcomeBox.Add(self.welcomeText)
        self.vbox.Add(self.welcomeBox);
        # Routine Duration
        self.durationBox = wx.BoxSizer(wx.HORIZONTAL);
        self.mGText = wx.StaticText(self, label="Select Start Date.", pos=(20, 280));
        self.calendarStart = wx.adv.DatePickerCtrl(self, id=wx.ID_ANY, dt=wx.DateTime().Today(), pos=(20, 175),
                                            size=(220, 150), name="RoutineStartDate");
        self.Bind(wx.adv.EVT_CALENDAR_WEEKDAY_CLICKED, self.onStartDateSelect, self.calendarStart);
        self.durationBox.Add(self.calendarStart);
        self.vbox.Add(self.durationBox);
        # Routine Type
        self.routineTypeBox = wx.BoxSizer(wx.HORIZONTAL);
        self.toggleEnduranceButton = wx.ToggleButton(self, label="Endurance Focused", pos =(350, 300));
        self.toggleStrengthButton = wx.ToggleButton(self, label="Strength Focused", pos =(500, 300));
        self.routineTypeText = wx.StaticText(self, label="Select Workout Focus", pos=(350, 280));
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleEndurance, self.toggleEnduranceButton);
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleStrength, self.toggleStrengthButton);
        self.routineTypeBox.Add(self.toggleEnduranceButton);
        self.routineTypeBox.Add(self.toggleStrengthButton);
        self.vbox.Add(self.routineTypeBox);
        # Rotate Workouts?

        #
        # Muscle Group Target Selection
        # self.checkbox.GetCheckedStrings() => Retrieve Muscle Groups from form.
        self.routineMetaBox = wx.BoxSizer(wx.HORIZONTAL);
        self.mGText = wx.StaticText(self, label="Select which muscle groups to target.", pos=(350, 370));
        self.selectAllBtn = wx.Button(self, id=wx.NewId(), label="Select All", pos=(350, 400), size=(100, 25));
        self.deselectAllBtn = wx.Button(self, id=wx.NewId(), label="Deselect All", pos=(450, 400), size=(100, 25));
        self.selectAllBtn.Bind(wx.EVT_BUTTON, self.onSelectAll);
        self.deselectAllBtn.Bind(wx.EVT_BUTTON, self.onDeselectAll);
        self.muscleGroupList = ['Quadriceps', 'Hamstrings', 'Soles']
        self.checkbox = wx.CheckListBox(self, id=wx.NewId(), pos=(350, 430), size=(200, 25*len(self.muscleGroupList)), choices=self.muscleGroupList,
                           style=0);
        self.routineMetaBox.Add(self.mGText);
        self.routineMetaBox.Add(self.selectAllBtn);
        self.routineMetaBox.Add(self.deselectAllBtn);
        self.routineMetaBox.Add(self.checkbox);

        # Generate Routine Button

        self.vbox.Add(self.routineMetaBox);
    # Event Handlers
    def onSelectAll(self, event=None):
        self.checkbox.SetCheckedStrings(self.muscleGroupList);
    def onDeselectAll(self, event=None):
        self.checkbox.SetCheckedStrings([]);
    def onToggleEndurance(self, event=None):
        if(self.toggleEnduranceButton):
            self.toggleEnduranceButton.SetValue(True);
            self.toggleStrengthButton.SetValue(False);
    def onToggleStrength(self, event=None):
        if(self.toggleStrengthButton):
            self.toggleStrengthButton.SetValue(True)
            self.toggleEnduranceButton.SetValue(False)
    def onStartDateSelect(self, event=None):
        pass




class RoutinePanel(wx.Panel):
    def __init__(self, parent):
        super(RoutinePanel, self).__init__(parent)
        lblList = ['Value X', 'Value Y', 'Value Z']
        rbox = wx.RadioBox(self, label='RadioBox', pos=(25, 10), choices=lblList,
                           majorDimension=1, style=wx.RA_SPECIFY_ROWS);

class NotesPanel(wx.Panel):
    def __init__(self, parent):
        super(NotesPanel, self).__init__(parent)
        text = wx.TextCtrl(self, pos=(0,0), style=wx.TE_MULTILINE, size=(980, 675))
class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super(SettingsPanel, self).__init__(parent)
        lblList = ['Value X', 'Value Y', 'Value Z']
        rbox = wx.RadioBox(self, label='RadioBox', pos=(25, 10), choices=lblList,
                           majorDimension=1, style=wx.RA_SPECIFY_ROWS);
