def prompt_question(question):
	answer = ''
	while answer != 'y' and answer != 'n':
		answer = input(question)
	if answer == 'y':
		return True
	if answer == 'n':
		return False

