"""
Módulo para análise de vigas
"""
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Beam:
    """Classe para análise de vigas"""
    length: float  # Comprimento (m)
    width: float   # Largura (m)
    height: float  # Altura (m)
    
    def moment_of_inertia(self) -> float:
        """Calcula momento de inércia"""
        return (self.width * self.height**3) / 12
    
    def section_area(self) -> float:
        """Área da seção transversal"""
        return self.width * self.height
    
    def max_deflection_uniform_load(self, load: float, E: float) -> float:
        """Deflexão máxima para carga uniforme"""
        return (5 * load * self.length**4) / (384 * E * self.moment_of_inertia())
