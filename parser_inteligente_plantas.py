#!/usr/bin/env python3
# parser_inteligente_plantas.py
import re
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class TipoPlanta(Enum):
    """Tipos de plantas no sistema"""
    ARQUITETONICA = "arquitetonica"
    ESTRUTURAL = "estrutural"
    ELETRICA = "eletrica"
    HIDRAULICA = "hidraulica"
    LAYOUT = "layout"
    DETALHAMENTO = "detalhamento"

@dataclass
class InfoPlanta:
    """Estrutura principal de uma planta"""
    tipo: TipoPlanta
    proposito_principal: str
    funcionalidades_essenciais: List[str] = field(default_factory=list)
    informacoes_relevantes: Dict[str, any] = field(default_factory=dict)
    detalhes_completos: Dict[str, any] = field(default_factory=dict)
    
class ParserInteligentePlantas:
    """Parser baseado nas 5 regras do framework"""
    
    def __init__(self):
        # 1. Definição de Propósito - Mapeamento de palavras-chave
        self.propositos = {
            TipoPlanta.ARQUITETONICA: {
                "palavras_chave": ["SALA", "QUARTO", "COZINHA", "BANHEIRO", "VARANDA"],
                "proposito": "Definir layout e distribuição dos ambientes",
                "funcoes_essenciais": ["Dimensionamento de ambientes", "Fluxo de circulação", "Aproveitamento de espaço"]
            },
            TipoPlanta.ESTRUTURAL: {
                "palavras_chave": ["PILAR", "VIGA", "LAJE", "FUNDAÇÃO", "CONCRETO"],
                "proposito": "Garantir estabilidade e segurança estrutural",
                "funcoes_essenciais": ["Distribuição de cargas", "Dimensionamento estrutural", "Especificações técnicas"]
            },
            TipoPlanta.ELETRICA: {
                "palavras_chave": ["TOMADA", "INTERRUPTOR", "QUADRO", "CIRCUITO", "ILUMINAÇÃO"],
                "proposito": "Distribuir energia elétrica com segurança",
                "funcoes_essenciais": ["Pontos de energia", "Circuitos elétricos", "Dimensionamento de cabos"]
            },
            TipoPlanta.HIDRAULICA: {
                "palavras_chave": ["ÁGUA", "ESGOTO", "REGISTRO", "CAIXA", "TUBULAÇÃO"],
                "proposito": "Distribuir água e coletar esgoto eficientemente",
                "funcoes_essenciais": ["Pontos hidráulicos", "Dimensionamento de tubulações", "Sistema de drenagem"]
            }
        }
        
        # Padrões de extração otimizados
        self.padroes = {
            "area": re.compile(r'(\d{1,4}[,.]\d{1,2})\s*m[²2]', re.IGNORECASE),
            "dimensao": re.compile(r'(\d{1,3}[,.]\d{1,2})\s*x\s*(\d{1,3}[,.]\d{1,2})', re.IGNORECASE),
            "ambiente": re.compile(r'\b(SALA|QUARTO|COZINHA|BANHEIRO|VARANDA|ÁREA|SUÍTE|LAVABO)\b', re.IGNORECASE),
            "medida_cm": re.compile(r'(\d{2,4})\s*cm', re.IGNORECASE),
            "pavimento": re.compile(r'(TÉRREO|PAVIMENTO|ANDAR|COBERTURA)\s*(\d*)', re.IGNORECASE)
        }
    
    def identificar_tipo_planta(self, texto: str) -> Optional[TipoPlanta]:
        """2. Foco no Usuário - Identifica o tipo baseado no conteúdo"""
        texto_upper = texto.upper()
        
        for tipo, config in self.propositos.items():
            matches = sum(1 for palavra in config["palavras_chave"] if palavra in texto_upper)
            if matches >= 2:  # Pelo menos 2 palavras-chave
                return tipo
        
        return TipoPlanta.ARQUITETONICA  # Default

