import pandas as pd


def load_raw_dataframes_from_paths(population_path, gdp_path, co2_path):
    '''Funkcja wczytuje dane z plików csv pod podanymi ścieżkami do obiektów pandas.DataFrame.'''
    df_population_raw = pd.read_csv(population_path, skiprows=4)
    df_gdp_raw = pd.read_csv(gdp_path, skiprows=4)
    df_co2_raw = pd.read_csv(co2_path)
    
    return [df_population_raw, df_gdp_raw, df_co2_raw]

def prepare_worldbank_df(raw_df):
    '''Funkcja przygotowuje dane z formatu z'data.worldbank.org'
    do analizy (tabela postaci lata x kraje)'''
    
    df = raw_df.T
    
    #czy niepowtarzalne nazwy w wierszu 'Country name'
    assert len(set(df.loc['Country Name'])) == len(df.columns)
    
    #ustaw nagłówek
    countries_caps = [c.upper() for c in df.loc['Country Name']]
    df.set_axis(list(countries_caps), axis=1, inplace=True)
    
    #pozostawiamy tylko wiersze z latami (w tym formacie tabeli: od czwartego poza nagłówkiem do przedostatniego)
    df = df[4:-1]
    
    return df
def co2_to_year_vs_country_format(co2_df):
    '''Funkcja konwertuje ramkę danych, zawierającą rekordy o emisji CO2 w danym roku przez dany kraj
    (ramka musi zawierać kolumny: 'Year', 'Country', 'Total')
    do ramki, w której indeksami są wartości z 'Year', nazwami kolumn wartości z 'Country', a wartościami zawartość kolumny'Total' '''
    
    ## w oryginalnych danych kolumna 'Year' przechowuje typ 'int', w worlbank to 'str' 
    df = co2_df.astype({'Year': 'str'})
    return df.pivot(index='Year', columns='Country', values='Total')

def load_dataframes(population_path, gdp_path, co2_path):
	dfs_raw = load_raw_dataframes_from_paths(population_path, gdp_path, co2_path)
	df_population, df_gdp = [prepare_worldbank_df(df) for df in dfs_raw[:-1]]
	df_co2 = co2_to_year_vs_country_format(dfs_raw[-1])

	return [df_population, df_gdp, df_co2]


def print_sizes(dfs, language='pl'):
    assert len(dfs) == 3
    assert language in {'pl', 'en'}

    if language == 'en':
        print("\tDataframes content:")
        for name, df in zip(['population', 'gdp', 'emission'], dfs):
            print(f"\t{name}: {df.shape[0]} years, {df.shape[1]} countries")

    if language == 'pl':
        print("\tZawartość ramek danych:")
        for name, df in zip(['population', 'gdp', 'emission'], dfs):
            print(f"\t{name}: {df.shape[0]} (lata) x {df.shape[1]} (kraje)")

if __name__ == "__main__":
	pass

