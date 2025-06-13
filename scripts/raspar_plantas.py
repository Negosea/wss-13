import requests
import os

# --- CONFIGURAÇÃO BASE ---
# OBS: Mude este valor para o início do padrão do seu storage S3, até o último hífen "-".
URL_BASE = "https://eu2.contabostorage.com/21ee0bc011104d38817cb2e2e95a3bbe:s3files/S_8940_O_2221_638096366993048374_C_1-"
# Início e fim dos tiles
TILE_INICIO = 1
TILE_FIM = 10  # ajuste para a quantidade de tiles que deseja baixar

# Pasta destino para salvar as imagens (garante a existência da pasta)
output_dir = "/home/sea/projetos/framework-construcao/dados/tiles_sequenciais"
os.makedirs(output_dir, exist_ok=True)

for i in range(TILE_INICIO, TILE_FIM + 1):
    url_tile = f"{URL_BASE}{i}.png"
    destino = os.path.join(output_dir, f"tile_{i}.png")
    print(f"Baixando tile {i}: {url_tile}")
    resp = requests.get(url_tile)
    if resp.status_code == 200:
        with open(destino, "wb") as arq:
            arq.write(resp.content)
        print(f"  ✅ Salvo '{destino}'")
    else:
        print(f"  ⚠️  Tile {i} não encontrado (status {resp.status_code}).")
        # Se não souber o total, pode colocar 'break' aqui para parar ao primeiro erro.
        # break

print("Download concluído.")