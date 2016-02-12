# Maggie Borkowski
# Intro to AI
# HW 3


# Knowledge cells take the form [x,b,s,p,w,Y], where:
# x indicates the cell has been visited,
# b indicates a breeze,
# s indicates a stench,
# p indicates the possibility of a pit,
# w indicates the possibility of a wumpus,
# and Y is filled by either W for wumpus, P for pit, or G for gold.
# All characters in the string are initiated to '-', resulting in a string of '------'.
# As more is discovered, the characters are changed accordingly.

import datetime

# arrays to store map and knowledge
map_arr = []
know_arr = []

# dead/win conditions
dead = False
win = False

# player position, direction & arrow status
pos = [1,1]
facing = 'EAST'
arrow = True

# used for naming log file
def getDateTimeStamp():
    d = datetime.datetime.now().timetuple()
    return "%d-%02.d-%02.d_%02.d-%02.d-%02.d" % (d[0], d[1], d[2], d[3], d[4], d[5])

# create logging file
log = open('KB_' + getDateTimeStamp() + '.txt', 'a')


# read file into map array, match dimensions of knowledge array to map array, initialize all knowledge cells to empty '-'
def initialize(filename, m, k):
	f = open(filename, 'r')
	for line in f:
		mrow = []
		krow = []
		for ch in line:
			ch = ch.upper()
			if ch=='X' or ch=='W' or ch=='P' or ch=='G':
				mrow.append(ch)
				krow.append(['-','-','-','-','-','-'])

		m.append(mrow)
		k.append(krow)

	# rows were added in reverse order
	m.reverse()
	k.reverse()

	# first cell is automatically explored
	k[0][0][0] = 'x'

	# close file
	f.close()


# searches for percepts in current cell, using map array; returns array to be updated in cell of knowledge array
def sense(m,cell):

	#variables for row and column values
	r = cell[1]-1
	c = cell[0]-1

	# cell is visited
	percepts = ['x','-','-','-','-','-']

	# whether a breeze has been found (to avoid double breeze logging)
	breeze=False

	# breeze or stench in cell
	if r>0:
		if m[r-1][c] == 'P':
			percepts[1] = 'b'
			# log
			log.write("B(" + str([c+1,r+1]) + ")\n")
			breeze=True
		elif m[r-1][c] == 'W':
			percepts[2] = 's'
			# log
			log.write("S(" + str([c+1,r+1]) + ")\n")
	if r<len(m)-1:
		if m[r+1][c] == 'P':
			percepts[1] = 'b'
			# log
			if breeze==False:
				log.write("B(" + str([c+1,r+1]) + ")\n")
				breeze=True
		elif m[r+1][c] == 'W':
			percepts[2] = 's'
			# log
			log.write("S(" + str([c+1,r+1]) + ")\n")
	if c>0:
		if m[r][c-1] == 'P':
			percepts[1] = 'b'
			# log
			if breeze==False:
				log.write("B(" + str([c+1,r+1]) + ")\n")
				breeze=True
		elif m[r][c-1] == 'W':
			percepts[2] = 's'
			# log
			log.write("S(" + str([c+1,r+1]) + ")\n")
	if c<len(m[0])-1:
		if m[r][c+1] == 'P':
			percepts[1] = 'b'
			# log
			if breeze==False:
				log.write("B(" + str([c+1,r+1]) + ")\n")
				breeze=True
		elif m[r][c+1] == 'W':
			percepts[2] = 's'
			# log
			log.write("S(" + str([c+1,r+1]) + ")\n")	

	# pit in cell
	if m[r][c] == 'P':
		percepts[5] = 'P'
		# log
		log.write("P(" + str([c+1,r+1]) + ")\n")

	# wumpus in cell
	elif m[r][c] == 'W':
		percepts[5] = 'W'
		# log
		log.write("W(" + str([c+1,r+1]) + ")\n")

	# gold in cell
	elif m[r][c] == 'G':
		percepts[5] = 'G'
		# log
		log.write("G(" + str([c+1,r+1]) + ")\n")

	return percepts


# returns string containing percepts from current cell; if no percepts, returns empty string
def return_percepts(k,p):

	cell = k[p[1]-1][p[0]-1]
	percepts = ""

	if cell[1]=='b':
		percepts += "\nThere is a BREEZE in here!"
	if cell[2]=='s':
		percepts += "\nThere is a STENCH in here!"

	return percepts


