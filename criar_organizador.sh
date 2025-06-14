#!/bin/bash
# criar_organizador.sh - Script completo para criar o Framework Organizer

echo "🚀 Criando Framework Organizer completo..."

# 1. Criar estrutura de diretórios
echo "📁 Criando estrutura de diretórios..."
mkdir -p scripts/organizer
mkdir -p config
mkdir -p dados/processed_archive
mkdir -p dados/raw_archive
mkdir -p logs/organizer

# 2. Criar o script Python principal
echo "📝 Criando framework_organizer.py..."
cat > scripts/organizer/framework_organizer.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Framework Organizer - Sistema Profissional de Organização e Manutenção
Autor: Framework Construção Civil
Versão: 1.0.0
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class OrganizationStats:
    """Estatísticas da organização"""
    files_cleaned: int = 0
    files_archived: int = 0
    duplicates_removed: int = 0
    space_freed: int = 0
    errors: List[str] = field(default_factory=list)
    
class FrameworkOrganizer:
    def __init__(self, config_path: str = "config/organizer_config.json", dry_run: bool = False):
        self.project_root = Path.cwd()
        self.config = self._load_config(config_path)
        self.dry_run = dry_run
        self.stats = OrganizationStats()
        self._setup_logging()
        
    def _load_config(self, config_path: str) -> dict:
        """Carrega configuração ou usa padrões"""
        default_config = {
            "temp_patterns": ["*.tmp", "*.temp", "*.cache", "*.pyc", ".DS_Store"],
            "temp_dirs": ["__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"],
            "archive_after_days": 30,
            "log_retention_days": 90,
            "excluded_dirs": [".git", "venv", "__pycache__"],
            "duplicate_check_extensions": [".py", ".json", ".txt", ".md"],
            "min_file_size_for_dup_check": 100
        }
        
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _setup_logging(self):
        """Configura sistema de logging"""
        log_dir = self.project_root / "logs" / "organizer"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def clean_temp_files(self):
        """Remove arquivos temporários e cache"""
        self.logger.info("🧹 Iniciando limpeza de arquivos temporários...")
        
        for root, dirs, files in os.walk(self.project_root):
            # Pular diretórios excluídos
            dirs[:] = [d for d in dirs if d not in self.config['excluded_dirs']]
            
            # Remover arquivos temporários
            for file in files:
                for pattern in self.config['temp_patterns']:
                    if Path(file).match(pattern):
                        file_path = Path(root) / file
                        self._remove_file(file_path)
            
            # Remover diretórios temporários
            for dir_name in dirs:
                if dir_name in self.config['temp_dirs']:
                    dir_path = Path(root) / dir_name
                    self._remove_directory(dir_path)
    
    def archive_old_files(self):
        """Arquiva arquivos antigos"""
        self.logger.info("📦 Arquivando arquivos antigos...")
        
        cutoff_date = datetime.now() - timedelta(days=self.config['archive_after_days'])
        archive_dirs = {
            'dados/raw': self.project_root / 'dados/raw_archive',
            'dados/processed': self.project_root / 'dados/processed_archive'
        }
        
        for source_dir, archive_dir in archive_dirs.items():
            source_path = self.project_root / source_dir
            if not source_path.exists():
                continue
                
            for file_path in source_path.rglob('*'):
                if file_path.is_file():
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mod_time < cutoff_date:
                        self._archive_file(file_path, archive_dir)
    
    def remove_duplicates(self):
        """Remove arquivos duplicados"""
        self.logger.info("🔍 Procurando arquivos duplicados...")
        
        file_hashes = defaultdict(list)
        
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in self.config['excluded_dirs']]
            
            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                
                if ext in self.config['duplicate_check_extensions']:
                    if file_path.stat().st_size >= self.config['min_file_size_for_dup_check']:
                        file_hash = self._calculate_hash(file_path)
                        if file_hash:
                            file_hashes[file_hash].append(file_path)
        
        # Remover duplicados (mantém o mais antigo)
        for file_hash, file_list in file_hashes.items():
            if len(file_list) > 1:
                file_list.sort(key=lambda x: x.stat().st_mtime)
                for duplicate in file_list[1:]:
                    self._remove_file(duplicate, is_duplicate=True)
    
    def manage_logs(self):
        """Gerencia rotação de logs"""
        self.logger.info("📋 Gerenciando logs...")
        
        log_dir = self.project_root / "logs"
        if not log_dir.exists():
            return
            
        cutoff_date = datetime.now() - timedelta(days=self.config['log_retention_days'])
        
        for log_file in log_dir.rglob('*.log'):
            mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mod_time < cutoff_date:
                self._remove_file(log_file)
    
    def _calculate_hash(self, file_path: Path) -> Optional[str]:
        """Calcula hash MD5 do arquivo"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Erro ao calcular hash de {file_path}: {e}")
            return None
    
    def _remove_file(self, file_path: Path, is_duplicate: bool = False):
        """Remove arquivo com logging"""
        try:
            size = file_path.stat().st_size
            if self.dry_run:
                self.logger.info(f"[DRY-RUN] Removeria: {file_path}")
            else:
                file_path.unlink()
                self.logger.info(f"✅ Removido: {file_path}")
            
            self.stats.space_freed += size
            if is_duplicate:
                self.stats.duplicates_removed += 1
            else:
                self.stats.files_cleaned += 1
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao remover {file_path}: {e}")
            self.stats.errors.append(str(e))
    
    def _remove_directory(self, dir_path: Path):
        """Remove diretório com logging"""
        try:
            if self.dry_run:
                self.logger.info(f"[DRY-RUN] Removeria diretório: {dir_path}")
            else:
                shutil.rmtree(dir_path)
                self.logger.info(f"✅ Diretório removido: {dir_path}")
            
            self.stats.files_cleaned += 1
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao remover diretório {dir_path}: {e}")
            self.stats.errors.append(str(e))
    
    def _archive_file(self, source: Path, archive_base: Path):
        """Arquiva arquivo mantendo estrutura"""
        try:
            relative_path = source.relative_to(self.project_root)
            archive_path = archive_base / relative_path
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            
            if self.dry_run:
                self.logger.info(f"[DRY-RUN] Arquivaria: {source} -> {archive_path}")
            else:
                shutil.move(str(source), str(archive_path))
                self.logger.info(f"📦 Arquivado: {source} -> {archive_path}")
            
            self.stats.files_archived += 1
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao arquivar {source}: {e}")
            self.stats.errors.append(str(e))
    
    def generate_report(self) -> str:
        """Gera relatório final"""
        report = f"""
