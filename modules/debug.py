import json
import sys
import pprint
import traceback
from django.conf import settings

def dd(*args):
    """
    Dump and Die para projetos Django.
    Exibe variáveis e finaliza a execução (exceto no shell interativo).
    """
    print("\n" + "="*40)
    print("📦 Dump and Die (dd) chamado:")
    print("="*40)

    # Mostrar a origem do dd() na stack
    stack = traceback.extract_stack()
    if len(stack) >= 2:
        caller = stack[-2]
        print(f"\n📍 Localização: {caller.filename}, linha {caller.lineno}")
        print(f"→ Código: {caller.line.strip() if caller.line else 'Desconhecido'}")
        print("-"*40)

    for i, arg in enumerate(args):
        print(f"\n🔹 Argumento {i+1}:")
        try:
            print(json.dumps(arg, indent=4, ensure_ascii=False))
        except (TypeError, OverflowError):
            pprint.pprint(arg)

    print("\n🚫 Execução encerrada pelo dd()\n")

    # Se não estiver no shell interativo, encerra o programa
    if not hasattr(sys, 'ps1'):
        sys.exit()
        
def d(*args):
    for arg in args:
        try:
            print(json.dumps(arg, indent=4, ensure_ascii=False))
        except (TypeError, OverflowError):
            pprint.pprint(arg)