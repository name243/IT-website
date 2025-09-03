from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import redirect


def index(request):
    return render(request, 'women/index.html')
def materials(request):
    return render(request, 'women/materials.html')
def polit(request):
    return render(request, 'women/polit.html')
def register(request):
    return render(request, 'users/register.html')
def login(request):
    return render(request, 'users/login.html')




# запись в вк
def zapis(request):
    return redirect('https://vk.com/im?entrypoint=community_page&media=&sel=-219581481')

# оставить отзыв
def odzew(request):
    return redirect('https://vk.com/topic-219581481_53600644')



# группа вк, тг, ютуб.
def vk(request):
    return redirect('https://vk.com/ea_panfilov_it_studying?from=groups')
def tg(request):
    return redirect('https://t.me/ea_panfilov_IT_studying')
def youtube(request):
    return redirect('https://www.youtube.com/@ea_panfilov_IT_studying')


# файлы для подготовки
def cek_list(request):
    return redirect('https://disk.yandex.ru/i/QCjzLdqjAj-2Gw')
def demo_2026(request):
    return redirect('https://disk.yandex.ru/d/wa3XCA4C100aSg')

# Полезные ссылки
def rewy_ege(request):
    return redirect('https://inf-ege.sdamgia.ru/')
def rewy_ore(request):
    return redirect('https://inf-oge.sdamgia.ru/')
def vipi(request):
    return redirect('https://fipi.ru/ege/otkrytyy-bank-zadaniy-ege')
def polakov(request):
    return redirect('https://kpolyakov.spb.ru/school/ege/generate.htm')






