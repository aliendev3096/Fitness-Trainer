import json;
import random

def searchWorkoutsByGroup(musclegroup):
    # Waist
    if musclegroup in ["Rectus Abdominis", "Obliques", "Erector Spinae", "Transverse Abdominis"]:
        with open("./musclegroups/waist.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    # Upperarms
    elif musclegroup in ["Biceps Brachii",  "Triceps Brachii", "Brachialis"]:
        with open("./musclegroups/upperarms.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    # Thighs
    elif musclegroup in ["Quadriceps",  "Rectus Femoris" , "Hamstrings", "Adductors"]:
        with open("./musclegroups/thighs.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    # Shoulders
    elif musclegroup in ["Supraspinatus",  "Posterior Deltoid", "Lateral Deltoid", "Anterior Deltoid"]:
        with open("./musclegroups/shoulders.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    #Hips
    elif musclegroup in ["Gluteus Maximus"]:
        with open("./musclegroups/hips.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    # Forearms
    elif musclegroup in ["Brachioradialis",  "Wrist Flexors", "Wrist Extensors", "Pronators", "Supinators"]:
        with open("./musclegroups/forearms.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    # Chest
    elif musclegroup in ["Pectorlis Major-Sternal",  "Pectoralis Minor", "Pectorlis Major-Clavicular"]:
        with open("./musclegroups/chest.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)
    # Back
    elif musclegroup in ["Infraspinatus",  "Trapezius", "Subscapularis", "Latissimus Dorsi",  "General Back"]:
        with open("./musclegroups/back.json", 'r') as jsonfile:
            workouts = json.load(jsonfile)
            allWorkouts = workouts["Workouts"];
            return getGroupWorkouts(musclegroup, allWorkouts)


def getGroupWorkouts(musclegroup, allowedWorkouts):
    groupWorkouts = []
    for workout in allowedWorkouts:
        # Compare only first muscle group, even though some workouts are multi targeting
        if(workout["targets"][0] == musclegroup):
            groupWorkouts.append(workout)
    # Lets shuffle so we don't get the same ordered list when generating workouts
    random.shuffle(groupWorkouts)
    return groupWorkouts

def getLeastUsedWorkout(workouts, tracker, musclegroup):
    trackedMuscleGroups = {}
    # if nothing has been tracked before, just return the first in the list
    if len(tracker) == 0:
        return workouts[0]

    # Iterate over list to find any untracked workouts
    for workout in workouts:
        # If workout is not tracked, return it
        if workout["name"] not in tracker.keys():
            return workout

    # Get only tracked workouts in specified muscle group
    for workout in workouts:
        if workout["name"] in tracker:
            trackedName = workout["name"]
            for trackedWorkout in tracker:
                if trackedWorkout == trackedName:
                    trackedMuscleGroups[trackedWorkout] = tracker[trackedWorkout]

    # This only happens if all workouts within a muscle group have been used at least once
    sortedTrackedWorkoutsAsList = sorted(trackedMuscleGroups.items(), key=lambda x: x[1])

    # Set least used as first element in sorted list, if there are any ties, just use the first one
    leastUsedWorkoutName = [x[0] for x in sortedTrackedWorkoutsAsList]

    # Get the workout object with least used name
    for workout in workouts:
        if leastUsedWorkoutName[0] == workout["name"]:
            return workout
