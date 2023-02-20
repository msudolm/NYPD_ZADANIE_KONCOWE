from tools.parse_args import parse_args
from tools.load_dataframes import load_dataframes, print_sizes
from tools.unify_data import unify_dataframes
from tools.analysis import analyze


print_df_sizes = True

#function loads data from files to dataframes: year x country_name
def load(args,  prt_sizes=print_df_sizes):
	print("\nWczytuję dane...") #print("\nLoading data from paths...")
	dfs = load_dataframes(args.population, args.gdp, args.emission)
	if prt_sizes: print_sizes(dfs)
	print("...gotowe.") #print("...done.")
	return dfs

#function filters years aceording to --start and --end arguments if provided
def filter_start_end(args, dfs,  prt_sizes=print_df_sizes):
	if args.start is not None or args.end is not None:
		print(f"\nFiltruję dane zgodnie z zadanymi parametrami start/end...")
		if args.start is not None: dfs = [df.loc[df.index >= args.start] for df in dfs]
		if args.end is not None: dfs = [df.loc[df.index <= args.end] for df in dfs]			
		
		if prt_sizes: print_sizes(dfs)
		print("...gotowe.")
	return dfs

#function crops dataframes to contain only countries and years present in all dataframes
def crop_to_shared_records(dfs,  prt_sizes=print_df_sizes):
	print("\nFiltrowanie krajów i lat występujących we wszystkich tabelach...")
	dfs = unify_dataframes(dfs)

	if prt_sizes: print_sizes(dfs)
	print("...gotowe.")
	return dfs


#function checks if any of the dataframes has no row indexes or no column names
def any_empty(dfs: list):
	return 0 in [df.shape[0] for df in dfs]+[df.shape[1] for df in dfs]




def run_analysis():
	#parsing arguments
	args = parse_args()	
	if args is None:
		print("Brak przekazanych argumentów. Kończę wykonywanie programu.")
		return

	#loading data from files to dataframes
	dfs = load(args)
	if any_empty(dfs):
		print("Co najmniej jedna z ramek danych wczytanych z podanych plików jest pusta. Kończę wykonywanie programu")
		return

	#filtering data according to start/end attributes
	dfs = filter_start_end(args, dfs)

	if any_empty(dfs):
		print("\nPo filtrowaniu względem zadanych argumentów start/end, co najmniej jedna z ramek danych jest pusta. Kończę wykonywanie programu")
		return

	#keep only countries and years present in all dataframes
	dfs = crop_to_shared_records(dfs)
	if any_empty(dfs):
		print("\nPo usunięciu wszystkich krajów oraz lat, które nie występują we wszystkich danych, co najmniej jedna z ramek danych jest pusta. Kończę wykonywanie programu")
		return


	#analyze data
	print("\nPrzeprowadzanie analiz i zapisywanie niewyświetlanych wyników...")
	if dfs[0].shape[0] < 5:
		print("\tUwaga! Liczba krajów w analizowanych danych jest mniejsza niż 5!")
	analyze(dfs)
	print("\nWyniki analiz dla top 5 emisji i top 5 wartości wskaźnika gdp dostępne w plikach: '../top5_gdp.csv' and '../top5_co2.csv'") 
	print("...gotowe.\n")


if __name__ == "__main__":

	run_analysis()


	



