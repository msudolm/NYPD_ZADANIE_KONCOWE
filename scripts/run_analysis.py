from tools.parse_args import parse_args
from tools.load_dataframes import load_dataframes
from tools.unify_data import unify_dataframes
from tools.analysis import analyze





if __name__ == "__main__":


	args = parse_args()
	#print(f"Checkpoint: sprawdzam ładowanie argumentów {args.population=}")

	#loading data to dataframes: year x country_name
	print("\nLoading data from paths...")
	dfs = load_dataframes(args.population, args.gdp, args.emission)
	print("...done.")

	########
	#
	#TODO: przefiltrować po start, end (łącznie z wyjątkiem)
	#
	########

	#cropping to common countries and common years
	print("Cropping data to shared countries and years...")
	dfs = unify_dataframes(dfs)
	print("...done.")
	print(f"\n{len(dfs[0])} years and {len(dfs[0].columns)} countries left after intersecting and filtering.")

	#####
	#
	#obsłużyć przypadek, w którym zostało mniej niż thresh krajów
	#
	#####

	print("Running and saving analysis...")
	analyze(dfs)
	print("...finished.",
		"Results in: '../top5_gdp.csv' and '../top5_co2.csv'")
	



