from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek
from apps.agendamentos.models import Agendamento
from apps.clientes.models import Cliente
from apps.profissionais.models import Profissional
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

def generate_relatorio_pdf(data_inicio=None, data_fim=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                           topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title', parent=styles['Title'], fontSize=20, spaceAfter=30, alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'Heading', parent=styles['Heading2'], fontSize=16, spaceAfter=12
    )
    
    Agendamento.atualizar_statuss()
    
    # Filtros
    agendamentos = Agendamento.objects.filter(status='CONCLUIDO')
    if data_inicio:
        agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)
    if data_fim:
        agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)
    
    story = []
    
    # CABEÇALHO
    story.append(Paragraph("RELATÓRIO GERENCIAL COMPLETO", title_style))
    story.append(Paragraph("Salão Rainbow Hair", styles['Heading1']))
    story.append(Paragraph(f"Período: {data_inicio or 'Início'} até {data_fim or 'Hoje'}", styles['Normal']))
    story.append(Paragraph(f"Gerado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # 1. RESUMO GERAL
    story.append(Paragraph("1. RESUMO GERAL", heading_style))
    total_agend = agendamentos.count()
    total_faturamento = agendamentos.aggregate(Sum('servico__preco'))['servico__preco__sum'] or 0
    total_clientes = Cliente.objects.count()
    agend_abertos = Agendamento.objects.filter(status='AGENDADO').count()
    
    resumo_data = [
        ['Métrica', 'Valor'],
        ['Agendamentos Concluídos', total_agend],
        ['Faturamento Total', f'R$ {total_faturamento:,.2f}'],
        ['Total Clientes', total_clientes],
        ['Agendamentos Abertos', agend_abertos]
    ]
    resumo_table = Table(resumo_data, colWidths=[6*cm, 6*cm])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgoldenrod),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(resumo_table)
    story.append(Spacer(1, 20))
    
# 2. AGENDAMENTOS POR DIA - GRÁFICO + TABELA
    story.append(Paragraph("2. AGENDAMENTOS POR DIA", heading_style))
    
    # Gráfico matplotlib
    por_dia = agendamentos.annotate(dia=TruncDay('data_hora'))\
        .values('dia')\
        .annotate(total=Count('id'))\
        .order_by('dia')
    
    datas = [item['dia'].strftime('%d/%m') for item in por_dia]
    valores = [item['total'] for item in por_dia]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(datas[:10], valores[:10], color='skyblue', edgecolor='navy')
    ax.set_title('Agendamentos Concluídos por Dia', fontsize=14, fontweight='bold')
    ax.set_xlabel('Data')
    ax.set_ylabel('Quantidade')
    ax.tick_params(axis='x', rotation=45)
    
    # Adiciona valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    img_buffer = BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(img_buffer)
    img_buffer.seek(0)
    img = Image(img_buffer, width=14*cm, height=8*cm)
    story.append(img)
    plt.close(fig)
    
    # Tabela
    dia_data = [['Data', 'Quantidade']] + [[item['dia'].strftime('%d/%m'), item['total']] for item in por_dia]
    dia_table = Table(dia_data, colWidths=[5*cm, 3*cm])
    dia_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.sandybrown),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))
    story.append(dia_table)
    story.append(Spacer(1, 12))

    # 3. FATURAMENTO DO PERÍODO - GRÁFICO + TABELA
    story.append(Paragraph("3. FATURAMENTO DO PERÍODO", heading_style))
    
    # Query do faturamento por dia (igual DadosRelatorioFaturamentoView)
    por_faturamento = agendamentos.select_related('servico').annotate(
        dia=TruncDay('data_hora')
    ).values('dia').annotate(
        total_fat=Sum('servico__preco'),
        quantidade=Count('id')
    ).order_by('dia')
    
    datas_fat = [str(item['dia'].date()) for item in por_faturamento]
    valores_fat = [float(item['total_fat'] or 0) for item in por_faturamento]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    line = ax.plot(datas_fat[:10], valores_fat[:10], marker='o', linewidth=2.5, markersize=8, color='green')
    ax.set_title('Faturamento por Dia', fontsize=14, fontweight='bold')
    ax.set_xlabel('Data')
    ax.set_ylabel('Faturamento (R$)')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    
    # Valores nas pontos
    for i, v in enumerate(valores_fat[:10]):
        ax.annotate(f'R$ {v:,.0f}', (i, v), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()
    
    img_buffer = BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(img_buffer)
    img_buffer.seek(0)
    img = Image(img_buffer, width=14*cm, height=8*cm)
    story.append(img)
    plt.close(fig)
    
    # Tabela faturamento
    fat_data = [['Data', 'Faturamento', 'Qtd Agendamentos']] + [
        [str(item['dia'].date()), f'R$ {float(item["total_fat"] or 0):,.2f}', item['quantidade']] for item in por_faturamento
    ]
    fat_table = Table(fat_data, colWidths=[4*cm, 5*cm, 4*cm])
    fat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))
    story.append(fat_table)
    story.append(Spacer(1, 12))
    
    # 4. SERVIÇOS MAIS POPULARES
    story.append(Paragraph("4. SERVIÇOS MAIS POPULARES", heading_style))
    por_servico = agendamentos.values('servico__nome', 'servico__preco')\
        .annotate(qtd=Count('id'), total=Sum('servico__preco'))\
        .order_by('-qtd')[:10]
    
    serv_data = [['Serviço', 'Preço', 'Qtd', 'Total']] + [
        [item['servico__nome'][:20], f'R$ {item["servico__preco"]:,.2f}', item['qtd'], f'R$ {item["total"]:,.2f}'] 
        for item in por_servico
    ]
    serv_table = Table(serv_data, colWidths=[5*cm, 2*cm, 1.5*cm, 3.5*cm])
    serv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkkhaki),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (3, -1), 'RIGHT'),
    ]))
    story.append(serv_table)
    story.append(Spacer(1, 12))
    
    # 5. PROFISSIONAIS
    story.append(Paragraph("5. DESEMPENHO PROFISSIONAIS", heading_style))
    from apps.profissionais.models import Profissional
    por_prof = agendamentos.values('profissional__nome', 'profissional__especialidade')\
        .annotate(qtd=Count('id'), total=Sum('servico__preco'))\
        .order_by('-qtd')[:10]
    
    prof_data = [['Profissional', 'Especialidade', 'Qtd', 'Faturado']] + [
        [item['profissional__nome'][:25], item['profissional__especialidade'][:20], item['qtd'], f'R$ {item["total"]:,.2f}']
        for item in por_prof
    ]
    prof_table = Table(prof_data, colWidths=[4*cm, 3*cm, 1.5*cm, 3.5*cm])
    prof_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gold),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (3, -1), 'RIGHT'),
    ]))
    story.append(prof_table)
    story.append(Spacer(1, 12))
    
