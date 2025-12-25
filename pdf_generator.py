import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

import matplotlib.pyplot as plt
import io
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import NOMINATIONS
from database import (
    get_votes_by_nomination,
    get_votes_count_by_nomination,
    get_total_voters,
    get_all_votes,
)

# O'zbek tilini qo'llab-quvvatlash uchun font
plt.rcParams['font.family'] = 'DejaVu Sans'

def create_pie_chart(nomination_key: str, nomination: dict, votes: list, total: int) -> bytes:
    """Pie chart yaratish"""
    if not votes or total == 0:
        # Bo'sh diagramma
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'Ovozlar yo\'q', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        votes_dict = {v['candidate_id']: v['vote_count'] for v in votes}
        
        labels = []
        sizes = []
        
        for candidate in nomination['candidates']:
            vote_count = votes_dict.get(candidate['id'], 0)
            if vote_count > 0:
                # Ismni qisqartirish
                name_parts = candidate['name'].split()
                short_name = f"{name_parts[0]} {name_parts[1][0]}." if len(name_parts) > 1 else name_parts[0]
                labels.append(f"{short_name}\n({vote_count} - {vote_count/total*100:.1f}%)")
                sizes.append(vote_count)
        
        if not sizes:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'Ovozlar yo\'q', ha='center', va='center', fontsize=16)
            ax.axis('off')
        else:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Ranglar
            colors_list = plt.cm.Set3(range(len(sizes)))
            
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels,
                autopct='',
                colors=colors_list,
                explode=[0.02] * len(sizes),
                shadow=True,
                startangle=90
            )
            
            # Matn stilini sozlash
            for text in texts:
                text.set_fontsize(9)
            
            ax.set_title(nomination['title'][:50] + "..." if len(nomination['title']) > 50 else nomination['title'], 
                        fontsize=12, fontweight='bold', pad=20)
    
    # Rasmni bytes ga o'tkazish
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()

def create_bar_chart(nomination_key: str, nomination: dict, votes: list, total: int) -> bytes:
    """Bar chart yaratish"""
    votes_dict = {v['candidate_id']: v['vote_count'] for v in votes}
    
    names = []
    vote_counts = []
    
    for candidate in nomination['candidates']:
        # Ismni qisqartirish
        name_parts = candidate['name'].split()
        short_name = f"{name_parts[0]} {name_parts[1][0] if len(name_parts) > 1 else ''}"
        names.append(short_name)
        vote_counts.append(votes_dict.get(candidate['id'], 0))
    
    fig, ax = plt.subplots(figsize=(12, max(6, len(names) * 0.5)))
    
    # Ranglar - ovoz soniga qarab
    max_votes = max(vote_counts) if vote_counts else 1
    colors_list = [plt.cm.YlGn(0.3 + 0.7 * (v / max_votes)) if max_votes > 0 else plt.cm.YlGn(0.3) for v in vote_counts]
    
    y_pos = range(len(names))
    bars = ax.barh(y_pos, vote_counts, color=colors_list, edgecolor='darkgreen', linewidth=0.5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('Ovozlar soni', fontsize=10)
    ax.set_title(nomination['title'][:60] + "..." if len(nomination['title']) > 60 else nomination['title'],
                fontsize=11, fontweight='bold', pad=15)
    
    # Ovoz sonini bar ustiga yozish
    for bar, count in zip(bars, vote_counts):
        width = bar.get_width()
        percentage = (count / total * 100) if total > 0 else 0
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2,
               f'{count} ({percentage:.1f}%)',
               ha='left', va='center', fontsize=8)
    
    ax.set_xlim(0, max(vote_counts) * 1.3 if vote_counts and max(vote_counts) > 0 else 10)
    ax.grid(axis='x', alpha=0.3)
    
    # Rasmni bytes ga o'tkazish
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()

