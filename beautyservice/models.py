from django.db import models


class Salon(models.Model):
    title = models.CharField("Название", max_length=100)
    address = models.CharField(verbose_name="Адрес", max_length=100, blank=True)
    image = models.ImageField(
        "Изображение",
        upload_to="salons/",
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Салон красоты"
        verbose_name_plural = "Салоны красоты"


class Service(models.Model):
    name = models.CharField("Название", max_length=100)
    price = models.IntegerField("Цена")
    image = models.ImageField(
        "Изображение",
        upload_to="services/",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Тип услуги",
        related_name="services",
        db_index=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Category(models.Model):
    name = models.CharField("Тип услуги", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип услуги"
        verbose_name_plural = "Типы услуг"


class Master(models.Model):
    name = models.CharField("ФИО", max_length=100, unique=True)
    image = models.ImageField(
        "Изображение",
        upload_to="masters/",
        blank=True,
        null=True,
    )
    salon = models.ManyToManyField(
        Salon, related_name="masters", verbose_name="Салоны мастера"
    )
    profession = models.CharField(
        "Профессия",
        max_length=100,
        blank=True,
        null=True,
    )
    experience = models.CharField(
        "Стаж работы",
        max_length=100,
        blank=True,
        null=True,
    )
    service = models.ManyToManyField(
        Service, related_name="masters", verbose_name="Услуги мастера"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
