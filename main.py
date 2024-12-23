from src.pipelines import download_video, extract_frames

if __name__ == "__main__":
    video_url = (
        "https://youtu.be/h4NwRcDnyFw?si=R7gvOY2B-hai86KM"  # Provide the video URL
    )
    downloads_folder = "downloads"  # Subfolder for downloaded videos
    frames_folder = "frames"  # Subfolder for extracted frames
    frame_interval = 10  # Interval in seconds to extract frames

    # Download the video and save it in the downloads directory
    video_path = download_video(video_url, output_folder=downloads_folder)

    # Extract frames and save them in the frames directory
    extract_frames(video_path, output_folder=frames_folder, interval=frame_interval)
