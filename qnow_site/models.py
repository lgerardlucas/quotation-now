from django.db import models
from datetime import date

class Contact(models.Model):
    # Usuário do contato
    name = models.CharField('Nome*',max_length=100, blank=False)

    # Data do envio
    date_send = models.DateField('Data do Envio',default=date.today)

    # Email do contato
    email_send = models.EmailField('E-mail*',max_length=100,blank=False)

    # Assunto
    SUBJECTCHOICES = (
    ('Elogio', 'Elogio'),
    ('Diverso', 'Diverso'),
    ('Dúvida', 'Dúvida'),
    ('Reclamação', 'Reclamação'),
    )
    subject_send = models.CharField('Assunto*',choices=SUBJECTCHOICES,max_length=100, blank=False)

    # Texto do email
    message_send  = models.TextField('Mensagem*',blank=False)

    # Cópia ao remetente
    copy_send = models.BooleanField('Enviar cópia',default=True)

    # Email retornado - Reposta ao cliente
    return_send = models.BooleanField('E-mail respondido?',default=False)

    # Texto de resposta ao e-mail do contato
    message_return = models.TextField('Resposta*',blank=False,default='')

    # Data da última ação
    date_update = models.DateField('Última ação',auto_now=True)


    class Meta:
        verbose_name = 'E-mail de contato'
        verbose_name_plural = 'E-mails de contatos'
        ordering = ["-date_send"]

    def __str__(self):
        return str(self.name)

