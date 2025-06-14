#!/usr/bin/env python3
"""
Gera relatório detalhado em Markdown sobre o ciclo de organização
"""
import json
import os
from datetime import datetime
import sqlite3

class ReportGenerator:
    def __init__(self):
        self.timestamp = datetime.now()
        self.report_dir = 'reports'
        os.makedirs(self.report_dir, exist_ok=True)
        
    def load_latest_metrics(self):
        """Carrega métricas mais recentes"""
        try:
            with open('data/metrics/latest.json', 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def load_check_log(self, filename='check_after.log'):
        """Carrega log do check_organization.sh"""
        try:
            with open(filename, 'r') as f:
                return f.read()
        except Exception:
            return "Log não disponível"
    
    def load_history(self, limit=10):
        """Carrega histórico do SQLite"""
        try:
            conn = sqlite3.connect('data/metrics/metrics.db')
            cursor = conn.execute('''
                SELECT timestamp, score_before, score_after, score_improvement,
                       temp_files_count, project_size_mb, untracked_files
                FROM metrics
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            history = []
            for row in cursor:
                history.append({
                    'timestamp': row[0],
                    'score_before': row[1],
                    'score_after': row[2],
                    'improvement': row[3],
                    'temp_files': row[4],
                    'project_size': row[5],
                    'untracked': row[6]
                })
            conn.close()
            return history
        except Exception:
            return []
    
    def extract_recommendations(self, check_log):
        """Extrai recomendações do log"""
        lines = check_log.split('\n')
        recommendations = []
        in_recommendations = False
        
        for line in lines:
            if '📋 RECOMENDAÇÕES' in line:
                in_recommendations = True
                continue
            elif in_recommendations and line.strip() and line.startswith('•'):
                recommendations.append(line.strip())
            elif in_recommendations and (not line.strip() or '=' in line):
                break
        return recommendations

    def generate_markdown_report(self):
        """Gera relatório completo em Markdown"""
        metrics = self.load_latest_metrics()
        check_log = self.load_check_log()
        history = self.load_history()
        recommendations = self.extract_recommendations(check_log)

        # Cabeçalho
        report = f"""# 📊 Relatório de Organização do Projeto

**Data/Hora:** {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}  
**Branch:** {metrics.get('branch', 'main')}  
**Score Final:** {metrics.get('score_after', 0)}/100 ({'+' if metrics.get('score_improvement', 0) >= 0 else ''}{metrics.get('score_improvement', 0)} pontos)

---

## 📈 Resumo Executivo

| Métrica | Antes | Depois | Mudança |
|---------|-------|--------|---------|
| **Score de Organização** | {metrics.get('score_before', 0)} | {metrics.get('score_after', 0)} | {'+' if metrics.get('score_improvement', 0) >= 0 else ''}{metrics.get('score_improvement', 0)} |
| **Arquivos Temporários** | - | {metrics.get('temp_files_count', 0)} | {metrics.get('temp_files_size_mb', 0)} MB |
| **Arquivos Grandes** | - | {metrics.get('large_files_count', 0)} | - |
| **Diretórios Vazios** | - | {metrics.get('empty_dirs_count', 0)} | - |
| **Arquivos Não Rastreados** | - | {metrics.get('untracked_files', 0)} | - |
| **Tamanho do Projeto** | - | {metrics.get('project_size_mb', 0)} MB | - |

### 🎯 Status da Organização

"""
        # Status baseado no score
        score = metrics.get('score_after', 0)
        if score >= 90:
            report += "✅ **EXCELENTE** - O projeto está muito bem organizado!\n"
        elif score >= 75:
            report += "🟢 **BOM** - O projeto está bem organizado com pequenas melhorias possíveis.\n"
        elif score >= 60:
            report += "🟡 **REGULAR** - Existem várias oportunidades de melhoria na organização.\n"
        else:
            report += "🔴 **ATENÇÃO** - O projeto precisa de organização urgente.\n"

        # Recomendações
        if recommendations:
            report += "\n## 📋 Recomendações Principais\n\n"
            for rec in recommendations[:5]:
                report += f"{rec}\n"

        # Output completo do check, corretamente FECHADO
        report += "\n## 🔍 Análise Detalhada\n\n"
        report += "<details>\n"
        report += "<summary>Clique para ver o output completo da análise</summary>\n\n"
        report += "```text\n"
        report += f"{check_log}\n"
        report += "```\n"
        report += "</details>\n"

        # Histórico
        if history:
            report += "\n## 📊 Histórico de Execuções\n\n"
            report += "| Data/Hora | Score Antes | Score Depois | Melhoria | Temp Files | Tamanho (MB) |\n"
            report += "|-----------|-------------|--------------|----------|------------|-------------|\n"
            for entry in history[:5]:
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%d/%m %H:%M')
                report += f"| {timestamp} | {entry['score_before']} | {entry['score_after']} | "
                report += f"{'+' if entry['improvement'] >= 0 else ''}{entry['improvement']} | "
                report += f"{entry['temp_files']} | {entry['project_size']} |\n"

        # Rodapé
        report += f"\n---\n\n*Relatório gerado automaticamente em {self.timestamp.strftime('%d/%m/%Y às %H:%M:%S')}*\n"

        return report

    def save_report(self, content):
        """Salva o relatório em arquivo markdown"""
        filename = f"report_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.report_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        # Salva também como latest.md
        latest_path = os.path.join(self.report_dir, 'latest.md')
        with open(latest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

def main():
    """Função principal"""
    generator = ReportGenerator()
    
    print("📊 Gerando relatório de organização...")
    
    # Gera o relatório
    report_content = generator.generate_markdown_report()
    
    # Salva o relatório
    filepath = generator.save_report(report_content)
    
    print(f"✅ Relatório salvo em: {filepath}")
    print(f"📄 Também disponível em: reports/latest.md")
    
    # Exibe preview do relatório
    print("\n--- PREVIEW DO RELATÓRIO ---")
    print(report_content[:500] + "...\n")

if __name__ == "__main__":
    main()