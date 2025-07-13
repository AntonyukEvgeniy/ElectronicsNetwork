import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from network.models import NetworkNode, Product

fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Заполняет базу данных случайными тестовыми данными"

    def handle(self, *args, **options):
        self.stdout.write("Начало заполнения базы данных...")

        try:
            with transaction.atomic():
                # Создаем заводы
                factories = []
                for _ in range(5):
                    factory = NetworkNode.objects.create(
                        name=f"Завод {fake.company()}",
                        type=NetworkNode.FACTORY,
                        email=fake.email(),
                        country=fake.country(),
                        city=fake.city(),
                        street=fake.street_name(),
                        building=str(fake.building_number()),
                    )
                    factories.append(factory)
                # Создаем розничные сети
                retail_networks = []
                for _ in range(10):
                    retail = NetworkNode.objects.create(
                        name=f"Сеть {fake.company()}",
                        type=NetworkNode.RETAIL,
                        email=fake.email(),
                        country=fake.country(),
                        city=fake.city(),
                        street=fake.street_name(),
                        building=str(fake.building_number()),
                    )
                    retail_networks.append(retail)
                # Создаем поставщиков (дистрибьюторы и дилеры)
                suppliers = []
                for _ in range(50):
                    supplier_type = random.choice(
                        [NetworkNode.DISTRIBUTOR, NetworkNode.DEALER]
                    )
                    parent = random.choice(
                        factories
                        if supplier_type == NetworkNode.DISTRIBUTOR
                        else factories + suppliers
                    )

                    supplier = NetworkNode.objects.create(
                        name=f"{'Дистрибьютор' if supplier_type == NetworkNode.DISTRIBUTOR else 'Дилер'} "
                        f"{fake.company()}",
                        type=supplier_type,
                        email=fake.email(),
                        country=fake.country(),
                        city=fake.city(),
                        street=fake.street_name(),
                        building=str(fake.building_number()),
                        parent=parent,
                        debt=Decimal(random.uniform(0, 1000000)).quantize(
                            Decimal("0.01")
                        ),
                    )
                    suppliers.append(supplier)
                # Создаем продукты
                products = []
                all_suppliers = factories + suppliers
                for _ in range(10000):
                    release_date = datetime.now() - timedelta(
                        days=random.randint(1, 1000)
                    )
                    product = Product.objects.create(
                        name=fake.word(),
                        model=f"Model-{fake.bothify(text='??-###')}",
                        release_date=release_date,
                        supplier=random.choice(all_suppliers),
                        price=Decimal(random.uniform(100, 100000)).quantize(
                            Decimal("0.01")
                        ),
                    )
                    products.append(product)
                self.stdout.write(self.style.SUCCESS("База данных успешно заполнена"))
                self.stdout.write("Создано:")
                self.stdout.write(f"- Заводов: {len(factories)}")
                self.stdout.write(f"- Розничных сетей: {len(retail_networks)}")
                self.stdout.write(f"- Поставщиков: {len(suppliers)}")
                self.stdout.write(f"- Продуктов: {len(products)}")
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при заполнении базы данных: {str(e)}")
            )