# 📊 Relatório de Organização - Framework Construção

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Modo:** {'Simulação (Dry-Run)' if self.dry_run else 'Execução Real'}

## 📈 Estatísticas

- 🧹 **Arquivos limpos:** {self.stats.files_cleaned}
- 📦 **Arquivos arquivados:** {self.stats.files_archived}
- 🔍 **Duplicados removidos:** {self.stats.duplicates_removed}
- 💾 **Espaço liberado:** {self._format_bytes(self.stats.space_freed)}
- ❌ **Erros encontrados:** {len(self.stats.errors)}

## 🎯 Ações Realizadas

1. ✅ Limpeza de arquivos temporários
2. ✅ Arquivamento de arquivos antigos
3. ✅ Remoção de duplicados
4. ✅ Gerenciamento de logs

"""
        if self.stats.errors:
            report += "\n## ⚠️ Erros Encontrados\n\n"
            for error in self.stats.errors:
                report += f"- {error}\n"
        
        return report
    
    def _format_bytes(self, bytes: int) -> str:
        """Formata bytes para formato legível"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"
    
    def run(self):
        """Executa todas as tarefas de organização"""
        self.logger.info("🚀 Iniciando organização do Framework Construção...")
        
        if self.dry_run:
            self.logger.info("⚠️  Modo DRY-RUN ativado - nenhuma alteração será feita")
        
        # Executar tarefas
        self.clean_temp_files()
        self.archive_old_files()
        self.remove_duplicates()
        self.manage_logs()
        
        # Gerar e salvar relatório
        report = self.generate_report()
        
        report_path = self.project_root / "logs" / "organizer" / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print("\n" + report)
        self.logger.info(f"📄 Relatório salvo em: {report_path}")

