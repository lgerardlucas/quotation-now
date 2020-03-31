from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Class usada somente para o cadastro e não para o login 
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email','username','phone', 'cep','street','district','city','state','password1','password1','birth_date','delivery_time','form_payment','information','contract_accepted']

        widgets = {
            'email': forms.TextInput(
                attrs={'placeholder': 'E-mail de contato. Ex: fulano@fulando.com'}
                ),
            'username': forms.TextInput(
                attrs={'placeholder': 'Nome completo. Ex: Fulano da Silva'}
                ),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Fone para contato. Ex: (DD) 99999-9999'}
                ),
            'cep': forms.TextInput(
                attrs={'placeholder': 'Seu CEP. Ex: 99999-999'}
                ),
            'city': forms.TextInput(
                attrs={'placeholder': 'Sua cidade. Ex: Pelotas'}
                ),
            'district': forms.TextInput(
                attrs={'placeholder': 'Seu bairro. Ex: Fragata'}
                ),
            'street': forms.TextInput(
                attrs={'placeholder': 'Sua rua, nº, bloco e apto se possuir'}
                ),
            'state': forms.TextInput(
                attrs={'placeholder': 'Estado de sua cidade. Ex: RS'}
                ),
            'birth_date': forms.DateInput(
                attrs={'type': 'text', 'class': 'datepicker-here date_format', 'data-language': 'pt-BR', 'data-position': 'bottom left', 'data-auto-close': 'true', 'autocomplete':'off',
                    'data-toggle':'tooltip', 'data-placement':'top'
                    }
                ),
            'delivery_time': forms.TextInput(
                attrs={'placeholder': 'Ex: 60 dias úteis'}
                ),
            'form_payment': forms.TextInput(
                attrs={'placeholder': 'Ex: 50% entrada + 50% na entrega'}
                ),
            'information': forms.Textarea(
                attrs={'cols': 40,'style':'width: 100%; height: 100%; resize: none; !important;','title':'',
                    'placeholder': '*** Informe algo assim ***\nEstamos a mais de X anos no mercado de móveis planejados. Trabalhamos com materiais de primeira linha, respeitamos sempre o prazo de entrega e ofertando as melhores condições de pagamento.\n\n*** Proibido colocar o nome da marcenaria ou qualquer outro contato neste campo! ***'
                    }
                )


        }


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email','username','phone','cep','city','state','district']

