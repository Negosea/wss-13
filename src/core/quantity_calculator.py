"""
Calculadora de quantitativos para construção civil.

Fornece métodos para calcular volumes de concreto, áreas de parede,
quantidade de blocos e volume de argamassa.
"""
from typing import Dict, List, Optional

class QuantityCalculator:
    """Classe utilitária para cálculos de quantitativos de materiais."""

    @staticmethod
    def concrete_volume(length: float, width: float, height: float) -> float:
        """
        Calcula o volume de concreto (m³).
        Args:
            length (float): Comprimento em metros.
            width (float): Largura em metros.
            height (float): Altura em metros.
        Returns:
            float: Volume em metros cúbicos.
        """
        if min(length, width, height) <= 0:
            raise ValueError("Todas as dimensões devem ser positivas.")
        return length * width * height

    @staticmethod
    def wall_area(length: float, height: float, 
                  openings: Optional[List[Dict[str, float]]] = None) -> float:
        """
        Calcula a área de parede descontando aberturas.
        Args:
            length (float): Comprimento da parede (m).
            height (float): Altura da parede (m).
            openings (list): Lista de dicionários com 'width' e 'height' das aberturas (m).
        Returns:
            float: Área líquida da parede (m²).
        """
        if min(length, height) <= 0:
            raise ValueError("Comprimento e altura devem ser positivos.")
        gross_area = length * height
        opening_area = 0.0
        if openings:
            for op in openings:
                w = op.get('width', 0)
                h = op.get('height', 0)
                if w > 0 and h > 0:
                    opening_area += w * h
        net_area = gross_area - opening_area
        return max(net_area, 0.0)

    @staticmethod
    def blocks_quantity(wall_area: float, block_width: float, 
                       block_height: float, mortar_joint: float = 0.01,
                       waste_factor: float = 1.05) -> Dict:
        """
        Calcula quantidade de blocos necessários para uma parede.
        Args:
            wall_area (float): Área da parede (m²).
            block_width (float): Largura do bloco (m).
            block_height (float): Altura do bloco (m).
            mortar_joint (float): Espessura da junta de argamassa (m).
            waste_factor (float): Fator de perda (default 5%).
        Returns:
            dict: Quantidade total, blocos por m² e fator de perda.
        """
        if min(wall_area, block_width, block_height, mortar_joint) <= 0:
            raise ValueError("Todos os parâmetros devem ser positivos.")
        # Dimensões efetivas do bloco com junta
        effective_width = block_width + mortar_joint
        effective_height = block_height + mortar_joint
        # Blocos por m²
        blocks_per_m2 = 1 / (effective_width * effective_height)
        total_blocks = int(wall_area * blocks_per_m2 * waste_factor)
        return {
            'blocks': total_blocks,
            'blocks_per_m2': round(blocks_per_m2, 2),
            'waste_factor': waste_factor
        }

    @staticmethod
    def mortar_volume(wall_area: float, block_thickness: float,
                     mortar_joint: float = 0.01) -> float:
        """
        Calcula volume aproximado de argamassa (m³).
        Args:
            wall_area (float): Área da parede (m²).
            block_thickness (float): Espessura do bloco (m).
            mortar_joint (float): Espessura da junta (m).
        Returns:
            float: Volume de argamassa (m³).
        """
        if min(wall_area, block_thickness, mortar_joint) <= 0:
            raise ValueError("Todos os parâmetros devem ser positivos.")
        # Estimativa: 0.02 m³/m² de parede (ajuste conforme necessário)
        return wall_area * 0.02
 