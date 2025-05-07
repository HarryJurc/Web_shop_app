from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Удаляет все данные и добавляет тестовые продукты'

    def handle(self, *args, **kwargs):
        self.stdout.write("Удаляем все данные из базы...\n")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Создаем категории...\n")
        electronics = Category.objects.create(name="Электроника", description="Товары для дома и офиса")
        clothes = Category.objects.create(name="Одежда", description="Модная одежда для всех")

        self.stdout.write("Добавляем тестовые продукты...\n")
        Product.objects.create(
            name="Смартфон",
            description="Современный смартфон с большим экраном.",
            image="images/smartphone.jpg",
            category=electronics,
            price=19999.99
        )
        Product.objects.create(
            name="Футболка",
            description="Комфортная футболка с принтом.",
            image="images/tshirt.jpg",
            category=clothes,
            price=499.99
        )

        self.stdout.write(self.style.SUCCESS("Тестовые продукты успешно добавлены!"))
