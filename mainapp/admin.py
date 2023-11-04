from django.contrib import admin
from mainapp import models as mainapp_models
from django.utils.translation import gettext_lazy as _


# Register your models here.

# регистрация приложения в админке (1-й способ)
# admin.site.register(mainapp_models.News)
# admin.site.register(mainapp_models.Lesson)

# регистрация модели (приложения) в админке (2-й способ):
# Регистрация модели через декоратора класса @admin.register(<имя_класса_модели>)
@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    # Поиск по содержимому
    search_fields = ["title", "preambule", "body"]  # Поля поиска


@admin.register(mainapp_models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", "get_course_name", "num", "title", "deleted"]  # вид отображения полей
    ordering = ["course__name", "-num"]  # сортировка

    # Пагинация страниц (Количество объектов на страницу)
    list_per_page = 10
    # фильтрация списка (появляется колонка справа страницы)
    list_filter = ["course", "created", "deleted"]
    actions = ["mark_deleted"]

    #
    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)
    # В заголовоке таблицы будет "Mark deleted"
    mark_deleted.short_description = _("Mark deleted")

    def get_course_name(self, obj):  # метод получения имени курса из таблицы "Courses"
        return obj.course.name
    # В заголовоке таблицы вместо названия поля "GET COURSE NAME" будет "COURSE"
    get_course_name.short_description = _("Course")
