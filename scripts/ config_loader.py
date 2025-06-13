#!/usr/bin/env python3
# config_loader.py
import json
from pathlib import Path
from typing import Dict, List, Any

class ConfigLoader:
    """Carregador de configurações para tipos de plantas"""
    
    def __init__(self, config_path: str = "config_tipos_plantas.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Carrega o arquivo de configuração JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Arquivo {self.config_path} não encontrado. Usando configuração padrão.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retorna configuração padrão mínima"""
        return {
            "tipos_plantas": {
                "arquitetonica": {
                    "nome": "Planta Arquitetônica",
                    "palavras_chave": ["planta baixa", "arquitetônica"]
                }
            },
            "ambientes_validos": ["SALA", "COZINHA", "QUARTO", "BANHEIRO"]
        }
    
    def get_tipos_plantas(self) -> Dict[str, Dict]:
        """Retorna todos os tipos de plantas configurados"""
        return self.config.get("tipos_plantas", {})
    
    def get_tipo_planta(self, tipo: str) -> Dict[str, Any]:
        """Retorna configuração específica de um tipo"""
        return self.config.get("tipos_plantas", {}).get(tipo, {})
    
    def get_ambientes_validos(self) -> List[str]:
        """Retorna lista de ambientes válidos"""
        return self.config.get("ambientes_validos", [])
    
    def get_palavras_chave(self, tipo: str) -> List[str]:
        """Retorna palavras-chave de um tipo específico"""
        tipo_config = self.get_tipo_planta(tipo)
        return tipo_config.get("palavras_chave", [])
    
    def get_padroes_regex(self, tipo: str) -> Dict[str, str]:
        """Retorna padrões regex de um tipo específico"""
        tipo_config = self.get_tipo_planta(tipo)
        return tipo_config.get("padroes_regex", {})
    
    def get_normas_tecnicas(self, tipo: str) -> List[str]:
        """Retorna normas técnicas aplicáveis"""
        tipo_config = self.get_tipo_planta(tipo)
        return tipo_config.get("normas_tecnicas", [])
    
    def adicionar_tipo_planta(self, tipo_id: str, config_tipo: Dict) -> bool:
        """Adiciona novo tipo de planta e salva no arquivo"""
        try:
            self.config["tipos_plantas"][tipo_id] = config_tipo
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Erro ao adicionar tipo: {e}")
            return False