import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

def entropy_plot_func(polish_value, english_value, french_value,hungarian_value ):

    # Dane przykładowe: entropia dla 4 języków
    languages = ["Polish", "English", "French", "Hungarian"]
    entropy_values = [polish_value,english_value, french_value, hungarian_value]  # Przykładowe wartości entropii
    
    # Tworzenie wykresu
    plt.figure(figsize=(8, 6))  # Rozmiar wykresu
    plt.bar(languages, entropy_values, color='skyblue', edgecolor='black')
    
    # Opisy osi i tytuł
    plt.xlabel("Language", fontsize=16)
    plt.ylabel("Huffman entropy value",  fontsize=16)
    plt.title("Entropy in every language", fontsize=16)
    
    # Wyświetlenie wykresu
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


