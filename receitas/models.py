from django.db import models

class Receita(models.Model):
    pdf = models.FileField(upload_to='receitas/')
    data_upload = models.DateTimeField(auto_now_add=True)
    texto_extraido = models.TextField(blank=True, null=True)  # Armazena o texto extraído do PDF

    def __str__(self):
        return f"Receita {self.id} - {self.data_upload}"

class Medicamento(models.Model):
    nome = models.CharField(max_length=200, db_index=True, unique=True) #Add an index to the nome field
    codigo_barras = models.CharField(max_length=200, blank=True, null=True, unique=True)
    fabricante = models.CharField(max_length=150, blank=True, null=True)
    dosagem = models.CharField(max_length=50, blank=True, null=True)
    forma_farmaceutica = models.CharField(max_length=50, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)    

    def __str__(self):
        return self.nome

class Estoque(models.Model):
    medicamento = models.OneToOneField(Medicamento, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"Estoque de {self.medicamento.nome}"

