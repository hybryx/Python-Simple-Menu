from enum import Enum
import textwrap

class option_types(Enum):
	USER_INPUT = "USER_INPUT"
	MENU_POINTER = "MENU_POINTER"
	EXIT = "EXIT"
	RETURN_PREV = "RETURN_PREV"

class Menu():
	def __init__(self, menu_title, menu_subtitle):
		self.menu_items = []
		self.menu_title = menu_title
		self.menu_subtitle = menu_subtitle

	def add_options(self, menu_items):
		# Adding all menu items to menu object
		for x in menu_items:
			# Getting the sub items from this one menu line
			sub_options = x[list(x)[0]]

			# Confirming that each sub menu has an option_type key
			if "option_type" not in sub_options.keys():
				exit("[!] Error: Each menu option must have the \"option_type\" key-value pair")
			
			# Confirming that each menu option is an instance of option_types class
			if not isinstance(sub_options["option_type"], option_types):
				exit("[!] Error: The value of the \"option_type\" key must be an instance of the option_types class")
			
			# Appending cleared menu item to menu object
			self.menu_items.append(x)

		final_option = {
			"Exit" : {
				"option_type" : "exit_program"
			}
		}

		self.menu_items.append(final_option)		

	def show_menu(self):
		# Clearing the screen		
		self.clear()

		# Finding max width
		width = 0
		optionWidth = 0
		for x in range(len(self.menu_items)):
			if len(list(self.menu_items[x])[0]) > optionWidth:
				optionWidth = len(list(self.menu_items[x])[0])

		width = max(optionWidth, len(self.menu_title))
		width += 8

		print("+" + ("-" * (width - 2)) + "+")
		print("|" + self.menu_title.center(width - 2) + "|")
		print("+" + ("-" * (width - 2)) + "+")

		middle = []
		for line in textwrap.fill(self.menu_subtitle, width - 2).split("\n"):
			print("|" + line.ljust(width - 2, " ") + "|")

		print("+" + "-" * (width - 2) + "+")
		for x in range(len(self.menu_items)):
			thisLine = str(x + 1) + ". " + list(self.menu_items[x])[0]
			while len(thisLine) != width - 2:
				thisLine += " "
			print("|" + thisLine + "|")
		print("+" + "-" * (width - 2) + "+")

		# Handling user input on current menu
		self.input_handler()

	def input_handler(self):
		print()
		result = input("> ")
		
		int_result = int(result) - 1

		menu_option = list(self.menu_items[int_result])[0]

		option_type = self.menu_items[int_result][menu_option]["option_type"]
		
		if option_type == option_types.USER_INPUT:
			# Collection list of questions
			questions = self.menu_items[int_result][menu_option]["questions"]
			# List to hold answers
			answers = []
			# Question prompt for all sets of questions
			question_prompt = self.menu_items[0][menu_option]["question_message"]
			
			# Getting max width of any question
			width = 0
			for x in range(len(questions)):
				print(len(questions[x]))
				if len(questions[x]) > width:
					width = len(questions[x])
			width += 20
			width = max(width, len(question_prompt) + 2)

			# While still answering questions
			while True:
				# Clearing entire screen
				self.clear()

				# Printing question prompt inside screen
				print("+" + str("-" * (width - 2)) + "+")
				print("|" + question_prompt + "|")
				print("+" + str("-" * (width - 2)) + "+")				
				
				for x in range(len(questions)):
					if x == len(answers):
						print("| > " + questions[x] + ":" + (" " * (width - len(questions[x]) - 6)) + "|")
					else:
						try:
							print("| " + questions[x] + ": " + answers[x] + (" " * (width - len(questions[x]) - len(answers[x]) - 6)) + " |")
						except:
							print("| " + questions[x] + ":" + (" " * (width - len(questions[x]) - 4)) + "|")

				print("+" + str("-" * (width - 2)) + "+")

				print()
				#print(len(answers), len(questions))
				answers.append(input("> "))
	
				answer = ""
				if len(answers) == len(questions):
					print("Is this all correct Y/N?")
					answer = input("> ")

				if answer.lower() == "y":
					# Call function with answers[] here
					break
				elif answer.lower() == "n":
					# Resetting
					answers = []

			answer_function = self.menu_items[int_result][menu_option]["call_function"]
			print(answer_function)
			
			if answer_function == None:
				# Reshowing current menu
				self.show_menu()
			else:
				answer_function(answers)
				# Reshowing current menu
				self.show_menu()
		elif option_type == option_types.MENU_POINTER:
			print("Need to link to a new menu")
			newMenu = self.menu_items[int_result][menu_option]["menu_pointer"]
			newMenu.show_menu()
		elif option_type == option_types.EXIT:
			# Exiting the program
			exit(0)
		elif option_type == option_types.RETURN_PREV:
			print("REturn ")
			newMenu = self.menu_items[int_result][menu_option]["menu_pointer"]
			newMenu.show_menu()

	def clear(self):
		print("\033c")

	def get_menu_name(self):
		return self.menu_name

