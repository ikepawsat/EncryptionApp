import random
from sympy import isprime
import cv2


def generate_large_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1

        if isprime(candidate):
            return candidate


def download_key(prime_number, filename="key.txt"):
    with open(filename, "w") as file:
        file.write(str(prime_number))


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    pixel_array = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flattened_array = gray_frame.flatten()
        pixel_array.extend(flattened_array)

    cap.release()
    cv2.destroyAllWindows()
    return pixel_array


if __name__ == "__main__":
    bits = 1024
    prime_number = generate_large_prime(bits)
    print(f"A {bits}-bit prime number: {prime_number}")

    download_key(prime_number)

    video_path = 'path_to_your_video.mp4'
    pixels = process_video(video_path)

    if pixels:
        print(f"Total pixels in the video: {len(pixels)}")
