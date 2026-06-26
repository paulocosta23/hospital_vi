"""
exportar_relatorio_pdf.py
────────────────────────────────────────────────────────────────────────
Gera um PDF do relatório de consultas: resumo numérico (total, convênio,
particular), os 3 gráficos (pizza, barras por médico, linha por dia) e o
detalhamento por médico/plano.

As figuras matplotlib são recebidas já prontas (mpl.figure.Figure) e
inseridas no PDF via buffer de memória — não depende de arquivos
temporários no disco nem de nenhuma lógica de banco.

Usado pelo botão "Exportar PDF" da ReportsView.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Mesma paleta usada em exportar_atendimento_pdf.py, para manter
# consistência visual entre os PDFs gerados pelo sistema.
AZUL_PRINCIPAL = colors.HexColor("#0284C7")
AZUL_CLARO = colors.HexColor("#E0F2FE")
CINZA_TEXTO = colors.HexColor("#334155")
CINZA_CLARO = colors.HexColor("#64748B")
VERDE = colors.HexColor("#16A34A")
LARANJA = colors.HexColor("#D97706")

styles = getSampleStyleSheet()

estilo_titulo = ParagraphStyle(
    "TituloClinica", parent=styles["Title"],
    fontSize=18, textColor=AZUL_PRINCIPAL, alignment=0, spaceAfter=2,
)
estilo_subtitulo = ParagraphStyle(
    "Subtitulo", parent=styles["Normal"],
    fontSize=9, textColor=CINZA_CLARO, alignment=0,
)
estilo_secao = ParagraphStyle(
    "Secao", parent=styles["Heading2"],
    fontSize=12, textColor=AZUL_PRINCIPAL, spaceBefore=14, spaceAfter=6,
)
estilo_corpo = ParagraphStyle(
    "Corpo", parent=styles["Normal"],
    fontSize=10, textColor=CINZA_TEXTO, leading=14,
)


def _figura_para_imagem(fig, largura_mm):
    """Converte uma Figure do matplotlib num Image do reportlab, via
    buffer de memória (sem arquivo temporário no disco). Mantém a
    proporção original da figura ao redimensionar para a largura dada.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)

    largura_pt = largura_mm * mm
    proporcao = fig.get_figheight() / fig.get_figwidth()
    altura_pt = largura_pt * proporcao

    return Image(buf, width=largura_pt, height=altura_pt)


def exportar_relatorio_pdf(
    caminho_saida: str,
    periodo_label: str,
    total: int,
    convenio: int,
    particular: int,
    medicos: dict,
    fig_pizza=None,
    fig_barras=None,
    fig_linha=None,
):
    """Gera o PDF do relatório.

    periodo_label: texto do filtro ativo (ex: "Último mês", "Personalizado
        (01/06/2026 a 26/06/2026)") — exibido no cabeçalho do PDF.
    medicos: dict no mesmo formato usado pela ReportsView, ex:
        {"Dr. Carlos": {"Unimed": 18, "Particular": 12}, ...}
    fig_pizza / fig_barras / fig_linha: Figures do matplotlib já
        prontas (mpl.figure.Figure), ou None para omitir aquele gráfico
        do PDF.
    """
    doc = SimpleDocTemplate(
        caminho_saida, pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )
    story = []

    # ── Cabeçalho ────────────────────────────────────────────────────────
    story.append(Paragraph("Clínica VIP", estilo_titulo))
    story.append(Paragraph(f"Relatório de Consultas — {periodo_label}", estilo_subtitulo))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.2, color=AZUL_PRINCIPAL))
    story.append(Spacer(1, 12))

    # ── Cards de resumo (tabela com 3 colunas) ──────────────────────────────
    tabela_resumo = Table(
        [["Total de consultas", "Convênio", "Particular"], [str(total), str(convenio), str(particular)]],
        colWidths=[55 * mm, 55 * mm, 55 * mm],
    )
    tabela_resumo.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, 1), 18),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, 1), (0, 1), AZUL_PRINCIPAL),
        ("TEXTCOLOR", (1, 1), (1, 1), VERDE),
        ("TEXTCOLOR", (2, 1), (2, 1), LARANJA),
        ("BACKGROUND", (0, 0), (0, -1), AZUL_PRINCIPAL),
        ("BACKGROUND", (1, 0), (1, -1), VERDE),
        ("BACKGROUND", (2, 0), (2, -1), LARANJA),
        ("BACKGROUND", (0, 1), (-1, 1), AZUL_CLARO),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 1), (-1, 1), 10),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.white),
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.white),
    ]))
    story.append(tabela_resumo)
    story.append(Spacer(1, 16))

    # ── Gráficos ──────────────────────────────────────────────────────────────
    if fig_pizza is not None:
        story.append(Paragraph("Convênio vs Particular", estilo_secao))
        story.append(_figura_para_imagem(fig_pizza, largura_mm=80))
        story.append(Spacer(1, 8))

    if fig_barras is not None:
        story.append(Paragraph("Consultas por médico", estilo_secao))
        story.append(_figura_para_imagem(fig_barras, largura_mm=160))
        story.append(Spacer(1, 8))

    if fig_linha is not None:
        story.append(Paragraph("Consultas por dia no período", estilo_secao))
        story.append(_figura_para_imagem(fig_linha, largura_mm=170))
        story.append(Spacer(1, 8))

    # ── Detalhamento por médico ────────────────────────────────────────────────
    story.append(Paragraph("Detalhamento por médico", estilo_secao))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1")))
    story.append(Spacer(1, 6))

    for medico, planos in medicos.items():
        linhas = [[medico, ""]]
        for plano, qtd in planos.items():
            linhas.append([plano, str(qtd)])

        tabela_medico = Table(linhas, colWidths=[120 * mm, 30 * mm])
        tabela_medico.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 0), (-1, 0), AZUL_PRINCIPAL),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9.5),
            ("TEXTCOLOR", (0, 1), (0, -1), CINZA_TEXTO),
            ("TEXTCOLOR", (1, 1), (1, -1), AZUL_PRINCIPAL),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 1), (-1, -2), 0.4, colors.HexColor("#E2E8F0")),
        ]))
        story.append(tabela_medico)
        story.append(Spacer(1, 10))

    # ── Rodapé ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Relatório gerado automaticamente pelo sistema Clínica VIP.",
        ParagraphStyle("Rodape", parent=estilo_corpo, fontSize=8, textColor=CINZA_CLARO),
    ))

    doc.build(story)