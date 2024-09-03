import cv2
import os
import numpy as np
import time
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ThreadPoolExecutor

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
    top_matches = ssim_scores[:3]
    return top_matches

# Caminho para a imagem do usuário
user_image_path = 'nami40x30.jpg'

# Caminho para a pasta com imagens
folder_path = 'frames1Dowscale40x30Metade'

# Carrega a imagem do usuário
user_image = cv2.imread(user_image_path)

# Compara a imagem do usuário com as imagens na pasta
top_matches = compare_images(user_image, folder_path)

# Imprime os nomes das 3 imagens mais semelhantes
print("As 3 imagens mais semelhantes são:")
for score, filename in top_matches:
    print(f"{filename} com SSIM: {score:.4f}")
