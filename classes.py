class Workout:
    def __init__(self, name, muscleGroups=[], reps=10, sets=3):
        self.__WORKOUT_NAME = name;
        self.__MUSCLEGROUPS = muscleGroups;
        self.__REPS = reps;
        self.__SETS = sets;
    def getMuscleGroups(self):
        return self.__MUSCLEGROUPS;

class DailyRoutine:
    def __init__(self, name, workouts=[]):
        self.__ROUTINE_NAME = name;
        self.__WORKOUTS = workouts;
    def addWorkout(self, workout):
        self.__WORKOUTS.append(workout);
    def getWorkouts(self):
        return self.__WORKOUTS;

class WeeklyRoutine:
    def __init__(self, week, routines=[]):
        self.__WEEK_NUMBER = week;
        self.__ROUTINES = routines;
    def addRoutine(self, routine):

        self.__ROUTINES.append(routine);
    def getRoutines(self):
        return self.__ROUTINES;