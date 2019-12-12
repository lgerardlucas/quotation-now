from django.contrib import admin
from qnow_user.models import User

# fields
# list_display
# list_filter
# search_fields

class UserAdmin(admin.ModelAdmin):
    # Campos que aparecerão ao entrar na model
    list_display = ('id','username','email','role','phone','cep','street','district','city','district','state')
    #list_display = ('id','name','email','role','phone','street','city')

    # Campo ou campos específico para usar como link de acesso aos dados
    list_display_links = ('username',)

    # Campos que aparecerão ao entra nos detalhes do model
    fields = ('username','email','is_active','role','phone','cep','street','district','city','state','password')

    # Campos que unidos são usados no processo de filtragem por seleção
    list_filter = ('city','district','state')   

    # Campos que unidos são usados no processo de filtragem por digitação
    search_fields = ('username','city','email')

    #readonly_fields = ('password',)

admin.site.register(User, UserAdmin)
