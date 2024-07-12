from django.contrib import admin
from .models import *

admin.site.register(Room)
admin.site.register(Instructor)
admin.site.register(MeetingTime)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Section)
admin.site.register(TimeTableModel)
admin.site.register(Batch)  # Registering the Batch model
@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')