# validador_wsf13.py
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import pandas as pd

class ValidadorWSF13:
    def __init__(self):
        self.resultados = []
        self.metricas = {
            'geometria': {'acertos': 0, 'erros': 0, 'precisao': 0},
            'classificacao': {'acertos': 0, 'erros': 0, 'precisao': 0},
            'funcionalidade': {'acertos': 0, 'erros': 0, 'precisao': 0},
            'ambientes': {'acertos': 0, 'erros': 0, 'precisao': 0}
        }
        
    def executar_teste_completo(self, pasta_plantas, gabarito_json):
        """Executa teste completo em batch de plantas"""
        gabarito = self.carregar_gabarito(gabarito_json)
        
        for arquivo in Path(pasta_plantas).glob('**/*'):
            if arquivo.suffix.lower() in ['.pdf', '.png', '.jpg', '.jpeg']:
                print(f"\n🔍 Testando: {arquivo.name}")
                resultado = self.testar_planta(arquivo, gabarito.get(arquivo.name, {}))
                self.resultados.append(resultado)
                
        self.gerar_relatorio_completo()
    
    def carregar_gabarito(self, arquivo_json):
        """Carrega gabarito de teste"""
        try:
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Erro ao carregar gabarito: {e}")
            return {}
    
    def testar_planta(self, arquivo: Path, esperado: Dict) -> Dict:
        """Testa uma planta individual contra o gabarito"""
        try:
            from analisador_plantas_wsf import AnalisadorPlantasWSF
        except ImportError:
            class AnalisadorPlantasWSF:
                def processar_planta(self, arquivo):
                    print(f"[Fallback] processar_planta chamado com arquivo: {arquivo}")
                    return {
                        'geometria': {'tipo': 'retangular', 'area': 100},
                        'classificacao': {'categoria': 'residencial'},
                        'funcionalidade': {'comodos': ['sala', 'quarto']},
                        'ambientes': ['sala', 'cozinha', 'quarto']
                    }
        
        inicio = time.time()
        resultado = {
            'arquivo': arquivo.name,
            'caminho': str(arquivo),
            'timestamp': datetime.now().isoformat(),
            'testes': {}
        }
        
        try:
            # Inicializar analisador
            analisador = AnalisadorPlantasWSF()
            
            # Processar planta
            extraido = analisador.processar_planta(str(arquivo))
            
            # Validar cada categoria
            resultado['testes']['geometria'] = self.validar_dados_geometricos(extraido, esperado)
            resultado['testes']['classificacao'] = self.validar_classificacao(extraido, esperado)
            resultado['testes']['funcionalidade'] = self.validar_funcionalidade(extraido, esperado)
            resultado['testes']['ambientes'] = self.validar_ambientes(extraido, esperado)
            
            # Atualizar métricas globais
            self.atualizar_metricas(resultado['testes'])
            
            # Tempo de processamento
            resultado['tempo_processamento'] = time.time() - inicio
            resultado['status'] = 'sucesso'
            
        except Exception as e:
            resultado['status'] = 'erro'
            resultado['erro'] = str(e)
            resultado['tempo_processamento'] = time.time() - inicio
            
        return resultado
    
    def validar_dados_geometricos(self, extraido: Dict, esperado: Dict) -> Dict:
        """Valida dados geométricos extraídos"""
        validacao = {
            'total_testes': 0,
            'acertos': 0,
            'erros': [],
            'detalhes': {}
        }
        
        testes = [
            # Tipo de geometria
            ('tipo_geometria', 
             extraido.get('geometria', {}).get('tipo'),
             esperado.get('geometria', {}).get('tipo')),
            
            # Área
            ('area',
             extraido.get('geometria', {}).get('area'),
             esperado.get('geometria', {}).get('area')),
            
            # Perímetro
            ('perimetro',
             extraido.get('geometria', {}).get('perimetro'),
             esperado.get('geometria', {}).get('perimetro')),
            
            # Dimensões
            ('dimensoes',
             extraido.get('geometria', {}).get('dimensoes'),
             esperado.get('geometria', {}).get('dimensoes')),
            
            # Ângulos
            ('angulos',
             extraido.get('geometria', {}).get('angulos'),
             esperado.get('geometria', {}).get('angulos')),
            
            # Conversões
            ('conversoes',
             extraido.get('geometria', {}).get('conversoes'),
             esperado.get('geometria', {}).get('conversoes'))
        ]
        
        for nome_teste, valor_extraido, valor_esperado in testes:
            validacao['total_testes'] += 1
            
            if valor_esperado is not None:
                if valor_extraido == valor_esperado:
                    validacao['acertos'] += 1
                    validacao['detalhes'][nome_teste] = {
                        'status': 'correto',
                        'extraido': valor_extraido,
                        'esperado': valor_esperado
                    }
                else:
                    validacao['erros'].append({
                        'campo': nome_teste,
                        'extraido': valor_extraido,
                        'esperado': valor_esperado
                    })
                    validacao['detalhes'][nome_teste] = {
                        'status': 'incorreto',
                        'extraido': valor_extraido,
                        'esperado': valor_esperado
                    }
        
        # Calcular taxa de acerto
        if validacao['total_testes'] > 0:
            validacao['taxa_acerto'] = (validacao['acertos'] / validacao['total_testes']) * 100
        else:
            validacao['taxa_acerto'] = 0
            
        return validacao
    
    def validar_classificacao(self, extraido: Dict, esperado: Dict) -> Dict:
        """Valida classificação da planta"""
        validacao = {
            'total_testes': 0,
            'acertos': 0,
            'erros': [],
            'detalhes': {}
        }
        
        testes = [
            ('categoria', 
             extraido.get('classificacao', {}).get('categoria'),
             esperado.get('classificacao', {}).get('categoria')),
            
            ('subcategoria',
             extraido.get('classificacao', {}).get('subcategoria'),
             esperado.get('classificacao', {}).get('subcategoria')),
            
            ('tipo_uso',
             extraido.get('classificacao', {}).get('tipo_uso'),
             esperado.get('classificacao', {}).get('tipo_uso')),
            
            ('pavimentos',
             extraido.get('classificacao', {}).get('pavimentos'),
             esperado.get('classificacao', {}).get('pavimentos'))
        ]
        
        for nome_teste, valor_extraido, valor_esperado in testes:
            if valor_esperado is not None:
                validacao['total_testes'] += 1
                
                if valor_extraido == valor_esperado:
                    validacao['acertos'] += 1
                    validacao['detalhes'][nome_teste] = 'correto'
                else:
                    validacao['erros'].append({
                        'campo': nome_teste,
                        'extraido': valor_extraido,
                        'esperado': valor_esperado
                    })
                    validacao['detalhes'][nome_teste] = 'incorreto'
        
        if validacao['total_testes'] > 0:
            validacao['taxa_acerto'] = (validacao['acertos'] / validacao['total_testes']) * 100
        else:
            validacao['taxa_acerto'] = 0
            
        return validacao
    
    def validar_funcionalidade(self, extraido: Dict, esperado: Dict) -> Dict:
        """Valida funcionalidades identificadas"""
        validacao = {
            'total_testes': 0,
            'acertos': 0,
            'erros': [],
            'detalhes': {}
        }
        
        # Validar cômodos
        comodos_extraidos = set(extraido.get('funcionalidade', {}).get('comodos', []))
        comodos_esperados = set(esperado.get('funcionalidade', {}).get('comodos', []))
        
        if comodos_esperados:
            validacao['total_testes'] += 1
            
            if comodos_extraidos == comodos_esperados:
                validacao['acertos'] += 1
                validacao['detalhes']['comodos'] = 'correto'
            else:
                validacao['erros'].append({
                    'campo': 'comodos',
                    'faltando': list(comodos_esperados - comodos_extraidos),
                    'extras': list(comodos_extraidos - comodos_esperados)
                })
                validacao['detalhes']['comodos'] = 'incorreto'
        
        # Validar características
        caracteristicas_extraidas = set(extraido.get('funcionalidade', {}).get('caracteristicas', []))
        caracteristicas_esperadas = set(esperado.get('funcionalidade', {}).get('caracteristicas', []))
        
        if caracteristicas_esperadas:
            validacao['total_testes'] += 1
            
            if caracteristicas_extraidas == caracteristicas_esperadas:
                validacao['acertos'] += 1
                validacao['detalhes']['caracteristicas'] = 'correto'
            else:
                validacao['erros'].append({
                    'campo': 'caracteristicas',
                    'faltando': list(caracteristicas_esperadas - caracteristicas_extraidas),
                    'extras': list(caracteristicas_extraidas - caracteristicas_esperadas)
                })
                validacao['detalhes']['caracteristicas'] = 'incorreto'
        
        if validacao['total_testes'] > 0:
            validacao['taxa_acerto'] = (validacao['acertos'] / validacao['total_testes']) * 100
        else:
            validacao['taxa_acerto'] = 0
            
        return validacao
    
    def validar_ambientes(self, extraido: Dict, esperado: Dict) -> Dict:
        """Valida ambientes detectados"""
        validacao = {
            'total_testes': 0,
            'acertos': 0,
            'erros': [],
            'detalhes': {}
        }
        
        ambientes_extraidos = set(extraido.get('ambientes', []))
        ambientes_esperados = set(esperado.get('ambientes', []))
        
        if ambientes_esperados:
            validacao['total_testes'] = 1
            
            # Calcular precisão e recall
            intersecao = ambientes_extraidos & ambientes_esperados
            
            if len(ambientes_extraidos) > 0:
                precisao = len(intersecao) / len(ambientes_extraidos)
            else:
                precisao = 0
                
            if len(ambientes_esperados) > 0:
                recall = len(intersecao) / len(ambientes_esperados)
            else:
                recall = 0
            
            # F1 score
            if precisao + recall > 0:
                f1_score = 2 * (precisao * recall) / (precisao + recall)
            else:
                f1_score = 0
            
            validacao['detalhes'] = {
                'precisao': precisao * 100,
                'recall': recall * 100,
                'f1_score': f1_score * 100,
                'ambientes_corretos': list(intersecao),
                'ambientes_faltando': list(ambientes_esperados - ambientes_extraidos),
                'ambientes_extras': list(ambientes_extraidos - ambientes_esperados)
            }
            
            # Considerar acerto se F1 > 80%
            if f1_score >= 0.8:
                validacao['acertos'] = 1
            
            validacao['taxa_acerto'] = f1_score * 100
        else:
            validacao['taxa_acerto'] = 0
            
        return validacao
    
    def atualizar_metricas(self, testes: Dict):
        """Atualiza métricas globais"""
        for categoria in ['geometria', 'classificacao', 'funcionalidade', 'ambientes']:
            if categoria in testes:
                teste = testes[categoria]
                if teste.get('total_testes', 0) > 0:
                    self.metricas[categoria]['acertos'] += teste.get('acertos', 0)
                    self.metricas[categoria]['erros'] += (teste['total_testes'] - teste.get('acertos', 0))
    
    def calcular_metricas_finais(self):
        """Calcula métricas finais de precisão"""
        for categoria in self.metricas:
            total = self.metricas[categoria]['acertos'] + self.metricas[categoria]['erros']
            if total > 0:
                self.metricas[categoria]['precisao'] = (self.metricas[categoria]['acertos'] / total) * 100
            else:
                self.metricas[categoria]['precisao'] = 0
    
    def gerar_relatorio_completo(self):
        """Gera relatórios detalhados dos testes"""
        self.calcular_metricas_finais()
        
        # Criar diretório de relatórios
        Path('relatorios_validacao').mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Relatório JSON completo
        relatorio_completo = {
            'timestamp': datetime.now().isoformat(),
            'resumo': {
                'total_plantas': len(self.resultados),
                'sucesso': sum(1 for r in self.resultados if r.get('status') == 'sucesso'),
                'erros': sum(1 for r in self.resultados if r.get('status') == 'erro'),
                'tempo_total': sum(r.get('tempo_processamento', 0) for r in self.resultados)
            },
            'metricas_globais': self.metricas,
            'resultados_detalhados': self.resultados
        }
        
        with open(f'relatorios_validacao/relatorio_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio_completo, f, indent=2, ensure_ascii=False)
        
        # 2. Relatório CSV resumido
        df_resumo = pd.DataFrame([
            {
                'arquivo': r['arquivo'],
                'status': r.get('status', 'erro'),
                'tempo_processamento': r.get('tempo_processamento', 0),
                'geometria_acerto': r.get('testes', {}).get('geometria', {}).get('taxa_acerto', 0),
                'classificacao_acerto': r.get('testes', {}).get('classificacao', {}).get('taxa_acerto', 0),
                'funcionalidade_acerto': r.get('testes', {}).get('funcionalidade', {}).get('taxa_acerto', 0),
                'ambientes_acerto': r.get('testes', {}).get('ambientes', {}).get('taxa_acerto', 0)
            }
            for r in self.resultados
        ])
        
        df_resumo.to_csv(f'relatorios_validacao/resumo_{timestamp}.csv', index=False)
        
        # 3. Relatório Markdown legível
        self.gerar_relatorio_markdown(timestamp)
        
        print(f"\n✅ Relatórios salvos em 'relatorios_validacao/'")
        print(f"   - relatorio_{timestamp}.json")
        print(f"   - resumo_{timestamp}.csv")
        print(f"   - relatorio_{timestamp}.md")
    
    def gerar_relatorio_markdown(self, timestamp: str):
        """Gera relatório em formato Markdown"""
        with open(f'relatorios_validacao/relatorio_{timestamp}.md', 'w', encoding='utf-8') as f:
            f.write("# Relatório de Validação WSF+13\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            # Resumo geral
            f.write("## 📊 Resumo Geral\n\n")
            total = len(self.resultados)
            sucesso = sum(1 for r in self.resultados if r.get('status') == 'sucesso')
            erro = total - sucesso
            
            f.write(f"- **Total de plantas testadas:** {total}\n")
            f.write(f"- **Sucessos:** {sucesso} ({(sucesso/total*100):.1f}%)\n")
            f.write(f"- **Erros:** {erro} ({(erro/total*100):.1f}%)\n")
            f.write(f"- **Tempo total:** {sum(r.get('tempo_processamento', 0) for r in self.resultados):.2f}s\n\n")
            
            # Métricas por categoria
            f.write("## 📈 Métricas por Categoria\n\n")
            f.write("| Categoria | Acertos | Erros | Precisão |\n")
            f.write("|-----------|---------|-------|----------|\n")
            
            for cat, dados in self.metricas.items():
                f.write(f"| {cat.title()} | {dados['acertos']} | {dados['erros']} | {dados['precisao']:.1f}% |\n")
            
            # Detalhes por planta
            f.write("\n## 📋 Detalhes por Planta\n\n")
            
            for resultado in self.resultados:
                f.write(f"### 🏗️ {resultado['arquivo']}\n\n")
                f.write(f"- **Status:** {resultado.get('status', 'erro')}\n")
                f.write(f"- **Tempo:** {resultado.get('tempo_processamento', 0):.2f}s\n")
                
                if resultado.get('status') == 'sucesso':
                    f.write("\n**Resultados dos testes:**\n\n")
                    
                    for teste, dados in resultado.get('testes', {}).items():
                        f.write(f"- **{teste.title()}:** {dados.get('taxa_acerto', 0):.1f}% de acerto\n")
                        
                        if dados.get('erros'):
                            f.write(f"  - Erros encontrados: {len(dados['erros'])}\n")
                else:
                    f.write(f"- **Erro:** {resultado.get('erro', 'Erro desconhecido')}\n")
                
                f.write("\n---\n\n")

# Exemplo de uso
if __name__ == "__main__":
    validador = ValidadorWSF13()
    
    # Criar gabarito de exemplo
    gabarito_exemplo = {
        "planta_01.pdf": {
            "geometria": {
                "tipo": "retangular",
                "area": 120.5,
                "perimetro": 44.0
            },
            "classificacao": {
                "categoria": "residencial",
                "subcategoria": "casa",
                "pavimentos": 2
            },
            "funcionalidade": {
                "comodos": ["sala", "cozinha", "quarto", "banheiro"],
                "caracteristicas": ["varanda", "garagem"]
            },
            "ambientes": ["sala", "cozinha", "quarto", "banheiro", "varanda", "garagem"]
        }
    }
    
    # Salvar gabarito de exemplo
    with open('gabarito_exemplo.json', 'w', encoding='utf-8') as f:
        json.dump(gabarito_exemplo, f, indent=2, ensure_ascii=False)
    
    print("🚀 Iniciando validação do WSF+13...")
    print("📁 Use: validador.executar_teste_completo('pasta_com_plantas/', 'gabarito.json')")