# returns string containing hints from adjacent cells; if no hints, returns empty string
def hint(k,p):
	hints = ""
	i=p[1]-1
	j=p[0]-1

	# make pit hint array
	pits = []
	if i>0:
		if k[i-1][j][3]=='p':
			pits.append([j,i-1])
	if i<len(k)-1:
		if k[i+1][j][3]=='p':
			pits.append([j,i+1])
	if j>0:
		if k[i][j-1][3]=='p':
			pits.append([j-1,i])
	if j<len(k[0])-1:
		if k[i][j+1][3]=='p':
			pits.append([j+1,i])

	#make wumpus hint array
	wumpus = []
	if i>0:
		if k[i-1][j][4]=='w':
			wumpus.append([j,i-1])
	if i<len(k)-1:
		if k[i+1][j][4]=='w':
			wumpus.append([j,i+1])
	if j>0:
		if k[i][j-1][4]=='w':
			wumpus.append([j-1,i])
	if j<len(k[0])-1:
		if k[i][j+1][4]=='w':
			wumpus.append([j+1,i])

	# add pit hints to string
	if len(pits)>0:
		if len(pits)>1:
			hints += "\nThere may be a pit in [" + str(pits[0][0]+1) + ", " + str(pits[0][1]+1) + "]"
			for x in range(1,len(pits)):
				hints += " or [" + str(pits[x][0]+1) + ", " + str(pits[x][1]+1) + "]"
			hints += "."
		else:
			hints += "\nThere is a pit in [" + str(pits[0][0]+1) + ", " + str(pits[0][1]+1) + "]" + "."

	# add wumpus hints to string
	if len(wumpus)>0:
		if len(wumpus)>1:
			hints += "\nThere may be a wumpus in [" + str(wumpus[0][0]+1) + ", " + str(wumpus[0][1]+1) + "]"
			for x in range(1,len(wumpus)):
				hints += " or [" + str(wumpus[x][0]+1) + ", " + str(wumpus[x][1]+1) + "]"
			hints += "."
		else:
			hints += "\nThere is a wumpus in [" + str(wumpus[0][0]+1) + ", " + str(wumpus[0][1]+1) + "]" + "."

	return hints


# provides info and asks for user input, returns 2-element array of cell that player moves to and direction player faces
def move(prompt,maxr,maxc,p,f,a):
	valid = False
	cell = p
	facing = f
	while valid==False:
		go = raw_input(prompt)
		go = go.upper()

		if go=='F':
			if f=='EAST':
				if p[0]<maxr:
					valid = True
					cell = [p[0]+1,p[1]]
				else:
					print "BUMP!!! You hit a wall!"
			elif f=='WEST':
				if p[0]>1:
					valid = True
					cell = [p[0]-1,p[1]]
				else:
					print "BUMP!!! You hit a wall!"
			elif f=='NORTH':
				if p[1]<maxc:
					valid = True
					cell = [p[0],p[1]+1]
				else:
					print "BUMP!!! You hit a wall!"
			else:
				if p[1]>1:
					valid = True
					cell = [p[0],p[1]-1]
				else:
					print "BUMP!!! You hit a wall!"
		elif go=='L':
			valid = True
			if f=='NORTH':
				facing = 'WEST'
			elif f=='EAST':
				facing = 'NORTH'
			elif f=='SOUTH':
				facing = 'EAST'
			else:
				facing = 'SOUTH'
		elif go=='R':
			valid = True
			if f=='NORTH':
				facing = 'EAST'
			elif f=='EAST':
				facing = 'SOUTH'
			elif f=='SOUTH':
				facing = 'WEST'
			else:
				facing = 'NORTH'
		elif go=='S':
			if a==True:
				valid = True
				cell = p
				facing = f
			else:
				print "You already used your arrow! :("
		else:
			print "INVALID ENTRY"

	return [cell,facing]


def infer(k):
	for i in range(0,len(k)):
		for j in range(0, len(k[0])):

			# remove potential pit/wumpus markings from explored cells
			if k[i][j][0]=='x' and k[i][j][3]=='p' and k[i][j][5]!='P':
				k[i][j][3]='-'
				# log
				log.write("~P(" + str([j+1,i+1]) + ")\n")
			if k[i][j][0]=='x' and k[i][j][4]=='w' and k[i][j][5]!='W':
				k[i][j][4]='-'
				# log
				log.write("~W(" + str([j+1,i+1]) + ")\n")

			# add potential pit marks to unexplored cells surrounding breeze cells
			pits=[]
			if k[i][j][1]=='b':
				if i>0:
					if k[i-1][j][0]=='-' and k[i-1][j][3]=='-':
						k[i-1][j][3]='p'
						pits.append([j+1,i])
				if i<len(k)-1:
					if k[i+1][j][0]=='-' and k[i+1][j][3]=='-':
						k[i+1][j][3]='p'
						pits.append([j+1,i+2])
				if j>0:
					if k[i][j-1][0]=='-' and k[i][j-1][3]=='-':
						k[i][j-1][3]='p'
						pits.append([j,i+1])
				if j<len(k[0])-1:
					if k[i][j+1][0]=='-' and k[i][j+1][3]=='-':
						k[i][j+1][3]='p'
						pits.append([j+2,i+1])

			# log potential pits
			if len(pits)>0:
				statement = "P(" + str(pits[0]) + ")"
				if len(pits)>1:
					for p in range(1,len(pits)):
						statement += " | P(" + str(pits[p]) + ")"
				statement+="\n"
				log.write(statement)

			# add potential wumpus marks to unexplored cells surrounding stench cells
			wumpus=[]
			if k[i][j][2]=='s':
				if i>0:
					if k[i-1][j][0]=='-':
						k[i-1][j][4]='w'
						wumpus.append([j+1,i])
				if i<len(k)-1:
					if k[i+1][j][0]=='-':
						k[i+1][j][4]='w'
						wumpus.append([j+1,i+2])
				if j>0:
					if k[i][j-1][0]=='-':
						k[i][j-1][4]='w'
						wumpus.append([j,i+1])
				if j<len(k[0])-1:
					if k[i][j+1][0]=='-':
						k[i][j+1][4]='w'
						wumpus.append([j+2,i+1])

			# if wumpus has already been found, don't add more potential wumpus locations
			if len(wumpus)==1:
				k[wumpus[0][1]-1][wumpus[0][0]-1][5]='W'
			elif len(wumpus)>1:
				for w in range(0,len(wumpus)):
					if k[wumpus[w][1]-1][wumpus[w][0]-1][5]=='W':
						wumpus = []
						break

			# log potential wumpus locations
			if len(wumpus)>0:
				statement = "W(" + str(wumpus[0]) + ")"
				if len(wumpus)>1:
					for w in range(1,len(wumpus)):
						statement += " | W(" + str(wumpus[w]) + ")"
				statement+="\n"
				log.write(statement)


