import datetime

from _decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Section(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='Необходимо ввести название раздела',
        unique=True,
        verbose_name='Название раздела',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def get_absolut_url(self):
        return reverse('section', args=[self.id])

    def __str__(self):
        return self.title


class Product(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, verbose_name='Раздел')
    title = models.CharField(max_length=70, verbose_name='Название')
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)],
        verbose_name='Год'
    )

    country = models.CharField(max_length=70, verbose_name='Страна')
    director = models.CharField(max_length=70, verbose_name='Режисер')
    play = models.IntegerField(
        validators=[MinValueValidator(180)],
        null=True,
        blank=True,
        verbose_name='Продолжительность',
        help_text='В секундах',
    )
    cast = models.TextField(verbose_name='В ролях')
    description = models.TextField(verbose_name='Описание')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        ordering = ['title', '-year']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.section.title)


class Discount(models.Model):
    code = models.CharField(max_length=10, verbose_name='Код купона')
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Размер скидки',
        help_text='В процентах'
    )

    class Meta:
        ordering = ['-value']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def value_percent(self):
        return str(self.value)+'%'

    def __str__(self):
        return str(self.code) + ' (' + str(self.value) + '%'

    value_percent.short_description = 'Размер скидки'

class Order(models.Model):
    need_delivery = models.BooleanField(verbose_name='Необходима доставка')
    discount = models.ForeignKey(Discount, verbose_name='Скидка', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=70, verbose_name='Имя')
    phone = models.CharField(max_length=70, verbose_name='Телефон')
    email = models.EmailField(max_length=70)
    address = models.TextField(blank=True, verbose_name='Адрес')
    notice = models.TextField(blank=True, verbose_name='Примечания к заказу')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    date_send = models.DateTimeField(null=True, blank=True, verbose_name='Дата отправки')

    STATUS = [
        ('NEW', 'Новый заказ'),
        ('APR', 'Подтвержден'),
        ('PAY', 'Оплачен'),
        ('CNL', 'Отменен'),
    ]

    status = models.CharField(choices=STATUS, max_length=3, default='NEW', verbose_name='Статус')

    class Meta:
        ordering = ['-date_order']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def display_products(self):
        display = ''
        for order_line in self.orderline_set.all():
            display += '{0}: {1} шт.; '.format(order_line.product.title,order_line.count)
        return display


    def display_amount(self):
        amount = 0
        for order_line in self.orderline_set.all():
            amount += order_line.price *order_line.count
        if self.discount:
            amount = round(amount * Decimal(1 - self.discount.value / 100))

        return '{0} руб'.format(amount)

    def __str__(self):
        return 'ID: ' + str(self.id)

    display_products.short_description ='Состав заказа'
    display_amount.short_description = 'Сумма'

class OrderLine(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    count = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказов'

    def __str__(self):
        return 'Заказ (ID {0}) {1}: {2} шт.'.format(self.order.id, self.product.title, self.count)
