# Action para marcas como respondido e devolver ao cliente a resposta
def check_email_contact(modeladmin, request, queryset):
    queryset.update(return_send=True)
check_email_contact.short_description = 'Action(Marcar os e-mails com resposta ao cliente)'

# Action para marcar como respondido sem enviar ao cliente
def check_email_contact_whith_return(modeladmin, request, queryset):
    queryset.update(return_send=True)
check_email_contact_whith_return.short_description = 'Action(Marcar os e-mails sem resposta ao cliente)'

# Action para marcas os e-mails respondidos 
def uncheck_email_contact(modeladmin, request, queryset):
    queryset.update(return_send=False)
uncheck_email_contact.short_description = 'Action(Desmarca os e-mails respondidos)'
