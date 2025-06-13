"""
Módulo para propriedades e cálculos de concreto
"""
import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class Concrete:
    """Classe para representar propriedades do concreto"""
    fck: float  # Resistência característica (MPa)
    slump: Optional[float] = None  # Abatimento (cm)
    
    @property
    def fcd(self) -> float:
        """Resistência de cálculo"""
        return self.fck / 1.4
    
    @property
    def fctm(self) -> float:
        """Resistência média à tração"""
        if self.fck <= 50:
            return 0.3 * (self.fck ** (2/3))
        else:
            return 2.12 * np.log(1 + 0.11 * self.fck)
    
    @property
    def eci(self) -> float:
        """Módulo de elasticidade inicial (GPa)"""
        if self.fck <= 50:
            return 5600 * np.sqrt(self.fck) / 1000
        else:
            return 21500 * ((self.fck/10 + 1.25) ** (1/3)) / 1000
    
    def __str__(self):
        return f"Concreto C{self.fck}"
