from django.contrib import admin
from .models import Bb, Rubric, AdvUser, Machine, Spare, Measure, Comment, Note, Img

class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'price', 'published', 'title_and_price')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

admin.site.register(Rubric)
admin.site.register(Comment)
admin.site.register(AdvUser)
admin.site.register(Machine)
admin.site.register(Spare)
admin.site.register(Measure)
admin.site.register(Note)
admin.site.register(Img)
admin.site.register(Bb, BbAdmin)

