import os
import re
from entropy_plot import entropy_plot_language, entropy_plot_languages
from plots.time_plot import time_plot_language, time_plot_languages

def parse_metrics(file_path):
    """
    Funkcja do odczytu i analizy danych z pliku tekstowego.
    Zwraca słownik zawierający wybrane wartości.
    """
    results = {}  # Słownik na dane
    general_results ={}
    # Otwieranie pliku i czytanie jego zawartości
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Wyodrębnianie sekcji dla różnych metod (Huffman, Arithmetic, ANS)
    sections = re.split(r"-{10,}", content)  # Oddzielamy na podstawie "-----"
    
    # Przetwarzanie każdej sekcji
    for section in sections:
        if "Language:" in section:
            # Wyciąganie języka
            language_match = re.search(r"Language: (\w+)", section)
            language = language_match.group(1) if language_match else "Unknown"
            results[language] = {}
            general_results[language]= {}

            general_data ={
                "Entropy": float(re.search(r"Entropy: ([\d.]+(?:e[-+]?\d+)?) bits per symbol", section).group(1)),
                "Original Size": float(re.search(r"Original Size: ([\d.]+(?:e[-+]?\d+)?) bytes", section).group(1)),
            }
            results[language]["General"] = general_data
        
        # Wyciąganie wartości dla Huffman
        if "Huffman" in section:
            huffman_data = {
                "Time": float(re.search(r"Huffman Time: ([\d.]+(?:e[-+]?\d+)?) seconds", section).group(1)),
                "Compressed Size": float(re.search(r"Huffman Compressed Size: ([\d.]+(?:e[-+]?\d+)?) bytes", section).group(1)),
                "Entropy": float(re.search(r"Huffman Entropy: ([\d.]+(?:e[-+]?\d+)?) bits per symbol", section).group(1)),
                "Efficiency": float(re.search(r"Huffman Efficiency: ([\d.]+(?:e[-+]?\d+)?)",section).group(1)),
            }
            results[language]["Huffman"] = huffman_data
        
        # Wyciąganie wartości dla Arithmetic
        if "Arithmetic" in section:
            arithmetic_data = {
                "Time": float(re.search(r"Arithmetic Time: ([\d.]+(?:e[-+]?\d+)?) seconds", section).group(1)),
                "Compressed Size": float(re.search(r"Arithmetic Compressed Size: ([\d.]+(?:e[-+]?\d+)?) bytes", section).group(1)),
                "Entropy": float(re.search(r"Arithmetic Entropy: ([\d.]+(?:e[-+]?\d+)?) bits per symbol", section).group(1)),
                "Efficiency": float(re.search(r"Arithmetic Efficiency: ([\d.]+(?:e[-+]?\d+)?)",section).group(1)),
            }
            results[language]["Arithmetic"] = arithmetic_data
        
        # Wyciąganie wartości dla ANS
        if "ANS" in section:
            ans_data = {
                "Time": float(re.search(r"ANS Time: ([\d.]+(?:e[-+]?\d+)?) seconds", section).group(1)),
                "Compressed Size": float(re.search(r"ANS Compressed Size: ([\d.]+(?:e[-+]?\d+)?) bytes", section).group(1)),
                "Entropy": float(re.search(r"ANS Entropy: ([\d.]+(?:e[-+]?\d+)?) bits per symbol", section).group(1)),
                "Efficiency": float(re.search(r"ANS Efficiency: ([\d.]+(?:e[-+]?\d+)?)",section).group(1)),
            }
            results[language]["ANS"] = ans_data
    
    return results


