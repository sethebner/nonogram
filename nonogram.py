import argparse
import copy
import time
import random

from itertools import chain, combinations

random.seed(1)

HEIGHT = 30
LENGTH = 30

# CLUES = {"row": [[1], [3], [5], [7], [9], [11], [13], [13], [15], [15], [15], [6, 1, 6], [4, 1, 4], [3], [5]],
# 		 "col": [[4], [7], [8], [9], [10], [10, 1], [10, 2], [15], [10, 2], [10, 1], [10], [9], [8], [7], [4]]}

# CLUES = {"row": [[1,1,6,3], [3,2,3,2], [3,1,5,1], [4,4,1], [5,5,1], [5,5,1], [3,3,2], [3,1,2,3], [3,1,7], [3,7], [3,3,3], [3,2,1,2], [2,2,3], [1,5], [15]],
# 		 "col": [[12,2], [12,1], [13,1], [3,1], [1,1,2,2,1], [2,1], [6,1], [1,4,1], [13,1], [13,1], [2,3,3,2], [2,1,2], [1,4,3], [2,9], [15]]}

# CLUES = {"row": [[6],[6],[4],[1],[10],[4,10],[4,1,1,1],[4,1,1,1],[2,1,1,1],[2,1,1,1],[12,4],[1,9,1,4],[2,9,8],[2,9,8],[2,1,1,8],[1,1,1,8],[19],[1,1,2],[14,3,3],[3,3,2,5,2],[3,3,1,3,8],[3,5,5,7],[3,2,2,2,2,3,3],[5,5,5],[3,3,3]],
# 		 "col": [[2],[3],[3,4],[5,3],[1,4,3],[7,1,5],[3,4,1,1,2,2],[9,1,1,5],[2,9,1,2,3],[2,3,4,1,3],[3,4,1,2,3],[3,4,1,1,5],[2,4,1,1,2,2],[2,7,1,5],[2,2,1,1,2,3],[1,13,3],[2,5,1,3],[2,6,5],[2,5,7],[13,4,2],[2,7,7],[2,8,5],[15,3],[2,2],[2]]}

# CLUES = {"row": [[3],[3,2],[6],[4],[7],[5],[8],[9],[4,5],[4,6],[1,2,7],[11,1],[10,1],[10,2],[9,1],[3,7,1],[2,2,3,1],[1,2,3,2],[2,2,5],[3,3,3]],
# 		 "col": [[2,1],[2,1],[3,1,2],[1,3,4,1],[12,2],[13,5],[6,6],[3,6],[10,1],[10,2],[14],[11],[8],[9],[8],[5],[2],[1,2],[2,2],[5]]}

# CLUES = {"row": [[7],[1,1,2,1,3],[1,1,1,2,1,3],[3,3,2,1,3],[1,1,1,2,2,2],[5,2,1,2,1],[2,5,1,2],[1,2,1,1],[1,4,1,1,2],[3,1,2,1,1],[4,3,1,1],[12,1,1],[8,1,1,1],[9,1,1,],[11,2],[5,5,1],[1,1,5],[1,1,3],[1,1],[1,1,1]],
# 		 "col": [[1],[1],[1,2],[2,2],[1,10],[2,6],[7,1],[4,9],[2,6,5,1],[1,2,14],[1,1,1,1,1,6,1],[2,2,9],[1,1,1,1,1,2],[3,1,1,6],[1,2,1,1,2],[2,1,1,1,4],[2,2,1,2],[5,1,2,3],[2,1,1,2,2],[1,1,1,2,4]]}

