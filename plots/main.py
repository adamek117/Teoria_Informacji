import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_compression_plot(df):
    """
    Generuje wykres słupkowy przedstawiający efektywność kompresji w różnych językach.

    :param df: DataFrame z danymi
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Language', y='Ratio', hue='Algorithm')
    plt.title('Efektywność kompresji (Współczynnik kompresji)')
    plt.ylabel('Współczynnik kompresji')
    plt.xlabel('Język')
    plt.legend(title='Algorytm')
    plt.tight_layout()
    plt.show()
    plt.savefig('compression_plot.png')


def generate_worktime_plot(df):
    """
    Generuje wykres słupkowy przedstawiający czas pracy algorytmów w różnych językach.

    :param df: DataFrame z danymi
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Algorithm', y='Time [s]', hue='Language')
    plt.title('Czas wykonania algorytmów dla różnych języków')
    plt.ylabel('Czas [s]')
    plt.xlabel('Algorytm')
    plt.legend(title='Język')
    plt.tight_layout()
    plt.show()
    plt.savefig('worktime_plot.png')


def generate_informationgained_plot(df):
    """
    Generuje wykres słupkowy przedstawiający ilość informacji zyskaną po kompresji w różnych językach.

    :param df: DataFrame z danymi
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Language', y='Information Gain [bytes]', hue='Algorithm')
    plt.title('Informacja zaoszczędzona dzięki kompresji')
    plt.ylabel('Zysk informacji [bajty]')
    plt.xlabel('Język')
    plt.legend(title='Algorytm')
    plt.tight_layout()
    plt.show()
    plt.savefig('informationgained_plot.png')


def generate_stability_boxplot(df):
    """
    Generuje wykres pudełkowy (box plot) dla stabilności czasowej algorytmów.

    :param df: DataFrame z danymi
    """
    # Ustawienia wykresu
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Algorithm', y='Stability Mean [s]')
    plt.title('Stabilność czasowa algorytmów')
    plt.ylabel('Czas wykonania (średnia) [s]')
    plt.xlabel('Algorytm')
    plt.tight_layout()
    plt.show()
    plt.savefig('stability_boxplot(.png')



if __name__ == '__main__':
    # Ścieżka do pliku CSV
    file_path = "../results/results_16_25.csv"

    # Mapowanie nazw języków z angielskiego na polski
    languages_translation = {
        "English": "Angielski",
        "French": "Francuski",
        "Hungary": "Węgierski",
        "Polish": "Polski",
    }

    # Wczytanie danych
    data = pd.read_csv(file_path)

    # Zmiana nazw języków na polskie
    data["Language"] = data["Language"].map(languages_translation)

    # Ustawienie stylu wykresów
    sns.set_theme(style="whitegrid")

    """Generowanie wykresów"""
    # Wykres efektywności kompresji
    generate_compression_plot(data)

    # Wykres czasu pracy algorytmów
    generate_worktime_plot(data)

    # Wykres informacji zaoszczędzonej dzięki kompresji
    generate_informationgained_plot(data)

    # Wykres stabilności czasowej algorytmów
    generate_stability_boxplot(data)
