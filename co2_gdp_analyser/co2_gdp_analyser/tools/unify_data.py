import pandas as pd


def crop_to_shared_labels(dfs:list, axis=0)->list:
    '''Funkcja dla zadanej listy ramek danych, zwraca ramki przefiltrowane po wspólnych etykietach
    (indeksach (axis=0) lub nazwach kolumn (axis=1))'''
    
    assert len(dfs) > 0
    assert axis in {0,1}
    
    ax = 'index' if not axis else 'columns'
    
    shared_labels = set(dfs[0].eval(ax))
    for df in dfs[1:]:
        shared_labels.intersection_update(set(df.eval(ax)))
    shared_labels = sorted(list(shared_labels))
    
    dfs_filtered_sorted = [df.filter(items=shared_labels, axis=axis) for df in dfs]
    return dfs_filtered_sorted
def remove_nan_columns(df):
    #axis: 0->remove rows, 1->remove columns
    return df.dropna(axis=1)
def sort_dfs(dfs):
    dfs_sorted = [df.sort_index(axis=0) for df in dfs]
    dfs_sorted = [df.sort_index(axis=1) for df in dfs_sorted]
    return dfs_sorted

def unify_dataframes(dfs: list)->list:
	dfs = [df.astype(float) for df in dfs]

	dfs = crop_to_shared_labels(dfs, axis=0)
	dfs = crop_to_shared_labels(dfs, axis=1)

	#removing columns witch contains any NaN values
	dfs = [remove_nan_columns(df) for df in dfs]

	#unifying data after deleting columns with nan's
	dfs = crop_to_shared_labels(dfs, axis=0)
	dfs = crop_to_shared_labels(dfs, axis=1)

	return dfs

if __name__ == "__main__":
	pass