import cv2

def compress_video(video_path, output_path, compression_level=1.0): #change compression-level when ready to pass in
    """
    Compresses a video file based on the given compression level.

    Args:
    - video_path (str): Path to the input video file.
    - output_path (str): Path to save the compressed video file.
    - compression_level (float): Compression level as a percentage of original quality (0.0 to 1.0).
                                1.0 represents no compression, 0.75 represents 75% compression, and so on.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change codec as per your requirement
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame based on compression level
        if compression_level < 1.0:
            frame = cv2.resize(frame, (0, 0), fx=compression_level, fy=compression_level)

        # Write the frame into the file 'output_path'
        out.write(frame)

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage:
# You can call compress_video with different compression levels from another script
# For example:
# compress_video('path_to_your_video.mp4', 'output_compressed.mp4', compression_level=0.75)
# compress_video('path_to_your_video.mp4', 'output_no_change.mp4', compression_level=1.0)
