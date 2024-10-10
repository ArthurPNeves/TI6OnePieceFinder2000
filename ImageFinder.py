import cv2
import os
import time
import numpy as np
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ThreadPoolExecutor
import h5py
from multiprocessing import Pool
import lmdb

class ImageFinder:
    def __init__(self):
        pass

    @staticmethod
    def compare_imagesImgPaths(user_image, image_paths):
        ssim_scores = []
        
        user_gray = cv2.cvtColor(user_image, cv2.COLOR_BGR2GRAY)


        # Converte a imagem do usuário para escala de cinza

        #height, width = user_gray.shape[:2]
        #mid_point = height // 2

        #top_half = user_gray[:mid_point, :]

        #mid_point = width // 2
        #top_half = top_half[:, :mid_point]

        # Início do temporizador
        print("Comparando imagens...")
        start_time = time.time()

        # Processamento paralelo das imagens
        with ThreadPoolExecutor() as executor:
            futures = []
            for image_path in image_paths:
                print(image_path)
                futures.append(executor.submit(ImageFinder.calculate_ssim, image_path, user_gray))

            for future in futures:
                score, filename = future.result()
                ssim_scores.append((score, filename))

        # Fim do temporizador
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Tempo total de comparação: {total_time:.2f} segundos")

        # Ordenação das imagens por pontuação SSIM
        print("Ordenando imagens...")
        start_time1 = time.time()

        ssim_scores.sort(reverse=True, key=lambda x: x[0])
        end_time1 = time.time()
        total_time1 = end_time1 - start_time1
        print(f"Tempo total de ordenação: {total_time1:.2f} segundos")

        # Retorna as 100 imagens mais semelhantes
        top_matches = ssim_scores[:3]
        return top_matches

    @staticmethod
    def upScaleTop100Images(upScalePath, top100):
        upscale_images = []

        for score, filename in top100:
            # Extrai o número do nome do arquivo (ex: "frame_0001.jpg" -> "0001")
            # frame_number = filename.split('_')[1].split('.')[0]  # Extrai "0001" de "frame_0001.jpg"

            # Constrói o nome do arquivo correspondente no upScalePath
            # frame_name = f"frames_{frame_number}.jpg"
            frame_path = os.path.join(upScalePath, filename)

            # Verifica se o arquivo existe
            if os.path.exists(frame_path):
                upscale_images.append(frame_path)
            else:
                print(f"Arquivo não encontrado: {frame_path}")

        return upscale_images
    

    
    def load_images_from_lmdb(self, lmdb_path):
        images = []
        env = lmdb.open(lmdb_path, readonly=True)

        with env.begin() as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                # Decodifica a imagem
                img = cv2.imdecode(np.frombuffer(value, np.uint8), cv2.IMREAD_GRAYSCALE)
                filename = key.decode('ascii')
                images.append((img, filename))

        return images



    @staticmethod
    def resize_image_to_match(image, target_size):
        h, w = image.shape[:2]
        target_h, target_w = target_size
        scale = min(target_w / w, target_h / h)
        resized_image = cv2.resize(image, (int(w * scale), int(h * scale)))

        delta_w = target_w - resized_image.shape[1]
        delta_h = target_h - resized_image.shape[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        color = [0, 0, 0]
        new_image = cv2.copyMakeBorder(resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

        return new_image

    @staticmethod
    def calculate_ssim(file_path, user_gray):
        folder_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        return ssim(user_gray, folder_image, full=False), os.path.basename(file_path)
    
    @staticmethod
    def pixelPorPixel(folder_image, user_gray):
        # Calculates pixel-wise difference
        diff = (folder_image[0] - user_gray) ** 2
        error = np.mean(diff)
        return error, folder_image[1]
    
    @staticmethod
    def load_images_parallel(folder_path):
        images = []
    
        def load_image(filename):
            file_path = os.path.join(folder_path, filename)
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            return (img, filename)
    
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(load_image, filename) for filename in sorted(os.listdir(folder_path))]
    
            for future in futures:
                image = future.result()
                if image[0] is not None:
                    images.append(image)
    
        return images
    

    def compare_images(self, user_image, folder_path):
        ssim_scores = []
        user_gray = cv2.cvtColor(user_image, cv2.COLOR_BGR2GRAY)

        # Loading images from folder
        print("Loading images...")
        start_time = time.time()
        images = self.load_images_from_lmdb(folder_path)
        end_time = time.time()
        print(f"Total loading time: {end_time - start_time:.2f} seconds")
        start_time1 = time.time()
        # Comparing images using ThreadPoolExecutor
        print("Comparing images...")
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.pixelPorPixel, img, user_gray) for img in images]


            for future in futures:
                score, filename = future.result()
                ssim_scores.append((score, filename))
        
        end_time = time.time()
        print(f"Total comparison time: {end_time - start_time:.2f} seconds")
        print("Sorting images...")
        start_time1 = time.time()

        ssim_scores.sort(reverse=False, key=lambda x: x[0])
        end_time1 = time.time()
        total_time1 = end_time1 - start_time1
        print(f"Total sorting time: {total_time1:.2f} seconds")

        top_matches = ssim_scores[:100]
        return top_matches
