"""
Módulo para propriedades do aço
"""
from dataclasses import dataclass
from enum import Enum

class SteelGrade(Enum):
    """Categorias de aço conforme NBR"""
    CA25 = 250
    CA50 = 500
    CA60 = 600

@dataclass
class Steel:
    """Classe para representar propriedades do aço"""
    grade: SteelGrade
    diameter: float  # mm
    
    @property
    def fyk(self) -> float:
        """Resistência característica ao escoamento (MPa)"""
        return self.grade.value
    
    @property
    def fyd(self) -> float:
        """Resistência de cálculo"""
        return self.fyk / 1.15
    
    @property
    def area(self) -> float:
        """Área da seção transversal (cm²)"""
        return 3.14159 * (self.diameter/10)**2 / 4
    
    @property
    def weight_per_meter(self) -> float:
        """Peso por metro linear (kg/m)"""
        return self.area * 7.85  # densidade do aço = 7.85 g/cm³
    
    @property
    def modulus_elasticity(self) -> float:
        """Módulo de elasticidade (GPa)"""
        return 210
