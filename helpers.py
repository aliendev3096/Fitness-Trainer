import json;
import random

def searchWorkouts(musclegroup):
    if musclegroup in ["Rectus Abdominis", "Obliques" , "Erector Spinae", "Transverse Abdominis"]:
        with open("./musclegroups/waist.json", 'r') as waistjson:
            workouts = json.load(waistjson)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    elif musclegroup in ["Biceps Brachii",  "Triceps Brachii" , "Brachialis"]:
        with open("./musclegroups/upperarms.json", 'r') as upperarmsjson:
            workouts = json.load(upperarmsjson)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)

def getGroupWorkouts(musclegroup, allowedWorkouts):
    groupWorkouts = []
    for workout in allowedWorkouts:
        # Compare only first muscle group, even though some workouts are multi targeting
        if(workout["targets"][0] == musclegroup):
            groupWorkouts.append(workout)
    # Lets shuffle so we don't get the same ordered list when generating workouts
    return groupWorkouts# random.shuffle(groupWorkouts)

def getLeastUsedWorkout(workouts, tracker):
    # if nothing has been tracked before, just return the first in the list
    if len(tracker) == 0:
        return workouts[0]

    # Iterate over list to find any untracked workouts
    for workout in workouts:
        # If workout is not tracked, return it
        if workout["name"] not in tracker.keys():
            return workout

    # This only happens if all workouts within a muscle group have been used at least once
    sortedTrackedWorkoutsAsList = sorted(tracker.items(), key=lambda x: x[1])

    # Set least used as first element in sorted list, if there are any ties, just use the first one
    leastUsedWorkoutName = sortedTrackedWorkoutsAsList[0]

    # Get the workout object with least used name
    for workout in workouts:
        if leastUsedWorkoutName == workout["name"]:
            return workout
