import cv2
import os

def downscale_image(image, scale_factor):
    """
    Reduz a escala da imagem pelo fator de escala fornecido.
    """
    height, width = image.shape[:2]
    new_dimensions = (int(width * scale_factor), int(height * scale_factor))
    return cv2.resize(image, new_dimensions, interpolation=cv2.INTER_AREA)

def downscale_folder_images(input_folder, output_folder, scale_factor=0.5):
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
            downscaled_image = downscale_image(image, scale_factor)

            # Define o caminho de saída
            output_path = os.path.join(output_folder, filename)

            # Salva a imagem redimensionada na pasta de saída
            cv2.imwrite(output_path, downscaled_image)

            #print(f"Imagem {filename} redimensionada e salva em {output_path}")

# Caminho para a pasta de entrada com imagens originais
input_folder = 'frames40x30Grey'

# Caminho para a pasta de saída onde as imagens redimensionadas serão salvas
output_folder = 'frames40x30Grey'

# Fator de escala para redimensionar as imagens (ex: 0.5 = 50% do tamanho original)
scale_factor = 0.0625

# Executa o redimensionamento das imagens na pasta
downscale_folder_images(input_folder, output_folder, scale_factor)
