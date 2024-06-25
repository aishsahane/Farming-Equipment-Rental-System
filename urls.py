from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView

urlpatterns = [
    path('', views.homeView , name ='home' ),
    path('register/' , views.signup , name = 'register'),
    path('login/' , views.user_login , name = 'login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('addproduct/' , views.create_product , name = 'addproduct'),
    path('productlist/' , views.product_list , name = 'productlist'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('booking/<int:pk>', views.book_product, name = 'book_product'),
    path('delete_product/<int:pk>/', views.delete_product, name = 'delete_product'),
    # path('crop_predict/', views.prediction, name='prediction'),
    path('predict_crop/', views.predict_crop, name='predict_crop'),

    path('forgot-password/', CustomPasswordResetView.as_view(), name='forgot_password'),


    path('forgot-password/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('forgot-password/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('forgot-password/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('forgot-password/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('bookingsuccess', vie)
]