# 6. STATUS - GRÁFICO DE PIZZA + TABELA
    story.append(Paragraph("6. AGENDAMENTOS POR STATUS", heading_style))
    
    all_agend = Agendamento.objects.all()
    if data_inicio:
        all_agend = all_agend.filter(data_hora__date__gte=data_inicio)
    if data_fim:
        all_agend = all_agend.filter(data_hora__date__lte=data_fim)
    
    por_status = all_agend.values('status').annotate(total=Count('id')).order_by('-total')
    
    status_labels = [item['status'] for item in por_status]
    status_valores = [item['total'] for item in por_status]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors_pizza = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    wedges, texts, autotexts = ax.pie(status_valores, labels=status_labels, autopct='%1.1f%%',
                                      colors=colors_pizza, startangle=90)
    ax.set_title('Distribuição por Status', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    img_buffer = BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(img_buffer)
    img_buffer.seek(0)
    img = Image(img_buffer, width=10*cm, height=8*cm)
    story.append(img)
    plt.close(fig)
    
    # Tabela
    status_data = [['Status', 'Quantidade']] + [
        [item['status'], item['total']] for item in por_status
    ]
    status_table = Table(status_data, colWidths=[6*cm, 4*cm])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))
    story.append(status_table)
    story.append(Spacer(1, 12))
    
    # 7. TOP CLIENTES
    story.append(Paragraph("7. TOP 10 CLIENTES", heading_style))
    por_cliente = agendamentos.values('cliente__nome', 'cliente__telefone')\
        .annotate(qtd=Count('id'), total=Sum('servico__preco'))\
        .order_by('-total')[:10]
    
    cliente_data = [['Cliente', 'Telefone', 'Visitas', 'Gasto']] + [
        [item['cliente__nome'][:25], item['cliente__telefone'] or '', item['qtd'], f'R$ {item["total"]:,.2f}']
        for item in por_cliente
    ]
    cliente_table = Table(cliente_data, colWidths=[4*cm, 3*cm, 2*cm, 3*cm])
    cliente_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (3, -1), 'RIGHT'),
    ]))
    story.append(cliente_table)
    
    doc.build(story)
    
    buffer.seek(0)
    return buffer
