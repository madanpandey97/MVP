import logging
import random
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, UserFollower
from dummy_data.user import user_list
from dummy_data.followers import follower_list
from dummy_data.products import product_list
from products.models import Product, ProductView


class Command(BaseCommand):
    help = "load user data"

    def add_user(self):
        time = timezone.now().strftime("%X")
        self.stdout.write("It's now %s" % time)
        dummy_phone = "+918709012345"
        for item in user_list:
            username = item["name"].split()[0]
            user = User.objects.create_user(
                username=username,
                email=f"{username}@gmail.com",
                fullname=item["name"],
                password=f"{username}123",
            )
            if user:
                print(f"user created with username {username}")

        total_user = User.objects.all().count()
        print(f"total user created-- {total_user}")

    def add_followers(self):
        user = User.objects.all()

        for item in follower_list:
            follower = UserFollower.objects.create(user=user.get(id=item["id"]))
            follower.followers.set(item["following"])
        fol = UserFollower.objects.all().count()
        print(f"follower added total length -- {fol}")

    def add_product(self):
        user = User.objects.all()
        description = """Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
                        when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
                        It has survived not only five centuries, but also the leap into electronic typesetting, 
                        remaining essentially unchanged. I"""
        for product in product_list:
            product = Product.objects.create(
                name=product["productName"],
                description=description,
                category_name=product["productCategory"],
                image=product["productImage"],
                in_stock=product["productStock"],
                sale_price=product["salePrice"],
                product_price=product["productPrice"],
                user=random.choice(user),
                last_updated_on=datetime.datetime.now(),
            )
        print("product data added")

    # def add_product_view_for_user(self):
    #     product = Product.objects.all()
    #     for item in product:
    #         product_view = ProductView.objects.create(product=item)
    #     print("table created for product View")

    def handle(self, *args, **kwargs):
        self.add_user()
        self.add_followers()
        self.add_product()