async def generate_results_pdf() -> str:
    """PDF hisobot yaratish"""
    
    # PDF fayl nomi
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"tanlov_natijalari_{timestamp}.pdf"
    
    # PDF yaratish - Landscape (gorizontal) formatda
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=landscape(A4),
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    # Stillar
    styles = getSampleStyleSheet()
    
    # Custom stillar
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=colors.HexColor('#1a5f7a')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=15,
        textColor=colors.HexColor('#2e8b57')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12
    )
    
    # Jadval katakchasi uchun stil (matn o'rashi bilan)
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        wordWrap='LTR'
    )
    
    cell_style_header = ParagraphStyle(
        'CellStyleHeader',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.whitesmoke,
        fontName='Helvetica-Bold'
    )
    
    # Hujjat elementlari
    elements = []
    
    # Sarlavha
    elements.append(Paragraph("KO'PRIKQURILISH AJ", title_style))
    elements.append(Paragraph("TANLOV NATIJALARI", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Sana va umumiy statistika
    total_voters = await get_total_voters()
    current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    info_data = [
        ["Hisobot sanasi:", current_date],
        ["Jami ovoz berganlar:", str(total_voters)],
        ["Nominatsiyalar soni:", str(len(NOMINATIONS))]
    ]
    
    info_table = Table(info_data, colWidths=[3*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Har bir nominatsiya uchun
    for nom_key, nomination in NOMINATIONS.items():
        # Nominatsiya sarlavhasi
        elements.append(Paragraph(nomination['title'], subtitle_style))
        
        # Ovozlarni olish
        votes = await get_votes_by_nomination(nom_key)
        total = await get_votes_count_by_nomination(nom_key)
        
        votes_dict = {v['candidate_id']: v['vote_count'] for v in votes}
        
        # Jadval ma'lumotlari - header Paragraph bilan
        table_data = [[
            Paragraph("#", cell_style_header),
            Paragraph("Nomzod", cell_style_header),
            Paragraph("Lavozim", cell_style_header),
            Paragraph("Ovozlar", cell_style_header),
            Paragraph("%", cell_style_header)
        ]]
        
        # Nomzodlarni ovoz soniga qarab tartiblash
        sorted_candidates = sorted(
            nomination['candidates'],
            key=lambda x: votes_dict.get(x['id'], 0),
            reverse=True
        )
        
        for i, candidate in enumerate(sorted_candidates, 1):
            vote_count = votes_dict.get(candidate['id'], 0)
            percentage = f"{vote_count/total*100:.1f}%" if total > 0 else "0%"
            
            # To'liq ism va lavozim - Paragraph bilan o'rash
            name = candidate['name']
            position = candidate['position']
            
            table_data.append([
                Paragraph(str(i), cell_style),
                Paragraph(name, cell_style),
                Paragraph(position, cell_style),
                Paragraph(str(vote_count), cell_style),
                Paragraph(percentage, cell_style)
            ])
        
        # Jadval - kengaytirilgan
        col_widths = [0.4*inch, 2.8*inch, 3.5*inch, 0.7*inch, 0.7*inch]
        table = Table(table_data, colWidths=col_widths)
        
        # Jadval stili - Paragraph ishlatganda VALIGN muhim
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5f7a')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (2, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ])
        
        # G'olib qatorini ajratish
        if votes:
            table_style.add('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e8f5e9'))
            table_style.add('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold')
        
        table.setStyle(table_style)
        elements.append(table)
        
        # Jami ovozlar
        elements.append(Paragraph(f"<b>Jami ovozlar: {total}</b>", normal_style))
        
        # Bar chart
        chart_bytes = create_bar_chart(nom_key, nomination, votes, total)
        chart_image = Image(io.BytesIO(chart_bytes))
        chart_image.drawWidth = 9*inch
        chart_image.drawHeight = 4*inch
        elements.append(Spacer(1, 0.2*inch))
        elements.append(chart_image)
        
        # Keyingi sahifa
        elements.append(PageBreak())
    
    # Umumiy statistika sahifasi
    elements.append(Paragraph("UMUMIY STATISTIKA", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Har bir nominatsiya uchun g'oliblar
    elements.append(Paragraph("G'OLIBLAR RO'YXATI", subtitle_style))
    
    # G'oliblar jadvali uchun stil
    winners_cell_style = ParagraphStyle(
        'WinnersCellStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        wordWrap='LTR'
    )
    
    winners_header_style = ParagraphStyle(
        'WinnersHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.whitesmoke,
        fontName='Helvetica-Bold'
    )
    
    winners_data = [[
        Paragraph("Nominatsiya", winners_header_style),
        Paragraph("G'olib", winners_header_style),
        Paragraph("Ovozlar", winners_header_style)
    ]]
    
    for nom_key, nomination in NOMINATIONS.items():
        votes = await get_votes_by_nomination(nom_key)
        total = await get_votes_count_by_nomination(nom_key)
        
        if votes:
            # Eng ko'p ovoz sonini topish
            max_votes = votes[0]['vote_count']
            
            # Teng ovozli barcha g'oliblarni topish
            winners = []
            for vote in votes:
                if vote['vote_count'] == max_votes:
                    for c in nomination['candidates']:
                        if c['id'] == vote['candidate_id']:
                            winners.append(c)
                            break
                else:
                    break  # Ovozlar tartiblangan, shuning uchun keyingilari kamroq
            
            if winners:
                nom_title = nomination['title']
                percentage = f"{max_votes/total*100:.1f}%" if total > 0 else "0%"
                
                # Barcha g'oliblar lavozimi va F.I.Sh. birga chiqariladi
                winner_names = "\n".join([f"{w['position']} ({w['name']})" for w in winners])
                
                # Agar bir nechta g'olib bo'lsa, "(teng)" qo'shish
                votes_text = f"{max_votes} ({percentage})"
                if len(winners) > 1:
                    votes_text += "\n(teng ovoz)"
                
                winners_data.append([
                    Paragraph(nom_title, winners_cell_style),
                    Paragraph(winner_names.replace('\n', '<br/>'), winners_cell_style),
                    Paragraph(votes_text.replace('\n', '<br/>'), winners_cell_style)
                ])
        else:
            nom_title = nomination['title']
            winners_data.append([
                Paragraph(nom_title, winners_cell_style),
                Paragraph("Ovoz berilmagan", winners_cell_style),
                Paragraph("-", winners_cell_style)
            ])
    
    winners_table = Table(winners_data, colWidths=[4.5*inch, 3*inch, 1.5*inch])
    winners_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e8b57')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fff0')]),
    ]))
    elements.append(winners_table)
    
    # PDF yaratish
    doc.build(elements)
    
    return pdf_filename


