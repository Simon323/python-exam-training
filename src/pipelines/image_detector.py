import json
import os
import re
import uuid

import pytesseract
from PIL import Image


def extract_text_from_images(directory_path, output_directory="questions"):
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

    # Utwórz katalog na wyniki, jeśli nie istnieje
    verified_dir = os.path.join(output_directory, "verified")
    issued_dir = os.path.join(output_directory, "issued")
    os.makedirs(verified_dir, exist_ok=True)
    os.makedirs(issued_dir, exist_ok=True)

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

            # Sprawdź, czy pytanie zaczyna się numerem
            question_id = None
            question_match = re.match(r"^(\d+)[ \.]", question)
            if question_match:
                question_id = question_match.group(1)

            # Określ katalog zapisu
            output_dir = verified_dir if question_id else issued_dir

            # Wygeneruj nazwę pliku
            file_name = f"{question_id}.json" if question_id else f"{uuid.uuid4()}.json"
            file_path = os.path.join(output_dir, file_name)

            # Zapisz wynik do pliku JSON
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)

            print(f"Wynik zapisany w pliku: {file_path}")

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {image_file}: {e}")


# Przykład użycia
# extract_text_from_images("ścieżka/do/katalogu", "ścieżka/do/questions")
