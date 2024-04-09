from django.urls import path
from .import views

urlpatterns = [
    path('account/',views.show_account,name="account"),
    path('register/', views.show_account, name='register'),
  path('logout/', views.sign_out, name='logout')


]