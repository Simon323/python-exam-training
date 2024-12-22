from pytubefix import YouTube
import cv2
import os

def create_folder(folder_path):
    """Creates a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to download video from YouTube
def download_video(url, output_folder="downloads"):
    create_folder(output_folder)  # Ensure the folder for downloaded videos exists
    download_path = os.path.join(output_folder, "downloaded_video.mp4")
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()  # Download the video in the highest quality
    stream.download(output_path=output_folder, filename="downloaded_video.mp4")
    print(f"Video downloaded to {download_path}")
    return download_path

# Function to extract frames every 60 seconds
def extract_frames(video_path, output_folder="frames"):
    create_folder(output_folder)  # Ensure the folder for frames exists

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video parameters
    fps = cap.get(cv2.CAP_PROP_FPS)  # frames per second
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # total number of frames
    duration = total_frames / fps  # video duration in seconds

    # Extract frames every 60 seconds
    for sec in range(0, int(duration), 60):
        # Set frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, sec * fps)

        # Capture frame
        ret, frame = cap.read()

        if ret:
            # Save frame to file
            frame_filename = os.path.join(output_folder, f"frame_{sec}s.png")
            cv2.imwrite(frame_filename, frame)
            print(f"Frame at {sec} seconds saved as {frame_filename}")
        else:
            print(f"Failed to extract frame at {sec} seconds")

    cap.release()

# Example usage
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=h4NwRcDnyFw&ab_channel=sthithapragna"  # Change to your video URL
    
    # Download video
    video_path = download_video(video_url, output_folder="downloads")

    # Extract frames
    extract_frames(video_path, output_folder="frames")
