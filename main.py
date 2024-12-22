from src.pipelines import download_video, extract_frames

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=yMqldbY2AAg&ab_channel=ByteByteGo"  # Podaj URL filmu
    downloads_folder = "downloads"  # Podfolder na pobrane filmy
    frames_folder = "frames"  # Podfolder na wyekstrahowane klatki
    
    # Pobierz film i zapisz w katalogu downloads
    video_path = download_video(video_url, output_folder=downloads_folder)
    
    # Wyciągnij klatki i zapisz w katalogu frames
    extract_frames(video_path, output_folder=frames_folder)
