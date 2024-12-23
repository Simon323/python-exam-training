import os
import re

import pytesseract
from PIL import Image


def extract_text_from_images(directory_path):
    # Sprawdź, czy katalog istnieje
    if not os.path.isdir(directory_path):
        print("Podana ścieżka nie jest katalogiem.")
        return

    # Pobierz listę plików graficznych w katalogu
    image_files = [
        f
        for f in os.listdir(directory_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
    ]

    if not image_files:
        print("Brak plików graficznych w katalogu.")
        return

    # Iteruj przez pliki graficzne
    for image_file in image_files:
        image_path = os.path.join(directory_path, image_file)
        try:
            # Wczytaj obraz
            image = Image.open(image_path)

            # Wyodrębnij tekst z obrazu
            text = pytesseract.image_to_string(image)

            # Rozdziel tekst na linie
            lines = text.strip().split("\n")
            question_lines = []
            answers = []
            current_answer = None

            # Flaga oznaczająca, czy zaczęliśmy przetwarzać odpowiedzi
            in_answers_section = False

            for line in lines:
                line = line.strip()

                # Sprawdź, czy linia zaczyna się od litery odpowiedzi (np. "A.", "B.", itd.)
                match = re.match(r"^[A-D]\.\s", line)

                if match:
                    # Jeśli jest to nowa odpowiedź, zapisz poprzednią odpowiedź
                    if current_answer:
                        answers.append(current_answer)
                    # Rozpocznij nową odpowiedź
                    current_answer = line
                    in_answers_section = True
                elif in_answers_section:
                    # Dodaj linie do bieżącej odpowiedzi, jeśli już zaczęliśmy część odpowiedzi
                    current_answer += " " + line
                else:
                    # Dodaj linie do pytania, jeśli jesteśmy nadal w sekcji pytania
                    question_lines.append(line)

            # Dodaj ostatnią odpowiedź do listy
            if current_answer:
                answers.append(current_answer)

            # Złóż pytanie w jeden ciąg tekstowy
            question = " ".join(question_lines)

            # Obiekt wynikowy
            result = {"question": question, "answers": answers}

            # Wyświetl wynik dla bieżącego pliku
            print(f"Wynik dla pliku {image_file}:")
            print(result)

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {image_file}: {e}")


# Przykład użycia
# extract_text_from_images("ścieżka/do/katalogu")
