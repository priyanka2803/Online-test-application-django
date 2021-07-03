from django.contrib import admin

from .models import Subject,Test,Question,Option,Score

admin.site.register(Subject)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Score)
