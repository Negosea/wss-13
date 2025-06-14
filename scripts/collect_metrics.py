#!/usr/bin/env python3
"""
Coleta e persiste métricas de organização do projeto
"""
import json
import argparse
import os
from datetime import datetime
import csv
import sqlite3
import subprocess

class MetricsCollector:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.metrics = {
            'timestamp': self.timestamp,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S')
        }
        
    def collect_git_metrics(self):
        """Coleta métricas do Git"""
        try:
            # Arquivos não rastreados
            result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], 
                                  capture_output=True, text=True)
            untracked_files = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            self.metrics['untracked_files'] = untracked_files
            
            # Branch atual
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True)
            self.metrics['branch'] = result.stdout.strip()
            
        except Exception as e:
            print(f"Erro ao coletar métricas Git: {e}")
            self.metrics['untracked_files'] = -1
            self.metrics['branch'] = 'unknown'
    
    def collect_disk_metrics(self):
        """Coleta métricas de disco"""
        try:
            # Tamanho total do projeto
            result = subprocess.run(['du', '-sb', '.'], capture_output=True, text=True)
            total_size = int(result.stdout.split()[0])
            self.metrics['project_size_bytes'] = total_size
            self.metrics['project_size_mb'] = round(total_size / 1024 / 1024, 2)
            
            # Espaço em arquivos temporários
            temp_size = 0
            temp_patterns = ['*.tmp', '*.temp', '*.cache', '*.log', '__pycache__']
            for pattern in temp_patterns:
                result = subprocess.run(['find', '.', '-name', pattern, '-type', 'f', '-exec', 'du', '-cb', '{}', '+'], 
                                      capture_output=True, text=True)
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    if lines and 'total' in lines[-1]:
                        temp_size += int(lines[-1].split()[0])
            
            self.metrics['temp_files_size_bytes'] = temp_size
            self.metrics['temp_files_size_mb'] = round(temp_size / 1024 / 1024, 2)
            
        except Exception as e:
            print(f"Erro ao coletar métricas de disco: {e}")
            self.metrics['project_size_bytes'] = -1
            self.metrics['temp_files_size_bytes'] = -1
    
    def parse_check_output(self, log_file='check_after.log'):
        """Analisa output do check_organization.sh"""
        try:
            with open(log_file, 'r') as f:
                content = f.read()
                
            # Extrair métricas do log
            metrics_map = {
                'Arquivos temporários encontrados': 'temp_files_count',
                'Arquivos grandes (>10MB)': 'large_files_count',
                'Diretórios vazios': 'empty_dirs_count',
                'Arquivos duplicados': 'duplicate_files_count'
            }
            
            for pattern, key in metrics_map.items():
                import re
                match = re.search(f'{pattern}:\s*(\d+)', content)
                if match:
                    self.metrics[key] = int(match.group(1))
                else:
                    self.metrics[key] = 0
                    
        except Exception as e:
            print(f"Erro ao analisar log: {e}")
    
    def save_metrics(self, score_before, score_after, organize_exit_code):
        """Salva métricas em múltiplos formatos"""
        self.metrics['score_before'] = score_before
        self.metrics['score_after'] = score_after
        self.metrics['score_improvement'] = score_after - score_before
        self.metrics['organize_exit_code'] = organize_exit_code
        self.metrics['organize_success'] = organize_exit_code == 0
        
        # Coletar outras métricas
        self.collect_git_metrics()
        self.collect_disk_metrics()
        self.parse_check_output()
        
        # Criar diretório de dados
        os.makedirs('data/metrics', exist_ok=True)
        
        # 1. Salvar em JSON (append-only)
        self.save_json()
        
        # 2. Salvar em CSV
        self.save_csv()
        
        # 3. Salvar em SQLite
        self.save_sqlite()
        
        # 4. Salvar última execução
        with open('data/metrics/latest.json', 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def save_json(self):
        """Salva em formato JSON append-only"""
        json_file = 'data/metrics/history.jsonl'
        with open(json_file, 'a') as f:
            f.write(json.dumps(self.metrics) + '\n')
    
    def save_csv(self):
        """Salva em formato CSV"""
        csv_file = 'data/metrics/history.csv'
        file_exists = os.path.exists(csv_file)
        
        with open(csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.metrics.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(self.metrics)
    
    def save_sqlite(self):
        """Salva em banco SQLite"""
        db_file = 'data/metrics/metrics.db'
        conn = sqlite3.connect(db_file)
        
        # Criar tabela se não existir
        conn.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                date TEXT,
                time TEXT,
                branch TEXT,
                score_before INTEGER,
                score_after INTEGER,
                score_improvement INTEGER,
                organize_exit_code INTEGER,
                organize_success BOOLEAN,
                temp_files_count INTEGER,
                temp_files_size_mb REAL,
                large_files_count INTEGER,
                empty_dirs_count INTEGER,
                duplicate_files_count INTEGER,
                untracked_files INTEGER,
                project_size_mb REAL
            )
        ''')
        
        # Inserir dados
        conn.execute('''
            INSERT INTO metrics (
                timestamp, date, time, branch, score_before, score_after,
                score_improvement, organize_exit_code, organize_success,
                temp_files_count, temp_files_size_mb, large_files_count,
                empty_dirs_count, duplicate_files_count, untracked_files,
                project_size_mb
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.metrics.get('timestamp'),
            self.metrics.get('date'),
            self.metrics.get('time'),
            self.metrics.get('branch', 'main'),
            self.metrics.get('score_before', 0),
            self.metrics.get('score_after', 0),
            self.metrics.get('score_improvement', 0),
            self.metrics.get('organize_exit_code', -1),
            self.metrics.get('organize_success', False),
            self.metrics.get('temp_files_count', 0),
            self.metrics.get('temp_files_size_mb', 0),
            self.metrics.get('large_files_count', 0),
            self.metrics.get('empty_dirs_count', 0),
            self.metrics.get('duplicate_files_count', 0),
            self.metrics.get('untracked_files', 0),
            self.metrics.get('project_size_mb', 0)
        ))
        
        conn.commit()
        conn.close()

def main():
    parser = argparse.ArgumentParser(description='Coleta métricas de organização')
    parser.add_argument('--score-before', type=int, required=True)
    parser.add_argument('--score-after', type=int, required=True)
    parser.add_argument('--organize-exit-code', type=int, required=True)
    
    args = parser.parse_args()
    
    collector = MetricsCollector()
    collector.save_metrics(args.score_before, args.score_after, args.organize_exit_code)
    
    print(f"✅ Métricas coletadas com sucesso!")
    print(f"   Score: {args.score_before} → {args.score_after} (+{args.score_after - args.score_before})")

if __name__ == '__main__':
    main()
