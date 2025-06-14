#!/bin/bash
# check_organization.sh - Verifica o estado de organização do projeto

echo "🔍 Analisando organização do Framework de Construção Civil..."
echo "=================================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Função para calcular tamanho de diretório
get_size() {
    du -sh "$1" 2>/dev/null | cut -f1
}

# 1. Estrutura de Diretórios
echo -e "${BLUE}📁 ESTRUTURA DE DIRETÓRIOS${NC}"
echo "------------------------"
for dir in src tests docs scripts config dados logs modelos relatorios; do
    if [ -d "$dir" ]; then
        size=$(get_size "$dir")
        echo -e "${GREEN}✓${NC} $dir/ ($size)"
    else
        echo -e "${RED}✗${NC} $dir/ (não existe)"
    fi
done
echo ""

# 2. Estatísticas de Arquivos
echo -e "${BLUE}📊 ESTATÍSTICAS DE ARQUIVOS${NC}"
echo "-------------------------"
total_files=$(find . -type f -not -path "./.git/*" -not -path "./venv/*" 2>/dev/null | wc -l)
echo "Total de arquivos: $total_files"
echo ""
echo "Por tipo:"
find . -type f -not -path "./.git/*" -not -path "./venv/*" -name "*.*" 2>/dev/null | \
    sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10
echo ""

# 3. Arquivos Temporários
echo -e "${BLUE}🗑️  ARQUIVOS TEMPORÁRIOS${NC}"
echo "---------------------"
temp_count=$(find . -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*.bak" -o -name "*.swp" -o -name ".DS_Store" \) -not -path "./.git/*" 2>/dev/null | wc -l)
if [ $temp_count -gt 0 ]; then
    echo -e "${YELLOW}⚠${NC} Encontrados $temp_count arquivos temporários:"
    find . -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*.bak" -o -name "*.swp" -o -name ".DS_Store" \) -not -path "./.git/*" 2>/dev/null | head -5
    [ $temp_count -gt 5 ] && echo "... e mais $(($temp_count - 5)) arquivos"
else
    echo -e "${GREEN}✓${NC} Nenhum arquivo temporário encontrado"
fi
echo ""

# 4. Arquivos Grandes
echo -e "${BLUE}💾 ARQUIVOS GRANDES (>10MB)${NC}"
echo "-------------------------"
large_files=$(find . -type f -size +10M -not -path "./.git/*" -not -path "./venv/*" 2>/dev/null | wc -l)
if [ $large_files -gt 0 ]; then
    echo -e "${YELLOW}⚠${NC} Encontrados $large_files arquivos grandes:"
    find . -type f -size +10M -not -path "./.git/*" -not -path "./venv/*" -exec ls -lh {} \; 2>/dev/null | awk '{print $5 " " $9}' | head -5
else
    echo -e "${GREEN}✓${NC} Nenhum arquivo grande encontrado"
fi
echo ""

# 5. Duplicados Potenciais
echo -e "${BLUE}🔄 POSSÍVEIS DUPLICADOS${NC}"
echo "--------------------"
echo "Arquivos com nomes similares:"
find . -type f -not -path "./.git/*" -not -path "./venv/*" 2>/dev/null | \
    sed 's/.*\///' | sort | uniq -d | head -5
echo ""

# 6. Estado do Git
echo -e "${BLUE}🔀 ESTADO DO GIT${NC}"
echo "--------------"
if [ -d .git ]; then
    untracked=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l)
    modified=$(git diff --name-only 2>/dev/null | wc -l)
    echo "Arquivos não rastreados: $untracked"
    echo "Arquivos modificados: $modified"
    
    if [ $untracked -gt 10 ]; then
        echo -e "${YELLOW}⚠${NC} Muitos arquivos não rastreados!"
    fi
else
    echo -e "${RED}✗${NC} Repositório Git não encontrado"
fi
echo ""

# 7. Saúde do Projeto
echo -e "${BLUE}🏥 SAÚDE DO PROJETO${NC}"
echo "-----------------"
# Verificar arquivos essenciais
essential_files=("README.md" "requirements.txt" ".gitignore" "pipeline.sh")
missing=0
for file in "${essential_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file (faltando)"
        ((missing++))
    fi
done
echo ""

# 8. Score de Organização
echo -e "${BLUE}📈 SCORE DE ORGANIZAÇÃO${NC}"
echo "--------------------"
score=100
[ $temp_count -gt 0 ] && score=$((score - 10))
[ $large_files -gt 5 ] && score=$((score - 10))
[ $untracked -gt 10 ] && score=$((score - 15))
[ $missing -gt 0 ] && score=$((score - 5 * missing))

if [ $score -ge 80 ]; then
    echo -e "${GREEN}Score: $score/100 - Excelente!${NC}"
elif [ $score -ge 60 ]; then
    echo -e "${YELLOW}Score: $score/100 - Bom, mas pode melhorar${NC}"
else
    echo -e "${RED}Score: $score/100 - Precisa de atenção${NC}"
fi
echo ""

# 9. Recomendações
echo -e "${BLUE}📋 RECOMENDAÇÕES${NC}"
echo "---------------"
if [ $temp_count -gt 0 ]; then
    echo "• Execute './organize.sh' para limpar arquivos temporários"
fi
if [ $large_files -gt 0 ]; then
    echo "• Considere mover arquivos grandes para Git LFS ou storage externo"
fi
if [ $untracked -gt 10 ]; then
    echo "• Revise arquivos não rastreados no Git"
fi
if [ $missing -gt 0 ]; then
    echo "• Crie os arquivos essenciais que estão faltando"
fi
if [ $score -ge 80 ]; then
    echo "• Projeto bem organizado! Continue assim 🎉"
fi

echo ""
echo "=================================================="
echo "Análise completa! Use './organize.sh' para organizar automaticamente."
