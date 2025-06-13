#!/usr/bin/env python3
import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Ambiente:
    nome: str
    area: Optional[float] = None
    dimensoes: Optional[Tuple[float, float]] = None

class ParserPlantaArquitetonica:
    """Parser especializado para plantas arquitetônicas"""
    def __init__(self, texto_ocr: str):
        self.texto = texto_ocr.upper()
        self.ambientes = []
        self.medidas = []

    def extrair_ambientes(self) -> List[Ambiente]:
        padroes_ambiente = {
            'QUARTO': [r'QUARTO\s*(\d+)?', r'DORMIT[ÓO]RIO\s*(\d+)?', r'SU[ÍI]TE'],
            'SALA': [r'SALA\s*(DE\s*)?(ESTAR|JANTAR|TV)?', r'LIVING'],
            'COZINHA': [r'COZINHA', r'COPA'],
            'BANHEIRO': [r'BANHEIRO', r'WC', r'LAVABO', r'BWC'],
            'VARANDA': [r'VARANDA', r'SACADA', r'TERRAÇO'],
            'ÁREA_SERVIÇO': [r'[ÁA]REA\s*(DE\s*)?SERVI[ÇC]O', r'LAVANDERIA'],
            'GARAGEM': [r'GARAGEM', r'VAGA', r'ESTACIONAMENTO']
        }
        for tipo, padroes in padroes_ambiente.items():
            for padrao in padroes:
                matches = re.finditer(padrao, self.texto)
                for match in matches:
                    area = self._buscar_area_proxima(match.start())
                    dimensoes = self._buscar_dimensoes_proximas(match.start())
                    ambiente = Ambiente(
                        nome=match.group(0),
                        area=area,
                        dimensoes=dimensoes
                    )
                    self.ambientes.append(ambiente)
        return self.ambientes

    def _buscar_area_proxima(self, posicao: int, janela: int = 100) -> Optional[float]:
        inicio = max(0, posicao - janela)
        fim = min(len(self.texto), posicao + janela)
        trecho = self.texto[inicio:fim]
        padroes_area = [
            r'(\d+[,.]?\d*)\s*M[²2]',
            r'(\d+[,.]?\d*)\s*METROS?\s*QUADRADOS?'
        ]
        for padrao in padroes_area:
            match = re.search(padrao, trecho)
            if match:
                valor = match.group(1).replace(',', '.')
                return float(valor)
        return None

    def _buscar_dimensoes_proximas(self, posicao: int, janela: int = 100) -> Optional[Tuple[float, float]]:
        inicio = max(0, posicao - janela)
        fim = min(len(self.texto), posicao + janela)
        trecho = self.texto[inicio:fim]
        padrao_dimensao = r'(\d+[,.]?\d*)\s*[Xx]\s*(\d+[,.]?\d*)'
        match = re.search(padrao_dimensao, trecho)
        if match:
            l = float(match.group(1).replace(',', '.'))
            c = float(match.group(2).replace(',', '.'))
            if l > 100 or c > 100:
                l = l / 100
                c = c / 100
            return (l, c)
        return None

    def extrair_medidas_gerais(self) -> List[float]:
        padroes = [
            r'(\d+[,.]?\d*)\s*M(?:ETROS?)?',
            r'(\d+[,.]?\d*)\s*CM',
            r'(\d+[,.]?\d*)\s*MM'
        ]
        medidas = []
        for padrao in padroes:
            matches = re.findall(padrao, self.texto)
            for match in matches:
                valor = float(match.replace(',', '.'))
                medidas.append(valor)
        return sorted(set(medidas))

    def gerar_relatorio(self) -> Dict:
        ambientes = self.extrair_ambientes()
        medidas = self.extrair_medidas_gerais()
        total_area = sum(a.area for a in ambientes if a.area)
        num_quartos = len([a for a in ambientes if 'QUARTO' in a.nome])
        num_banheiros = len([a for a in ambientes if any(b in a.nome for b in ['BANHEIRO', 'WC', 'LAVABO'])])
        return {
            'resumo': {
                'total_ambientes': len(ambientes),
                'area_total_identificada': round(total_area, 2) if total_area > 0 else None,
                'num_quartos': num_quartos,
                'num_banheiros': num_banheiros
            },
            'ambientes': [asdict(a) for a in ambientes],
            'medidas_encontradas': medidas[:20], 
            'estatisticas': {
                'total_medidas': len(medidas),
                'menor_medida': min(medidas) if medidas else None,
                'maior_medida': max(medidas) if medidas else None
            }
        }

if __name__ == "__main__":
    arquivo_ocr = "dados/pipeline_output/planta_principal_ocr.txt"
    try:
        with open(arquivo_ocr, 'r', encoding='utf-8') as f:
            texto = f.read()
        parser = ParserPlantaArquitetonica(texto)
        relatorio = parser.gerar_relatorio()
        with open('dados/pipeline_output/analise_planta.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
        print("📊 Análise da Planta:")
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {arquivo_ocr}")
