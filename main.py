import cv2
import os
import shutil

# ASCII characters from darkest to lightest
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Convert pixel to ASCII character
def pixel_to_ascii(pixel):
    return ASCII_CHARS[pixel // 25]

# Convert frame to ASCII
def frame_to_ascii(frame):
    terminal_size = shutil.get_terminal_size((80, 24))  # Default size if not detected
    terminal_width, terminal_height = terminal_size.columns, terminal_size.lines

    # Resize frame to fit terminal width (keeping aspect ratio)
    height, width, _ = frame.shape
    aspect_ratio = height / width
    new_width = terminal_width
    new_height = int(aspect_ratio * new_width / 2)  

    if new_height > terminal_height:
        new_height = terminal_height

    # Resize frame and convert to grayscale
    resized_frame = cv2.resize(frame, (new_width, new_height))
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # Convert each pixel to an ASCII character
    ascii_frame = "\n".join(
        "".join(pixel_to_ascii(pixel) for pixel in row) for row in gray_frame
    )
    
    return ascii_frame

def play_video_in_ascii(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Cannot open video file at {video_path}.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Video opened successfully! Resolution: {frame_width}x{frame_height}, Total frames: {frame_count}")

    # Read and process frames
    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Error: Frame could not be read or end of video reached.")
                break

            # Convert frame to ASCII
            ascii_frame = frame_to_ascii(frame)

            # Clear the terminal and print the ASCII frame
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_frame)

            # Speed up display by 1.5x by reducing the delay
            cv2.waitKey(33)  # 33ms delay for approximately 1.5x speed

    except KeyboardInterrupt:
        print("Video interrupted.")
    finally:
        cap.release()

if __name__ == "__main__":
    video_path = "video/【東方】Bad Apple!! ＰＶ【影絵】.mp4"  # Update with your video path
    play_video_in_ascii(video_path)
