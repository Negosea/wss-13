# Diagramas WSF+13

## 1. Fluxo Principal (fluxo-principal.drawio)
- Upload → OCR → IA → Relatório

## 2. Arquitetura do Sistema (arquitetura.drawio)
- Frontend (React/Vue)
- Backend (FastAPI)
- AI Engine (GPT-4/Claude)
- Database (PostgreSQL)
- Cache (Redis)

## 3. Fluxo de Dados (data-flow.drawio)
- Entrada: PDF/DWG
- Processamento: OCR + IA
- Saída: JSON/Excel/PDF

## 4. Diagrama de Classes (classes.drawio)
- PlantProcessor
- AIAnalyzer
- ReportGenerator
- DatabaseManager

## 5. Sequência de Processamento (sequence.drawio)
- User → Upload → Process → Analyze → Store → Report

## 6. Infraestrutura (infra.drawio)
- Docker containers
- Load balancer
- Auto-scaling
- Backup strategy
