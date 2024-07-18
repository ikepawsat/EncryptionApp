import cv2
import sys

def compress_video(video_path, output_path, compression_level=1.0):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if compression_level < 1.0:
            frame = cv2.resize(frame, (0, 0), fx=compression_level, fy=compression_level)

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python compression.py <video_path> <output_path> <compression_level>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    compression_level = float(sys.argv[3])
    
    compress_video(video_path, output_path, compression_level)
