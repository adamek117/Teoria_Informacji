import pandas as pd

if __name__ == '__main__':
    # Wczytaj dane z pliku CSV
    file_path = 'results/results_multi.csv'
    results_df = pd.read_csv(file_path)

    # Grupowanie danych według języka i algorytmu oraz obliczenie średnich
    grouped_results = results_df.groupby(['Language', 'Algorithm']).mean()

    # Zresetowanie indeksu dla czytelniejszego wyświetlania
    grouped_results = grouped_results.reset_index()

    # Zapisanie wyników do nowego pliku CSV
    output_file = 'results/grouped_results.csv'
    grouped_results.to_csv(output_file, index=False)

    print(f'Zgrupowane wyniki zapisano w pliku: {output_file}')
