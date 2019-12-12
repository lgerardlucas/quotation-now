# Action para remover cotações selecionadas
def remove_quotation(modeladmin, request, queryset):
    queryset.update(removed=True)
remove_quotation.short_description = 'Action(Remover cotações)'

# Action para remover cotações selecionadas
def return_quotation(modeladmin, request, queryset):
    queryset.update(removed=False)
return_quotation.short_description = 'Action(Retornar cotações)'