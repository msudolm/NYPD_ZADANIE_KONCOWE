import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Analyze data')
	parser.add_argument('--population', required=True)
	parser.add_argument('--gdp', required=True)
	parser.add_argument('--emission', required=True)

	parser.add_argument('--start', default=None)
	parser.add_argument('--end', default=None)

	args = parser.parse_args()

	#print(args)
	return args


if __name__ == "__main__":
	pass
