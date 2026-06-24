"""
exportar_atendimento_pdf.py
────────────────────────────────────────────────────────────────────────
Gera um PDF de uma única consulta do histórico do paciente, com os
campos estruturados do atendimento (queixa, observações, diagnóstico,
receita, exames). NÃO inclui anexos — só os dados de texto, conforme
decidido: o anexo fica disponível só pra visualização na tela, não é
empacotado junto no PDF exportado.

Usado pelo botão "Exportar PDF" no modal "Ver completo" da DoctorView.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Paleta baseada no tema azul/cyan do Clínica VIP
AZUL_PRINCIPAL = colors.HexColor("#0284C7")
AZUL_CLARO = colors.HexColor("#E0F2FE")
CINZA_TEXTO = colors.HexColor("#334155")
CINZA_CLARO = colors.HexColor("#64748B")

styles = getSampleStyleSheet()

estilo_titulo_clinica = ParagraphStyle(
    "TituloClinica", parent=styles["Title"],
    fontSize=18, textColor=AZUL_PRINCIPAL, alignment=TA_LEFT, spaceAfter=2,
)
estilo_subtitulo = ParagraphStyle(
    "Subtitulo", parent=styles["Normal"],
    fontSize=9, textColor=CINZA_CLARO, alignment=TA_LEFT,
)
estilo_secao = ParagraphStyle(
    "Secao", parent=styles["Heading2"],
    fontSize=11, textColor=AZUL_PRINCIPAL, spaceBefore=14, spaceAfter=4,
)
estilo_corpo = ParagraphStyle(
    "Corpo", parent=styles["Normal"],
    fontSize=10.5, textColor=CINZA_TEXTO, leading=15,
)
estilo_corpo_vazio = ParagraphStyle(
    "CorpoVazio", parent=estilo_corpo, textColor=CINZA_CLARO, fontName="Helvetica-Oblique",
)


def exportar_atendimento_pdf(registro: dict, paciente: dict, caminho_saida: str):
    """Gera um PDF de uma única consulta do histórico, com os campos
    estruturados (queixa, observações, diagnóstico, receita, exames).
    NÃO inclui anexos — só os dados de texto da consulta, como decidido.
    """
    doc = SimpleDocTemplate(
        caminho_saida, pagesize=A4,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )
    story = []

    # ── Cabeçalho da clínica ────────────────────────────────────────────
    story.append(Paragraph("Clínica VIP", estilo_titulo_clinica))
    story.append(Paragraph("Registro de Atendimento Médico", estilo_subtitulo))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.2, color=AZUL_PRINCIPAL))
    story.append(Spacer(1, 14))

    # ── Dados do paciente e da consulta (tabela de cabeçalho) ──────────
    dados_tabela = [
        ["Paciente:", paciente.get("nome", "—"), "Data:", registro.get("data", "—")],
        ["CPF:", paciente.get("cpf", "—"), "Médico:", registro.get("medico", "—")],
    ]
    tabela = Table(dados_tabela, colWidths=[28 * mm, 65 * mm, 22 * mm, 55 * mm])
    tabela.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), CINZA_TEXTO),
        ("BACKGROUND", (0, 0), (-1, -1), AZUL_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.5, AZUL_PRINCIPAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(tabela)
    story.append(Spacer(1, 8))

    # ── Seções de conteúdo clínico ──────────────────────────────────────
    secoes = [
        ("Queixa", registro.get("queixa", "")),
        ("Observações", registro.get("observacoes", "")),
        ("Diagnóstico", registro.get("diagnostico", "")),
        ("Receita", registro.get("receita", "")),
        ("Exames solicitados", registro.get("exames", "")),
    ]

    for titulo, texto in secoes:
        story.append(Paragraph(titulo, estilo_secao))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1")))
        story.append(Spacer(1, 4))
        if texto and texto.strip():
            story.append(Paragraph(texto.replace("\n", "<br/>"), estilo_corpo))
        else:
            story.append(Paragraph("Não informado.", estilo_corpo_vazio))
        story.append(Spacer(1, 4))

    # ── Rodapé ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Documento gerado pelo sistema Clínica VIP. Este registro não substitui "
        "o prontuário oficial arquivado no sistema.",
        ParagraphStyle("Rodape", parent=estilo_corpo, fontSize=8, textColor=CINZA_CLARO),
    ))

    doc.build(story)