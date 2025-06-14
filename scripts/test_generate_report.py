import os
import json
import sqlite3
import pytest
from unittest import mock
from scripts.generate_report import ReportGenerator

@pytest.fixture
def report_gen(tmp_path, monkeypatch):
    # Setup temp report dir
    monkeypatch.setattr('os.makedirs', lambda *a, **kw: None)
    rg = ReportGenerator()
    rg.report_dir = tmp_path / "reports"
    return rg

def test_load_latest_metrics_success(tmp_path, report_gen, monkeypatch):
    metrics_path = tmp_path / "latest.json"
    data = {"score_after": 90}
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(data))
    monkeypatch.setattr('builtins.open', lambda f, mode='r': open(metrics_path, mode) if 'latest.json' in f else open(f, mode))
    monkeypatch.chdir(tmp_path)
    os.makedirs("data/metrics", exist_ok=True)
    with open("data/metrics/latest.json", "w") as f:
        json.dump(data, f)
    assert report_gen.load_latest_metrics() == data

def test_load_latest_metrics_missing(report_gen, monkeypatch):
    monkeypatch.setattr('builtins.open', mock.mock_open(side_effect=FileNotFoundError))
    assert report_gen.load_latest_metrics() == {}

def test_load_check_log_success(tmp_path, report_gen):
    log_path = tmp_path / "check_after.log"
    log_content = "log content"
    log_path.write_text(log_content)
    assert report_gen.load_check_log(str(log_path)) == log_content

def test_load_check_log_missing(report_gen):
    assert report_gen.load_check_log("nonexistent.log") == "Log não disponível"

def test_load_history_success(tmp_path, report_gen):
    db_path = tmp_path / "metrics.db"
    os.makedirs(tmp_path, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE metrics (
        timestamp TEXT, score_before INTEGER, score_after INTEGER, score_improvement INTEGER,
        temp_files_count INTEGER, project_size_mb REAL, untracked_files INTEGER
    )''')
    conn.execute('''INSERT INTO metrics VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 ("2024-01-01 12:00:00", 60, 80, 20, 2, 1.5, 3))
    conn.commit()
    conn.close()
    # Patch connect to use our db
    with mock.patch('sqlite3.connect', return_value=sqlite3.connect(db_path)):
        history = report_gen.load_history(limit=1)
        assert len(history) == 1
        assert history[0]['score_before'] == 60
        assert history[0]['score_after'] == 80

def test_load_history_missing(report_gen, monkeypatch):
    monkeypatch.setattr('sqlite3.connect', mock.Mock(side_effect=Exception))
    assert report_gen.load_history() == []

def test_extract_recommendations(report_gen):
    log = """
Some log
📋 RECOMENDAÇÕES
• Limpar arquivos temporários
• Remover diretórios vazios
========================
"""
    recs = report_gen.extract_recommendations(log)
    assert "• Limpar arquivos temporários" in recs
    assert "• Remover diretórios vazios" in recs

def test_extract_recommendations_none(report_gen):
    log = "No recommendations here"
    assert report_gen.extract_recommendations(log) == []

def test_generate_markdown_report_basic(report_gen, monkeypatch):
    monkeypatch.setattr(report_gen, 'load_latest_metrics', lambda: {
        'branch': 'main', 'score_after': 95, 'score_before': 90, 'score_improvement': 5,
        'temp_files_count': 0, 'temp_files_size_mb': 0, 'large_files_count': 0,
        'empty_dirs_count': 0, 'untracked_files': 0, 'project_size_mb': 1
    })
    monkeypatch.setattr(report_gen, 'load_check_log', lambda: "📋 RECOMENDAÇÕES\n• Teste\n====")
    monkeypatch.setattr(report_gen, 'load_history', lambda: [])
    monkeypatch.setattr(report_gen, 'extract_recommendations', lambda log: ["• Teste"])
    md = report_gen.generate_markdown_report()
    assert "# 📊 Relatório de Organização do Projeto" in md
    assert "✅ **EXCELENTE**" in md
    assert "• Teste" in md
    assert "Clique para ver o output completo da análise" in md