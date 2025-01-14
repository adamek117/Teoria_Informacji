import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

def entropy_plot_func():
    # Dane przykładowe: entropia dla 4 języków
    languages = ["Polish", "English", "French", "Hungarian"]
    entropy_values = [4.5, 4.3, 4.6, 4.4]  # Przykładowe wartości entropii
    
    # Tworzenie wykresu
    plt.figure(figsize=(8, 6))  # Rozmiar wykresu
    plt.bar(languages, entropy_values, color='skyblue', edgecolor='black')
    
    # Opisy osi i tytuł
    plt.xlabel("Language", fontsize=16)
    plt.ylabel("Entropy value", fontsize=16)
    plt.title("Entropy in every language", fontsize=16)
    
    # Wyświetlenie wykresu
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

