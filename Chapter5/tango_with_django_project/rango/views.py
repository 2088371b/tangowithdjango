from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there world! <br/> <a href='/rango/about/'>about</a>")
def about(request):
	return HttpResponse("Rango says here is the about page <br/> <a href='/rango/index/'>index</a>"+"    This Tutorial has been put together by Jack Berreby, 2088371")
