"""
a simple implementation of the popular game wordle.

usage: python wordle.py --num_chars 5
"""

from argparse import ArgumentParser
from english_words import get_english_words_set
import secrets

class Wordle():
	"""
	main class to play the game wordle
	"""

	def __init__(self, num_chars):

		self.num_chars = num_chars
		
		self.candidate_words = None
		self.answer = None
		self.guess_list = []
		self.result_list = []

		self.game_state = None # can be "in_progress", "won", "lost"

		print(f"\nStarted a Wordle instance of {num_chars} characters.\n")
		
	def SelectAnswerWord(self):
		"""
		randomly select the final answer word of num_chars characters
		"""

		print(f"Randomly selecting a {self.num_chars} characters word from the corpus.")
		all_english_words = get_english_words_set(['web2'], lower=True, alpha=True)
		print(f"All English words = {len(all_english_words)}")
		self.candidate_words = [word for word in all_english_words if len(word) == self.num_chars]
		print(f"Candidate words = {len(self.candidate_words)}")
		self.answer = secrets.choice(self.candidate_words)
		print(f"Done. Ready to start Wordle.\n")
		self.game_state = "in_progress"

		return self.answer

	def GetUserInput(self):
		"""
		get user's input and check for restrictions
		"""

		print("\n" + "="*50)
		print(f"ROUND {len(self.guess_list)+1}\n")

		while True:

			guess = input("Enter Guess (-1 to end game): ")
			guess = guess.strip().lower()

			if guess == "-1":
				self.game_state = "lost"
				return None

			if len(guess) != self.num_chars:
				print(f"Please enter a word of {self.num_chars} characters.\n")
				continue

			if guess not in self.candidate_words:
				print("Word not in dictionary. Please try again.\n")
				continue

			self.guess_list.append(guess)
			return guess

	def ValidateCurrentGuess(self):
		"""
		validate the currectness of the current guess
		and update the result history
		"""

		current_guess = self.guess_list[-1]
		current_result = ""

		for idx in range(len(current_guess)):

			# the position and the value, both correct
			if current_guess[idx] == self.answer[idx]:
				current_result += "G"

			# the value is correct but the position is not
			elif current_guess[idx] in self.answer:
				current_result += "Y"

			# neither the position nor the value is correct
			else:
				current_result += "B"

		self.result_list.append(current_result)
		return current_result

	def PrintResultHistory(self):
		"""
		pretty print the result history
		"""

		result_map = {
			"G": "Green, Position and Value both correct.",
			"Y": "Yellow, Value is correct, Position is incorrect.",
			"B": "Black, neither Position nor Value is correct.",
		}

		for idx in range(len(self.guess_list)):

			print("\n" + self.guess_list[idx])

			for c, r in zip(self.guess_list[idx], self.result_list[idx]):
				print(f"{c}: {result_map[r]}")

	def CheckGameWon(self):
		"""
		check if the game is won
		"""

		if list(set(self.result_list[-1])) == ["G"]:
			self.game_state = "won"


def main(num_chars):
	"""
	start and play the wordle game with num_chars
	"""

	# instantiate the game
	game = Wordle(num_chars)

	# select the answer word
	answer = game.SelectAnswerWord()
	# print(answer)

	while game.game_state == "in_progress":

		# get the validated user input
		user_input = game.GetUserInput()

		if user_input is None:
			continue

		# check for the correctness of the guess
		# and print the state and results
		current_result = game.ValidateCurrentGuess()
		# print(current_result)

		# print the result history
		game.PrintResultHistory()

		# check if the game is won
		game.CheckGameWon()

	print("\n" + "="*50 + "\n")
	print(f"Final Game State = {game.game_state}")
	print(f"Number of Rounds = {len(game.guess_list)}")
	print(f"Correct Answer = {game.answer}")
	print("\n" + "="*50 + "\n")


if __name__ == '__main__':

	# set up argument parser
	parser = ArgumentParser(description='argument parser for wordle config')
	parser.add_argument('--num_chars', default=5, type=int, help='number of chars in the word')
	args = parser.parse_args()

	# call the main wordle function
	main(args.num_chars)
