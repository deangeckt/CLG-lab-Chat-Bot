import os
os.chdir('../../code_switch')
from code_switch.utils import hazard

def test_hazard() -> None:
	"""
	This function tests the hazard function
	@return: This function only prints out the results to the screen
	"""
	r = [0, 4, 2, 1, 1]
	for s in range(len(r)+1):
		h = hazard(r, s)
		print("s = {}".format(s))
		print("h = {}".format(h))
		print("*"*3)

def run_tests():
	test_hazard()

if __name__ == '__main__':
	run_tests()