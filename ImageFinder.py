import cv2
import os
import time
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ThreadPoolExecutor

class ImageFinder:
    def __init__(self):
        pass

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

    def compare_images(self, user_image, folder_path):
        ssim_scores = []
        user_gray = cv2.cvtColor(user_image, cv2.COLOR_BGR2GRAY)

        height, width = user_gray.shape[:2]
        mid_point = height // 2
        top_half = user_gray[:mid_point, :]

        print("Comparing images...")
        start_time = time.time()

        with ThreadPoolExecutor() as executor:
            futures = []
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                futures.append(executor.submit(self.calculate_ssim, file_path, top_half))

            for future in futures:
                score, filename = future.result()
                ssim_scores.append((score, filename))

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total comparison time: {total_time:.2f} seconds")

        print("Sorting images...")
        start_time1 = time.time()

        ssim_scores.sort(reverse=True, key=lambda x: x[0])
        end_time1 = time.time()
        total_time1 = end_time1 - start_time1
        print(f"Total sorting time: {total_time1:.2f} seconds")

        top_matches = ssim_scores[:3]
        return top_matches
