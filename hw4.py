# Maggie Borkowski
# Intro to AI
# HW 4

import operator

# adds word w to dict d, adds w to previous word pw's sub-dictionary
# (if w already in pw sub-dict, updates frequency)
def addword(d,w,pw):

	# add w to d; value of w is subdict, to be filled with all words that directly follow w
	if w not in d:
		subdict = dict()
		d[w] = subdict

	# 1st word of twocities won't have a previous word
	if len(pw)>0:
		# add w to pw's sub-dict if it is not already there
		if w not in d[pw]:
			d[pw][w] = 1

		# otherwise, increase the frequency of w in pw's sub-dict by 1
		else:
			d[pw][w] += 1


if __name__ == "__main__":

	# store entire text in twocities
	f = open('twocities.txt', 'r')
	twocities = f.read()
	f.close()

	# convert to uppercase to avoid case-sensitive dictionary duplicates
	twocities = twocities.upper()

	# dictionary to store each word
	dickensdict = dict()

	# tokenize text into words, add all words to dictionary
	word = ""
	prevword = ""
	for ch in twocities:
		if (ch.isalnum()==True or ch=='-'):
			word += ch
			# '-' is part of a word, while '--' is a delimiter
			if word.endswith('--'):
				word = word[:(len(word)-2)]
				addword(dickensdict,word,prevword)
				prevword = word
				word = ""
		else:
			if len(word)>0:
				addword(dickensdict,word,prevword)
				prevword = word
				word = ""

	# change word frequencies to probabilities
	for w in dickensdict:
		# float so that later division doesn't truncate
		total = 0.0

		# get total number of words that follow word w
		for x in dickensdict[w]:
			total += dickensdict[w][x]

		# divide each word y's frequency by total to get probability of y following w
		for y in dickensdict[w]:
			dickensdict[w][y] /= total
			# round decimal to 2 points
			dickensdict[w][y] = round(dickensdict[w][y], 2)

	print dickensdict

	# user interaction loop
	print "\nWelcome to the Charles Dickens Texting Assistant!\n"
	message = ""
	cont = True
	while cont==True:

		# prompt user for text, repeat prompt if text is only whitespace
		usertext = ""
		while len(usertext)==0:
			usertext = raw_input("Enter a word or phrase, or enter TTYL to quit:\n")
			usertext = usertext.strip()
		usertext = usertext.upper()

		# quit
		if usertext=='TTYL':
			cont = False
			continue
		# add input to full message
		else:
			if len(message)>0:
				message += " "
			message += usertext

		# if user entered multiple words, use only the last word
		if ' ' in usertext:
			last = usertext.rfind(' ')
			usertext = usertext[last+1:]

		# find usertext in dictionary
		if usertext in dickensdict:
			if len(dickensdict[usertext])>0:
				
				# sort following words by probability, highest first
				# yields list of [key,value] tuples
				suggestions = sorted(dickensdict[usertext].items(), key=operator.itemgetter(1), reverse=True)

				# print 4 suggestions, or all suggestions if length of list < 4
				print "\n-----SUGGESTIONS FOR NEXT WORD:-----"
				r = 4
				if len(suggestions)<4:
					r = len(suggestions)
				for i in range(r):
					print suggestions[i][0] + "\t\t\t\tP=" + str(suggestions[i][1])

				print "\n"

			# no following words for usertext
			else:
				print "\nAlas, no suggestions\t\t\t\tP=0.0\n"

		# usertext not in dictionary
		else:
			print "\nAlas, no suggestions\t\t\t\tP=0.0\n"

	# print complete user message
	print "\nHere is your full message:"
	print message



