from django import forms    
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact

        fields = (
            'name','email_send','subject_send','message_send','copy_send'
        )

        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Informe seu nome e sobrenome'}
                ),
            'email_send': forms.TextInput(
                attrs={'placeholder': 'Informe seu e-mail de contato'}
                ),
            'message_send': forms.Textarea(
                attrs={'cols': 40,'style':'width: 100%; height: 50%; resize: none; !important;',
                    'placeholder': 
                        'Dúvidas, reclamações, elogios podem ser sanadas nos enviando uma e-mail.\nDeixe o nº do telefone(Whats) que entraremos em contato.'
                    }
            )
        }
