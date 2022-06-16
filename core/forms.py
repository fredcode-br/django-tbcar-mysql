from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from core.models import Cliente, Fabricante, Veiculo, Tabela, Rotativo, Mensalista
from django.forms import ModelForm


class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class FormFabricante(ModelForm):
    class Meta:
        model = Fabricante
        fields = ['descricao']

class FormVeiculo(ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'

class FormTabela(ModelForm):
    class Meta:
        model = Tabela
        fields = '__all__'

class FormRotativo(ModelForm):
    class Meta:
        model = Rotativo
        fields = '__all__'
        widgets = {'data_entrada': DateTimePickerInput(), 'data_saida': DateTimePickerInput()}

class FormMensalista(ModelForm):
    class Meta:
        model = Mensalista
        fields = '__all__'
