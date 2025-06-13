"""
Sistema completo de cálculo de quantitativos para Drywall
Inclui paredes, forros e estruturas metálicas
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import math

class TipoChapa(Enum):
    """Tipos de chapa de drywall"""
    STANDARD = "ST"  # Branca - uso geral
    RESISTENTE_UMIDADE = "RU"  # Verde - áreas úmidas
    RESISTENTE_FOGO = "RF"  # Rosa - resistente ao fogo
    
class EspessuraChapa(Enum):
    """Espessuras padrão de chapas (mm)"""
    E12_5 = 12.5
    E15_0 = 15.0
    
class TipoPerfil(Enum):
    """Tipos de perfis metálicos"""
    MONTANTE_48 = "M48"
    MONTANTE_70 = "M70"
    MONTANTE_90 = "M90"
    GUIA_48 = "G48"
    GUIA_70 = "G70"
    GUIA_90 = "G90"
    CANALETA_F530 = "F530"
    TABICA = "TABICA"

@dataclass
class DimensoesAmbiente:
    """Dimensões do ambiente"""
    comprimento: float  # metros
    largura: float      # metros
    altura: float       # metros
    
    @property
    def area_piso(self) -> float:
        return self.comprimento * self.largura
    
    @property
    def perimetro(self) -> float:
        return 2 * (self.comprimento + self.largura)

@dataclass
class Abertura:
    """Representa portas e janelas"""
    largura: float
    altura: float
    tipo: str = "porta"  # porta ou janela
    
    @property
    def area(self) -> float:
        return self.largura * self.altura

class CalculadorDrywall:
    """Calculador principal de quantitativos para drywall"""
    
    # Dimensões padrão das chapas (metros)
    CHAPA_LARGURA = 1.20
    CHAPA_ALTURA = 2.40  # Padrão, mas pode ter 2.60, 2.80, 3.00
    
    # Espaçamentos padrão (metros)
    ESPACAMENTO_MONTANTE = 0.60  # Pode ser 0.40 em casos especiais
    ESPACAMENTO_SUPORTE_FORRO = 0.60
    
    # Perdas e folgas
    PERDA_CHAPA = 0.10  # 10% de perda
    PERDA_PERFIL = 0.05  # 5% de perda
    FOLGA_PERIMETRO = 0.01  # 1cm de folga no perímetro
    
    def __init__(self, ambiente: DimensoesAmbiente):
        self.ambiente = ambiente
        self.aberturas: List[Abertura] = []
        
    def adicionar_abertura(self, abertura: Abertura):
        """Adiciona porta ou janela"""
        self.aberturas.append(abertura)
    
    def calcular_parede_simples(self, tipo_chapa: TipoChapa = TipoChapa.STANDARD,
                                espessura: EspessuraChapa = EspessuraChapa.E12_5,
                                altura_chapa: float = 2.40) -> Dict:
        """
        Calcula quantitativos para parede simples (1 chapa cada lado)
        """
        # Área total de paredes
        area_paredes = self.ambiente.perimetro * self.ambiente.altura
        
        # Descontar aberturas
        area_aberturas = sum(ab.area for ab in self.aberturas)
        area_liquida = area_paredes - area_aberturas
        
        # Cálculo de chapas
        area_chapa = self.CHAPA_LARGURA * altura_chapa
        num_chapas = math.ceil(area_liquida / area_chapa)
        num_chapas_com_perda = math.ceil(num_chapas * (1 + self.PERDA_CHAPA))
        
        # Como é parede simples, precisa dos dois lados
        total_chapas = num_chapas_com_perda * 2
        
        # Cálculo de montantes
        num_montantes_por_parede = math.ceil(self.ambiente.perimetro / self.ESPACAMENTO_MONTANTE) + 4  # extras nos cantos
        num_montantes_com_perda = math.ceil(num_montantes_por_parede * (1 + self.PERDA_PERFIL))
        
        # Cálculo de guias (superior e inferior)
        metros_guia = self.ambiente.perimetro * 2  # superior + inferior
        metros_guia_com_perda = metros_guia * (1 + self.PERDA_PERFIL)
        
        # Cálculo de parafusos
        parafusos_chapa_estrutura = total_chapas * 35  # média 35 por chapa
        parafusos_estrutura = num_montantes_por_parede * 8  # fixação guias
        
        # Cálculo de fita e massa
        metros_fita = area_liquida * 2.5  # 2.5m de fita por m² 
        kg_massa = area_liquida * 1.0  # 1kg por m²
        
        # Lã mineral (opcional)
        m2_la_mineral = area_liquida
        
        return {
            "resumo": {
                "area_total_paredes": round(area_paredes, 2),
                "area_aberturas": round(area_aberturas, 2),
                "area_liquida": round(area_liquida, 2),
                "perimetro": round(self.ambiente.perimetro, 2)
            },
            "chapas": {
                "tipo": tipo_chapa.value,
                "espessura_mm": espessura.value,
                "quantidade": total_chapas,
                "area_total_m2": round(total_chapas * area_chapa, 2)
            },
            "estrutura_metalica": {
                "montantes": {
                    "tipo": "M70",  # padrão para paredes
                    "quantidade_pecas": num_montantes_com_perda,
                    "metros_lineares": round(num_montantes_com_perda * self.ambiente.altura, 2)
                },
                "guias": {
                    "tipo": "G70",  # padrão para paredes
                    "metros_lineares": round(metros_guia_com_perda, 2),
                    "quantidade_barras_3m": math.ceil(metros_guia_com_perda / 3)
                }
            },
            "fixacao": {
                "parafusos_chapa_estrutura": parafusos_chapa_estrutura,
                "parafusos_estrutura": parafusos_estrutura,
                "parafusos_total": parafusos_chapa_estrutura + parafusos_estrutura
            },
            "acabamento": {
                "fita_metros": round(metros_fita, 2),
                "massa_corrida_kg": round(kg_massa, 2),
                "massa_rapida_kg": round(kg_massa * 0.3, 2)  # para primeira demão
            },
            "isolamento": {
                "la_mineral_m2": round(m2_la_mineral, 2),
                "la_mineral_rolos": math.ceil(m2_la_mineral / 12.5)  # rolos de 12.5m²
            }
        }
    
    def calcular_parede_dupla(self, tipo_chapa: TipoChapa = TipoChapa.STANDARD,
                             espessura: EspessuraChapa = EspessuraChapa.E12_5) -> Dict:
        """
        Calcula quantitativos para parede dupla (2 chapas cada lado)
        Usado para isolamento acústico ou resistência ao fogo
        """
        # Primeiro calcula como parede simples
        resultado = self.calcular_parede_simples(tipo_chapa, espessura)
        
        # Dobra a quantidade de chapas
        resultado["chapas"]["quantidade"] *= 2
        resultado["chapas"]["area_total_m2"] *= 2
        
        # Aumenta parafusos (mais fixações)
        resultado["fixacao"]["parafusos_chapa_estrutura"] *= 1.5
        
        # Aumenta acabamento (mais juntas)
        resultado["acabamento"]["fita_metros"] *= 1.3
        resultado["acabamento"]["massa_corrida_kg"] *= 1.3
        
        resultado["tipo_parede"] = "DUPLA - Maior isolamento acústico"
        
        return resultado
    
    def calcular_forro(self, tipo_chapa: TipoChapa = TipoChapa.STANDARD,
                      estrutura_metalica: bool = True) -> Dict:
        """
        Calcula quantitativos para forro de drywall
        """
        area_forro = self.ambiente.area_piso
        
        # Cálculo de chapas
        area_chapa = self.CHAPA_LARGURA * self.CHAPA_ALTURA
        num_chapas = math.ceil(area_forro / area_chapa)
        num_chapas_com_perda = math.ceil(num_chapas * (1 + self.PERDA_CHAPA))
        
        if estrutura_metalica:
            # Estrutura com perfis F530
            # Perfis principais (sentido maior)
            num_perfis_principais = math.ceil(self.ambiente.largura / self.ESPACAMENTO_SUPORTE_FORRO)
            metros_perfis_principais = num_perfis_principais * self.ambiente.comprimento
            
            # Perfis secundários (travessas)
            num_travessas = math.ceil(self.ambiente.comprimento / self.ESPACAMENTO_SUPORTE_FORRO)
            metros_travessas = num_travessas * self.ambiente.largura
            
            # Cantoneiras de borda
            metros_cantoneira = self.ambiente.perimetro
            
            # Tirantes e suportes
            num_tirantes = math.ceil(area_forro / 1.44)  # 1 a cada 1.2m x 1.2m
            
            estrutura = {
                "perfis_principais_F530": {
                    "metros_lineares": round(metros_perfis_principais * 1.05, 2),
                    "quantidade_barras_3m": math.ceil(metros_perfis_principais * 1.05 / 3)
                },
                "travessas_F530": {
                    "metros_lineares": round(metros_travessas * 1.05, 2),
                    "quantidade_barras_3m": math.ceil(metros_travessas * 1.05 / 3)
                },
                "cantoneira_perimetral": {
                    "metros_lineares": round(metros_cantoneira * 1.05, 2),
                    "quantidade_barras_3m": math.ceil(metros_cantoneira * 1.05 / 3)
                },
                "tirantes": num_tirantes,
                "suportes_niveladores": num_tirantes
            }
        else:
            estrutura = {"tipo": "Estrutura de madeira - calcular separadamente"}
        
        # Parafusos e acabamento
        parafusos = num_chapas_com_perda * 30  # 30 por chapa no forro
        metros_fita = area_forro * 2.0  # 2m de fita por m²
        kg_massa = area_forro * 0.8  # 0.8kg por m² no forro
        
        return {
            "resumo": {
                "area_forro": round(area_forro, 2),
                "perimetro": round(self.ambiente.perimetro, 2)
            },
            "chapas": {
                "tipo": tipo_chapa.value,
                "quantidade": num_chapas_com_perda,
                "area_total_m2": round(num_chapas_com_perda * area_chapa, 2)
            },
            "estrutura_metalica": estrutura,
            "fixacao": {
                "parafusos_chapa_estrutura": parafusos,
                "buchas_tirantes": num_tirantes if estrutura_metalica else 0
            },
            "acabamento": {
                "fita_metros": round(metros_fita, 2),
                "massa_corrida_kg": round(kg_massa, 2)
            }
        }
    
    def calcular_divisoria(self, comprimento: float, altura: float,
                          tipo_chapa: TipoChapa = TipoChapa.STANDARD) -> Dict:
        """
        Calcula quantitativos para uma divisória específica
        """
        area_divisoria = comprimento * altura
        
        # Cálculo de chapas (dois lados)
        area_chapa = self.CHAPA_LARGURA * self.CHAPA_ALTURA
        num_chapas = math.ceil(area_divisoria / area_chapa) * 2
        num_chapas_com_perda = math.ceil(num_chapas * (1 + self.PERDA_CHAPA))
        
        # Montantes
        num_montantes = math.ceil(comprimento / self.ESPACAMENTO_MONTANTE) + 2
        
        # Guias
        metros_guia = comprimento * 2  # superior e inferior
        
        return {
            "dimensoes": {
                "comprimento": comprimento,
                "altura": altura,
                "area_total": round(area_divisoria * 2, 2)  # dois lados
            },
            "chapas": {
                "tipo": tipo_chapa.value,
                "quantidade": num_chapas_com_perda
            },
            "estrutura": {
                "montantes_M70": num_montantes,
                "guias_G70_metros": round(metros_guia * 1.05, 2)
            }
        }
    
    def gerar_relatorio_completo(self, incluir_parede: bool = True,
                                incluir_forro: bool = True,
                                tipo_parede: str = "simples") -> Dict:
        """
        Gera relatório completo com todos os quantitativos
        """
        relatorio = {
            "dados_ambiente": {
                "comprimento": self.ambiente.comprimento,
                "largura": self.ambiente.largura,
                "altura": self.ambiente.altura,
                "area_piso": round(self.ambiente.area_piso, 2),
                "perimetro": round(self.ambiente.perimetro, 2),
                "aberturas": len(self.aberturas)
            }
        }
        
        if incluir_parede:
            if tipo_parede == "simples":
                relatorio["parede_simples"] = self.calcular_parede_simples()
            else:
                relatorio["parede_dupla"] = self.calcular_parede_dupla()
        
        if incluir_forro:
            relatorio["forro"] = self.calcular_forro()
        
        # Resumo de materiais
        self._adicionar_resumo_materiais(relatorio)
        
        return relatorio
    
    def _adicionar_resumo_materiais(self, relatorio: Dict):
        """Adiciona resumo consolidado de materiais"""
        resumo = {
            "chapas_total": 0,
            "montantes_total": 0,
            "guias_metros_total": 0,
            "parafusos_total": 0,
            "fita_metros_total": 0,
            "massa_kg_total": 0
        }
        
        # Soma paredes
        if "parede_simples" in relatorio:
            dados = relatorio["parede_simples"]
            resumo["chapas_total"] += dados["chapas"]["quantidade"]
            resumo["montantes_total"] += dados["estrutura_metalica"]["montantes"]["quantidade_pecas"]
            resumo["guias_metros_total"] += dados["estrutura_metalica"]["guias"]["metros_lineares"]
            resumo["parafusos_total"] += dados["fixacao"]["parafusos_total"]
            resumo["fita_metros_total"] += dados["acabamento"]["fita_metros"]
            resumo["massa_kg_total"] += dados["acabamento"]["massa_corrida_kg"]
        
        # Soma forro
        if "forro" in relatorio:
            dados = relatorio["forro"]
            resumo["chapas_total"] += dados["chapas"]["quantidade"]
            resumo["parafusos_total"] += dados["fixacao"]["parafusos_chapa_estrutura"]
            resumo["fita_metros_total"] += dados["acabamento"]["fita_metros"]
            resumo["massa_kg_total"] += dados["acabamento"]["massa_corrida_kg"]
        
        relatorio["resumo_materiais"] = resumo
        
        # Adiciona lista de compras formatada
        relatorio["lista_compras"] = self._formatar_lista_compras(resumo)
    
    def _formatar_lista_compras(self, resumo: Dict) -> List[str]:
        """Formata lista de compras organizada"""
        lista = []
        
        # Chapas (vendidas por unidade)
        lista.append(f"Chapas de Drywall Standard 1.20x2.40m: {resumo['chapas_total']} unidades")
        
        # Perfis (vendidos em barras de 3m)
        lista.append(f"Montantes M70: {resumo['montantes_total']} peças")
        lista.append(f"Guias G70: {math.ceil(resumo['guias_metros_total'] / 3)} barras de 3m")
        
        # Parafusos (caixas de 1000)
        caixas_parafusos = math.ceil(resumo['parafusos_total'] / 1000)
        lista.append(f"Parafusos para drywall: {caixas_parafusos} caixas (1000 un cada)")
        
        # Fita (rolos de 50m)
        rolos_fita = math.ceil(resumo['fita_metros_total'] / 50)
        lista.append(f"Fita para juntas: {rolos_fita} rolos de 50m")
        
        # Massa (sacos de 20kg)
        sacos_massa = math.ceil(resumo['massa_kg_total'] / 20)
        lista.append(f"Massa para drywall: {sacos_massa} sacos de 20kg")
        
        return lista
