from django.core.validators import MinValueValidator
from django.db import models

class Product(models.Model):
    """Модель продукта."""
    name = models.CharField("Название", max_length=255)
    model = models.CharField("Модель", max_length=100)
    release_date = models.DateField("Дата выхода на рынок")
    supplier = models.ForeignKey(
        to="network.NetworkNode",
        on_delete=models.CASCADE,
        related_name="supplied_products",  # Изменено с "products" на "supplied_products"
        verbose_name="Поставщик",
    )
    price = models.DecimalField(
        "Цена", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "model"]
    def __str__(self):
        return f"{self.name} - {self.model}"

class NetworkNode(models.Model):
    """Модель узла сети (завод, дистрибьютор, дилер, розничная сеть)."""
    FACTORY = "factory"
    DISTRIBUTOR = "distributor"
    DEALER = "dealer"
    RETAIL = "retail"
    NODE_TYPES = [
        (FACTORY, "Завод"),
        (DISTRIBUTOR, "Дистрибьютор"),
        (DEALER, "Дилер"),
        (RETAIL, "Розничная сеть"),
    ]
    name = models.CharField("Название", max_length=255)
    products = models.ManyToManyField(
        Product,
        through="ProductAvailability",
        verbose_name="Продукты"
    )
    type = models.CharField("Тип", max_length=20, choices=NODE_TYPES)
    email = models.EmailField("Email")
    country = models.CharField("Страна", max_length=100)
    city = models.CharField("Город", max_length=100)
    street = models.CharField("Улица", max_length=255)
    building = models.CharField("Номер дома", max_length=20)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        "Задолженность перед поставщиком",
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    class Meta:
        verbose_name = "Узел сети"
        verbose_name_plural = "Узлы сети"
        ordering = ["name"]
    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"

class ProductAvailability(models.Model):
    """Модель наличия продукта в узле сети."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт"
    )
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        verbose_name="Узел сети"
    )
    quantity = models.PositiveIntegerField(
        "Количество",
        validators=[MinValueValidator(0)]
    )
    class Meta:
        verbose_name = "Наличие продукта"
        verbose_name_plural = "Наличие продуктов"
