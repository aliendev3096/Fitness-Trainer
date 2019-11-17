class Workout:
    def __init__(self, name, muscleGroup, reps=10, sets=3):
        self.__WORKOUT_NAME = name;
        self.__MUSCLEGROUP = muscleGroup;
        self.__REPS = reps;
        self.__SETS = sets;
    def getMuscleGroups(self):
        return self.__MUSCLEGROUPS;

class Session:
    def __init__(self, date, workouts=[]):
        self.date = date;
        self.__WORKOUTS = workouts;
    def addWorkout(self, workout):
        self.__WORKOUTS.append(workout);
    def getWorkouts(self):
        return self.__WORKOUTS;

class Routine:
    def __init__(self, name, session=[]):
        self.__ROUTINE_NAME = name;
        self.__SESSIONS = session;
    def addSession(self, session):
        self.__SESSIONS.append(session);
    def getSessions(self):
        return self.__SESSIONS;