# Lista de ambientes válidos (fora da classe)
AMBIENTES_VALIDOS = {
    'SALA', 'COZINHA', 'QUARTO', 'SUÍTE', 'BANHEIRO', 'WC', 
    'VARANDA', 'ÁREA', 'ÁREA DE SERVIÇO', 'DESPENSA', 'GARAGEM',
    'ESCRITÓRIO', 'CLOSET', 'LAVABO', 'HALL', 'CORREDOR',
    'SACADA', 'TERRAÇO', 'CHURRASQUEIRA', 'PISCINA'
}
#!/usr/bin/env python3
# parser_inteligente_plantas.py
import re
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class TipoPlanta(Enum):
    """Tipos de plantas no sistema"""
    ARQUITETONICA = "arquitetonica"
    ESTRUTURAL = "estrutural"
    ELETRICA = "eletrica"
    HIDRAULICA = "hidraulica"
    LAYOUT = "layout"
    DETALHAMENTO = "detalhamento"

@dataclass
class InfoPlanta:
    """Estrutura principal de uma planta"""
    tipo: TipoPlanta
    proposito_principal: str
    funcionalidades_essenciais: List[str] = field(default_factory=list)
    informacoes_relevantes: Dict[str, any] = field(default_factory=dict)
    detalhes_completos: Dict[str, any] = field(default_factory=dict)

# Lista de ambientes válidos (fora da classe)
AMBIENTES_VALIDOS = {
    'SALA', 'COZINHA', 'QUARTO', 'SUÍTE', 'BANHEIRO', 'WC', 
    'VARANDA', 'ÁREA', 'ÁREA DE SERVIÇO', 'DESPENSA', 'GARAGEM',
    'ESCRITÓRIO', 'CLOSET', 'LAVABO', 'HALL', 'CORREDOR',
    'SACADA', 'TERRAÇO', 'CHURRASQUEIRA', 'PISCINA'
}

