from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Ola, voce esta no index do app Q&A")

