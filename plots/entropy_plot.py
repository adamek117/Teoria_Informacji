import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

def entropy_plot_languages(values,algorithm):

    # Dane przykładowe: entropia dla 4 języków
    languages = ["English", "French","Hungarian","Polish"]
    entropy_values = [values[0], values[1], values[2], values[3]]  # Przykładowe wartości entropii
    
    # Tworzenie wykresu
    plt.figure(figsize=(8, 7))  # Rozmiar wykresu
    plt.bar(languages, entropy_values, color='skyblue', edgecolor='black')
    
    # Ustalanie zakresu osi Y
    y_min = 0 # Niewielki margines poniżej minimum
    y_max = max(entropy_values) + 0.1  # Niewielki margines powyżej maksimum
    plt.ylim(y_min, y_max)

    # Automatyczne tworzenie podziałów osi Y w oparciu o dane
    yticks = np.linspace(y_min, y_max, num=30)  # 10 równych podziałów w zakresie danych
    plt.yticks(yticks, fontsize=10)
    
    # Opisy osi i tytuł
    plt.xlabel("Language", fontsize=16)
    plt.ylabel(f"{algorithm} entropy value",  fontsize=16)
    plt.title(f"{algorithm} entropy in every language", fontsize=16)
    
    # Wyświetlenie wykresu
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def entropy_plot_language(values,language):
# Dane przykładowe: entropia dla 4 języków
    languages = ["General", "Huffman", "Arithmetic", "ANS"]
    entropy_values = [values[0], values[1], values[2],values[3]]  # Przykładowe wartości entropii
    
    # Tworzenie wykresu
    plt.figure(figsize=(8, 7))  # Rozmiar wykresu
    plt.bar(languages, entropy_values, color='skyblue', edgecolor='black')
    # Ustalanie zakresu osi Y
    y_min = 0 # Niewielki margines poniżej minimum
    y_max = max(entropy_values) + 0.1  # Niewielki margines powyżej maksimum
    plt.ylim(y_min, y_max)

    # Automatyczne tworzenie podziałów osi Y w oparciu o dane
    yticks = np.linspace(y_min, y_max, num=30)  # 30 równych podziałów w zakresie danych
    plt.yticks(yticks, fontsize=10)
    
    # Opisy osi i tytuł
    plt.xlabel("Algorithm", fontsize=16)
    plt.ylabel(f"{language} entropy value",  fontsize=16)
    plt.title(f"Entropy in every algorithms", fontsize=16)
    
    # Wyświetlenie wykresu
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()