class ParserInteligentePlantas:
    """Parser baseado nas 5 regras do framework"""
    
    def __init__(self):
        self.propositos = {
            TipoPlanta.ARQUITETONICA: {
                "palavras_chave": ["SALA", "QUARTO", "COZINHA", "BANHEIRO", "VARANDA"],
                "proposito": "Definir layout e distribuição dos ambientes",
                "funcoes_essenciais": ["Dimensionamento de ambientes", "Fluxo de circulação", "Aproveitamento de espaço"]
            },
            TipoPlanta.ESTRUTURAL: {
                "palavras_chave": ["PILAR", "VIGA", "LAJE", "FUNDAÇÃO", "CONCRETO"],
                "proposito": "Garantir estabilidade e segurança estrutural",
                "funcoes_essenciais": ["Distribuição de cargas", "Dimensionamento estrutural", "Especificações técnicas"]
            },
            TipoPlanta.ELETRICA: {
                "palavras_chave": ["TOMADA", "INTERRUPTOR", "QUADRO", "CIRCUITO", "ILUMINAÇÃO"],
                "proposito": "Distribuir energia elétrica com segurança",
                "funcoes_essenciais": ["Pontos de energia", "Circuitos elétricos", "Dimensionamento de cabos"]
            },
            TipoPlanta.HIDRAULICA: {
                "palavras_chave": ["ÁGUA", "ESGOTO", "REGISTRO", "CAIXA", "TUBULAÇÃO"],
                "proposito": "Distribuir água e coletar esgoto eficientemente",
                "funcoes_essenciais": ["Pontos hidráulicos", "Dimensionamento de tubulações", "Sistema de drenagem"]
            }
        }
        self.padroes = {
            "area": re.compile(r'(\d{1,4}[,.]\d{1,2})\s*m[²2]', re.IGNORECASE),
            "dimensao": re.compile(r'(\d{1,3}[,.]\d{1,2})\s*x\s*(\d{1,3}[,.]\d{1,2})', re.IGNORECASE),
            "ambiente": re.compile(r'\b(SALA|QUARTO|COZINHA|BANHEIRO|VARANDA|ÁREA|SUÍTE|LAVABO)\b', re.IGNORECASE),
            "medida_cm": re.compile(r'(\d{2,4})\s*cm', re.IGNORECASE),
            "pavimento": re.compile(r'(TÉRREO|PAVIMENTO|ANDAR|COBERTURA)\s*(\d*)', re.IGNORECASE)
        }
    
    def identificar_tipo_planta(self, texto: str) -> Optional[TipoPlanta]:
        texto_upper = texto.upper()
        for tipo, config in self.propositos.items():
            matches = sum(1 for palavra in config["palavras_chave"] if palavra in texto_upper)
            if matches >= 2:
                return tipo
        return TipoPlanta.ARQUITETONICA

    def extrair_informacoes_relevantes(self, texto: str, tipo: TipoPlanta) -> Dict:
        """3. Exibição Direta - Extrai apenas o essencial"""
        relevantes = {}
        
        # Informações sempre relevantes
        areas = self.padroes["area"].findall(texto)
        if areas:
            relevantes["areas_m2"] = [area.replace(",", ".") for area in areas]
        
        ambientes = self.padroes["ambiente"].findall(texto)
        if ambientes:
            relevantes["ambientes"] = list(set(amb.upper() for amb in ambientes))
        
        # Informações específicas por tipo
        if tipo == TipoPlanta.ARQUITETONICA:
            dimensoes = self.padroes["dimensao"].findall(texto)
            if dimensoes:
                relevantes["dimensoes"] = [(d1.replace(",", "."), d2.replace(",", ".")) for d1, d2 in dimensoes]
        
        elif tipo == TipoPlanta.ESTRUTURAL:
            # Buscar informações estruturais específicas
            if "FCK" in texto.upper():
                fck_match = re.search(r'FCK\s*(\d+)', texto, re.IGNORECASE)
                if fck_match:
                    relevantes["resistencia_concreto"] = f"FCK {fck_match.group(1)} MPa"
        
        return relevantes

    def gerar_checklist_resumido(self, info_planta: InfoPlanta) -> List[str]:
        checklist = []
        for func in info_planta.funcionalidades_essenciais:
            checklist.append(f"✓ {func}")
        if "ambientes" in info_planta.informacoes_relevantes:
            qtd = len(info_planta.informacoes_relevantes["ambientes"])
            checklist.append(f"✓ {qtd} ambientes identificados")
        if "areas_m2" in info_planta.informacoes_relevantes:
            checklist.append(f"✓ Áreas calculadas disponíveis")
        return checklist

    def processar_planta(self, texto_ocr: str, modo_detalhado: bool = False) -> InfoPlanta:
        tipo = self.identificar_tipo_planta(texto_ocr)
        config = self.propositos[tipo]
        planta = InfoPlanta(
            tipo=tipo,
            proposito_principal=config["proposito"],
            funcionalidades_essenciais=config["funcoes_essenciais"],
            informacoes_relevantes=self.extrair_informacoes_relevantes(texto_ocr, tipo)
        )
        if modo_detalhado:
            planta.detalhes_completos = self._extrair_detalhes_completos(texto_ocr, tipo)
        return planta

    def _extrair_detalhes_completos(self, texto: str, tipo: TipoPlanta) -> Dict:
        detalhes = {}
        medidas_cm = self.padroes["medida_cm"].findall(texto)
        if medidas_cm:
            detalhes["medidas_cm"] = medidas_cm
        pavimentos = self.padroes["pavimento"].findall(texto)
        if pavimentos:
            detalhes["pavimentos"] = pavimentos
        detalhes["texto_original"] = texto
        return detalhes

    def exibir_resumo_usuario(self, planta: InfoPlanta) -> str:
        resumo = f"""
🏗️ **PLANTA {planta.tipo.value.upper()}**

📌 **O que esta planta faz:**
   {planta.proposito_principal}

📋 **Checklist Rápido:**
{chr(10).join(f'   {item}' for item in self.gerar_checklist_resumido(planta))}

🔍 **Informações Principais:**
"""
        if planta.informacoes_relevantes.get("ambientes"):
            resumo += f"   • Ambientes: {', '.join(planta.informacoes_relevantes['ambientes'])}\n"
        if planta.informacoes_relevantes.get("areas_m2"):
            resumo += f"   • Áreas identificadas: {len(planta.informacoes_relevantes['areas_m2'])} medições\n"
        resumo += "\n💡 *Para mais detalhes, use modo_detalhado=True*"
        return resumo