CLUES = {"row": [[2,1,1,2],[4,3,1,1,1,2,2],[1,7,1,3,2,1],[1,3,1,2,2,2],[2,1,1,1,2],[2,1,1],[3,7,3],[2,10,2],[2,18,2],[3,2,14,2],[2,1,5,6,2,3,3],[1,7,7,10],[1,8,7,9],[11,6,8],[13,4,11],[14,6],[1,16,3],[1,16],[18],[10,7],[3,6,8],[4,6,7],[4,5,1,7],[5,4,2,6],[5,4,3,5],[6,4,4,5],[5,4,4,5],[4,4,4,5,4],[5,5,4,5,2,3],[5,4,4,7]],
		 "col": [[3,2,4,5],[2,3,4,12],[3,4,1,17],[7,1,18],[1,5,1,9,6,2],[3,1,10,3],[2,1,13],[2,1,19],[2,1,20],[1,20],[22],[2,6,1,2],[5,7,6],[7,7,7],[1,1,8,7,6],[9,8,5],[9,9,2],[1,1,9,11],[1,4,3,1,11],[1,1,5,2,9],[2,10,7],[1,1,4,6,4],[2,1,10,2],[1,1,9,1],[1,2,5,2],[3,4,2],[1,1,1,4,1,1],[3,1,5,3],[9,1,3],[6,1,3]]}

# CLUES = {"row":[[4],[2,1],[1,4,2],[3,2,3,1,3],[2,1,2,3,2],[1,1,1,6,1,1],[2,2,2,2,2,1],[1,3,3,2,1],[2,6,5,2],[1,2,5,2],[3,3,5],[1,2,2,2],[8,1,1],[1,2,2],[1,4],[4,3],[5,4],[4,9],[1,2,6,1,1],[7,1],[5,5,3],[8,4,7],[1,11,5,2],[1,7,3,3,2],[7,12],[2,4,4],[2,3],[2,4],[5],[2,5],[3,4,2,1],[10,2],[4,4],[4],[2]],
# 		 "col":[[4],[2,4],[2,2,2,1],[3,2,5],[2,1,1,5],[1,2,2,1,5],[1,2,1,2,1,5,1],[1,3,1,3,3,1,1],[1,4,1,3,3,1,5],[2,2,1,5,1,9],[1,1,1,1,1,15],[1,1,1,2,2,2,10,2],[1,2,2,1,1,1,7,1,2],[1,1,1,1,2,6,2,2],[1,2,1,1,2,5,1,3],[1,2,1,4,4,2,3],[1,2,2,1,3,3,3,1,2],[1,3,1,6,5,1,2],[4,1,1,2,2,2,2,2,1],[1,2,2,1,2,1,2,2,3],[1,2,1,2,1,2,2,1],[1,2,5,1,2,1],[2,4,4],[5,1,3],[2]]}


UNK = "\u25A1"
YES = "\u25A0"
NO = " "
INCONCLUSIVE = "?"

BOARD = [[UNK]*LENGTH for _ in range(HEIGHT)]

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose', action='store_true')
	parser.add_argument('--slow', action='store_true')
	parser.add_argument('--step', action='store_true')

	args = parser.parse_args()

	return args

def print_board(board, axis, index):
	s = ""
	for i,row in enumerate(board):
		s += " ".join(row)
		if axis == "row" and index == i:
			s += "\t<"
		if i != len(board)-1:
			s += '\n'

	s += '\n'
	if axis == "col":
		s += '  '*index + '^' + '\n'
	else:
		s += '\n'
	
	print(s)

def get_line(board, axis, index):
	if axis == "row":
		return board[index]
	elif axis == "col":
		return [row[index] for row in board]
	else:
		raise ValueError(f"unrecognized axis: {axis}")

def all_clues_satisfied(s):
	return all(s["row"]) and all(s["col"])

def get_solved_line_signature(solved_line):
	if not all([cell in [YES, NO] for cell in solved_line]):
		# not a fully solved line
		return None

	signature = []
	in_block = False
	block_length = 0
	for cell in solved_line + [NO]:  # sentinel for end of line
		if cell == YES:
			if not in_block:
				in_block = True
			
			block_length += 1
		elif cell == NO:
			if in_block:
				signature.append(block_length)
				in_block = False
				block_length = 0
		else:
			raise ValueError(f"solved line has unexpected {cell} cell")

	return signature

def powerset(iterable):
	# https://stackoverflow.com/a/1482316
	s = list(iterable)
	return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def same(iterable):
	if all([x == iterable[0] for x in iterable]):
		return iterable[0]
	else:
		return INCONCLUSIVE

