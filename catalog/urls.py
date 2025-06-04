from django.urls import path
from .views import (
    HomeView, ContactsView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    unpublish_product, ProductsByCategoryView, DraftProductsListView,
    publish_product, delete_product_from_detail
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/delete-from-detail/', delete_product_from_detail, name='product_delete_from_detail'),
    path('product/<int:pk>/unpublish/', unpublish_product, name='product_unpublish'),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('drafts/', DraftProductsListView.as_view(), name='drafts_list'),
    path('product/<int:pk>/publish/', publish_product, name='product_publish'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)