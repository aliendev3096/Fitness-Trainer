import wx;

class HomePanel(wx.Panel):
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL);

        self.welcomeBox = wx.BoxSizer(wx.HORIZONTAL);
        self.welcomeText = wx.StaticText(self, label="Welcome to Fitness-Trainer", pos=(20,60));
        self.welcomeBox.Add(self.welcomeText)

        self.routineMetaBox = wx.BoxSizer(wx.HORIZONTAL);
        self.mGText = wx.StaticText(self, label="Select which muscle groups to target.", pos=(20, 370));
        self.selectAllBtn = wx.Button(self, id=wx.NewId(), label="Select All", pos=(20, 400), size=(100, 25));
        self.deselectAllBtn = wx.Button(self, id=wx.NewId(), label="Deselect All", pos=(120, 400), size=(100, 25));
        self.selectAllBtn.Bind(wx.EVT_BUTTON, self.onSelectAll);
        self.deselectAllBtn.Bind(wx.EVT_BUTTON, self.onDeselectAll);
        self.muscleGroupList = ['Quadriceps', 'Hamstrings', 'Soles']
        self.cbox = wx.CheckListBox(self, id=wx.NewId(), pos=(20, 450), size=(200, 25*len(self.muscleGroupList)), choices=self.muscleGroupList,
                           style=wx.RA_SPECIFY_ROWS);
        self.routineMetaBox.Add(self.mGText);
        self.routineMetaBox.Add(self.selectAllBtn);
        self.routineMetaBox.Add(self.deselectAllBtn);
        self.routineMetaBox.Add(self.cbox);

        self.vbox.Add(self.routineMetaBox);
    def onSelectAll(self, event=None):
        self.cbox.SetCheckedStrings(self.muscleGroupList);
    def onDeselectAll(self, event=None):
        self.cbox.SetCheckedStrings([]);


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
