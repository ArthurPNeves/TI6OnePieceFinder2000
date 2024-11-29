from concurrent.futures import ThreadPoolExecutor
import cv2
import os

class ImageDownsizer:
    def __init__(self, scale_factor=0.0625, num_threads = 4):
        self.scale_factor = scale_factor
        self.num_threads = num_threads

    def downscale_image(self, image):
        height, width = image.shape[:2]
        new_dimensions = (int(width * self.scale_factor), int(height * self.scale_factor))
        return cv2.resize(image, new_dimensions, interpolation=cv2.INTER_AREA)

    def downscale_folder_images(self, input_folder, output_folder):
        image_tasks = []

        for root, dirs, files in os.walk(input_folder):
            relative_path = os.path.relpath(root, input_folder)
            current_output_folder = os.path.join(output_folder, relative_path)

            if not os.path.exists(current_output_folder):
                os.makedirs(current_output_folder)

            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    input_path = os.path.join(root, filename)
                    output_path = os.path.join(current_output_folder, filename)
                    image_tasks.append((input_path, output_path))

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            executor.map(self.process_image_task, image_tasks)
        
    def process_image_task(self, task):
        input_path, output_path = task
        image = cv2.imread(input_path)
        if image is not None:
            downscaled_image = self.downscale_image(image)
            cv2.imwrite(output_path, downscaled_image)

    

# Uso do código
root_folder = r"C:\Users\arthu\OneDrive\Documentos\puc6periodo\TI6\TI6OnePieceFinder2000\EpFrames"
output_path = r"C:\Users\arthu\OneDrive\Documentos\puc6periodo\TI6\EpFrames40x30"

downsizer = ImageDownsizer(scale_factor=0.0625)
downsizer.downscale_folder_images(root_folder, output_path)