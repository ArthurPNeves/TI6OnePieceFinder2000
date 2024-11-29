import cv2
import os

class ImageSplitter:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def split_image_horizontally(self, image):
        """
        Divide uma imagem em duas metades horizontais (superior e inferior).

        Args:
            image (numpy.ndarray): A imagem a ser dividida.

        Returns:
            tuple: Duas metades da imagem (superior, inferior).
        """
        height, width = image.shape[:2]
        mid_point = height // 2

        top_half = image[:mid_point, :]
        bottom_half = image[mid_point:, :]

        return top_half, bottom_half

    def split_folder_images(self):
        """
        Percorre a pasta de entrada e subpastas, divide as imagens e salva na pasta de saída 
        mantendo a estrutura de diretórios.
        """
        for root, _, files in os.walk(self.input_folder):
            # Define o caminho relativo da pasta atual
            relative_path = os.path.relpath(root, self.input_folder)
            current_output_folder = os.path.join(self.output_folder, relative_path)

            # Cria a pasta correspondente na saída, se necessário
            if not os.path.exists(current_output_folder):
                os.makedirs(current_output_folder)

            for filename in files:
                # Verifica se é um arquivo de imagem
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    input_path = os.path.join(root, filename)

                    # Carrega a imagem
                    image = cv2.imread(input_path)
                    if image is None:
                        print(f"Erro ao carregar a imagem: {filename}. Pulando...")
                        continue

                    # Divide a imagem em duas metades
                    top_half, bottom_half = self.split_image_horizontally(image)

                    # Define os nomes dos arquivos de saída
                    name, ext = os.path.splitext(filename)
                    top_filename = f"{name}_top{ext}"
                    bottom_filename = f"{name}_bottom{ext}"

                    # Define os caminhos de saída
                    top_output_path = os.path.join(current_output_folder, top_filename)
                    bottom_output_path = os.path.join(current_output_folder, bottom_filename)

                    # Salva as imagens divididas
                    cv2.imwrite(top_output_path, top_half)
                    cv2.imwrite(bottom_output_path, bottom_half)

                    print(f"Imagem '{filename}' dividida em '{top_filename}' e '{bottom_filename}'.")

# Uso do código

if __name__ == "__main__":
    root_folder = r"C:\Users\arthu\OneDrive\Documentos\puc6periodo\TI6\TI6OnePieceFinder2000\EpFrames20x15"
    output_path = r"C:\Users\arthu\OneDrive\Documentos\puc6periodo\TI6\EpFrames20x15_Split"

    splitter = ImageSplitter(root_folder, output_path)
    splitter.split_folder_images()

