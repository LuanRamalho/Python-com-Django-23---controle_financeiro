from django.shortcuts import render, redirect, get_object_or_404
from .models import Receita, Despesa
from .forms import ReceitaForm, DespesaForm
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import JsonResponse

# Exibir a página principal com receitas e despesas
def index(request):
    receitas = Receita.objects.all()
    despesas = Despesa.objects.all()
    return render(request, 'index.html', {'receitas': receitas, 'despesas': despesas})

# Formulário para adicionar receita
def adicionar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ReceitaForm()
    return render(request, 'formulario.html', {'form': form, 'tipo': 'Receita'})

# Formulário para adicionar despesa
def adicionar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DespesaForm()
    return render(request, 'formulario.html', {'form': form, 'tipo': 'Despesa'})

# Função para editar receita
def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ReceitaForm(instance=receita)
    return render(request, 'formulario.html', {'form': form, 'tipo': 'Receita'})

# Função para excluir receita
def excluir_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    if request.method == 'POST':
        receita.delete()
        return redirect('index')
    return render(request, 'confirmar_exclusao.html', {'tipo': 'Receita', 'item': receita})

# Função para editar despesa
def editar_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DespesaForm(instance=despesa)
    return render(request, 'formulario.html', {'form': form, 'tipo': 'Despesa'})

# Função para excluir despesa
def excluir_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id)
    if request.method == 'POST':
        despesa.delete()
        return redirect('index')
    return render(request, 'confirmar_exclusao.html', {'tipo': 'Despesa', 'item': despesa})

# Gerar gráfico de pizza
def gerar_grafico(request):
    # Receitas e despesas totais
    receitas = Receita.objects.all()
    despesas = Despesa.objects.all()

    receita_total = sum([r.valor for r in receitas])
    despesa_total = sum([d.valor for d in despesas])

    # Para os gráficos mensais
    mes = request.GET.get('mes', None)
    ano = request.GET.get('ano', None)

    if mes and ano:
        receitas_mes = Receita.objects.filter(data__month=mes, data__year=ano)
        despesas_mes = Despesa.objects.filter(data__month=mes, data__year=ano)
    else:
        receitas_mes = []
        despesas_mes = []

    receita_mes_total = sum([r.valor for r in receitas_mes])
    despesa_mes_total = sum([d.valor for d in despesas_mes])

    # Para os gráficos anuais
    if ano:
        receitas_ano = Receita.objects.filter(data__year=ano)
        despesas_ano = Despesa.objects.filter(data__year=ano)
    else:
        receitas_ano = []
        despesas_ano = []

    receita_ano_total = sum([r.valor for r in receitas_ano])
    despesa_ano_total = sum([d.valor for d in despesas_ano])

    return render(request, 'grafico.html', {
        'receita_total': receita_total,
        'despesa_total': despesa_total,
        'receita_mes_total': receita_mes_total,
        'despesa_mes_total': despesa_mes_total,
        'receita_ano_total': receita_ano_total,
        'despesa_ano_total': despesa_ano_total,
    })

# Gerar relatório em PDF
def gerar_pdf(request):
    receitas = Receita.objects.all()
    despesas = Despesa.objects.all()
    receita_total = sum([r.valor for r in receitas])
    despesa_total = sum([d.valor for d in despesas])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.pdf"'
    
    c = canvas.Canvas(response, pagesize=letter)
    c.drawString(100, 750, f'Relatório Financeiro')
    c.drawString(100, 730, f'Receitas: R$ {receita_total:.2f}')
    c.drawString(100, 710, f'Despesas: R$ {despesa_total:.2f}')
    
    c.showPage()
    c.save()
    
    return response
