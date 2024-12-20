from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Salon(models.Model):
    title = models.CharField(
        "Название",
        max_length=100
        )
    address = models.CharField(
        "Адрес",
        max_length=100,
        blank=True
        )
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
    name = models.CharField(
        "Тип услуги",
        max_length=100
        )

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
        Salon,
        related_name="masters",
        verbose_name="Салоны мастера"
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
        Service,
        related_name="masters",
        verbose_name="Услуги мастера"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"


class Client(models.Model):
    name = models.CharField(
        'Имя',
        max_length=255,
        db_index=True
    )
    phone = PhoneNumberField(
        'телефон',
        db_index=True
    )

    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Schedule(models.Model):
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    date = models.DateField(
        "Дата"
    )
    time = models.TimeField(
        "Время"
    )
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.master.name

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"


class Note(models.Model):
    salon = models.ForeignKey(Salon,
                              on_delete=models.CASCADE,
                              related_name='notes',
                              verbose_name='Салон')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='notes',
                               verbose_name='Клиент')
    master = models.ForeignKey(Master,
                               on_delete=models.CASCADE,
                               related_name='notes',
                               verbose_name='Мастер')
    service = models.ForeignKey(Service,
                                on_delete=models.CASCADE,
                                verbose_name='Услуга')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                blank=True,
                                verbose_name='Итоговая цена')
    date = models.DateField(
        "Дата записи",
        blank=True,
        null=True
    )
    time = models.TimeField(
        "Время записи",
        blank=True,
        null=True
    ) 
    created_at = models.DateTimeField(verbose_name='Дата создания',
                                      auto_now=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'