from django.contrib import admin
from qnow_user.models import User

# fields
# list_display
# list_filter
# search_fields

class UserAdmin(admin.ModelAdmin):
    # Campos que aparecerão ao entrar na model
    list_display = ('id','get_number_launch_client_liberado','get_number_launch_client_orcado','get_number_launch_client_aprovado',
    'username','email','role','phone','cep','street','district','city','state','approved','is_active','contract_accepted','contract_date_accepted','birth_date','get_birth_date_provider','delivery_time','form_payment')
    #list_display = ('id','name','email','role','phone','street','city')

    # Campo ou campos específico para usar como link de acesso aos dados
    list_display_links = ('username',)

    # Paginação para o listplay
    list_per_page = 30
    
    # Campos que aparecerão ao entra nos detalhes do model
    #fields = ('username','email','is_active','approved','role','phone','cep','street','district','city','state','password')


    # Campos que aparecerão ao entrar nos detalhes do model
    # Modo agrupado - Denomina um grupo de informações separada por um título
    fieldsets = (
        ('Cadastro',     {'fields': ('username','email','role',)}),
        ('Liberações',   {'fields': ('is_active','approved', )}),
        ('Endereçamento',{'fields': ('phone','cep','street','district','city','state',)}),
        ('Valores Padrões',{'fields': ('birth_date','delivery_time','form_payment','information',)}),
    )

    # Campos que unidos são usados no processo de filtragem por seleção
    list_filter = ('role','state','city','district')   

    # Campos que unidos são usados no processo de filtragem por digitação
    search_fields = ('pk','username','city','email','phone','cep','street','district','state','role')

    #readonly_fields = ('password',)

admin.site.register(User, UserAdmin)
