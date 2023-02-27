import pandas as pd

###########################
# Moduł przeprowadzający analizy wartości emisji oraz gdp w przeliczeniu na mieszkańca.
# Wyznaczanie krajów o top 5 wartościach emisji / gdp w przeliczeniu na mieszkańca dla każdego roku występującego w dostarczonych ramkach danych (lata muszą być zgodne między ramkami)
# oraz wypisywanie nazw krajów, które w największym stopniu zmniejszyły / zwiększyły emisje CO2 na osobę w przeciągu ostatnich k (k=10) lat.
#
############################


def per_capita_dfs(dfs):
    df_population, df_gdp, df_co2 = dfs
    df_co2_per_capita = (df_co2 / df_population).astype(float).sort_index(axis=0)
    df_gdp_per_capita = (df_gdp / df_population).astype(float).sort_index(axis=0)

    dfs_per_capita = [df_gdp_per_capita, df_co2_per_capita]
    return dfs_per_capita
def top_5_scores(df_per_capita, df_total, k=5):
    '''Funkcja dla przekazanych ramek danych: z wartościami per capita i z wartościami sumarycznie,
    zwraca ramkę danych, posortowaną po latach, z krajami o top k wartościach w ramce per-capita
    i wartościach dla tych krajów w ramce df_total.
    Uwaga - obie rami muzą mieć zgodne indeksy oraz nazwy kolumn.'''
    
    assert (df_per_capita.index == df_total.index).all()
    assert (df_per_capita.columns == df_total.columns).all()
    
    df_list = []
    
    for year in df_per_capita.index:
        largest_5 = df_per_capita.loc[year].nlargest(k)
        largest_5_totals = df_total.loc[year][largest_5.index]
        
        df_c = pd.concat([largest_5, largest_5_totals], axis=1).reset_index()
        df_c.insert(0,'Year', year)
        df_c.columns = ['Year', 'Country', 'Per capita', 'Total']
        df_list.append(df_c)
    df_all = pd.concat(df_list, axis=0) #, ignore_index=True)
    #df_all = df_all.sort_values('Year')
    
    return df_all
def calculate_tables(dfs, dfs_per_capita):
    '''Funkcja zwraca jako listę pandas.DataFrame's tabele, które zosały zdefiniowane w poleceniu.'''
    top5_gdp_df = top_5_scores(dfs_per_capita[-2], dfs[-2])
    top5_co2_df = top_5_scores(dfs_per_capita[-1], dfs[-1])
    return [top5_gdp_df, top5_co2_df]

def save_tables(df_tables:list):
    df_tables[0].to_csv('../top5_gdp.csv')
    df_tables[1].to_csv('../top5_co2.csv')
    return

def top_differences(df, k=10):
    '''Funkcja dla podanej ramki danych wypisuje nazwy kolumn (krajów),
    dla których odnotowano najwyższy wzrost/spadek w wartościach między ostatnim a -k-tym wierszem (rokiem).
    Jeżeli dla żadnej z kolumn nie nastąpił wzrost/(spadek), wypisany zostanie odpowiedni komunikat.
    Uwaga: ta funkcja nie sortuje danych, uzytkownik dostarcza dane w wybranym przez siebie porządku.'''
    
    assert k >0
    if len(df) < k:
        print(f"\tUwaga! Zadany przedział lat ({k}) jest większy niż liczba lat dostępnych w danych ({df.shape[0]}).",
            "Nie zostanie przeprowadzona analiza spadku / wzrostu emisji dla okresu ostatnich 10 lat.")
        return
    
    #obliczanie różnicy wartości między ostatnim a k-tym od końca wierszem tabeli, dla każdej z kolumn
    diffs = df.iloc[-1] - df.iloc[-k]
    #nazwy krajów o największych różnicach
    ctr_max, ctr_min = diffs.idxmax(), diffs.idxmin()
    
    print("\n###########################################################################################")
    #kraj o największej zmianie w emisji między ostatnim wierszem w danych a k-tym
    if diffs[ctr_max] > 0:
        print(f"Kraj o największym wzroście emisji CO2 na osobę w przeciągu {k} ostatnich lat (z danych):")
        print(f"{ctr_max}: wzrost o {round(diffs[ctr_max], 6)} na osobę")
    else:
        print("Żaden z uwzględnionych krajów nie zwiększył emisji względem początku rozpatrywanego przedziału.")
    
    #największy spadek w emisji
    if diffs[ctr_min] < 0:
        print(f"\nKraj o największym spadku emisji CO2 na osobę w przeciągu {k} ostatnich lat (z danych):")
        print(f"{ctr_min}: spadek o {round(-diffs[ctr_min], 6)} na osobę")
    else:
        print("\nŻaden z uwzględnionych krajów nie zwiększył emisji względem początku rozpatrywanego przedziału.")
    print("###########################################################################################\n")
#Funkcja wykonująca wszystkie operacje z wykorzystaniem powyższych funkcji
def analyze(dfs):
    dfs_per_capita = per_capita_dfs(dfs)

    #zapisanie wspólnych nazw krajów i lat, które ostatecznie zostały poddane analizie do plików csv
    countries_left, years_left = dfs_per_capita[0].columns.to_series(), dfs_per_capita[0].index.to_series()
    countries_left.to_csv('../analyzed_countries.csv', index=False)
    years_left.to_csv('../analyzed_years.csv', index=False)
    print("\n\n##########",
        "# Nazwy krajów oraz lata, dla których przeprowadzono analizy,",
        "# zostały zapisane w plikach '../analyzed_countries.csv' oraz '../analyzed_years.csv'",
        "###########\n", sep="\n")

    results = calculate_tables(dfs, dfs_per_capita)
    save_tables(results)
    top_differences(dfs_per_capita[-1]) #co2 per capita


    return





if __name__ == "__main__":
	pass