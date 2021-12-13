print('\n')
#import(s)
import pandas as pd
import math

#file path(s)
infile = "./CaribouTrailLeagueRankings.csv"
outfile = open("./FinalReportCTLRankings.txt", 'w')


#open file(s)
runningdata = pd.read_csv(infile)

#gets list of times
times = runningdata.iloc[:,3]

#Split up times and converts the times to seconds for each entry
timeSplit = []
timeInMin = []
timeInSec = []

for i in times:
    timeMin = times.str.split(":")
    for i in timeMin:
        for x in i:
            timeSplit.append(float(x))

for i in range(len(timeSplit)):
    if i % 2 == 0:
        timeInMin.append(timeSplit[i])
    else:
        timeInSec.append(timeSplit[i])

time = []
for i in range(50):
    time.append((60 * timeInMin[i]) + timeInSec[i])
    
#Create a time in seconds column for computation
runningdata = runningdata.assign(TimeInSeconds = time)
#-------------------------------------------------------------

#Get the distinct team names
teams = runningdata.iloc[:,6]
uniqueTeams = [teams[0]]
for i in teams:
    if i not in uniqueTeams:
        uniqueTeams.append(i)
        
#Getting team lineup from data
schoolRunners = []
for i in uniqueTeams:
    schoolRunners.append(runningdata.query("Team == @i"))

#Getting runner's ranks for each team
ranks = []
for i in schoolRunners:
   ranks.append(i.iloc[:,0])
   
   
#Calculates the scores for the teams
sums = []
for i in ranks:
    add = 0
    listRunners = []
    for n in i:
        listRunners.append(n)
    for x in range(5): #Range set to five because top five for each team score
        add = add + listRunners[x]
    sums.append(add)

#Sorts team ranks
teamScores = zip(uniqueTeams, sums)
teamScores = dict(teamScores)
teamScores = sorted(teamScores.items(), key = lambda x: x[1], reverse = False)

#Format and output text/result for team scores
text = []
print("Team Scores and Rankings for CTL: ")
outfile.write("Team Scores and Rankings for CTL: \n")
for key, value in teamScores:
    text.append(f"{key} got score of {value}. ")
for i in range(len(teamScores)):
    text[i] = (text[i] + f"They placed {i + 1} in the league by hypothetical meet. ")

for i in range(len(text)):
    print(text[i])
    outfile.write(text[i] + '\n')
print('\n')
outfile.write('\n')
    
#------------------------------------------------------------------------------   
    
#Calculating the grade average times and overall average time for the league

#Gets unique grade levels
grades = runningdata.iloc[:,1]
uniqueGrades = [grades[0]]
for i in grades:
    if i not in uniqueGrades:
        uniqueGrades.append(i)

#Breaks up each grade level
runnerGrades = []
for i in uniqueGrades:
    runnerGrades.append(runningdata.query("Grade == @i"))

#Getting times for each grade level
gradeTimes = []
for i in runnerGrades:
    gradeTimes.append(i.iloc[:,7])

#Calculates the average times for each grade level
averages = []
for i in gradeTimes:
    add = 0
    for n in i:
        add = add + n
    averages.append(add/len(i))

#Calculate the average overall time for the league
avgTime = runningdata.iloc[:,7]
overallAverage = 0
for i in avgTime:
    overallAverage = overallAverage + i
overallAverage = overallAverage/len(avgTime)
updatedOverallAverage = str(math.floor(overallAverage/60)) + ":" + str(round(overallAverage%60, 1))

#Formatting time text
updatedAverage = []
for i in averages:
    minutes = math.floor(i / 60)
    seconds = round(i % 60, 1)
    updatedAverage.append(str(minutes) + ":" + str(seconds))

#Organized for output
gradeAverages = zip(uniqueGrades, updatedAverage)
gradeAverages = dict(gradeAverages)

#Format and output text/result for averages
text = []
print("Average times for the 5000 meter distance for each grade level and overall: ")
outfile.write("Average times for the 5000 meter distance for each grade level and overall: \n")

for i in range(len(uniqueGrades)):
    text.append(f"Grade {uniqueGrades[i]} had an average time of {updatedAverage[i]}. ")


for i in range(len(text)):
    print(text[i])
    outfile.write(text[i] + '\n')
print(f"The overall average for the league is {updatedOverallAverage}. ")
outfile.write(f"The overall average for the league is {updatedOverallAverage}. \n")
print('\n')
outfile.write('\n')

#------------------------------------------------------------------------------

#My personal best time in seconds (16:52.7 minutes)
best = 1012.7
updatedBest = str(math.floor(best/60)) + ":" + str(round(best%60, 1))

#Difference in time between my best and the league average
differenceOfBest = round(overallAverage - best,1)

#Calculates the standard deviation of runner's times in seconds
stdTimes = runningdata.iloc[:,7]
add = 0
for i in range(len(stdTimes)):
    add = pow(stdTimes[i]-overallAverage,2)
stdv = add/len(stdTimes)
stdd = round(math.sqrt(stdv),1)

#How many standard deviations I am from the mean/average
deviation = round(differenceOfBest/stdd,2)

#Output data to file/console
print("My best time compared to the league: ")
outfile.write("My best time compared to the league: \n")

print(f"My best time for the 5000 meters was {updatedBest}.")
outfile.write(f"My best time for the 5000 meters was {updatedBest}. \n")

if differenceOfBest > 0:
    print(f"That time is {differenceOfBest} second(s) faster than the league average time.")
    outfile.write(f"That time is {differenceOfBest} second(s) faster than the league average time.\n")
else:
    print(f"That time is {differenceOfBest} second(s) slower than the league average time.")
    outfile.write(f"That time is {differenceOfBest} second(s) slower than the league average time.\n")

print(f"My time is {deviation} standard deviation(s) from the average time of the league.")
outfile.write(f"My time is {deviation} standard deviation(s) from the average time of the league.\n")

print('\n')
outfile.write('\n')

outfile.close()