def solve_clue(clue, line, line_num, axis, args):
	print(axis, line_num+1, clue)
	if axis == "row":
		axis_length = LENGTH
	elif axis == "col":
		axis_length = HEIGHT
	else:
		raise ValueError(f"unrecognized axis: {axis}")

	solved_line = copy.deepcopy(line)

	minimum_cells_required = sum(clue) + (len(clue)-1)  # number of cells required if all blocks are separated by a single space
	num_buffer_cells = axis_length - minimum_cells_required
	idx = 0
	for block_num, block_size in enumerate(clue):
		if block_size > num_buffer_cells:
			num_placeable = block_size - num_buffer_cells

			idx += num_buffer_cells
			solved_line[idx:idx+num_placeable] = [YES]*num_placeable

			if (num_buffer_cells == 0) and (idx+num_placeable < len(solved_line)):
				# there is only one way to fill this row
				solved_line[idx+num_placeable] = NO

			idx += num_placeable + 1  # skip one cell past end of block, then skip a cell to separate the block from the next block
		else:
			idx += block_size + 1


	# TODO: replace UNKs with NOs around blocks that are solved


	# Try replacing all UNKs with NOs since clues tend to have only a few blocks
	proposed_solved_line = copy.deepcopy(solved_line)
	unk_idxs = [i for i,cell in enumerate(solved_line) if cell == UNK]
	for i in unk_idxs:
		proposed_solved_line[i] = NO
		if get_solved_line_signature(proposed_solved_line) == clue:
			solved_line = proposed_solved_line

	# Brute force all possibilities
	# TODO: compute overlaps while iterating to early stop some options that aren't guaranteed to be YES/NO
	unk_idxs = [i for i,cell in enumerate(solved_line) if cell == UNK]
	candidate_toggle_idxs = copy.deepcopy(unk_idxs)
	line_superposition = copy.deepcopy(solved_line)
	num_brute_force_proposals = 0
	num_yes_current = sum([1 for cell in solved_line if cell == YES])
	num_yes_in_clue = sum(clue)
	if len(unk_idxs) <= 20:
		possible_solutions = []
		# toggle_sets = list(powerset(candidate_toggle_idxs))
		# random.shuffle(toggle_sets)  # shuffle to try to uncover inconclusive cells more quickly
		toggle_sets = powerset(candidate_toggle_idxs)
		# if args.verbose:
		# 	print(f'{len(toggle_sets)} enumerations')
		for toggle_set in toggle_sets:
			if num_yes_current + len(toggle_set) != num_yes_in_clue:
				# proposed line solution wouldn't have the right signature, so skip it
				continue

			num_brute_force_proposals += 1
			proposed_solved_line = copy.deepcopy(solved_line)
			for i in unk_idxs:
				if i in toggle_set:
					proposed_solved_line[i] = YES
				else:
					proposed_solved_line[i] = NO
			if get_solved_line_signature(proposed_solved_line) == clue:
				possible_solutions.append(proposed_solved_line)
				for _i,_cell in enumerate(proposed_solved_line):
					if line_superposition[_i] == UNK:
						# first instantiated value for this cell, so copy from proposed solution
						line_superposition[_i] = proposed_solved_line[_i]
					elif proposed_solved_line[_i] == line_superposition[_i]:
						# they match, so do nothing
						pass
					else:
						line_superposition[_i] = INCONCLUSIVE
						# we don't know the value of this cell, so don't bother toggling it when enumerating possible solutions
						# NOTE: has odd interactions with determining the line signature because of the UNKs present that aren't set to YES/NO when enumerating proposals
						# if _i in candidate_toggle_idxs:
						# 	candidate_toggle_idxs.remove(_i)
						# 	toggle_sets = list(powerset(candidate_toggle_idxs))
						# 	random.shuffle(toggle_sets)
						# 	if args.verbose:
						# 		print(f"Removed {_i} from toggle set")


			if all([line_superposition[j] == INCONCLUSIVE for j in unk_idxs]):
				# we can't conclude anything new about the line, so exit early
				if args.verbose:
					print("Exiting brute force early")
				break

		solved_cells = [same(l) for l in zip(*possible_solutions)]  # cells that take the same value across all possible solutions, so they are guaranteed to be correct

		for unk_idx in unk_idxs:
			try:
				if solved_cells[unk_idx] != INCONCLUSIVE:
					# print("Brute forced a solved cell")
					solved_line[unk_idx] = solved_cells[unk_idx]
			except:
				import pdb; pdb.set_trace()

		if args.verbose:
			print(f"{num_brute_force_proposals} brute force proposals")

	# solving shouldn't modify the length of the line
	assert len(solved_line) == len(line)
	if solved_line != line:
		if args.verbose:
			num_new_cells_solved = len(solved_line) - len([same(l) for l in zip(line, solved_line) if same(l) != INCONCLUSIVE])
			print(f"Solved {num_new_cells_solved} more cells.")			
			print(line)
			print(solved_line)

	return solved_line

