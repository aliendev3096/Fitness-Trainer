import wx;
import wx.adv;
import json;
import classes;
from helpers import searchWorkouts
from helpers import getLeastUsedWorkout

SUCCESS_ICON = "images/success-icon.jpg"
ERROR_ICON = "images/error-icon.jpg"
class HomePanel(wx.Panel):
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL);
        # Set Form Validations to False, we don't start with a valid form.
        self.validDuration = False;
        self.validRoutineType = False;
        self.validMuscleGroup = False;
        self.rotate = False;
        self.exclude = False;

        # Intro Text
        self.welcomeBox = wx.BoxSizer(wx.HORIZONTAL);
        description = "This application is not intended to help with weight loss. " \
                              "The purpose of Dynamite Fit is to provide a feeling for diverse \n workouts to help you on your " \
                              "journey to healthiness. By no means should you follow these workouts strictly. \n You are " \
                              "free to manipulate your workouts as you want. If you are limited in anyway to perform any of these workouts, " \
                              "please do not feel obligated to \n do them as there are plenty of other workouts to choose from." \
                              "Dynamite Fit is intended ONLY as a guide. \n" \
                              "For the purpose of simplicity, Dynamite Fit generates workout only up to a year from the start date, " \
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
        self.days = 0;
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

        # Routine Schedule Details
        self.amountOfWorkouts = 4
        self.routineDetailsText = wx.StaticText(self, label="How many workouts/day?", pos=(650, 320));
        self.customDetailsInput = wx.Choice(self, pos=(820, 320), size=(75, 25), choices=["1", "2", "3", "4", "5", "6", "7", "8"]);
        self.customDetailsInput.SetSelection(self.amountOfWorkouts-1)
        self.Bind(wx.EVT_CHOICE, self.onChoice, self.customDetailsInput)
        self.relationshipNoteText = wx.StaticText(self, label="* Each Workout in a session corresponds to a single muscle group.", pos=(20, 650));

        # Exclude Weekends
        self.excludeWeekends = wx.CheckBox(self, id= wx.ID_ANY, label="Exclude Weekends", pos=(20, 570))
        self.Bind(wx.EVT_CHECKBOX, self.onExclude, self.excludeWeekends)

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
                                "Brachialis",
                                "Rectus Abdominis",
                                "Obliques",
                                "Erector Spinae"]
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
        self.routineName = wx.TextCtrl(self, value="", pos=(775, 610), size=(200, 25))
        self.routineName.SetHint("Enter a routine name")
        self.generateWorkoutBtn = wx.Button(self, label="Generate Workout", pos =(775, 600), size=(200, 100));
        self.Bind(wx.EVT_BUTTON, self.onGenerate, self.generateWorkoutBtn)
        self.vbox.Add(self.routineMetaBox);

    # Event Handlers
    def onChoice(self, event=None):
        self.amountOfWorkouts = event.GetEventObject().GetSelection();
    def onRotate(self, event=None):
        if(self.rotate):
            self.rotate = False;
        else:
            self.rotate = True;
    def onExclude(self, event=None):
        if(self.exclude):
            self.exclude = False;
        else:
            self.exclude = True;
    def onCheck(self, event=None):
        if event.IsChecked():
            self.selectedMuscleGroups.append(event.GetEventObject().GetName())
            self.validMuscleGroup = True
            self.muscleValidationImage = wx.Image(name=SUCCESS_ICON, type=wx.BITMAP_TYPE_ANY, index=0).Scale(30, 30);
            self.muscleBmp.SetBitmap(wx.Bitmap(self.muscleValidationImage))
        else:
            self.selectedMuscleGroups.remove(event.GetEventObject().GetName())
            if(len(self.selectedMuscleGroups) == 0):
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
            # Check for Errors based on Form Validation
            for error in errors:
                errorMessage += error
            errorDialog = wx.MessageDialog(self, message=errorMessage, caption="Failed to generate workouts")
            errorDialog.ShowModal()
        else:
            # Instantiate Routine
            newEmptyRoutine = classes.Routine(name=self.routineName.GetValue(), session=[], tracker={})
            # Generate Routine
            newRoutine = self.generateRoutine(newEmptyRoutine)

            # Open File for Reading and Deserialize
            user = self.GetParent().GetParent().active_user.replace("&", "");
            with open('./profiles/{}.json'.format(user), 'r') as userjson:
                data = json.load(userjson)

            # Serialize Routine
            serialized = json.dumps(newRoutine.__dict__, default=lambda o: o.__dict__).replace("\n", "");

            # Deserialize and Append
            deserialized = json.loads(serialized)
            data["Routines"].append(deserialized)

            # Update Menu Bar with Routine Selection
            mainWindow = self.GetParent().GetParent();
            # If there are 5 menus, we have routines
            if len(mainWindow.windowMenuBar.GetMenus()) == 5:
                routineMenu = mainWindow.windowMenuBar.GetMenu(4)
                tab = routineMenu.Append(wx.NewId(), "&{}".format(deserialized["routineName"]), "Change to Routine {}".format(deserialized["routineName"]))
                mainWindow.Bind(wx.EVT_MENU, mainWindow.OnSwitchRoutine, tab);
            else:
                routineTab = wx.Menu();
                tab = routineTab.Append(wx.NewId(), "&{}".format(deserialized["routineName"]), "Change to Routine {}".format(deserialized["routineName"]));
                mainWindow.Bind(wx.EVT_MENU, mainWindow.OnSwitchRoutine, tab);

            # Serialize and Save to json profile
            with open('./profiles/{}.json'.format(user), 'w+') as updatedUserJson:
                json.dump(data, updatedUserJson, indent=4);

            # Change Notebook Pages
            notebook = self.GetParent()
            notebook.SetSelection(1)

    def generateRoutine(self, routine):
        # Set Days based on exclude weekends parameter
        if self.exclude:
            routineDays = 5 * self.duration + self.days
        else:
            routineDays = 7 * self.duration + self.days

        # Copy Musclegroups List
        mgStart = 0
        mgEnd = self.amountOfWorkouts + 1
        # If we target less/equal groups than workouts/day, send the entire list of groups
        if(len(self.selectedMuscleGroups) <= mgEnd):
            musclegroups = self.selectedMuscleGroups;
        # Else, we have more groups to account for in single session, send only a subset
        else:
            musclegroups = self.selectedMuscleGroups[mgStart:mgEnd];

        # Create a Workout Session for each day in a single routine
        for day in range(0, routineDays+1):
            startDate = wx.DateTime(self.calendarStart.GetValue());
            # Exclude weekends logic
            if self.exclude:
                nextDay = startDate.Add(wx.DateSpan(days=day))
                while (nextDay.GetWeekDay() == wx.DateTime.Sat or nextDay.GetWeekDay() == wx.DateTime.Sun):
                    nextDay = startDate.Add(wx.DateSpan(days=1))
            else:
                nextDay = startDate.Add(wx.DateSpan(days=day))

            nextDay = nextDay.Format("%A, %D");

            # Create Session
            newSession = classes.Session(date=nextDay, workouts=self.generateWorkouts(groups=musclegroups, tracker=routine.tracker))
            routine.addSession(newSession)

            # Use the next section of muscle groups for the next day
            mgStart = mgEnd;
            mgEnd += self.amountOfWorkouts + 1
            # If we reach the end of the muscle groups list, wrap around to beginning of list.
            if len(self.selectedMuscleGroups) < mgEnd:
                musclegroups = self.selectedMuscleGroups[mgStart:-1]
                mgStart = 0;
                mgEnd = self.amountOfWorkouts + 1
                musclegroups.extend(self.selectedMuscleGroups[mgStart:mgEnd])
            else:
                musclegroups = self.selectedMuscleGroups[mgStart:mgEnd]

        return routine
    def generateWorkouts(self, groups, tracker):
        workouts = [];
        # Generate a workout for each muscle group
        for group in groups:
            if self.toggleEnduranceButton.GetValue() == True:
                reps = 20
                sets = 3
            else:
                reps = 5
                sets = 2
            # Search for workouts of a muscle group
            newWorkoutsAsList = searchWorkouts(group);
            # Search for least used workout in routine
            singleWorkout = getLeastUsedWorkout(newWorkoutsAsList, tracker)

            # Extract workout properties
            name = singleWorkout["name"]
            targets = singleWorkout["targets"]
            variations = singleWorkout["variations"]

            # Create the workout & add to session
            newWorkout = classes.Workout(name=name, muscleGroup=targets[0],
                                         reps=reps, sets=sets, variations=variations)

            # Track the workout to the routine history
            # If it exists, add a count, else add one to the count
            if(name in tracker.keys()):
                tracker[name] = tracker[name] + 1
            else:
                tracker[name] = 1
            # Add workout to session workout list
            workouts.append(newWorkout)
        return workouts;