def main():
    parser = argparse.ArgumentParser(description='Framework Organizer - Organização e Manutenção')
    parser.add_argument('--config', default='config/organizer_config.json', help='Caminho para arquivo de configuração')
    parser.add_argument('--dry-run', action='store_true', help='Simula execução sem fazer alterações')
    parser.add_argument('--verbose', action='store_true', help='Saída detalhada')
    
    args = parser.parse_args()
    
    try:
        organizer = FrameworkOrganizer(
            config_path=args.config,
            dry_run=args.dry_run
        )
        
        if args.verbose:
            organizer.logger.setLevel(logging.DEBUG)
        
        organizer.run()
        
    except KeyboardInterrupt:
        print("\n\nOrganização interrompida pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
PYTHON_EOF

# 3. Criar arquivo de configuração
echo "⚙️  Criando arquivo de configuração..."
cat > config/organizer_config.json << 'JSON_EOF'
{
    "temp_patterns": [
        "*.tmp",
        "*.temp",
        "*.cache",
        "*.pyc",
        ".DS_Store",
        "Thumbs.db",
        "*.swp",
        "*.swo",
        "*~"
    ],
    "temp_dirs": [
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "node_modules",
        ".coverage",
        "htmlcov",
        ".tox"
    ],
    "archive_after_days": 30,
    "log_retention_days": 90,
    "excluded_dirs": [
        ".git",
        "venv",
        "__pycache__",
        ".vscode",
        ".idea"
    ],
    "duplicate_check_extensions": [
        ".py",
        ".json",
        ".txt",
        ".md",
        ".csv",
        ".log"
    ],
    "min_file_size_for_dup_check": 100
}
JSON_EOF

# 4. Criar script de execução
echo "🔧 Criando script de execução..."
cat > organize.sh << 'BASH_EOF'
#!/bin/bash
# organize.sh - Script para executar o Framework Organizer

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Executar organizador
python3 scripts/organizer/framework_organizer.py "$@"
BASH_EOF

# 5. Tornar scripts executáveis
chmod +x scripts/organizer/framework_organizer.py
chmod +x organize.sh

# 6. Criar script de integração com pipeline
echo "🔗 Criando integração com pipeline..."
cat > integrate_with_pipeline.sh << 'INTEGRATE_EOF'
#!/bin/bash
# integrate_with_pipeline.sh - Adiciona organizador ao pipeline

# Fazer backup do pipeline.sh
if [ -f "pipeline.sh" ]; then
    cp pipeline.sh pipeline.sh.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup do pipeline.sh criado"
fi

# Adicionar organização ao início do pipeline
if [ -f "pipeline.sh" ]; then
    # Criar novo pipeline com organização
    cat > pipeline_temp.sh << 'EOF'
#!/bin/bash
# Pipeline com Framework Organizer integrado

echo "🧹 Organizando projeto antes do processamento..."
./organize.sh

# Continuar com o pipeline original
EOF
    
    # Adicionar conteúdo original do pipeline (pulando shebang)
    tail -n +2 pipeline.sh >> pipeline_temp.sh
    
    # Substituir pipeline
    mv pipeline_temp.sh pipeline.sh
    chmod +x pipeline.sh
    
    echo "✅ Organizador integrado ao pipeline.sh"
else
    echo "⚠️  pipeline.sh não encontrado"
fi
INTEGRATE_EOF

chmod +x integrate_with_pipeline.sh

echo "✅ Framework Organizer instalado com sucesso!"
echo ""
echo "📚 Como usar:"
echo "  ./organize.sh              # Executar organização"
echo "  ./organize.sh --dry-run    # Simular sem alterações"
echo "  ./organize.sh --verbose    # Modo detalhado"
echo ""
echo "🔗 Para integrar ao pipeline:"
echo "  ./integrate_with_pipeline.sh"
echo ""
echo "📊 Logs e relatórios serão salvos em: logs/organizer/"