from src.pipelines import download_video, extract_frames

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=yMqldbY2AAg&ab_channel=ByteByteGo"  # Provide the video URL
    downloads_folder = "downloads"  # Subfolder for downloaded videos
    frames_folder = "frames"  # Subfolder for extracted frames

    # Download the video and save it in the downloads directory
    video_path = download_video(video_url, output_folder=downloads_folder)

    # Extract frames and save them in the frames directory
    extract_frames(video_path, output_folder=frames_folder)