def main():
	# Defining menu objects
	mainMenu = Menu("VMWare Automation Toolkit", "Please make a selection from below. Option 1 will build the most simple and basic lab. Other options are to follow but they will require more information")
	subMenu = Menu("subMenu", "Test")
	subMenu2 = Menu("subSubMenu", "Test")

	"""
	testingMenu =[
		{
			"Enter data here" : {
				"option_type" : option_types.USER_INPUT,
				"question_message" : "Message prompt for subsequent question",
				"questions" : [
					"Question 1",
					"Question 2",
					"Question 3"
				],
				"call_function" : func,
			}
		},
		{
			"Go to sub menu" : {
				"option_type" : "menu_pointer",
				"menu_pointer" : subMenu
			}
		},
		{
			"Go to sub menu" : {
				"menu_pointer" : subMenu
			}
		},
	]
	"""

	# Defining menu options
	mainMenuItems = [
		{
			"Build simple lab" : {
				"option_type" : option_types.USER_INPUT,
				"question_message" : "Message prompt for subsequent question",
				"questions" : [
					"Question 1",
					"Question 2",
					"Question 3"
				],
				"call_function" : func,
			}
		},
		{
			"Go to sub menu" : {
				"option_type" : option_types.MENU_POINTER,
				"menu_pointer" : subMenu
			}
		}
	]

	subMenuItems = [
		{
			"Sub screen 1 question section" : {
				"option_type" : option_types.USER_INPUT,
				"question_message" : "Message prompt for subsequent question",
				"questions" : [
					"Question to ask 1",
					"Question to ask 2"
				],
				"call_function" : None
			},
		},
		{
			"Sub screen 2, pointer to sub sub" : {
				"option_type" : option_types.MENU_POINTER,
				"menu_pointer" : subMenu2
			},
		},
		{
			"Return to previous menu": {
				"option_type" : option_types.RETURN_PREV,
				"menu_pointer" : mainMenu
			}
		}
	]

	subMenu2Items = [
		{
			"This is an input type" : {
				"option_type" : option_types.USER_INPUT,
				"question_message" : "Message prompt for subsequent question",
				"questions" : [
					"What is your favorite color?",
					"What is your age?",
					"What is your sex?"
				],
				"call_function" : None
			}
		},
		{
			"Return to previous menu": {
				"option_type" : option_types.RETURN_PREV,
				"menu_pointer" : subMenu
			}
		}
	]

	# Adding options to menus
	mainMenu.add_options(mainMenuItems)
	subMenu.add_options(subMenuItems)
	subMenu2.add_options(subMenu2Items)

	mainMenu.show_menu()

def func(listOfStuff):
	print("In func")
	print(listOfStuff)
main()
#print(option_types.USER_INPUT)
