from django.db import models
from django.utils.html import mark_safe
# Create your models here.

class Worker(models.Model):
    """Модель сотрудника"""
    id = models.BigAutoField(verbose_name='Идентификатор сотрудника', primary_key=True)
    lastName = models.CharField(verbose_name='Фамилия', max_length=20)
    firstName = models.CharField(verbose_name='Имя', max_length=20)
    patronymic = models.CharField(verbose_name='Отчество', max_length=20)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.lastName} {self.firstName} {self.patronymic}'

class Client(models.Model):
    """Модель клиента"""
    id = models.BigAutoField(verbose_name='Идентификатор клиента', primary_key=True)
    lastName = models.CharField(verbose_name='Фамилия', max_length=20)
    firstName = models.CharField(verbose_name='Имя', max_length=20)
    patronymic = models.CharField(verbose_name='Отчество', max_length=20)
    document = models.CharField(verbose_name='Документ', max_length=80)
    serial = models.CharField(verbose_name='Серия документа', max_length=10)
    number = models.CharField(verbose_name='Номер документа', max_length=20)
    date = models.DateField(verbose_name='Дата выдачи')
    region = models.CharField(verbose_name='Кем выдан документ', max_length=30)
    born = models.DateField(verbose_name='Дата рождения')
    picture = models.ImageField(verbose_name='Фотография клиента', upload_to='img')
    passport = models.BooleanField(verbose_name='Наличие заграничного паспорта', default=False)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.lastName} {self.firstName} {self.patronymic}'

    # def get_fullname(self):
    #     return f'{self.lastName} {self.firstName} {self.patronymic}'
    # get_fullname.short_description = 'ФИО'

    def image_tag(self):
        if self.pk is None:
            image = '<p>Предпросмотр пока не доступен, загрузите изображение и сохраните объект</p>'
        else:
            image = f'<a href="/media/{self.picture}">' \
                    f'<img src="/media/{self.picture}" width="30%" />' \
                    '</a>'
        return mark_safe(image)
    image_tag.short_description = 'Изображение'
    image_tag.allow_tags = True


class Hotel(models.Model):
    """Модель гостиницы"""
    name = models.CharField(verbose_name='Название гостиницы', max_length=20)
    type = models.IntegerField(verbose_name='Класс гостиницы (***, ****)')
    address = models.CharField(verbose_name=' Адрес гостиницы', max_length=100)

    def __str__(self):
        return f'{self.name} - {self.address}'

    class Meta:
        verbose_name = 'Гостиница'
        verbose_name_plural = 'Гостиницы'


class Route(models.Model):
    """Модель маршрута"""
    id = models.BigAutoField(verbose_name='Идентификатор маршрута', primary_key=True)
    routeName = models.CharField(verbose_name='Название маршрута', max_length=30)
    country = models.CharField(verbose_name='Название страны', max_length=30)
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    period = models.IntegerField(verbose_name='Срок пребывания(дни)', default=0)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Представитель на маршруте', max_length=20)
    cost = models.IntegerField(verbose_name='Стоимость путевки', default=0)
    exempt = models.IntegerField(verbose_name='Скидка', default=0)
    amount = models.IntegerField(verbose_name='Конечная стоимость', default=0)
    returnCost = models.IntegerField(verbose_name='Неустойка', default=0)
    dateStart = models.DateTimeField(verbose_name='Дата вылета')
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return self.routeName


    def get_towns(self):
        return " - ".join([o.town for o in RoutePoint.objects.filter(route=self.id)])
    get_towns.short_description = 'Города'



class RoutePoint(models.Model):
    """Модель пункта маршрута"""
    route = models.ForeignKey(Route, verbose_name='Маршрут', on_delete=models.CASCADE)
    town = models.CharField(verbose_name='Пункт маршрута', max_length=20)
    count = models.IntegerField(verbose_name='Срок пребывания в пункте маршрута')
    hotel = models.ForeignKey(Hotel, verbose_name='Гостиница', on_delete=models.CASCADE)
    startDate = models.DateTimeField(verbose_name='Дата прибытия в пункт маршрута')
    stopDate = models.DateTimeField(verbose_name='Дата убытия')
    comment = models.TextField(verbose_name='Экскурсионная программа')

    class Meta:
        verbose_name = 'Пункт маршрута'
        verbose_name_plural = 'Пункты маршрутов'