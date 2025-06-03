from django.contrib import admin
from .models import Abonent, Tarif, Tolov

@admin.register(Abonent)
class AbonentAdmin(admin.ModelAdmin):
    list_display = ('FIO', 'telefon', 'tarif', 'status')
    list_filter = ('status', 'tarif')
    search_fields = ('FIO', 'telefon')
    ordering = ('FIO',)

@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'narx')
    search_fields = ('nomi',)
    ordering = ('nomi',)

@admin.register(Tolov)
class TolovAdmin(admin.ModelAdmin):
    list_display = ('abonent', 'sana', 'summa')
    list_filter = ('sana',)
    search_fields = ('abonent__FIO', 'abonent__telefon')
    ordering = ('-sana',)
