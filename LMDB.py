import lmdb
import cv2
import os
import numpy as np

def save_images_to_lmdb(folder_path, lmdb_path):
    # Define o tamanho máximo do banco de dados
    map_size = 10 * 1024 * 1024  # 10 GB, ajuste conforme necessário
    
    # Cria o ambiente LMDB
    env = lmdb.open(lmdb_path, map_size=map_size)
    
    with env.begin(write=True) as txn:
        for filename in sorted(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, filename)
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                # Codifica a imagem para um formato binário
                img_encoded = cv2.imencode('.png', img)[1].tobytes()
                # Usa o nome do arquivo como chave
                txn.put(filename.encode('ascii'), img_encoded)
    print("Imagens salvas em LMDB:", lmdb_path)

save_images_to_lmdb("frames20x15grey1quarto", "frames20x15grey1quarto.lmdb")