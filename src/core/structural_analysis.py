"""
Módulo principal de análise estrutural
"""
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from ..materials.concrete import Concrete
from ..materials.steel import Steel, SteelGrade

@dataclass
class StructuralElement:
    """Elemento estrutural genérico"""
    name: str
    concrete: Concrete
    
    def safety_check(self) -> Dict[str, bool]:
        """Verificações de segurança"""
        raise NotImplementedError

class Column(StructuralElement):
    """Pilar de concreto armado"""
    def __init__(self, name: str, concrete: Concrete, 
                 width: float, height: float, length: float,
                 main_steel: List[Steel], stirrups: Steel):
        super().__init__(name, concrete)
        self.width = width  # cm
        self.height = height  # cm
        self.length = length  # m
        self.main_steel = main_steel
        self.stirrups = stirrups
    
    @property
    def area(self) -> float:
        """Área da seção (cm²)"""
        return self.width * self.height
    
    @property
    def steel_ratio(self) -> float:
        """Taxa de armadura longitudinal (%)"""
        steel_area = sum(bar.area for bar in self.main_steel)
        return (steel_area / self.area) * 100
    
    def slenderness_ratio(self) -> float:
        """Índice de esbeltez"""
        i = min(self.width, self.height) / np.sqrt(12)  # raio de giração
        return (self.length * 100) / i  # converter m para cm
    
    def check_minimum_steel(self) -> bool:
        """Verifica armadura mínima (0.4% NBR 6118)"""
        return self.steel_ratio >= 0.4
    
    def check_maximum_steel(self) -> bool:
        """Verifica armadura máxima (8% NBR 6118)"""
        return self.steel_ratio <= 8.0
    
    def check_slenderness(self) -> bool:
        """Verifica esbeltez máxima (λ ≤ 200)"""
        return self.slenderness_ratio() <= 200
