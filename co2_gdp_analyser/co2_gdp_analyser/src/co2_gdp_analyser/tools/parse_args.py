import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Analyze data')
	parser.add_argument('--population', required=True, help="Path to file with population data.")
	parser.add_argument('--gdp', required=True, help="Path to file with gdpdata.")
	parser.add_argument('--emission', required=True, help="Path to file with emission data.")

	parser.add_argument('--start', default=None, help="Eaerliest year considered.", type=int)
	parser.add_argument('--end', default=None, help="Latest year considered", type=int)

	args = parser.parse_args()

	if args.start is not None and args.end is not None:
		if args.start > args.end:
			print(f"Niepoprawne wartości argumentów --start, --end ({args.start} > {args.end}).",
				"Podaj niepusty zakres", sep="\n")
			return

	#print(args)
	return args


if __name__ == "__main__":

	args = parse_args()
	print(args)
	print(args.start is None)
	pass
