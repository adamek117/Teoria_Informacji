import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_compression_plot(df, save_to_png):
    """
    Generuje wykres słupkowy przedstawiający efektywność kompresji w różnych językach.

    :param df: DataFrame z danymi
    :param save_to_png: Zapisywanie do pliku
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Language', y='Ratio', hue='Algorithm')
    plt.title('Efektywność kompresji (Współczynnik kompresji)')
    plt.ylabel('Współczynnik kompresji')
    plt.xlabel('Język')
    plt.legend(title='Algorytm')
    plt.tight_layout()
    plt.show()
    if save_to_png:
        plt.savefig('compression_plot.png')


def generate_time_plot(df, save_to_png):
    """
    Generuje wykres słupkowy przedstawiający czas pracy algorytmów w różnych językach.

    :param df: DataFrame z danymi
    :param save_to_png: Zapisywanie do pliku
    """
    # Pobierz unikalne języki
    languages = df['Language'].unique()

    # Przygotowanie układu 2x2 dla każdego języka
    fig, axs = plt.subplots(2, 2, figsize=(14, 12))
    axs = axs.flatten()

    for i, lang in enumerate(languages):
        # Filtrowanie danych dla bieżącego języka
        lang_data = df[df['Language'] == lang]
        # Grupowanie po algorytmach i obliczanie średnich czasów
        lang_times = lang_data.groupby('Algorithm')[['Encode time [s]', 'Decode time [s]']].mean()

        # Tworzenie wykresu dla bieżącego języka
        lang_times.plot(kind='bar', ax=axs[i], logy=True, alpha=0.8, legend=False)
        axs[i].set_title(f"{lang}", fontsize=12)  # Tylko nazwa języka
        axs[i].set_ylabel("Czas (s, skala logarytmiczna)", fontsize=10)
        axs[i].set_xlabel("")
        axs[i].tick_params(axis='x', rotation=0)

    # Dodanie jednej wspólnej legendy poniżej wykresów
    fig.legend(['Czas kodowania', 'Czas dekodowania'], loc='lower center', fontsize=10, ncol=2, title="Operacja",
               title_fontsize=12, bbox_to_anchor=(0.5, -0.1))

    # Dodanie głównego tytułu dla całej figury
    fig.suptitle("Porównanie czasów kodowania i dekodowania dla różnych języków i algorytmów", fontsize=14)

    # Dostosowanie odstępów w dolnej części, aby legenda się zmieściła
    plt.subplots_adjust(bottom=0.2)

    # Wyświetlenie wykresów
    plt.show()

    if save_to_png:
        plt.savefig('time_plot.png')


def generate_information_gained_plot(df, save_to_png):
    """
    Generuje wykres słupkowy przedstawiający ilość informacji zyskaną po kompresji w różnych językach.

    :param df: DataFrame z danymi
    :param save_to_png: Zapisywanie do pliku
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Language', y='Information Gain [bytes]', hue='Algorithm')
    plt.title('Informacja zaoszczędzona dzięki kompresji')
    plt.ylabel('Zysk informacji [bajty]')
    plt.xlabel('Język')
    plt.legend(title='Algorytm')
    plt.tight_layout()
    plt.show()
    if save_to_png:
        plt.savefig('information_gained_plot.png')


def generate_stability_boxplot(df, save_to_png):
    """
    Generuje wykres pudełkowy (box plot) dla stabilności czasowej algorytmów.

    :param df: DataFrame z danymi
    :param save_to_png: Zapisywanie do pliku
    """
    # Ustawienia wykresu
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Algorithm', y='Stability Mean [s]')
    plt.title('Stabilność czasowa algorytmów')
    plt.ylabel('Czas wykonania (średnia) [s]')
    plt.xlabel('Algorytm')
    plt.tight_layout()
    plt.show()
    if save_to_png:
        plt.savefig('stability_boxplot.png')



if __name__ == '__main__':
    # Ścieżka do pliku CSV
    file_path = "../results/grouped_results.csv"

    # Czy zapisywać wykresy?
    save_to_png = False

    # Mapowanie nazw z angielskiego na polski
    languages_translation = {
        "English": "Angielski",
        "French": "Francuski",
        "Hungary": "Węgierski",
        "Polish": "Polski",
    }

    algorithms_translation = {
        "Huffman": "Huffman",
        "Arithmetic": "Arytmetyczne",
        "ANS": "ANS"
    }

    # Wczytanie danych
    data = pd.read_csv(file_path)

    # Zmiana nazw na polskie
    data["Language"] = data["Language"].map(languages_translation)
    data["Algorithm"] = data["Algorithm"].map(algorithms_translation)

    # Ustawienie stylu wykresów
    sns.set_theme(style="whitegrid")

    """Generowanie wykresów"""
    # Wykres efektywności kompresji
    generate_compression_plot(data, save_to_png)

    # Wykres czasu pracy kodowania i dekodowania
    generate_time_plot(data, save_to_png)

    # Wykres informacji zaoszczędzonej dzięki kompresji
    generate_information_gained_plot(data, save_to_png)

    # Wykres stabilności czasowej algorytmów
    generate_stability_boxplot(data, save_to_png)
