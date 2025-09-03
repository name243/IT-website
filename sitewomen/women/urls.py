from django.urls import path
from women import views

urlpatterns = [
    path('', views.index, name='index'),
    path('materials/', views.materials, name='materials'),
    path('odzew/', views.odzew, name='odzew'),
    path('zapis/', views.zapis, name='zapis'),
    path('polit/', views.polit, name='polit'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),


    path('vk/', views.vk, name='vk'),
    path('tg/', views.tg, name='tg'),
    path('youtube/', views.youtube, name='youtube'),

    path('cek-list/', views.cek_list, name='cek-list'),
    path('demo-2026/', views.demo_2026, name='demo-2026'),
    path('rewy-ege/', views.rewy_ege, name='rewy-ege'),
    path('rewy-ore/', views.rewy_ore, name='rewy-ore'),
    path('vipi/', views.vipi, name='vipi'),
    path('polakov/', views.polakov, name='polakov'),
]
