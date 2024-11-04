import cv2
import os

number_of_picture = 0
def process_video(video_path, output_folder):
    global number_of_picture
    frame_num = 0
    cap = cv2.VideoCapture(video_path)
    cap.set(1, frame_num)  # Indeksiranje frejmova

    # Kreiranje izlaznog foldera ako ne postoji
    os.makedirs(output_folder, exist_ok=True)

    # Analiza videa frejm po frejm
    while True:
        frame_num += 1

        grabbed, frame = cap.read()

        if not grabbed:
            break

        # Ako je trenutni frejm svaki deseti frejm
        if frame_num % 10 == 0:
            filename = f"{output_folder}/crunch_{str(number_of_picture)}.png"

            cv2.imwrite(filename, frame)
            number_of_picture +=1

    cap.release()

if __name__ == '__main__':
    folder_path = "C:\\Users\\zoric\\Downloads\\crunch\\"
    for filename in os.listdir(folder_path):
        video_path = os.path.join(folder_path, filename)
        output_path = "C:\\Users\\zoric\\Downloads\\crunch images"
        process_video(video_path, output_path)
    print(number_of_picture)
