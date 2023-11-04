from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


# Автоматическая фильтрация удалённых объектов
class OjectDelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


# "News" - текущий класс модели наследуется от класса models.Model,
# который определяет основное поведение моделей в рамках Django ORM.
# В модуле models также есть набор классов, который позволяет задать типы полей.
class News(models.Model):
    objects = OjectDelManager()
    title = models.CharField(max_length=256, verbose_name="Title")
    preambule = models.CharField(max_length=1024, verbose_name="Preambule")
    body = models.TextField(blank=True, null=True, verbose_name="Body")
    body_as_markdown = models.BooleanField(default=False, verbose_name="As markdown")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Edited", editable=False)
    deleted = models.BooleanField(default=False)

    # метод отвечет вид объекта (строковое представление объектов ) при печати "первичный ключ" "заголовок"
    # так будет отображаться список и в админке
    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    # Метод delete обеспечит установку свойства с последующим сохранением объекта
    def delete(self, *args):
        self.deleted = True
        self.save()

    # Корректировка отображения названия списка, относящегося к объектам модели, в административном разделе
    # Убираем в названии множественное число ("Newss" -> "News")
    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-created",)  # сортировка (дата создания) по убыванию. Сначала свежее


class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


# Связь "один ко многим" к одному курсу — множество уроков.
# Он реализуется через поле типа models.ForeignKey
class Courses(models.Model):
    objects = CoursesManager()

    name = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cost", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Cover")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Edited")
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    def delete(self, *args):
        self.deleted = True
        self.save()


# Есть связь с таблицей "Courses" - models.ForeignKey(Courses)
class Lesson(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Edited", editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        ordering = ("course", "num")  # Сортировка сначала по "course" а затем по "num"
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")


# Связь "многие ко многим" - models.ManyToManyField(Courses)
class CourseTeachers(models.Model):
    course = models.ManyToManyField(Courses)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(verbose_name="Birth date")
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)

    def delete(self, *args):
        self.deleted = True
        self.save()


# Модель отзывов "Feedback"
class CourseFeedback(models.Model):
    # "RATING" константа для данной модели
    RATING = ((5, "⭐⭐⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (3, "⭐⭐⭐"), (2, "⭐⭐"), (1, "⭐"))
    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, verbose_name=_("Course")
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("User")
    )
    feedback = models.TextField(
        default=_("No feedback"), verbose_name=_("Feedback")
    )
    rating = models.SmallIntegerField(
        choices=RATING, default=5, verbose_name=_("Rating")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} ({self.user})"