# Script principal
if __name__ == "__main__":
    parser = ParserInteligentePlantas()
    with open("dados/pipeline_output/construcode_ocr.txt", "r", encoding="utf-8") as f:
        texto_ocr = f.read()
    planta = parser.processar_planta(texto_ocr, modo_detalhado=False)
    print(parser.exibir_resumo_usuario(planta))
    resultado = {
        "tipo": planta.tipo.value,
        "proposito": planta.proposito_principal,
        "informacoes_relevantes": planta.informacoes_relevantes,
        "checklist": parser.gerar_checklist_resumido(planta)
    }
    with open("dados/saidas_parser/planta_resumo.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print("\n✅ Resumo salvo em: dados/saidas_parser/planta_resumo.json")
class ParserInteligentePlantas:
    """Parser baseado nas 5 regras do framework"""
    
    def __init__(self):
        # 1. Definição de Propósito - Mapeamento de palavras-chave
        self.propositos = {
            TipoPlanta.ARQUITETONICA: {
                "palavras_chave": ["SALA", "QUARTO", "COZINHA", "BANHEIRO", "VARANDA"],
                "proposito": "Definir layout e distribuição dos ambientes",
                "funcoes_essenciais": ["Dimensionamento de ambientes", "Fluxo de circulação", "Aproveitamento de espaço"]
            },
            TipoPlanta.ESTRUTURAL: {
                "palavras_chave": ["PILAR", "VIGA", "LAJE", "FUNDAÇÃO", "CONCRETO"],
                "proposito": "Garantir estabilidade e segurança estrutural",
                "funcoes_essenciais": ["Distribuição de cargas", "Dimensionamento estrutural", "Especificações técnicas"]
            },
            TipoPlanta.ELETRICA: {
                "palavras_chave": ["TOMADA", "INTERRUPTOR", "QUADRO", "CIRCUITO", "ILUMINAÇÃO"],
                "proposito": "Distribuir energia elétrica com segurança",
                "funcoes_essenciais": ["Pontos de energia", "Circuitos elétricos", "Dimensionamento de cabos"]
            },
            TipoPlanta.HIDRAULICA: {
                "palavras_chave": ["ÁGUA", "ESGOTO", "REGISTRO", "CAIXA", "TUBULAÇÃO"],
                "proposito": "Distribuir água e coletar esgoto eficientemente",
                "funcoes_essenciais": ["Pontos hidráulicos", "Dimensionamento de tubulações", "Sistema de drenagem"]
            }
        }
        
        # Padrões de extração otimizados
        self.padroes = {
            "area": re.compile(r'(\d{1,4}[,.]\d{1,2})\s*m[²2]', re.IGNORECASE),
            "dimensao": re.compile(r'(\d{1,3}[,.]\d{1,2})\s*x\s*(\d{1,3}[,.]\d{1,2})', re.IGNORECASE),
            "ambiente": re.compile(r'\b(SALA|QUARTO|COZINHA|BANHEIRO|VARANDA|ÁREA|SUÍTE|LAVABO)\b', re.IGNORECASE),
            "medida_cm": re.compile(r'(\d{2,4})\s*cm', re.IGNORECASE),
            "pavimento": re.compile(r'(TÉRREO|PAVIMENTO|ANDAR|COBERTURA)\s*(\d*)', re.IGNORECASE)
        }
    
    def identificar_tipo_planta(self, texto: str) -> Optional[TipoPlanta]:
        """2. Foco no Usuário - Identifica o tipo baseado no conteúdo"""
        texto_upper = texto.upper()
        
        for tipo, config in self.propositos.items():
            matches = sum(1 for palavra in config["palavras_chave"] if palavra in texto_upper)
            if matches >= 2:  # Pelo menos 2 palavras-chave
                return tipo
        
        return TipoPlanta.ARQUITETONICA  # Default

    def extrair_informacoes_relevantes(self, texto: str, tipo: TipoPlanta) -> Dict:
        """3. Exibição Direta - Extrai apenas o essencial"""
        relevantes = {}
        
        # Informações sempre relevantes
        areas = self.padroes["area"].findall(texto)
        if areas:
            relevantes["areas_m2"] = [area.replace(",", ".") for area in areas]
        
        ambientes = self.padroes["ambiente"].findall(texto)
        if ambientes:
            relevantes["ambientes"] = list(set(amb.upper() for amb in ambientes))
        
        # Informações específicas por tipo
        if tipo == TipoPlanta.ARQUITETONICA:
            dimensoes = self.padroes["dimensao"].findall(texto)
            if dimensoes:
                relevantes["dimensoes"] = [(d1.replace(",", "."), d2.replace(",", ".")) for d1, d2 in dimensoes]
        
        elif tipo == TipoPlanta.ESTRUTURAL:
            # Buscar informações estruturais específicas
            if "FCK" in texto.upper():
                fck_match = re.search(r'FCK\s*(\d+)', texto, re.IGNORECASE)
                if fck_match:
                    relevantes["resistencia_concreto"] = f"FCK {fck_match.group(1)} MPa"
        
        return relevantes

    def gerar_checklist_resumido(self, info_planta: InfoPlanta) -> List[str]:
        """4. Opções Interativas - Checklist das funcionalidades"""
        checklist = []
        
        # Adiciona funcionalidades essenciais
        for func in info_planta.funcionalidades_essenciais:
            checklist.append(f"✓ {func}")
        
        # Adiciona informações relevantes como checklist
        if "ambientes" in info_planta.informacoes_relevantes:
            qtd = len(info_planta.informacoes_relevantes["ambientes"])
            checklist.append(f"✓ {qtd} ambientes identificados")
        
        if "areas_m2" in info_planta.informacoes_relevantes:
            checklist.append(f"✓ Áreas calculadas disponíveis")
        
        return checklist

    def processar_planta(self, texto_ocr: str, modo_detalhado: bool = False) -> InfoPlanta:
        """5. Acesso Detalhado sob Demanda - Processa conforme necessidade"""
        
        # Identifica tipo e propósito
        tipo = self.identificar_tipo_planta(texto_ocr)
        config = self.propositos[tipo]
        
        # Cria objeto InfoPlanta
        planta = InfoPlanta(
            tipo=tipo,
            proposito_principal=config["proposito"],
            funcionalidades_essenciais=config["funcoes_essenciais"],
            informacoes_relevantes=self.extrair_informacoes_relevantes(texto_ocr, tipo)
        )
        
        # Só processa detalhes se solicitado
        if modo_detalhado:
            planta.detalhes_completos = self._extrair_detalhes_completos(texto_ocr, tipo)
        
        return planta

    def _extrair_detalhes_completos(self, texto: str, tipo: TipoPlanta) -> Dict:
        """Extração completa apenas quando solicitada"""
        detalhes = {}
        
        # Todas as medidas em cm
        medidas_cm = self.padroes["medida_cm"].findall(texto)
        if medidas_cm:
            detalhes["medidas_cm"] = medidas_cm
        
        # Pavimentos
        pavimentos = self.padroes["pavimento"].findall(texto)
        if pavimentos:
            detalhes["pavimentos"] = pavimentos
        
        # Texto completo para análise posterior
        detalhes["texto_original"] = texto
        
        return detalhes

    def exibir_resumo_usuario(self, planta: InfoPlanta) -> str:
        """Interface amigável para o usuário"""
        resumo = f"""
🏗️ **PLANTA {planta.tipo.value.upper()}**

📌 **O que esta planta faz:**
   {planta.proposito_principal}

📋 **Checklist Rápido:**
{chr(10).join(f'   {item}' for item in self.gerar_checklist_resumido(planta))}

🔍 **Informações Principais:**
"""
        
        if planta.informacoes_relevantes.get("ambientes"):
            resumo += f"   • Ambientes: {', '.join(planta.informacoes_relevantes['ambientes'])}\n"
        
        if planta.informacoes_relevantes.get("areas_m2"):
            resumo += f"   • Áreas identificadas: {len(planta.informacoes_relevantes['areas_m2'])} medições\n"
        
        resumo += "\n💡 *Para mais detalhes, use modo_detalhado=True*"
        
        return resumo

# Script principal
if __name__ == "__main__":
    # Inicializa parser
    parser = ParserInteligentePlantas()
    
    # Carrega OCR
    with open("dados/pipeline_output/construcode_ocr.txt", "r", encoding="utf-8") as f:
        texto_ocr = f.read()
    
    # Processa planta (modo resumido por padrão)
    planta = parser.processar_planta(texto_ocr, modo_detalhado=False)
    
    # Exibe resumo para usuário
    print(parser.exibir_resumo_usuario(planta))
    
    # Salva resultado estruturado
    resultado = {
        "tipo": planta.tipo.value,
        "proposito": planta.proposito_principal,
        "informacoes_relevantes": planta.informacoes_relevantes,
        "checklist": parser.gerar_checklist_resumido(planta)
    }
    
    with open("dados/saidas_parser/planta_resumo.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Resumo salvo em: dados/saidas_parser/planta_resumo.json")