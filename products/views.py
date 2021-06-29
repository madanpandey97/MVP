import logging
import random
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings as pagination_settings
from rest_framework import generics
from products import serializers
from products.models import Product, ProductView
from products import utils


class ProductListView(generics.ListAPIView):
    __doc__ = """
    List View for the product created by user
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.ProductListSerializer
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    def get_queryset(self, request, user):
        params = self.request.query_params
        sort_by = params.get("sort_by")
        order_by = params.get("order_by")
        if sort_by == "id" and order_by == "ascending":
            sort_text = "id"

        if sort_by == "id" and order_by == "descending":
            sort_text = "-id"

        if sort_by == "last_updated" and order_by == "ascending":
            sort_text = "updated"

        if sort_by == "last_updated" and order_by == "descending":
            sort_text = "-updated"

        if sort_by is None and order_by is None:
            sort_text = "-created"

        queryset = Product.objects.all().order_by(sort_text)
        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user
        logging.info(f"{user} requested to get the list of all product ")

        queryset = self.get_queryset(request, user)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class ProductDetailListView(generics.RetrieveAPIView):
    __doc__ = """
    Retrieve View for the product section
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        product_id = kwargs.get("pk")
        logging.info(f"{user} request to get details  of product of id {id}")
        queryset = Product.objects.filter(id=kwargs.get("pk")).first()
        serializer = self.serializer_class(queryset, context={"user": request.user})
        if queryset:
            utils.record_product_view(user, queryset)
            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        return Response(
            {"status": False, "message": "No Product with this Id exist"},
            status=status.HTTP_404_NOT_FOUND,
        )


class ProductCreateView(generics.CreateAPIView):
    __doc__ = """
    Create View for the product 
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductSerializer

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        user = request.user
        data = request.data
        data["user"] = user.id
        logging.info(f"{user} request to create product with  {data}")
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid(raise_exception=True):
            logging.info(f"{user} got error in creating product with {data}")
            return Response(
                {"status": False, "message": serializer.errors},
                status=status.HTTP_200_OK,
            )
        logging.info(f"{user} created product with data {data}")
        serializer.save()
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED
        )


class ProductUpdateView(generics.UpdateAPIView):
    __doc__ = """
    Update View for the product 
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductSerializer

    queryset = Product.objects.all()

    def put(self, request, *args, **kwargs):
        user = request.user
        data = self.partial_update(request, *args, **kwargs)
        logging.info(f"{user} request update product with data {request.data}")
        new_data = data.data
        return Response(
            {"status": True, "data": new_data},
            status=status.HTTP_200_OK,
        )


class RecommendProductView(APIView):
    __doc__ = """ api to get list of recommend_product based on random sampling """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductListSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user.id)
        followers_list = utils.get_user_followers(user)
        recommend_product = utils.product_viewed_by_friend(
            user, followers_list.followers.all()
        )
        print(followers_list.followers.all().values_list("id", flat=True))

        if len(recommend_product) > 5:
            recommend_product = random.sample(list(recommend_product), 5)

        serializer = self.serializer_class(recommend_product, many=True)
        return Response(
            {"status": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )
