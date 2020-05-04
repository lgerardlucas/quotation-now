from django import forms
from .models import QuotationPrice
from qnow_client.models import Quotation
from django.forms.models import inlineformset_factory

class QuotationPriceForm(forms.ModelForm):
    class Meta:
        model = QuotationPrice
        fields = (
            'quotation_number',
            'quotation_provider',
            'date_create',
            'date_validate',
            'quotation_value',
            'delivery_time',
            'form_payment',
            'comments',
            'cancel_quotation',
            'cancel_comments'
        )

        labels = {
            'quotation_number': 'Cliente',
            'quotation_provider': 'Marcenaria',
            'date_create':'Data do Orçamento',
            'date_validate': 'Validade do Orçamento',
            'quotation_value': 'Valor do Orçamento',
            'delivery_time':'Prazo de Entrega',
            'form_payment':'Forma de Pagamento.',
            'comments':'Comentário da Marcenaria'
        }

        widgets = {
            'date_create': forms.DateInput(
                attrs={'type': 'text', 'class': 'date_format', 'data-language': 'pt-BR', 'autocomplete':'off','readonly':'true',
                    'data-toggle':'tooltip', 'data-placement':'top', 'title':'Data de lançamento da cotação.'
                    }
                ),
            'date_validate': forms.DateInput(
                attrs={'type': 'text', 'class': 'datepicker-here date_format', 'data-language': 'pt-BR', 'data-position': 'bottom right', 'data-auto-close': 'true', 'autocomplete':'off',
                    'data-toggle':'tooltip', 'data-placement':'top', 'title':'Data de validade do valor orçado por sua empresa.'
                    }
                ),
            'quotation_value': forms.TextInput(
                attrs={'class': 'dinheiro', 'autocomplete':'off',
                    'data-toggle':'tooltip', 'data-placement':'top','title':'Informe seu valor para esta cotação.'
                    }
                ),
            'delivery_time': forms.TextInput(
                attrs={'autocomplete':'on',
                    'data-toggle':'tooltip', 'data-placement':'top','title':'Indique o total em dias para entrega do produto. Ex: "60 dias úteis".'
                    }
                ),
            'form_payment': forms.TextInput(
                attrs={'autocomplete':'on',
                    'data-toggle':'tooltip', 'data-placement':'top','title':'Especifique aqui, a forma de pagamento usada por sua empresa.'
                    }
                ),
            'quotation_number': forms.TextInput(
                attrs={'placeholder': 'Cliente desta cotação.', 'style':'display: none;','title':''}
                ),
            'quotation_provider': forms.TextInput(
                attrs={'placeholder': 'Fornecedor desta cotação', 'style':'display: none;','title':''}
                ),
            'comments': forms.Textarea(
                attrs={'cols': 40,'style':'width: 100%; height: 100%; resize: none; !important;','title':'',
                    'placeholder': 
                        'Obs: Se possuir ainda dúvidas sobre a cotação deste cliente, utilize o botão "Perguntar"'
                    }
                )
        } 

    '''
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data.get('quotation_value'))
        cleaned_data['quotation_value'] = str(cleaned_data.get('quotation_value')).replace(',','.')
        print(cleaned_data['quotation_value'])

        senha = cleaned_data.get('senha')
        confirma_senha = cleaned_data.get('confirma_senha')

        email = cleaned_data.get('email')
        confirma_email = cleaned_data['confirma_email']

        if senha != confirma_senha:
                raise forms.ValidationError('Senha não confere! Digite a mesma senha nos campos Senha e Confirmar Senha.')

        if email and confirma_email:
                if email != confirma_email:
                        raise forms.ValidationError('E-Mail não confere! Digite o mesmo e-mail nos campos E-mail e Confirma E-mail')
        return cleaned_data        
    '''
    '''
    QuotationPriceFormSet = inlineformset_factory(Quotation, QuotationPrice,
                                            form=QuotationPriceForm, extra=1)
    '''
    