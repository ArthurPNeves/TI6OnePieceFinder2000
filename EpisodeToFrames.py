import cv2
import os
import time

class VideoToFrames:
    def __init__(self, video_path, frames_dir):
        self.video_path = video_path
        self.frames_dir = frames_dir

    def extract_frames(self):
        # Cria uma pasta para salvar os frames
        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)

        # Captura o vídeo
        video = cv2.VideoCapture(self.video_path)

        # Variável para contar os frames
        frame_count = 0

        # Inicia o cronômetro
        start_time = time.time()

        while True:
            # Lê o frame
            ret, frame = video.read()

            # Se não conseguir ler o frame, sai do loop
            if not ret:
                break

            # Salva o frame como uma imagem
            frame_path = os.path.join(self.frames_dir, f'frame_{frame_count:04d}.jpg')
            cv2.imwrite(frame_path, frame)

            # Incrementa o contador de frames
            frame_count += 1

        # Libera o vídeo
        video.release()

        # Calcula o tempo total e os frames por segundo
        end_time = time.time()
        total_time = end_time - start_time
        fps = frame_count / total_time

        print(f'Extração concluída. {frame_count} frames salvos em {self.frames_dir}.')
        print(f'Tempo total: {total_time:.2f} segundos')
        print(f'FPS de processamento: {fps:.2f} frames por segundo')