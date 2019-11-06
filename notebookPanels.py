import wx;
import wx.adv;

SUCCESS_ICON = "images/success-icon.jpg"
ERROR_ICON = "images/error-icon.jpg"
class HomePanel(wx.Panel):
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL);
        self.validDuration = False;
        self.validRoutineType = False;
        self.validMuscleGroup = False;
        self.rotate = False;

        # Intro Text
        self.welcomeBox = wx.BoxSizer(wx.HORIZONTAL);
        self.welcomeText = wx.StaticText(self, label="Welcome to Fitness-Trainer", pos=(20,60));
        self.infotext = wx.TextCtrl(self, pos=(20,100), style=wx.TE_MULTILINE|wx.BORDER_NONE|wx.TE_READONLY, size=(930, 100))
        self.infotext.Value = "Fitness Trainer"
        self.welcomeBox.Add(self.welcomeText)
        self.welcomeBox.Add(self.infotext)
        self.vbox.Add(self.welcomeBox);
        # Routine Duration
        self.durationBox = wx.BoxSizer(wx.HORIZONTAL);
        self.routineStartDate = wx.DateTime().Today();
        self.routineEndDate = wx.DateTime().Today();
        self.duration = 0;
        self.selectStartText = wx.StaticText(self, label="Select Start Date.", pos=(20, 280));
        self.calendarStart = wx.adv.DatePickerCtrl(self, id=wx.ID_ANY, dt=self.routineStartDate, pos=(20, 175),
                                            size=(220, 150), name="RoutineStartDate");
        self.startDateText = wx.StaticText(self, label="Start Date: {}".format(wx.DateTime(self.routineStartDate).Format("%B, %D")), pos=(20, 330));
        self.addOneWeek = wx.Button(self, label="Add 1 Week", pos =(20, 360));
        self.addTwoWeeks = wx.Button(self, label="Add 2 Weeks", pos=(120, 360));
        self.customerWeeksText = wx.StaticText(self, label="Number in weeks: ", pos=(20, 400));
        self.customWeekInput = wx.TextCtrl(self, pos=(130, 400), size=(75, 25));
        self.addCustomWeeksBtn = wx.Button(self, label="Add", pos=(220, 400), size=(75, 25));
        self.selectEndText = wx.StaticText(self, label="Select End Date.", pos=(20, 425));
        self.calendarEnd = wx.adv.DatePickerCtrl(self, id=wx.ID_ANY, dt=self.routineEndDate, pos=(20, 425),
                                            size=(220, 50), name="RoutineStartDate");
        self.endDateText = wx.StaticText(self, label="End Date: {}".format(wx.DateTime(self.routineEndDate).Format("%B, %D")), pos=(20, 500));
        self.durationText = wx.StaticText(self, label="Routine Duration: {} Weeks".format(str(self.duration)), pos=(20, 520));

        self.Bind(wx.EVT_BUTTON, lambda event: self.onAddWeeks(event, 1), self.addOneWeek);
        self.Bind(wx.EVT_BUTTON, lambda event: self.onAddWeeks(event, 2), self.addTwoWeeks);
        self.Bind(wx.EVT_BUTTON, lambda event: self.onAddWeeks(event, self.customWeekInput.GetValue()), self.addCustomWeeksBtn);
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.onStartDateSelect, self.calendarStart);
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.onEndDateSelect, self.calendarEnd);

        self.durationBox.Add(self.calendarStart);
        self.durationBox.Add(self.startDateText);
        self.durationBox.Add(self.addOneWeek);
        self.durationBox.Add(self.addTwoWeeks);
        self.durationBox.Add(self.customerWeeksText);
        self.durationBox.Add(self.customWeekInput);
        self.durationBox.Add(self.addCustomWeeksBtn);
        self.durationBox.Add(self.durationText);
        self.durationBox.Add(self.endDateText);
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
        # Rotate Workouts
        self.rotateExercises = wx.CheckBox(self, id= wx.ID_ANY, label="Rotate Exercises", pos=(20, 600))
        self.Bind(wx.EVT_CHECKBOX, self.onRotate, self.rotateExercises)
        # Muscle Group Target Selection
        # self.checkbox.GetCheckedStrings() => Retrieve Muscle Groups from form.
        self.routineMetaBox = wx.BoxSizer(wx.HORIZONTAL);
        self.mGText = wx.StaticText(self, label="Select which muscle groups to target.", pos=(350, 370));
        self.selectAllBtn = wx.Button(self, id=wx.NewId(), label="Select All", pos=(350, 400), size=(100, 25));
        self.deselectAllBtn = wx.Button(self, id=wx.NewId(), label="Deselect All", pos=(450, 400), size=(100, 25));
        self.muscleGroupList = ['Quadriceps', 'Hamstrings', 'Soles']
        self.checkbox = wx.CheckListBox(self, id=wx.NewId(), pos=(350, 430), size=(200, 25*len(self.muscleGroupList)), choices=self.muscleGroupList,
                           style=0);

        self.selectAllBtn.Bind(wx.EVT_BUTTON, self.onSelectAll);
        self.deselectAllBtn.Bind(wx.EVT_BUTTON, self.onDeselectAll);

        self.routineMetaBox.Add(self.mGText);
        self.routineMetaBox.Add(self.selectAllBtn);
        self.routineMetaBox.Add(self.deselectAllBtn);
        self.routineMetaBox.Add(self.checkbox);

        # Form Validation Status
        self.durationValidationText = wx.StaticText(self, label="Routine Duration", pos=(775, 500));
        self.durationValidationText.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.durationValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.durationBmp = wx.StaticBitmap(self, -1, wx.BitmapFromImage(self.durationValidationImage), pos=(925, 495))

        self.typeValidationText = wx.StaticText(self, label="Routine Type", pos=(775, 540));
        self.typeValidationText.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.typeValidationImage = wx.Image(name="images/error-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.typeBmp = wx.StaticBitmap(self, -1, wx.BitmapFromImage(self.typeValidationImage), pos=(925, 535))

        self.muscleValidationText = wx.StaticText(self, label="Muscle Groups", pos=(775, 580));
        self.muscleValidationText.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.muscleValidationImage = wx.Image(name="images/error-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.muscleBmp = wx.StaticBitmap(self, -1, wx.BitmapFromImage(self.muscleValidationImage), pos=(925, 575))

        # Generate Routine Button
        self.generateWorkoutBtn = wx.Button(self, label="Generate Workout", pos =(775, 600), size=(200, 100));
        self.Bind(wx.EVT_BUTTON, self.onGenerate, self.generateWorkoutBtn)
        self.vbox.Add(self.routineMetaBox);
    # Event Handlers
    def onRotate(self, event=None):
        if(self.rotate):
            self.rotate = False;
        else:
            self.rotate = True;
    def onSelectAll(self, event=None):
        self.checkbox.SetCheckedStrings(self.muscleGroupList);
        self.muscleValidationImage = wx.Image(name=SUCCESS_ICON, type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.muscleBmp.SetBitmap(wx.BitmapFromImage(self.muscleValidationImage))
    def onDeselectAll(self, event=None):
        self.checkbox.SetCheckedStrings([]);
        self.muscleValidationImage = wx.Image(name=ERROR_ICON, type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.muscleBmp.SetBitmap(wx.BitmapFromImage(self.muscleValidationImage))
    def onToggleEndurance(self, event=None):
        if(self.toggleEnduranceButton):
            self.toggleEnduranceButton.SetValue(True);
            self.toggleStrengthButton.SetValue(False);
        self.validRoutineType = True;
    def onToggleStrength(self, event=None):
        if(self.toggleStrengthButton):
            self.toggleStrengthButton.SetValue(True)
            self.toggleEnduranceButton.SetValue(False)
        self.validRoutineType = True;
    def onStartDateSelect(self, event=None):
        self.routineStartDate = self.calendarStart.GetValue();
        self.startDateText.SetLabel("Start Date: {}".format(wx.DateTime(self.routineStartDate).Format("%B, %D")))
        self.startDateText.Update();
    def onEndDateSelect(self, event=None):
        startDate = wx.DateTime(self.calendarStart.GetValue());
        endDate = wx.DateTime(self.calendarEnd.GetValue());
        if(startDate < endDate):
            if(endDate.GetYear() == startDate.GetYear()):
                self.duration = (int(endDate.Format("%j")) - int(startDate.Format("%j"))) // 7
                self.days = (int(endDate.Format("%j")) - int(startDate.Format("%j"))) % 7
            elif(endDate.GetYear() - startDate.GetYear() >= 2):
                self.duration = 0
                self.days = 0
                self.durationText.SetLabel(
                    "Routine Duration: {} Weeks, {} Days".format(str(self.duration), str(self.days)));
                self.endDateText.SetForegroundColour(wx.RED)
                self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(endDate).Format("%B, %D")))
                self.durationText.Update();
                self.endDateText.Update();
                return 0;
            else:
                daysLeftInStartYear = 365 - int(startDate.Format("%j"))
                daysSetInEndYear = abs(0 - int(endDate.Format("%j")))
                self.duration = (daysLeftInStartYear + daysSetInEndYear) // 7
                self.days = (daysLeftInStartYear + daysSetInEndYear) % 7

            self.routineEndDate = endDate;
            self.durationText.SetLabel("Routine Duration: {} Weeks, {} Days".format(str(self.duration), str(self.days)));
            self.endDateText.SetForegroundColour(wx.BLACK)
            self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(endDate).Format("%B, %D")))
            self.durationText.Update();
            self.endDateText.Update();
        else:
            self.endDateText.SetForegroundColour(wx.RED)
            self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(endDate).Format("%B, %D")))
            self.endDateText.Update();
    def onAddWeeks(self, event=None, weeks=0):
        self.duration = weeks
        newEndDate = wx.DateTime(self.routineStartDate).Add(wx.DateSpan(weeks=int(self.duration)));
        self.routineEndDate = newEndDate
        self.calendarEnd.SetValue(newEndDate)
        self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(newEndDate).Format("%A, %B %d %G")))
        self.durationText.SetLabel("Routine Duration: {} Weeks".format(str(self.duration)));
        self.durationText.Update();
        self.calendarEnd.Update();
    def onGenerate(self, event=None):
        errors = []
        errorMessage = ""
        if(not self.validRoutineType):
            errors.append("No Routine Type Selected");
        if(not self.validDuration):
            errors.append("Invalid Duration -  See duration parameters for setting a valid date.");
        if(not self.validMuscleGroup):
            errors.append("You must select one or more muscle groups");

        if(len(errors) > 0):
            for error in errors:
                errorMessage += error
            errorDialog = wx.MessageDialog(self, message=errorMessage, caption="Failed to generate workouts")
            errorDialog.ShowModal()

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
