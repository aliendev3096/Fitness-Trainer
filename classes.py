class Workout:
    def __init__(self, name, muscleGroup, reps, sets, weight=0, variations=[]):
        self.workoutName = name;
        self.muscleGroup = muscleGroup;
        self.reps = reps;
        self.sets = sets;
        self.weight = weight;
        self.variations = variations


class Session:
    def __init__(self, date, workouts=[]):
        self.date = date;
        self.workouts = workouts;

class Routine:
    def __init__(self, name, session=[], tracker={}):
        self.routineName = name;
        self.sessions = session;
        self.tracker = tracker;
    def addSession(self, session):
        self.sessions.append(session);
    def getSessions(self):
        return self.sessions;