def main():
	args = parse_args()

	assert len(CLUES["row"]) == HEIGHT
	assert len(CLUES["col"]) == LENGTH

	# number of YES cells should be the same row-wise and column-wise
	assert sum([sum(clue) for clue in CLUES["row"]]) == sum([sum(clue) for clue in CLUES["col"]])

	# print_board(BOARD)

	satisfied_clues = {"row": [False]*HEIGHT,
					   "col": [False]*LENGTH}

	# keep track of solution progress to avoid doing work if line is in the same state as the last time we visited it
	previous_state = {"row": [None for _ in range(HEIGHT)],
					  "col": [None for _ in range(LENGTH)]}

	axis = "row"
	while not all_clues_satisfied(satisfied_clues):
		for i,clue in enumerate(CLUES[axis]):
			current_clue = clue
			if satisfied_clues[axis][i]:
				# swap axis if at end of row/column
				if i == len(CLUES[axis])-1:
					if axis == "row":
						axis = "col"
						# print(f"New axis: {axis}")
					elif axis == "col":
						axis = "row"
						# print(f"New axis: {axis}")
					else:
						raise ValueError(f"unrecognized axis: {axis}")
				
				continue

			# get line for this clue
			if axis == "row":
				line = BOARD[i]
			elif axis == "col":
				line = [row[i] for row in BOARD]
			else:
				raise ValueError(f"unrecognized axis: {axis}")

			if previous_state[axis][i] == line:
				# this line is the same as the last time we visited it, so don't redo the same work
				if args.verbose:
					print(f'No change to {axis} {i} since last time: {clue}, {line}')

				# swap axis if at end of row/column
				if i == len(CLUES[axis])-1:
					if axis == "row":
						axis = "col"
						# print(f"New axis: {axis}")
					elif axis == "col":
						axis = "row"
						# print(f"New axis: {axis}")
					else:
						raise ValueError(f"unrecognized axis: {axis}")
				continue

			previous_state[axis][i] = line  # what the line looked like before making progress on it

			solved_line = solve_clue(clue, line, i, axis, args)
			made_progress = (solved_line != line)

			# set line for this clue
			if axis == "row":
				BOARD[i] = solved_line
			elif axis == "col":
				for j,cell in enumerate(solved_line):
					BOARD[j][i] = cell
			else:
				raise ValueError(f"unrecognized axis: {axis}")

			if UNK not in solved_line:
				satisfied_clues[axis][i] = True

			print_board(BOARD, axis, i)

			# swap axis if at end of row/column
			if i == len(CLUES[axis])-1:
				if axis == "row":
					axis = "col"
					# print(f"New axis: {axis}")
				elif axis == "col":
					axis = "row"
					# print(f"New axis: {axis}")
				else:
					raise ValueError(f"unrecognized axis: {axis}")

			if made_progress:
				if args.slow:
					time.sleep(2)
				if args.step:
					input("Press Enter to continue.")

			print()

	print("SOLVED THE PUZZLE!!!")


if __name__ == "__main__":
	main()