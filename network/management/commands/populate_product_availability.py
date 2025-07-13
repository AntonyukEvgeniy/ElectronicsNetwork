import random

from django.core.management.base import BaseCommand
from django.db import transaction

from network.models import NetworkNode, Product, ProductAvailability


class Command(BaseCommand):
    help = "Заполняет таблицу ProductAvailability данными из Product и NetworkNode"

    def add_arguments(self, parser):
        parser.add_argument(
            "--min-quantity",
            type=int,
            default=0,
            help="Минимальное количество продукта",
        )
        parser.add_argument(
            "--max-quantity",
            type=int,
            default=100,
            help="Максимальное количество продукта",
        )

    def handle(self, *args, **options):
        min_quantity = options["min_quantity"]
        max_quantity = options["max_quantity"]
        with transaction.atomic():
            # Очищаем существующие записи
            ProductAvailability.objects.all().delete()
            nodes = NetworkNode.objects.all()
            availability_objects = []

            for node in nodes:
                # Для каждого узла берем все продукты его поставщика
                if node.parent:
                    supplier_products = Product.objects.filter(supplier=node.parent)
                else:
                    supplier_products = Product.objects.filter(supplier=node)
                for product in supplier_products:
                    quantity = random.randint(min_quantity, max_quantity)
                    availability = ProductAvailability(
                        product=product, network_node=node, quantity=quantity
                    )
                    availability_objects.append(availability)
            # Пакетное создание записей
            ProductAvailability.objects.bulk_create(availability_objects)
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано {len(availability_objects)} записей ProductAvailability"
            )
        )