# Funkcja do przetwarzania wielu plików
def parse_multiple_files(directory_path):
    """
    Funkcja do analizy wielu plików w podanym katalogu.
    Zwraca zbiorczy słownik z wynikami dla wszystkich plików.
    """
    all_results = {}  # Zbiorczy słownik na wyniki
    general_file_results ={}
    # Iteracja po wszystkich plikach w katalogu
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Tylko pliki tekstowe
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {file_path}")
            
            # Parsowanie danych z pliku
            file_results = parse_metrics(file_path)
            # Łączenie wyników w zbiorczym słowniku
            for language, metrics in file_results.items():
                if language not in all_results:
                    all_results[language] = []
                all_results[language].append(metrics)
    
    return all_results

def plots_main_func():
    directory_path = "results"  # Zamień na ścieżkę do swojego katalogu z plikami
    parsed_data= parse_multiple_files(directory_path)
    compression_values={}
    entropy_values ={}
    time_values ={}
    efficency_values ={}

    # Wyświetlenie wyników
    for lang, data_list in parsed_data.items():
        #print(f"\nLanguage: {lang}")
        entropy_values[lang] =[]
        time_values[lang] = []
        compression_values[lang]=[]
        efficency_values[lang] =[]
        for i, data in enumerate(data_list):
            #print(f"  File {i + 1}:")
            for method, values in data.items():
                #print(f"    {method}:")
                for key, value in values.items():
                    if key == "Entropy":
                        entropy_values[lang].append(value)
                    if key == "Time":
                        time_values[lang].append(value)
                    if key == "Compressed Size":
                        compression_values[lang].append(value)
                    if key =="Efficiency":
                        efficency_values[lang].append(value)
                        #print(f" {key}: {value}")
    
    general_text_entropy =[]
    entropy_Huffman=[] 
    entropy_ANS =[]
    entropy_arithmetic=[]
    time_Huffman=[]
    time_ANS =[]
    time_arithmetic=[]
    compressed_size_Huffman=[]
    compressed_size_ANS=[]
    compressed_size_arithmetic=[]
    efficency_Huffman=[]
    efficency_ANS=[]
    efficency_arithmetic=[]
    

    """Entropy"""
    for lang in parsed_data.keys():
        general_text_entropy.append(entropy_values[lang][0])
        entropy_Huffman.append(entropy_values[lang][1])
        entropy_arithmetic.append(entropy_values[lang][2])
        entropy_ANS.append(entropy_values[lang][3])
        time_Huffman.append(time_values[lang][0])
        time_arithmetic.append(time_values[lang][1])
        time_ANS.append(time_values[lang][2])
        compressed_size_Huffman.append(compression_values[lang][0])
        compressed_size_ANS.append(compression_values[lang][1])
        compressed_size_arithmetic.append(compression_values[lang][2])
        efficency_Huffman.append(efficency_values[lang][0])
        efficency_arithmetic.append(efficency_values[lang][1])
        efficency_ANS.append(efficency_values[lang][2])

    entropy_plot_languages(entropy_Huffman,"Huffman")
    entropy_plot_languages(entropy_arithmetic,"Arithmetic")
    entropy_plot_languages(entropy_ANS,"ANS")
    
    entropy_English=(entropy_values["English"])
    entropy_French = entropy_values["French"]
    entropy_Hungary = entropy_values["Hungary"]
    entropy_Polish = entropy_values["Polish"]
    entropy_plot_language(entropy_English,"English")
    entropy_plot_language(entropy_French,"French")
    entropy_plot_language(entropy_Hungary,"Hungary")
    entropy_plot_language(entropy_Polish,"Polish")

    """time_plot"""
    time_plot_languages(time_Huffman,"Huffman")
    time_plot_languages(time_arithmetic,"Arithmetic")
    time_plot_languages(time_ANS,"ANS")

    time_English = time_values["English"]
    time_French = time_values["French"]
    time_Hungary = time_values["Hungary"]
    time_Polish = time_values["Polish"]
    time_plot_language(time_English,"English")
    time_plot_language(time_French,"French")
    time_plot_language(time_Hungary,"Hungary")
    time_plot_language(time_Polish,"Polish")

plots_main_func()
