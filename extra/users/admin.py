from django.contrib import admin

from .forms import Contact_usForm
from .models import User, Course, About_Edu, Contact_us, Location_Edu, User_Course, About_Edu_Media, CourseMedia

from import_export import resources
from import_export.admin import ExportActionMixin


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'phone_number', 'activity', 'telegram_id', 'phone_number2', 'date_joined')


class UserAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = UserResource
    fields = ('id', 'username', 'full_name', 'email', 'phone_number', 'activity', 'telegram_id', 'phone_number2', 'date_joined')
    readonly_fields = ('date_joined', 'id')

class UserCourseResource(resources.ModelResource):
    class Meta:
        model = User_Course
        fields = ('id', 'user_name', 'user_phone_number', 'user_phone_number2', 'course_name', 'course_type', 'date_joined')


class UserCourseAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = UserCourseResource
    fields = ('id', 'user_name', 'user_phone_number', 'user_phone_number2', 'course_name', 'course_type', 'date_joined')
    readonly_fields = ('date_joined', 'id')


class Contact_usAdmin(admin.ModelAdmin):
    form = Contact_usForm

    fieldsets = (
        ('Markaz ma\'lumotlari', {
            'fields': ('phone_number', 'email'),
        }),
        ('Telegram', {
            'fields': ('telegram_admin', 'telegram_chanel'),
        }),
        ('Ijtimoiy tarmoq', {
            'fields': ('instagram', 'you_tube'),
        }),
    )


class AboutEduMediaInline(admin.TabularInline):
    model = About_Edu_Media


@admin.register(About_Edu)
class ProductAdmin(admin.ModelAdmin):
    inlines = [AboutEduMediaInline]


class CourseInline(admin.TabularInline):
    model = CourseMedia


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseInline]


# Register your models here.
admin.site.register(Location_Edu)
admin.site.register(Contact_us, Contact_usAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(User_Course, UserCourseAdmin)
