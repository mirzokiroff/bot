from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import CharField, AutoField, BigIntegerField, Model, FileField, FloatField, DateTimeField, \
    BooleanField, URLField, TextField, ImageField, ForeignKey, CASCADE
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    id = AutoField(primary_key=True)
    full_name = CharField(verbose_name="F.I.SH", max_length=111, default='new_user', blank=True, null=True)
    username = CharField(verbose_name="Telegram username", unique=True, max_length=111, null=True, blank=True)
    phone_number = CharField(verbose_name="Telefon raqami", max_length=50, null=True, blank=True)
    telegram_id = BigIntegerField(unique=True, null=True, default=1, blank=True)
    date_joined = DateTimeField(null=True, blank=True, default=timezone.now)
    language = CharField(verbose_name="Tanlangan til", max_length=33, null=True, blank=True)
    confirmation_code = CharField(verbose_name="Tasdiqlash kodi", max_length=11, null=True, blank=True)
    location = CharField(verbose_name="Foydalanuvchi Manzili", max_length=222, null=True, blank=True)
    #
    last_login = DateTimeField(auto_now=True, null=True)
    password = CharField(max_length=111, null=True)
    is_superuser = BooleanField(default=False, null=True)
    first_name = CharField(verbose_name="Ism", max_length=111, default='new_user', null=True)
    last_name = CharField(verbose_name="Familya", max_length=111, default='new_user', null=True)
    email = CharField(verbose_name="Email", max_length=111, default='new_user@gmail.com', null=True)
    is_staff = BooleanField(default=False, null=True)
    is_active = BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.telegram_id} - {self.full_name}"


class Restaurant(Model):
    name = CharField(verbose_name="Restoran nomi", max_length=333, null=True, blank=True)
    location_latitude = FloatField(verbose_name="Lokatsiya Latidude", max_length=111, default=40.93639, null=True,
                                   blank=True)
    location_longitude = FloatField(verbose_name="Lokatsiya Longitude", max_length=111, default=68.76972, null=True,
                                    blank=True)
    location_text = TextField(verbose_name="Lokatsiya Matni", null=True, blank=True)
    location_video = FileField(verbose_name="Lokatsiya Videosi", upload_to='location/',
                               validators=[FileExtensionValidator(['mp4', 'mov', 'webm'])], blank=True, null=True)


class Course(Model):
    id = AutoField(primary_key=True)
    course_name = CharField(verbose_name="Kurs Nomi", max_length=111, blank=True)


class CourseMedia(Model):
    media = ForeignKey(Course, on_delete=CASCADE, null=True, blank=True)
    course_video = CharField(verbose_name="Kurs Videosi ID'si", blank=True, null=True)
    course_text = TextField(verbose_name="Kurs Matni", blank=True, null=True)
    course_photo = ImageField(verbose_name="Kurs Rasmi", upload_to='kurslar/', null=True, blank=True)
    course_pdf = FileField(verbose_name="Kurs PDF Fayl", upload_to='kurslar/', null=True, blank=True)


class User_Course(Model):
    id = AutoField(primary_key=True)
    user_name = CharField(verbose_name="Foydalanuvchi Ismi", max_length=111, default='new_user', null=True, blank=True)
    user_phone_number = CharField(verbose_name="Foydalanuvchi Telefon Raqami", max_length=50, null=True, blank=True)
    user_phone_number2 = CharField(verbose_name="Foydalanuvchi Aloqa raqami", max_length=50, null=True, blank=True)
    course_name = CharField(verbose_name="Kurslar", max_length=111, blank=True)
    course_type = CharField(verbose_name="Kurs Turi", max_length=33, null=True, blank=True)


class About_Edu(Model):
    description = TextField(verbose_name="text", null=True, blank=True)
    edu_photo = ImageField(verbose_name="Markaz Rasmi 1 dona", blank=True, null=True, upload_to='markaz/')


class About_Edu_Media(Model):
    media = ForeignKey(About_Edu, on_delete=CASCADE, null=True, blank=True)
    video = FileField(upload_to='markaz/', verbose_name='Markaz videosi',
                      validators=[FileExtensionValidator(['mp4', 'webm', 'mov'])], blank=True,
                      null=True)
    photo = ImageField(upload_to='markaz/', verbose_name='Markaz rasmi', blank=True, null=True)
    pdf_file = FileField(upload_to='markaz/', verbose_name='Markaz pdf', blank=True, null=True)


class Contact_us(Model):
    phone_number = CharField(verbose_name='Markaz telefon raqami', max_length=50, null=True, blank=True)
    telegram_admin = URLField(verbose_name="Telegram Admin", max_length=111, null=True, blank=True)
    telegram_chanel = URLField(verbose_name='Telegram Kanal', null=True, blank=True, max_length=111)
    instagram = URLField(verbose_name="Instagram", max_length=111, null=True, blank=True)
    you_tube = URLField(max_length=111, null=True, blank=True)
    email = CharField(max_length=111, null=True, blank=True)


class Location_Edu(Model):
    location_latitude = FloatField(verbose_name="Lokatsiya Latidude", max_length=111, default=41.3112)
    location_longitude = FloatField(verbose_name="Lokatsiya Longitude", max_length=111, default=69.2797)
    location_text = TextField(verbose_name="Lokatsiya Matni", null=True, blank=True)
    location_video = FileField(verbose_name="Lokatsiya Videosi", upload_to='location/',
                               validators=[FileExtensionValidator(['mp4', 'mov', 'webm'])], blank=True, null=True)
