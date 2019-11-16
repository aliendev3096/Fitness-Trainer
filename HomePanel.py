import wx;
import wx.adv;

SUCCESS_ICON = "images/success-icon.jpg"
ERROR_ICON = "images/error-icon.jpg"
class HomePanel(wx.Panel):
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL);
        # Form Validations
        self.validDuration = False;
        self.validRoutineType = False;
        self.validMuscleGroup = False;
        self.rotate = False;
        self.validScheduleType = False;

        # Intro Text
        self.welcomeBox = wx.BoxSizer(wx.HORIZONTAL);
        description = "This application is not intended to help with weight loss. " \
                              "The purpose of Dynamite Fit is to provide a feeling for diverse \n workouts to help you on your " \
                              "journey to healthiness. If you are limited in anyway to perform any of these workouts, please do not feel " \
                              "obligated to \n do them as there are plenty of other workouts to choose from. " \
                              "For the purpose of simplicity, Dynamite Fit generates workout only up to a year \n from the start date, " \
                              "although this is not recommended. \n" \
                              "** To Begin, please provide the following: start date, end date, workout routine type and which muscle groups you with " \
                              "to target. ** \n" \
                              "Workouts brought to you by: https://exrx.net/"
        self.welcomeText = wx.StaticText(self, label="Welcome to Dynamite Fit", pos=(20,60));
        self.infotext = wx.StaticText(self, label=description, pos=(20,80), style=wx.TE_MULTILINE|wx.BORDER_NONE|wx.TE_READONLY, size=(930, 130))
        self.welcomeBox.Add(self.welcomeText)
        self.welcomeBox.Add(self.infotext)
        self.vbox.Add(self.welcomeBox);
        # Routine Duration
        self.durationBox = wx.BoxSizer(wx.HORIZONTAL);
        self.routineStartDate = wx.DateTime().Today();
        self.routineEndDate = wx.DateTime().Today();
        self.duration = 0;
        self.selectStartText = wx.StaticText(self, label="Select Start Date.", pos=(20, 200));
        self.calendarStart = wx.adv.DatePickerCtrl(self, id=wx.ID_ANY, dt=self.routineStartDate, pos=(20, 100),
                                            size=(220, 150), name="RoutineStartDate");
        self.startDateText = wx.StaticText(self, label="Start Date: {}".format(wx.DateTime(self.routineStartDate).Format("%B, %D")), pos=(20, 260));
        self.addOneWeek = wx.Button(self, label="1 Week", pos =(20, 300));
        self.addTwoWeeks = wx.Button(self, label="2 Weeks", pos=(120, 300));
        self.customWeeksText = wx.StaticText(self, label="Number in weeks: ", pos=(20, 340));
        self.customWeekInput = wx.Choice(self, pos=(140, 340), size=(75, 25), choices=["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]);
        self.selectEndText = wx.StaticText(self, label="Select End Date.", pos=(20, 380));
        self.calendarEnd = wx.adv.DatePickerCtrl(self, id=wx.ID_ANY, dt=self.routineEndDate, pos=(20, 380),
                                            size=(220, 50), name="RoutineStartDate");
        self.endDateText = wx.StaticText(self, label="End Date: {}".format(wx.DateTime(self.routineEndDate).Format("%B, %D")), pos=(20, 440));
        self.durationText = wx.StaticText(self, label="Routine Duration: {} Weeks".format(str(self.duration)), pos=(20, 460));

        self.Bind(wx.EVT_BUTTON, lambda event: self.onAddWeeks(event, 1), self.addOneWeek);
        self.Bind(wx.EVT_BUTTON, lambda event: self.onAddWeeks(event, 2), self.addTwoWeeks);
        self.Bind(wx.EVT_CHOICE, lambda event: self.onAddWeeks(event, int(self.customWeekInput.GetSelection())), self.customWeekInput);
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.onStartDateSelect, self.calendarStart);
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.onEndDateSelect, self.calendarEnd);

        self.durationBox.Add(self.calendarStart);
        self.durationBox.Add(self.startDateText);
        self.durationBox.Add(self.addOneWeek);
        self.durationBox.Add(self.addTwoWeeks);
        self.durationBox.Add(self.customWeeksText);
        self.durationBox.Add(self.customWeekInput);
        self.durationBox.Add(self.durationText);
        self.durationBox.Add(self.endDateText);
        self.vbox.Add(self.durationBox);
        # Routine Type
        self.routineTypeBox = wx.BoxSizer(wx.HORIZONTAL);
        self.toggleEnduranceButton = wx.ToggleButton(self, label="Endurance Focused", pos =(650, 230));
        self.toggleStrengthButton = wx.ToggleButton(self, label="Strength Focused", pos =(790, 230));
        self.routineTypeText = wx.StaticText(self, label="Select Workout Focus", pos=(650, 210));

        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleEndurance, self.toggleEnduranceButton);
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleStrength, self.toggleStrengthButton);

        self.routineTypeBox.Add(self.toggleEnduranceButton);
        self.routineTypeBox.Add(self.toggleStrengthButton);
        self.vbox.Add(self.routineTypeBox);
        # Routine Schedule
        self.routineScheduleBox = wx.BoxSizer(wx.HORIZONTAL);
        self.toggleBalanced = wx.ToggleButton(self, label="Balance Groups", pos =(650, 280));
        self.togglePriority = wx.ToggleButton(self, label="Prioritize Groups", pos =(770, 280));
        self.routineScheduleText = wx.StaticText(self, label="Select Muscle Group Ordering", pos=(650, 260));
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleBalanced, self.toggleBalanced);
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onTogglePriority, self.togglePriority);

        self.routineScheduleBox.Add(self.toggleBalanced);
        self.routineScheduleBox.Add(self.togglePriority);

        # Routine Schedule Details
        self.amountOfWorkouts = 4
        self.routineDetailsText = wx.StaticText(self, label="How many workouts/day?", pos=(650, 320));
        self.customDetailsInput = wx.Choice(self, pos=(820, 320), size=(75, 25), choices=["1", "2", "3", "4", "5", "6", "7", "8"]);
        self.customDetailsInput.SetSelection(self.amountOfWorkouts-1)
        self.Bind(wx.EVT_CHOICE, self.onChoice, self.customDetailsInput)
        # Rotate Workouts
        self.rotateExercises = wx.CheckBox(self, id= wx.ID_ANY, label="Rotate Exercises", pos=(20, 600))
        self.Bind(wx.EVT_CHECKBOX, self.onRotate, self.rotateExercises)
        rotateStaticText = "* Rotating workouts will ensure you don't perform the same workouts every week."
        self.rotateText = wx.StaticText(self, label=rotateStaticText,  pos=(20,630), style=wx.TE_MULTILINE|wx.BORDER_NONE|wx.TE_READONLY, size=(930, 100))
        # Muscle Group Target Selection
        self.routineMetaBox = wx.BoxSizer(wx.HORIZONTAL);
        self.mGText = wx.StaticText(self, label="Select which muscle groups to target.", pos=(350, 210));
        self.selectAllBtn = wx.Button(self, id=wx.NewId(), label="Select All", pos=(350, 230), size=(100, 25));
        self.deselectAllBtn = wx.Button(self, id=wx.NewId(), label="Deselect All", pos=(450, 230), size=(100, 25));
        self.muscleGroupList = ['Quadriceps',
                                "Gluteus Maximus",
                                "Anterior Deltoid",
                                "Lateral Deltoid",
                                "Posterior Deltoid",
                                "Supraspinatus",
                                'Hamstrings',
                                'Soles',
                                'General Back',
                                'Latissimus Dorsi',
                                'Trapezius',
                                'Infraspinatus',
                                'Subscapularis',
                                "Pectorlis Major-Sternal",
                                "Pectoralis Minor",
                                "Pectorlis Major-Clavicular",
                                "Brachioradialis",
                                "Wrist Flexors",
                                "Pronators",
                                "Supinators",
                                "Adductors",
                                "Rectus Femoris",
                                "Triceps Brachii",
                                "Biceps Brachii",
                                "Rectus Abdominis",
                                "Obliques",
                                "Erector Spinae"
                                 ]
        self.checkBoxList = []
        self.selectedMuscleGroups = [];
        self.muscleGroupList.sort();
        spacer = 270;
        spacer_2 = 270;
        top_half = len(self.muscleGroupList)//2;
        for muscle in self.muscleGroupList[0:top_half]:
            cb = checkbox = wx.CheckBox(self, id=wx.ID_ANY, label=muscle, pos=(330, spacer), name=muscle)
            self.Bind(wx.EVT_CHECKBOX, self.onCheck, cb)
            self.checkBoxList.append(checkbox)
            spacer = spacer + 20
        for muscle in self.muscleGroupList[top_half:-1]:
            cb = checkbox = wx.CheckBox(self, id=wx.ID_ANY, label=muscle, pos=(470, spacer_2), name=muscle)
            self.Bind(wx.EVT_CHECKBOX, self.onCheck, cb)
            self.checkBoxList.append(checkbox)
            spacer_2 = spacer_2 + 20

        self.selectAllBtn.Bind(wx.EVT_BUTTON, self.onSelectAll);
        self.deselectAllBtn.Bind(wx.EVT_BUTTON, self.onDeselectAll);

        self.routineMetaBox.Add(self.mGText);
        self.routineMetaBox.Add(self.selectAllBtn);
        self.routineMetaBox.Add(self.deselectAllBtn);

        # Form Validation Status
        self.scheduleValidationText = wx.StaticText(self, label="Schedule Type", pos=(775, 460));
        self.scheduleValidationText.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.scheduleValidationImage = wx.Image(name="images/error-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.scheduleBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.scheduleValidationImage), pos=(925, 455))

        self.durationValidationText = wx.StaticText(self, label="Routine Duration", pos=(775, 500));
        self.durationValidationText.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.durationValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.durationBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.durationValidationImage), pos=(925, 495))

        self.typeValidationText = wx.StaticText(self, label="Routine Type", pos=(775, 540));
        self.typeValidationText.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.typeValidationImage = wx.Image(name="images/error-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.typeBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.typeValidationImage), pos=(925, 535))


        self.muscleValidationText = wx.StaticText(self, label="Muscle Groups", pos=(775, 580));
        self.muscleValidationText.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.muscleValidationImage = wx.Image(name="images/error-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.muscleBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.muscleValidationImage), pos=(925, 575))

        # Generate Routine Button
        self.generateWorkoutBtn = wx.Button(self, label="Generate Workout", pos =(775, 600), size=(200, 100));
        self.Bind(wx.EVT_BUTTON, self.onGenerate, self.generateWorkoutBtn)
        self.vbox.Add(self.routineMetaBox);
    # Event Handlers
    def onChoice(self, event=None):
        self.amountOfWorkouts = event.GetEventObject().GetSelection()-1;
    def onRotate(self, event=None):
        if(self.rotate):
            self.rotate = False;
        else:
            self.rotate = True;
    def onCheck(self, event=None):
        if event.IsChecked():
            self.selectedMuscleGroups.append(event.GetEventObject().GetName())
            self.validMuscleGroup = True
            self.muscleValidationImage = wx.Image(name=SUCCESS_ICON, type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
            self.muscleBmp.SetBitmap(wx.Bitmap(self.muscleValidationImage))
        else:
            self.selectedMuscleGroups.remove(event.GetEventObject().GetName())
            self.validMuscleGroup = False
            self.muscleValidationImage = wx.Image(name=ERROR_ICON, type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
            self.muscleBmp.SetBitmap(wx.Bitmap(self.muscleValidationImage))
    def onSelectAll(self, event=None):
        self.validMuscleGroup = True
        for box in self.checkBoxList:
            box.SetValue(True);
            self.selectedMuscleGroups.append(box.GetName())
        self.muscleValidationImage = wx.Image(name=SUCCESS_ICON, type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.muscleBmp.SetBitmap(wx.Bitmap(self.muscleValidationImage))
    def onDeselectAll(self, event=None):
        if(self.validMuscleGroup == True):
            for box in self.checkBoxList:
                box.SetValue(False);
                self.selectedMuscleGroups.remove(box.GetName())
        self.validMuscleGroup = False
        self.muscleValidationImage = wx.Image(name=ERROR_ICON, type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.muscleBmp.SetBitmap(wx.Bitmap(self.muscleValidationImage))
    def onToggleBalanced(self, event=None):
        if(self.toggleBalanced):
            self.toggleBalanced.SetValue(True);
            self.togglePriority.SetValue(False);
        self.validScheduleType = True;
        self.scheduleValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.scheduleBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.scheduleValidationImage), pos=(925, 455))
    def onTogglePriority(self, event=None):
        if(self.togglePriority):
            self.togglePriority.SetValue(True)
            self.toggleBalanced.SetValue(False)
        self.validScheduleType = True;
        self.scheduleValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.scheduleBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.scheduleValidationImage), pos=(925, 455))
    def onToggleEndurance(self, event=None):
        if(self.toggleEnduranceButton):
            self.toggleEnduranceButton.SetValue(True);
            self.toggleStrengthButton.SetValue(False);
        self.validRoutineType = True;
        self.typeValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.typeBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.typeValidationImage), pos=(925, 535))
    def onToggleStrength(self, event=None):
        if(self.toggleStrengthButton):
            self.toggleStrengthButton.SetValue(True)
            self.toggleEnduranceButton.SetValue(False)
        self.validRoutineType = True;
        self.typeValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
        self.typeBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.typeValidationImage), pos=(925, 535))
    def onStartDateSelect(self, event=None):
        self.routineStartDate = self.calendarStart.GetValue();
        self.startDateText.SetLabel("Start Date: {}".format(wx.DateTime(self.routineStartDate).Format("%B, %D")))
        self.startDateText.Update();
    def onEndDateSelect(self, event=None):
        startDate = wx.DateTime(self.calendarStart.GetValue());
        endDate = wx.DateTime(self.calendarEnd.GetValue());
        if(startDate < endDate):
            if(endDate.GetYear() == startDate.GetYear()):
                self.validDuration = True
                self.duration = (int(endDate.Format("%j")) - int(startDate.Format("%j"))) // 7
                self.days = (int(endDate.Format("%j")) - int(startDate.Format("%j"))) % 7
                self.durationValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY,
                                                        index=0).Scale(30, 30);
                self.durationBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.durationValidationImage), pos=(925, 495))
            elif(endDate.GetYear() - startDate.GetYear() >= 2):
                self.duration = 0
                self.days = 0
                self.durationText.SetLabel(
                    "Routine Duration: {} Weeks, {} Days".format(str(self.duration), str(self.days)));
                self.endDateText.SetForegroundColour(wx.RED)
                self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(endDate).Format("%B, %D")))
                self.durationValidationImage = wx.Image(name="images/error-icon.jpg", type=wx.BITMAP_TYPE_ANY,
                                                        index=0).Scale(30, 30);
                self.durationBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.durationValidationImage), pos=(925, 495))
                self.validDuration = False
                self.durationText.Update();
                self.endDateText.Update();
                self.durationBmp.Update();
                return 0;
            else:
                daysLeftInStartYear = 365 - int(startDate.Format("%j"))
                daysSetInEndYear = abs(0 - int(endDate.Format("%j")))
                self.duration = (daysLeftInStartYear + daysSetInEndYear) // 7
                self.days = (daysLeftInStartYear + daysSetInEndYear) % 7
                self.durationValidationImage = wx.Image(name="images/success-icon.jpg", type=wx.BITMAP_TYPE_ANY,
                                                        index=0).Scale(30, 30);
                self.durationBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.durationValidationImage), pos=(925, 495))
                self.validDuration = True

            self.routineEndDate = endDate;
            self.durationText.SetLabel("Routine Duration: {} Weeks, {} Days".format(str(self.duration), str(self.days)));
            self.endDateText.SetForegroundColour(wx.BLACK)
            self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(endDate).Format("%B, %D")))
            self.durationText.Update();
            self.endDateText.Update();
        else:
            self.endDateText.SetForegroundColour(wx.RED)
            self.durationValidationImage = wx.Image(name="images/error-icon.jpg", type=wx.BITMAP_TYPE_ANY,
                                                    index=0).Scale(30, 30);
            self.durationBmp = wx.StaticBitmap(self, -1, wx.Bitmap(self.durationValidationImage), pos=(925, 495))
            self.validDuration = False
            self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(endDate).Format("%B, %D")))
            self.endDateText.Update();
    def onAddWeeks(self, event=None, weeks=0):
        self.duration = weeks
        self.validDuration = True
        newEndDate = wx.DateTime(self.routineStartDate).Add(wx.DateSpan(weeks=int(self.duration)));
        self.routineEndDate = newEndDate
        self.calendarEnd.SetValue(newEndDate)
        self.endDateText.SetLabel("End Date: {}".format(wx.DateTime(newEndDate).Format("%A, %B %d %G")))
        self.durationText.SetLabel("Routine Duration: {} Weeks".format(str(self.duration)));
        self.durationText.Update();
        self.calendarEnd.Update();
    def onGenerate(self, event=None):
        errors = []
        # Form Validation
        errorMessage = ""
        if(not self.validRoutineType):
            errors.append("No Routine Type Selected \n");
        if(not self.validDuration):
            errors.append("Invalid Duration -  See duration parameters for setting a valid date. \n");
        if(not self.validMuscleGroup):
            errors.append("You must select one or more muscle groups \n");

        if(len(errors) > 0):
            for error in errors:
                errorMessage += error
            errorDialog = wx.MessageDialog(self, message=errorMessage, caption="Failed to generate workouts")
            errorDialog.ShowModal()
        else:
            # Change Notebook Pages
            notebook = self.GetParent()
            notebook.SetSelection(1)



