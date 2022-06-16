from django.db import models
from math import ceil, floor, trunc

# Create your models here.


class Cliente(models.Model):
    nome = models.CharField(max_length=50, verbose_name='Nome')
    endereco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Endereço')
    complemento = models.CharField(max_length=50, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=50, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=50, blank=True, null=True, verbose_name='Cidade')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    foto = models.ImageField(upload_to='fotos_clientes', blank=True, null=True, verbose_name='Foto')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Clientes'


class Fabricante(models.Model):
    descricao = models.CharField(max_length=30, verbose_name='Descrição')

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name_plural = 'Fabricantes'


class Veiculo(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    id_fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE, verbose_name='Fabricante')
    modelo = models.CharField(max_length=30, verbose_name='Modelo')
    ano = models.IntegerField(default=2022, blank=True, null=True, verbose_name='Ano')
    cor = models.CharField(max_length=50, blank=True, null=True, verbose_name='Cor')
    placa = models.CharField(max_length=12, verbose_name='Placa')
    foto = models.ImageField(upload_to='fotos_veiculos', blank=True, null=True, verbose_name='Foto')

    def __str__(self):
        return f'{self.modelo} {self.cor} {self.placa} '

    class Meta:
        verbose_name_plural = 'Veículos'


class Tabela (models.Model):
    descricao = models.CharField(max_length=30, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Valor')
    horaAdicional = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Hora adicional')
    moto = models.BooleanField(default=False, verbose_name='Moto')

    def __str__(self):
        return f'{self.descricao}:{self.valor}'

    class Meta:
        verbose_name_plural = 'Tabela'


class FormaPagamento (models.Model):
    descricao = models.CharField (max_length=50, verbose_name='Tipo de Pagamento')

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name_plural = 'Formas de pagamento'


class Mensalista (models.Model):
    id_veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, verbose_name='Veiculo')
    id_tabela = models.ForeignKey(Tabela,on_delete=models.CASCADE, verbose_name='Tarifa')
    data_pagamento = models.DateTimeField(auto_now=False, blank=True, null=True, verbose_name='Data de Pagamento')
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name='Tipo de pagamento')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0, verbose_name='Total')
    #sugestoes: desconto pro pix, foi pago ou nao / relacionamento com tabela de meses de pagamento (armazenado se confirmar que foi pago)

    def __str__(self):
        return f'{self.id_veiculo}:{self.id_tabela}'

    class Meta:
        verbose_name_plural = 'Mensalistas'

    def calcula_desconto (self):
        if self.forma_pagamento:
            objeto = Tabela.objects.get(id=self.id_tabela.pk)
            if self.forma_pagamento.descricao.upper() == 'DINHEIRO':
                self.total = float (objeto.valor) * 0.95
            else:
                self.total = objeto.valor
            return self.total
        else:
            return 0.0


class Rotativo (models.Model):
    id_veiculo = models.ForeignKey(Veiculo, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Veiculo')
    id_tabela = models.ForeignKey(Tabela,on_delete=models.CASCADE, verbose_name='Tarifa')
    data_entrada = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Entrada')
    data_saida = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Saída')
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0, verbose_name='Total')
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Tipo de pagamento')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')

    def __str__(self):
        return f'{self.id_veiculo}:{self.total}'

    class Meta:
        verbose_name_plural = 'Rotativos'

    #regra de negocio para calculo do total a pagar
    def calcula_Total(self):
        if self.data_saida:
            horas = (self.data_saida - self.data_entrada).total_seconds()/3600
            if horas <0:
                return False
            obj = Tabela.objects.get(id = self.id_tabela.pk)
        #tolerancia de 15m
        #    diferenca = horas - trunc(horas)
        #    if diferenca < 0.25:
        #        horas = floor(horas)
        #    else:
        #        horas = ceil(horas)
        #   self.total = horas * obj.valor
            #print (self.total)
        #    return self.total
            if obj.moto:
                total = obj.valor*ceil(horas)
            elif horas <= 0.5:
                total = obj.horaAdicional
            elif horas <= 1:
                total = obj.valor
            else:
                total = obj.valor + (ceil(horas)-1)*obj.horaAdicional
            self.total = total
            return True
        else:
            return False
