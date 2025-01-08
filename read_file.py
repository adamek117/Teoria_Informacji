def read_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()  # Odczytuje cały plik
            text = text.replace('\n', ' ')  # Opcjonalnie zamiana nowych linii na spacje
            text = text.replace('\u202f', ' ')  # Zamiana wąskiej spacji na zwykłą
            #text = text.strip()  # Usunięcie zbędnych białych znaków
        return text
    except FileNotFoundError:
        print(f"Plik o ścieżce {file_path} nie został znaleziony.")
        return None
    except IOError:
        print(f"Wystąpił błąd podczas odczytu pliku {file_path}.")
        return None
