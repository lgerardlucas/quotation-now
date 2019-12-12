from django import forms
from .models import Quotation, MobilieType, QuotationStage

class MobileTypeForm(forms.ModelForm):
    class Meta:
        model = MobilieType

        fields = (
            '__all__'
        )

class QuotationStageForm(forms.ModelForm):
    class Meta:
        model = QuotationStage

        fields = (
            '__all__'
        )

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = (
            'id',
            'house_type',
            'house_set',
            'mobile_type',
            'mobile_description',
            'particulars',
            'image_environment',
            'image_project'

        )

        labels = {
            'id': 'Nº da Cotação',
            'house_type': 'Como é seu imóvel?',
            'house_set':'Nome do condomínio ou residencial',
            'mobile_type': 'Para qual móvel deseja cotações?',
            'mobile_description':'Para "_Outro", coloque o nome aqui.(Ex: Aparador)',
            'particulars': 'Nos conte como deseja seu móvel',
            'image_environment':'Imagem do ambiente - Uma foto do ambiente, nos ajudará a entender melhor caso precisemos projetá-lo(Projeto simples e sem custo).',
            'image_project':'Imagem do projeto - Projeto, desenho ou qualquer imagem, caso tenha, de como gostaria que fosse seu móvel.'
        }

        widgets = {
            'house_set': forms.TextInput(
                attrs={'placeholder': 'Nome do condomínio ou residencial'}
                ),
            'mobile_description': forms.TextInput(
                attrs={'placeholder': 'Se a escolha foi "Outro" indique aqui o móvel a ser cotar'}
                ),
            'particulars': forms.Textarea(
                attrs={'cols': 40,'style':'width: 100%; height: 50%; resize: none; !important;',
                    'placeholder': 
                        'Informe aqui, as caracteristicas importantes de como deseja este móvel e as medidas do ambiente em questão. '
                        +'\n\n'+
                        'Se não souber explicar, podemos entrar em contato e lhe ajudar.'+'\n'+
                        'O nosso primeiro contato é pelo whatsapp, com isto, deixe aqui seu nº.'
                    }
                )
        }
