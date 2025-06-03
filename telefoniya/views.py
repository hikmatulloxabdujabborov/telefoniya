from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Abonent, Tolov, Tarif
from .serializers import AbonentSerializer, TolovSerializer, TarifSerializer
from django.shortcuts import render, redirect
from .forms import AbonentForm  # agar form bo‘lsa

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# Abonentlar ro'yxati sahifasi
@login_required
def abonentlar(request):
    abonentlar = Abonent.objects.all()
    context = {'abonentlar': abonentlar}
    return render(request, 'abonentlar.html', context)


# To'lovlar ro'yxati sahifasi
@login_required
def tolovlar_view(request):
    tolovlar = Tolov.objects.all()
    context = {'tolovlar': tolovlar}
    return render(request, 'tolovlar.html', context)


@login_required
def tolov_qoshish(request):
    abonentlar = Abonent.objects.all()  # form uchun abonentlar ro'yxati

    if request.method == 'POST':
        abonent_id = request.POST.get('abonent_id')
        summa = request.POST.get('summa')
        try:
            abonent = Abonent.objects.get(id=abonent_id)
            Tolov.objects.create(abonent=abonent, summa=summa)
            return redirect('tolovlar')
        except Abonent.DoesNotExist:
            error = 'Abonent topilmadi.'
            return render(request, 'tolov_qoshish.html', {'abonentlar': abonentlar, 'error': error})

    return render(request, 'tolov_qoshish.html', {'abonentlar': abonentlar})


# Foydalanuvchi login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Login yoki parol noto‘g‘ri'})
    return render(request, 'login.html')


# Foydalanuvchi logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# API Views uchun Rest Framework sinflari

class AbonentListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        abonentlar = Abonent.objects.all()
        serializer = AbonentSerializer(abonentlar, many=True)
        return Response(serializer.data)


class TarifListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tariflar = Tarif.objects.all()
        serializer = TarifSerializer(tariflar, many=True)
        return Response(serializer.data)


class TolovListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tolovlar = Tolov.objects.all()
        serializer = TolovSerializer(tolovlar, many=True)
        return Response(serializer.data)
