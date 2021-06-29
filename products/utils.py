import datetime
from products.models import ProductView, Product
from core.models import User, UserFollower


def product_directory_path(instance, filename):
    # upload to user product directory
    return f"user_{instance.user.id}/{filename}"


def get_user_followers(user):
    user_followers = UserFollower.objects.get(user=user)
    return user_followers


def product_viewed_by_friend(user, friend_list):
    product_list = list()
    for friend in friend_list:
        product_view = list(
            ProductView.objects.filter(user=friend, view_count__gte=0).values_list(
                "product", flat=True
            )
        )
        product_list.extend(product_view)
    product_list = Product.objects.filter(id__in=set(product_list))
    return product_list


def record_product_view(user, product):
    product_view_object, created = ProductView.objects.update_or_create(
        product=product, user=user
    )
    product_view_object.view_count += 1
    product_view_object.last_viewed_on = datetime.datetime.now()
    product_view_object.save()
