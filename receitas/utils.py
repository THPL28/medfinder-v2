import easyocr
from pdf2image import convert_from_path
import platform
import re
from fuzzywuzzy import process
from rapidfuzz import process
from receitas.models import Medicamento, Estoque
from receitas.ocr_pre_processing import preprocess_image
from receitas.models import Medicamento
# Instanciando o leitor EasyOCR com suporte ao português
reader = easyocr.Reader(['pt'])

def extract_easyocr(caminho_pdf, psm=3) -> dict:
    try:
        imagens = convert_from_path(caminho_pdf)
        texto_completo = ""
        confianca_total = 0
        num_imagens = len(imagens)

        for imagem in imagens:
            # PREPROCESSAMENTO AQUI
            imagem_processada = preprocess_image(imagem)

            # Extração de texto usando EasyOCR
            resultado = reader.readtext(imagem_processada)
            for res in resultado:
                texto_completo += res[1] + "\n"

            # Média de confiança
            confianca_total += sum([res[2] for res in resultado]) / len(resultado) if resultado else 0

        confianca_media = confianca_total / num_imagens if num_imagens > 0 else 0
        return {'text': texto_completo, 'confidence': round(confianca_media, 2)}

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado no caminho: {caminho_pdf}")
        return {'text': "", 'confidence': 0}
    except Exception as e:
        print(f"Erro durante OCR com EasyOCR: {e}")
        return {"text": "", "confidence": 0}


import re
from receitas.models import Medicamento

def extrair_quantidade(texto, nome_medicamento):
    """
    Tenta encontrar a quantidade prescrita de um medicamento no texto.
    Exemplo de padrão: "Paracetamol 2 caixas", "Paracetamol: 1 unidade"
    """
    padrao = re.compile(rf'{re.escape(nome_medicamento)}.*?(\d+)\s*(caixas|unidades|cp|comprimidos)?', re.IGNORECASE)
    match = padrao.search(texto)
    if match:
        return int(match.group(1))
    return None

def check_medicine_availability(medicamentos):
    """
    Função para verificar a disponibilidade dos medicamentos.
    """
    medicamentos_disponiveis = []
    nomes_verificados = set()

    if isinstance(medicamentos, list):
        for nome_medicamento in medicamentos:
            if nome_medicamento not in nomes_verificados:
                medicamento = Medicamento.objects.filter(nome=nome_medicamento).first()
                if medicamento:
                    medicamentos_disponiveis.append(medicamento)
                    nomes_verificados.add(nome_medicamento)
    else:
        medicamento = Medicamento.objects.filter(nome=medicamentos).first()
        if medicamento:
            medicamentos_disponiveis.append(medicamento)

    return medicamentos_disponiveis



def clean_medicine_names(medicine_names):
    cleaned_names = []
    for name in medicine_names:
        name = name.replace("rn", "m").replace("0", "O")
        match = re.search(r"([a-zA-Z\s]+)\s*([\d.,]+)?", name)
        if match:
            medicine_name = match.group(1).strip()
            cleaned_names.append(medicine_name)
        else:
            cleaned_names.append(name)
    return cleaned_names


from rapidfuzz import process

def fuzzy_match_medicine_names(medicine_names, threshold=85):
    """
    Faz correspondência fuzzy com limite mínimo de similaridade para evitar falsos positivos.
    """
    all_medicine_names = [medicine.nome for medicine in Medicamento.objects.all()]
    corrected_names = set()

    for name in medicine_names:
        best_match = process.extractOne(name, all_medicine_names, score_cutoff=threshold)
        if best_match:
            corrected_names.add(best_match[0])
        else:
            corrected_names.add(name)

    return list(corrected_names)


def populate_database():
    medicamentos_data = [
        {"nome": "Dipirona", "codigo_barras": "1234567890", "fabricante": "EMS", "dosagem": "500mg", "forma_farmaceutica": "Comprimido", "preco": decimal.Decimal("10.50"), "quantidade": 100},
        {"nome": "Amoxicilina", "codigo_barras": "9876543210", "fabricante": "Sandoz", "dosagem": "250mg", "forma_farmaceutica": "Cápsula", "preco": decimal.Decimal("15.99"), "quantidade": 50},
        {"nome": "Paracetamol", "codigo_barras": "1122334455", "fabricante": "Medley", "dosagem": "750mg", "forma_farmaceutica": "Comprimido", "preco": decimal.Decimal("8.75"), "quantidade": 75},
        {"nome": "Ibuprofeno", "codigo_barras": "5544332211", "fabricante": "Neo Química", "dosagem": "400mg", "forma_farmaceutica": "Comprimido", "preco": decimal.Decimal("12.30"), "quantidade": 60},
        {"nome": "Loratadina", "codigo_barras": "1020304050", "fabricante": "Eurofarma", "dosagem": "10mg", "forma_farmaceutica": "Comprimido", "preco": decimal.Decimal("20.00"), "quantidade": 40},
    ]

    for data in medicamentos_data:
        try:
            medicamento = Medicamento.objects.get(nome=data["nome"])
        except Medicamento.DoesNotExist:
            medicamento = Medicamento.objects.create(
                nome=data["nome"], codigo_barras=data["codigo_barras"], fabricante=data["fabricante"],
                dosagem=data["dosagem"], forma_farmaceutica=data["forma_farmaceutica"], preco=data["preco"]
            )

        try:
            Estoque.objects.get(medicamento=medicamento)
        except Estoque.DoesNotExist:
            Estoque.objects.create(medicamento=medicamento, quantidade=data["quantidade"])