# shoots arrow; if arrow hits, removes wumpus from map array and stenches/potential wumpuses from knowledge array, outputs scream
def shoot(m,k,p,f):

	# initialize beginning and end of range for arrow to travel
	low = 0
	high = 0

	# initialize whether arrow will travel on X-axis or Y-axis
	x = True

	# set range and axis
	if f=='EAST':
		low = p[0]-1
		high = len(m)
	elif f=='WEST':
		high = p[0]
	elif f=='NORTH':
		low = p[1]-1
		high = len(m[0])
		x = False
	else:
		high = p[1]
		x = False

	# shoot arrow on X-axis
	if x==True:
		for i in range(low,high):

			# arrow hits wumpus
			if m[p[1]-1][i]=='W':
				# remove wumpus from map
				m[p[1]-1][i]='X'
				# remove wumpus stench/inferences from knowledge base
				for a in range(0,len(k)):
					for b in range(0,len(k[a])):
						if k[a][b][2]=='s':
							k[a][b][2] = '-'
							# log
							log.write("~S(" + str([b+1,a+1]) + ")\n")
						if k[a][b][4]=='w':
							k[a][b][4] = '-'
							# log
							log.write("~W(" + str([b+1,a+1]) + ")\n")
				print "You hear a SCREAM!"
				break

	# shoot arrow on Y-axis
	else:
		for i in range(low,high):

			# arrow hits wumpus
			if m[i][p[0]-1]=='W':
				# remove wumpus from map
				m[i][p[0]-1]='X'
				# remove wumpus stench/inferences from knowledge base
				for a in range(0,len(k)):
					for b in range(0,len(k[a])):
						if k[a][b][2]=='s':
							k[a][b][2] = '-'
							# log
							log.write("~S(" + str([b+1,a+1]) + ")\n")
						if k[a][b][4]=='w':
							k[a][b][4] = '-'
							# log
							log.write("~W(" + str([b+1,a+1]) + ")\n")
				print "You hear a SCREAM!"


if __name__ == "__main__":

	world = raw_input("Enter input file name: ")
	initialize(world, map_arr, know_arr)
	maxr = len(map_arr)
	maxc = len(map_arr[0])

	#set percepts and inferences for starting square
	sense(map_arr,pos)
	infer(know_arr)

	while dead==False and win==False:
		prompt = "You are in room " + str(pos) + " of the cave. Facing " + facing + "."
		prompt += return_percepts(know_arr,pos)
		prompt += hint(know_arr,pos)
		prompt += "\nWhat would you like to do? Please enter command [R,L,F,S]: "
		playerMove = move(prompt,maxr,maxc,pos,facing,arrow)

		# player moves forward
		if playerMove[0]!=pos:
			pos = playerMove[0]

			# update dead and win conditions
			if map_arr[pos[1]-1][pos[0]-1]=='P' or map_arr[pos[1]-1][pos[0]-1]=='W':
				dead = True
			if map_arr[pos[1]-1][pos[0]-1]=='G':
				win = True

			# update percepts if current cell is unexplored
			if know_arr[pos[1]-1][pos[0]-1][0]=='-':
				percept_holder = sense(map_arr,pos)
				for i in range(0,len(know_arr[pos[1]-1][pos[0]-1])):
					if percept_holder[i]!='-':
						know_arr[pos[1]-1][pos[0]-1][i]=percept_holder[i]

			# update inferences
			infer(know_arr)

		# player turns
		elif playerMove[1]!=facing:
			facing = playerMove[1]

		# player shoots arrow
		else:
			shoot(map_arr,know_arr,pos,facing)
			arrow = False

	if dead==True:
		print "YOU LOSE :("
	if win==True:
		print "YOU WIN :)"
	
	# close logger
	log.close()




