from django.contrib import admin

from guesswho.core import models


class GameAdmin(admin.ModelAdmin):
    pass


class PersonTraitInline(admin.TabularInline):
    model = models.PersonTrait


class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonTraitInline]


class TraitAdmin(admin.ModelAdmin):
    pass


class TraitValueAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Game, GameAdmin)
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Trait, TraitAdmin)
admin.site.register(models.TraitValue, TraitValueAdmin)
