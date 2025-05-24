from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Receita

# Função auxiliar para aplicar classes e rótulos aos campos
def aplicar_estilo_campos(form_instance, campos_labels=None, classe='form-control text-white'):
    for nome, campo in form_instance.fields.items():
        campo.widget.attrs.update({'class': classe})
        if campos_labels and nome in campos_labels:
            campo.label = campos_labels[nome]

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilo_campos(self, {
            'username': 'Nome de usuário',
            'password': 'Senha',
        })

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilo_campos(self, {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirme a senha',
        })
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("A senha é muito curta. Ela deve conter pelo menos 8 caracteres.")
            if password.isdigit():
                raise forms.ValidationError("A senha não pode conter apenas números.")
            if password.lower() in ['senha123', '12345678', 'password', 'admin']:
                raise forms.ValidationError("A senha é muito comum. Escolha uma senha mais segura.")
        return password

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['pdf']

    def clean_pdf(self):
        pdf = self.cleaned_data.get('pdf')
        if not pdf:
            raise forms.ValidationError("Por favor, selecione um arquivo PDF.")
        if not pdf.name.lower().endswith('.pdf'):
            raise forms.ValidationError("O arquivo deve ser do tipo PDF.")
        max_size = 5 * 1024 * 1024  # 5 MB
        if pdf.size > max_size:
            raise forms.ValidationError("O arquivo não pode exceder 5MB.")
        return pdf
