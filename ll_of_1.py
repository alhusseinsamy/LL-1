import argparse



def get_first(lit, rules):
	for rule in rules:
		if rule[0] == lit:
			return rule[2]



def compute_ll(rules, alphabet):
	matches = []
	for rule in rules:
		# print(rule[0])
		firsts = rule[2]
		found_epsilon = False
		match_firsts = []
		for first in firsts:
			matching_rs = []
			if first != 'epsilon':
				for rs in rule[1]:
					if rs.startswith(first):
						matching_rs.append((rule[0],first,rs))
						matches.append((rule[0],first,rs))
					else:
						if rs[0].isupper():
							if rs[0] == rule[0]:
								return 'invalid'
								matching_rs.append((rule[0],first,rs))
								matches.append((rule[0],first,rs))
							else:
								if first in get_first(rs[0], rules):
									matching_rs.append((rule[0],first,rs))
									matches.append((rule[0],first,rs))
			else:
				found_epsilon = True

			if len(matching_rs)>1:
				return 'invalid'	
			
			# print(matching_rs)	

		if found_epsilon == True:
			follows = rule[3]
			has_epsilon = []
			for follow in follows:
				matches.append((rule[0],follow, 'epsilon'))
				has_epsilon.append((rule[0],follow, 'epsilon'))
	

	return matches			



def check_input(inp, output_1, start_symbol, alphabet):
	# print(alphabet)
	stack = []
	stack.append('$')
	stack.append(start_symbol)

	my_input = inp.split(' ')
	my_input.append('$')
	print(my_input)	

	print(alphabet)

	i = 0

	while(True):
		print(my_input[i])
		print(stack[len(stack)-1])
		print('___________-')
		if (my_input[i] != '$') and (not stack[len(stack)-1].isupper()) and (stack[len(stack)-1] != '$'):
			stack.pop()
			i+=1


		elif (my_input[i] != '$') and (stack[len(stack)-1].isupper()):
			found = False
			for o in output_1:
				val = my_input[i]
				if (stack[len(stack)-1] == o[0]) and (o[1] == val) and (o[2] != ' '):
					stack.pop()
					chars = o[2]
					if chars == 'epsilon':
						found = True
						break
					to_push = []
					to_push.extend(chars)
					to_push.reverse()

					dash = ''
					for el in to_push:
						if ((el+dash) not in alphabet) and ((el+dash) not in list(set([x[0] for x in output_1]))) and ((el+dash) != 'epsilon'):
							dash=(el+dash)
						else:	
							stack.append(el+dash)
							dash=''
					found = True	
					break
			if found == False:
				return 'no'	

		elif (my_input[i] == '$') and (not stack[len(stack)-1].isupper()) and (stack[len(stack)-1] != '$'):
			return 'no'

		elif (my_input[i] == '$') and (stack[len(stack)-1].isupper()):
			found = False
			for o in output_1:
				val = my_input[i]
				if (stack[len(stack)-1] == o[0]) and (o[1] == val) and (o[2] != ' '):
					stack.pop()
					chars = o[2]
					if chars == 'epsilon':
						found = True
						break
					to_push = []
					to_push.extend(chars)
					to_push.reverse()

					dash = ''
					for el in to_push:
						if ((el+dash) not in alphabet) and ((el+dash) not in list(set([x[0] for x in output_1]))) and ((el+dash) != 'epsilon'):
							dash=(el+dash)
						else:	
							stack.append(el+dash)
							dash=''
					found = True	
					break
			if found == False:
				return 'no'

		elif (my_input[i] != '$') and (stack[len(stack)-1] == '$'):
			return 'no'

		elif (my_input[i] == '$') and (stack[len(stack)-1] == '$'):	
			return 'yes'				
		

								










if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--grammar', action="store", help="path of file to take as input to read grammar", nargs="?", metavar="dfa_file")
    parser.add_argument('--input', action="store", help="path of file to take as input to test strings on LL table", nargs="?", metavar="input_file")
    
    args = parser.parse_args()

    print(args.grammar)
    print(args.input)

    rules = []
    alphabet = []
    start_symbol = ''
    with open(args.grammar) as fl:
    	start_symbol = fl.readline().split(':')[0].replace(' ','')

    with open(args.grammar) as f:
    	for line in f:
    		arr = line.split(':')
    		arr1 = line.split()
    		for x in arr1:
    			if (x != ':') and (not (x.isupper())) and (x != '|') and (x != 'epsilon'):
    				alphabet.append(x)
    		left_side = arr[0].replace(' ', '')
    		right = arr[1].replace(' ', '').replace('\n', '')
    		right_side = right.split('|')
    		firsts = arr[2].replace('\n', '').split(' ')
    		follows = arr[3].replace('\n', '').split(' ')
    		firsts = list(filter(None, firsts))
    		follows = list(filter(None, follows))
    		matches = []
    		rule_temp = [left_side, right_side, firsts, follows, matches]
    		rule = tuple(rule_temp)
    		rules.append(rule)

    	alphabet = list(set(alphabet))

    	# print(rules)	

    	matches = compute_ll(rules, alphabet)

    	# print(matches)


    	if matches != 'invalid':
    		output_1=[]
	    	for rule in rules:
	    		for a in alphabet:
	    			found = False
	    			for match in matches:
	    				if (match[0] == rule[0]) and (match[1] == a):
	    					output_1.append((rule[0], a, match[2]))
	    					found = True
	    			if found == False:
	    				output_1.append((rule[0], a, ' '))
	    	print(output_1)	
	    	# print(start_symbol)

	    	with open('task_6_1_result.txt', 'w') as f2:
	    		# for x in output_1:
	    		# 	f2.write(x[0] + ' : ' + x[1] + ' : ' + x[2])
	    		# 	f2.write('\n')

	    		for x in output_1:
	    			third_arg = x[2]
	    			thrd_arg = []
	    			thrd_arg.extend(third_arg)
	    			thrd_arg.reverse()
	    			print(thrd_arg)
	    			my_x =[]
	    			if (len(thrd_arg)>1) and (third_arg!='epsilon'):
	    				dash = ''
	    				for el in thrd_arg:
	    					if ((el+dash) not in alphabet) and ((el+dash) not in list(set([x[0] for x in output_1]))) and ((el+dash) != 'epsilon'):
	    						dash = el+dash
	    					else:
	    						my_x.append(el+dash)
	    						dash = ''
	    				my_x.reverse()			
	    				
	    				
	    				f2.write(x[0] + ' : ' + x[1] + ' : ')
	    				for v in my_x:
	    					f2.write(v+' ')
	    				f2.write('\n')
	    			else:
	    				f2.write(x[0] + ' : ' + x[1] + ' : ' + x[2])
	    				f2.write('\n')			


	    	with open(args.input) as f1:	
	    		inp = f1.readline()		
	    		ret = check_input(inp, output_1, start_symbol, alphabet)
	    		
	    		with open('task_6_2_result.txt', 'w') as f3:
	    			f3.write(ret)

    	else:
	    	with open('task_6_1_result.txt', 'w') as f2:
	    		f2.write('invalid LL(1) grammar')

	    			