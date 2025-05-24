import logging
import os
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .forms import ReceitaForm
from .models import Receita, Medicamento, Estoque
from .utils import clean_medicine_names, fuzzy_match_medicine_names, check_medicine_availability
from .ocr_pre_processing import pre_process_pdf
import easyocr
import fitz  # PyMuPDF
from modules.debug import dd

# Configuração do logger
logger = logging.getLogger(__name__)

# Instanciando o EasyOCR Reader
reader = easyocr.Reader(['pt', 'en'])  # Definindo os idiomas para OCR (português e inglês)

def register_view(request):
    """
    View para o cadastro de novos usuários.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
# def register_view(request):
#     """
#     View para o cadastro de novos usuários.
#     """
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='login')
def inicio(request):
    return render(request, 'inicio.html')

# A função para processar o texto diretamente do PDF com PyMuPDF
def extract_text_from_pdf(pdf_path):
    try:
        print(f"extract_text_from_pdf >>> Extraindo texto do PDF no caminho: {pdf_path}")  # Log para depuração
        # Abre o arquivo PDF
        doc = fitz.open(pdf_path)
        text = ""
        
        # Percorre todas as páginas do PDF
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)  # Carrega a página
            text += page.get_text("text")  # Extrai o texto da página
        
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {e}")
        return None

class ReceitaUploadView(LoginRequiredMixin, View):
    """
    View para o upload de receitas médicas.
    """
    login_url = 'login'
    template_name = 'receitas/upload.html'

    def get(self, request):
        form = ReceitaForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Trata requisições POST, processando o upload da receita e extraindo o texto.
        """
        try:
            form = ReceitaForm(request.POST, request.FILES)
            if form.is_valid():
                # Salva a Receita no banco de dados (com o PDF)
                receita = form.save()
                caminho_pdf = os.path.join(settings.MEDIA_ROOT, receita.pdf.name)

                # Extrai o texto diretamente do PDF com PyMuPDF
                texto_extraido = extract_text_from_pdf(caminho_pdf)

                if texto_extraido:
                    confianca = 100  # PyMuPDF não fornece diretamente a confiança, então podemos definir como 100

                    # Armazena o texto extraído na instância da receita
                    receita.texto_extraido = texto_extraido
                    receita.ocr_confianca = confianca
                    receita.save()

                    # Mensagem de sucesso
                    messages.success(request, "Receita enviada e processada com sucesso!")
                    return redirect('resultado', pk=receita.pk)
                else:
                    messages.error(request, "Ocorreu um erro ao processar o PDF da receita.")
                    return render(request, self.template_name, {'form': form})

            else:
                messages.error(request, "Ocorreu um erro ao enviar a receita. Verifique os dados.")
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            logger.error(f"Erro ao processar o upload da receita: {e}")
            messages.error(request, "Ocorreu um erro interno ao processar sua receita. Por favor, tente novamente mais tarde.")
            return render(request, self.template_name, {'form': form})

@login_required(login_url='login')
def list_medicines_view(request):
    """
    View para listar todos os medicamentos no banco de dados.
    """
    try:
        medicamentos = Medicamento.objects.all()
        return render(request, 'receitas/list_medicines.html', {'medicamentos': medicamentos})
    except Exception as e:
        logger.error(f"Erro ao listar os medicamentos: {e}")
        messages.error(request, "Ocorreu um erro interno ao processar sua receita. Por favor, tente novamente mais tarde.")
        return render(request, 'receitas/upload.html')

@login_required(login_url='login')
def resultado_view(request, pk):
    """
    View para exibir o resultado da extração de texto da receita e os medicamentos encontrados.
    """
    receita = get_object_or_404(Receita, pk=pk)
    texto_extraido = receita.texto_extraido

    if not texto_extraido:
        medicamentos_encontrados = []
    else:
        nomes_limpos = clean_medicine_names(texto_extraido.splitlines())
        nomes_corrigidos = fuzzy_match_medicine_names(nomes_limpos)

        medicamentos_disponiveis = check_medicine_availability(nomes_corrigidos)

        medicamentos_encontrados = []
        for medicamento in medicamentos_disponiveis:
            medicamento_info = {
                'nome': medicamento.nome,
                'fabricante': medicamento.fabricante,
                'dosagem': medicamento.dosagem,
            }
            medicamentos_encontrados.append(medicamento_info)

    context = {
        'receita': receita,
        'medicamentos_encontrados': medicamentos_encontrados
    }
    return render(request, 'receitas/resultado.html', context)


@login_required(login_url='login')
def historico_receitas(request):
    """
    View para exibir o histórico de receitas.
    """
    receitas = Receita.objects.all().order_by('-id')
    return render(request, 'receitas/historico.html', {'receitas': receitas})

@login_required(login_url='login')
def contato(request):
    """View para exibir a página de contato."""
    return render(request, 'receitas/contato.html')
