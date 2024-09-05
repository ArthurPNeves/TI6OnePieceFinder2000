import cv2
import os

class ImageDownsizer:
    def __init__(self, scale_factor=0.5):
        self.scale_factor = scale_factor

    def downscale_image(self, image):
        """
        Reduz a escala da imagem pelo fator de escala fornecido.
        """
        height, width = image.shape[:2]
        new_dimensions = (int(width * self.scale_factor), int(height * self.scale_factor))
        return cv2.resize(image, new_dimensions, interpolation=cv2.INTER_AREA)

    def downscale_folder_images(self, input_folder, output_folder):
        """
        Reduz a escala de todas as imagens na pasta de entrada e as salva na pasta de saída.
        """
        # Cria a pasta de saída, se não existir
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Percorre todas as imagens na pasta de entrada
        for filename in os.listdir(input_folder):
            input_path = os.path.join(input_folder, filename)

            # Verifica se é um arquivo de imagem
            if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                # Carrega a imagem
                image = cv2.imread(input_path)

                # Reduz a escala da imagem
                downscaled_image = self.downscale_image(image)

                # Define o caminho de saída
                output_path = os.path.join(output_folder, filename)

                # Salva a imagem redimensionada na pasta de saída
                cv2.imwrite(output_path, downscaled_image)