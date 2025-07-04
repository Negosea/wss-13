# criar-diagrama-wsf13.py
def criar_diagrama_wsf13():
    """Cria diagrama completo do WSF+13"""

    template = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="5.0" version="21.1.2">
  <diagram name="WSF+13 Framework" id="wsf13-complete">
    <mxGraphModel dx="1422" dy="754" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Título Principal -->
        <mxCell id="title" value="WSF+13 - Framework de Construção Civil" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=24;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="350" y="20" width="470" height="40" as="geometry" />
        </mxCell>
        
        <!-- Core do Framework -->
        <mxCell id="core" value="CORE WSF+13" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="480" y="200" width="200" height="80" as="geometry" />
        </mxCell>
        
        <!-- Módulo Planta -->
        <mxCell id="planta" value="Módulo Planta" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="200" y="120" width="140" height="60" as="geometry" />
        </mxCell>
        
        <!-- Módulo Orçamento -->
        <mxCell id="orcamento" value="Módulo Orçamento" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="200" y="220" width="140" height="60" as="geometry" />
        </mxCell>
        
        <!-- Módulo Cronograma -->
        <mxCell id="cronograma" value="Módulo Cronograma" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="200" y="320" width="140" height="60" as="geometry" />
        </mxCell>
        
        <!-- Módulo IA -->
        <mxCell id="ia" value="Módulo IA" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="820" y="120" width="140" height="60" as="geometry" />
        </mxCell>
        
        <!-- Módulo Relatórios -->
        <mxCell id="relatorios" value="Módulo Relatórios" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="820" y="220" width="140" height="60" as="geometry" />
        </mxCell>
        
        <!-- Módulo Integração -->
        <mxCell id="integracao" value="Módulo Integração" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="820" y="320" width="140" height="60" as="geometry" />
        </mxCell>
        
        <!-- Conexões -->
        <mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="planta" target="core">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="orcamento" target="core">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="edge3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="cronograma" target="core">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="edge4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="core" target="ia">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="edge5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="core" target="relatorios">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="edge6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="core" target="integracao">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <!-- Base de Dados -->
        <mxCell id="database" value="Base de Dados&#xa;WSF+13" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="520" y="400" width="120" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="edge7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="core" target="database">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
     
    with open('docs/diagramas/wsf13-completo.drawio', 'w') as f:
        f.write(template)
    print("✅ Diagrama WSF+13 completo criado!")

if __name__ == "__main__":
    criar_diagrama_wsf13()

