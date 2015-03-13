from django.contrib import admin
from ourapp.models import Category, Game, Thread

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
	
admin.site.register(Category, CategoryAdmin)
admin.site.register(Game)
admin.site.register(Thread)