async def generate_votes_detail_pdf() -> str:
    """Kim qaysi nomzodga ovoz berganini chiroyli ko'rsatadigan PDF."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"tanlov_ovozlar_tahlili_{timestamp}.pdf"

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "VotesTitle",
        parent=styles["Heading1"],
        fontSize=17,
        alignment=1,
        textColor=colors.HexColor("#1a5f7a"),
        spaceAfter=18,
    )

    subtitle_style = ParagraphStyle(
        "VotesSubtitle",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#2e8b57"),
        spaceBefore=10,
        spaceAfter=8,
    )

    small_grey_style = ParagraphStyle(
        "SmallGrey",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#666666"),
        spaceAfter=6,
    )

    cell_style = ParagraphStyle(
        "VotesCell",
        parent=styles["Normal"],
        fontSize=9,
        leading=11,
        wordWrap="LTR",
    )

    cell_header_style = ParagraphStyle(
        "VotesHeaderCell",
        parent=styles["Normal"],
        fontSize=9,
        leading=11,
        textColor=colors.whitesmoke,
        fontName="Helvetica-Bold",
    )

    elements = []
    elements.append(Paragraph("KO'PRIKQURILISH AJ", title_style))
    elements.append(Paragraph("OVOZLAR TAHLILI", title_style))

    all_votes = await get_all_votes()
    vote_count = len(all_votes)
    distinct_voters = len({v["user_id"] for v in all_votes})
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    intro_text = (
        f"Jami qayd etilgan ovozlar: <b>{vote_count}</b><br/>"
        f"Ovoz bergan foydalanuvchilar: <b>{distinct_voters}</b><br/>"
        f"Hisobot sanasi: <b>{created_at}</b>"
    )
    elements.append(Paragraph(intro_text, small_grey_style))
    elements.append(Spacer(1, 0.15 * inch))

    # Nominatsiyalarni har biri uchun jadval ko'rinishida chiqaramiz
    for idx, (nom_key, nomination) in enumerate(NOMINATIONS.items(), 1):
        elements.append(Paragraph(nomination["title"], subtitle_style))

        # Nomzodlarga ovoz berganlar ro'yxatini tayyorlash
        table_data = [[
            Paragraph("#", cell_header_style),
            Paragraph("Foydalanuvchi", cell_header_style),
            Paragraph("Ism, familiya", cell_header_style),
            Paragraph("Ovoz bergan nomzod", cell_header_style),
            Paragraph("Sana", cell_header_style),
        ]]

        nomination_votes = [v for v in all_votes if v["nomination_key"] == nom_key]

        # Vaqt bo'yicha teskari tartibda (yangi ovozlar yuqorida)
        nomination_votes.sort(key=lambda v: v.get("voted_at", ""), reverse=True)

        if not nomination_votes:
            table_data.append([
                Paragraph("-", cell_style),
                Paragraph("Ovoz berilmagan", cell_style),
                Paragraph("-", cell_style),
                Paragraph("-", cell_style),
                Paragraph("-", cell_style),
            ])
        else:
            # Nomzod nomini tez topish uchun lug'at
            candidate_lookup = {
                c["id"]: f"{c['name']} ({c['position']})" for c in nomination["candidates"]
            }

            for row_idx, vote in enumerate(nomination_votes, 1):
                username = vote.get("username") or "—"
                username_text = f"@{username}" if username and username != "—" and not username.startswith("@") else username
                full_name = vote.get("full_name") or "—"
                candidate_text = candidate_lookup.get(vote["candidate_id"], "Noma'lum")
                voted_at = vote.get("voted_at") or ""

                table_data.append([
                    Paragraph(str(row_idx), cell_style),
                    Paragraph(username_text, cell_style),
                    Paragraph(full_name, cell_style),
                    Paragraph(candidate_text, cell_style),
                    Paragraph(voted_at, cell_style),
                ])

        table = Table(table_data, colWidths=[0.4 * inch, 1.5 * inch, 2.8 * inch, 3.5 * inch, 1.2 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a5f7a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafd")]),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.25 * inch))

        if idx < len(NOMINATIONS):
            elements.append(PageBreak())

    doc.build(elements)

    return pdf_filename
