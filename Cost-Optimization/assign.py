# Q1. Formulation: 
#	(a)State space: There will be just one state with the placement of students in either of teams #(All possible combinations of students put into groups of size 1/2/3)
#	(b)Initial state: All the students each with individual as a team #(one student per team) 
#	(c)Successor Function: Swapping one student i.e adding/removing member from group, whichever minimize's the cost
#	(d)Goal state: Goal state for the problem is unknown but the least cost of team formation can be considered as goal #(but the least cost over multiple iterations is chosen as the best cost)
#	(e)Cost function: One swap of student in matrix will take uniform cost i.e one
#	(f)Heuristic function: Swap that takes the minimum conflict and results in less cost than predecessor #Evaluates the conf;icts that arise by having moved a student from one group to another
#
# Q2. Working of Algo:
#	The local search algorithm is used to solve this problem. Initially each student is assigned as a team of one. Thereafter, the successors with combinations of students which minimizes
#	the costs are generated and the one with least cost is considered for which the successors are generated until the least cost is obtained(i.e. cost does not change from one iteration to
#	the next). The combinations over here are carried out by swapping each student in such a way that the overall cost of the finally formed successor will always be less than its predecessor. #       At each and every level the matrix of teams is reduced for the teams which have 0 members in total. The problem uses matrix of Nx3 where N are number of people and 3 is max of people in one #	team.
#
# Q3. 	Problems faced: Deciding on how to approach the problem, Defining the model for problem
#	Assumptions made: 1.Adding students based on preferences in the initial state but which attribute should be given more weightage is tough to decide.
#			  2.Swapping based on random places on matrix was not feasible if we generate random positions for swap, the probability to miss some of positions which might result in
#			  low cost will be missed and the computation time to derive the missing number from random will be high while probability to get that number will be low if data is high
#	Simplifications: For the given algorithm the simplification to be made was to remove the teams(rows in matrix) with 0 members so that traversing will be limited only to members with team
#			 Swapping of student with student or place takes place only when the overall cost of matrix is affected.
#	Design Decision: As per discussion with Professor Crandall the designing of problem with respect to n-queens problem formulation was the decision made.
import sys
import csv
import copy
from datetime import datetime
def data_read(input_file):
		f = open(input_file)
		reader = csv.reader(f, delimiter = ' ')
		for r in reader:
			teams.append([r[0],0,0])
			r[1] = int(r[1])
			partners = r[2].split(",")
			r[2] = partners
			no_need = r[3].split(",")
			r[3] = no_need
			data[r[0]] = r[1:]

#get count of members that were requested but not assigned
def count_req_not_assigned(mem, current_team):
	pref = data[mem][1]
	count = 0
	if(pref[0] != '_'):
		for i in pref:
			if i not in current_team:
				count += 1
	else:
		return 0
	return count

#get count of members that were not requested but assigned	
def count_not_req_assigned(mem, current_team):
	not_pref = data[mem][2]
	count = 0
	if(not_pref[0] != '_'):
		for i in current_team:
			if i in not_pref:
				count += 1
	else:
		return 0
	return count
	
#final formatted output of all teams formed
def disp_output(teams):
	for row in teams:
		for mem in row:
			print mem,
		print

#formatting matrix to remove 0's or no memeber in a particular team		
def format_team(teams):
	nameteam = []
	for i in teams:
		rowlist = []
		for j in i:
			if(j != 0):
				rowlist.append(j)
			else:
				continue
		if rowlist != []:
			nameteam.append(rowlist)
	return nameteam		
	
#calculate total cost based on students preferences			
def cal_cost(teams):
	team_data = format_team(teams) 
	total_cost = k * len(team_data)
	group_size_issue = 0
	req_not_assigned = 0
	not_req_assigned = 0
	for row in team_data:
		for mem in row:
			if(len(row) != data[mem][0] and data[mem][0] > 0):
				group_size_issue += 1
			req_not_assigned += count_req_not_assigned(mem, row)
			not_req_assigned += count_not_req_assigned(mem, row)	
	return (total_cost + group_size_issue + (n * req_not_assigned) + (m * not_req_assigned))

#to check if swapping on same count of row or not
def memonrow(team,r):
	count = 0
	for i in range(0, 3):
		if team[r][i] != 0:
			count += 1
	return count

#for removing the groups which have no memebers
def reduce_matrix(team):
	team2 = []
	for r in team:
		count = 0
		for c in r:
			if c == 0:
				count += 1
			else:
				continue
		if count != 3:
			team2.append(r)
		else:
			continue
	return team2

#swapping members within groups
def make_swap(team, r, c, i, j):
	team2 = copy.deepcopy(team)
	team2[r][c], team2[i][j] = team2[i][j], team2[r][c]
	return team2

#generating successor
def successor(team):
	succ = []
	check = {}
	min_cost_succ_state = team
	min_succ_cost = cal_cost(team)
	for r in range(0, len(team)):
		for c in range(0, 3):
			for i in range(0, len(team)):
				for j in range(0, 3):
					if(i != r and j != c ):
						if((memonrow(team,r) != 1 and memonrow(team,i) != 0)or(memonrow(team,r) != 0 and memonrow(team,i) != 0) or (memonrow(team,r) != 1 and memonrow(team,i) != 1)):
							swap = make_swap(team, r, c, i, j)
							if(check.has_key(str(swap)) == False):
								check[str(swap)] = ""
								swap_succ_cost = cal_cost(swap)
								if swap_succ_cost < min_succ_cost:
									min_succ_cost = swap_succ_cost
									min_cost_succ_state = swap
	min_cost_succ_state = reduce_matrix(min_cost_succ_state)
	succ.append(min_cost_succ_state)
	return succ


def solver(teams):
	fringe = [teams]
	prev_cost = cal_cost(teams)
	current_state = teams
	k = 0
	while len(fringe)>0:
		for s in successor(fringe.pop()):
			cur_succ_cost = cal_cost(s)
			if prev_cost == cur_succ_cost:
				k += 1
				if k == 100:
					return s
				else:
					prev_cost = cur_succ_cost
			else:
				prev_cost = cur_succ_cost
			fringe.append(s)
			
			
		
#initial team formation based on preferences from entry 1 to n
def team_formation(data):
	for i in data:
		if check_assigned.has_key(i):
			continue
		else:
			team_up = []
			team_up.append(i)
			check_assigned[i] = ""
			for pref in data[i][1]:
				if pref == '_':
					continue
				if check_assigned.has_key(pref):
					continue
				else:
					if(len(team_up) <= 3):
						team_up.append(pref)
						check_assigned[pref] = ""
			teams.append(team_up)
def team_mat(teams):
	for i in range(0, len(teams)):
		while(len(teams[i]) < 3):
			teams[i].append(0)
	return teams
	
t1 = datetime.now()
input_file = str(sys.argv[1])
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])
data = {}
teams = []
data_read(input_file)
check_assigned = {}
final_team = solver(teams)
final = format_team(final_team)
disp_output(final)
print cal_cost(final)
