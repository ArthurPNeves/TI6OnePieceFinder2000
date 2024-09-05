import cv2
import os
import numpy as np
import time
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ThreadPoolExecutor
import os
import shutil

import os

def compare_imagesImgPaths(user_image, image_paths):
    ssim_scores = []
    
    # Converte a imagem do usuário para escala de cinza
    #user_gray = cv2.cvtColor(user_image, cv2.COLOR_BGR2GRAY)
    
    #height, width = user_gray.shape[:2]
    #id_point = height // 2
    

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
            #print(user_image)
            #print(image_path)
            print(image_path)
            futures.append(executor.submit(calculate_ssim, image_path, user_image))

        for future in futures:
            score, image_path = future.result()
            ssim_scores.append((score, image_path))

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

def upScaleTop100Images(upScalePath, top100):
    upscale_images = []
    
    for score, filename in top100:
        # Extrai o número do nome do arquivo (ex: "frame_0001.jpg" -> "0001")
        #frame_number = filename.split('_')[1].split('.')[0]  # Extrai "0001" de "frame_0001.jpg"
        
        # Constrói o nome do arquivo correspondente no upScalePath
        #frame_name = f"frames_{frame_number}.jpg"
        frame_path = os.path.join(upScalePath, filename)
        
        # Verifica se o arquivo existe
        if os.path.exists(frame_path):
            upscale_images.append(frame_path)
        else:
            print(f"Arquivo não encontrado: {frame_path}")
    
    return upscale_images

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

def calculate_ssim(file_path, user_gray):
    # Esta Demorando esse gray sacale ?
    folder_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    return ssim(user_gray, folder_image, full=False), os.path.basename(file_path)

def compare_images(user_image, folder_path):
    ssim_scores = []
    # Precompute the grayscale user image
    user_gray = cv2.cvtColor(user_image, cv2.COLOR_BGR2GRAY)
    
    height, width = user_gray.shape[:2]
    mid_point = height // 2
    

    top_half = user_gray[:mid_point, :]

    mid_point = width // 2
    top_half = top_half[:, :mid_point]
    
    # Start timing
    print("Comparando imagens...")
    start_time = time.time()

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            futures.append(executor.submit(calculate_ssim, file_path, top_half))

        for future in futures:
            score, filename = future.result()
            ssim_scores.append((score, filename))

    # Timing end
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tempo total de comparação: {total_time:.2f} segundos")

    # Ordena as imagens pelas maiores pontuações de SSIM
    print("Ordenando imagens...")
    start_time1 = time.time()
    
    ssim_scores.sort(reverse=True, key=lambda x: x[0])
    end_time1 = time.time()
    total_time1 = end_time1 - start_time1
    print(f"Tempo total de ordenação: {total_time1:.2f} segundos")
    # Retorna os nomes das 3 imagens mais semelhantes
    top_matches = ssim_scores[:100]
    return top_matches

# Caminho para a imagem do usuário
user_image_path = './DesiredFrame/nami40x30.jpg'

user_imagePathOrigim = 'nami40x30.jpg'
# Caminho para a pasta com imagens
folder_path = 'frames20x15grey1quarto'

# Carrega a imagem do usuário
user_image = cv2.imread(user_image_path)

user_imageOrigin = cv2.imread(user_imagePathOrigim)


# Compara a imagem do usuário com as imagens na pasta
top_matches = compare_images(user_image, folder_path)

start_time1 = time.time()

ImagensUpscale = upScaleTop100Images('frames40x30', top_matches)
end_time1 = time.time()
total_time1 = end_time1 - start_time1
print(f"Tempo total de Upscale: {total_time1:.2f} segundos")

top3 = compare_imagesImgPaths(user_imageOrigin, ImagensUpscale)

# Imprime os nomes das 3 imagens mais semelhantes
print("As 3 imagens mais semelhantes são:")
for score, filename in top3:
    print(f"{filename} com SSIM: {score:.4f}")
