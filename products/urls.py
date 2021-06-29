from django.urls import path, include

from products import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('crud', views.ProductViewSet, basename="product_routes")

urlpatterns = [
    # path(
    #     "list/",
    #     views.ProductListView.as_view(),
    #     name="product-list",
    # ),
    # path("retrieve/<int:pk>/", views.ProductDetailListView.as_view()),
    # path("create/", views.ProductCreateView.as_view()),
    path("recommend_product/", views.RecommendProductView.as_view()),
    # path("update/<int:pk>/", views.ProductUpdateView.as_view()),
    path('products/', include(router.urls))
]
