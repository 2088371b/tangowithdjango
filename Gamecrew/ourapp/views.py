from django.shortcuts import render
from django.http import HttpResponse
from ourapp.models import Category
from ourapp.models import Game
from ourapp.models import Thread

def mainpage(request):
    category_list = Category.objects.order_by('name')[:5]
    game_list = Game.objects.order_by('views')[:5]
    context_dict = {'categories': category_list,'games': game_list}
	
    return render(request, 'ourapp/mainpage.html', context_dict)

def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        games = Game.objects.filter(category=category)
        context_dict['games'] = games
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'ourapp/category.html', context_dict)
	
def game(request, category_name_slug, gameID_slug):
    context_dict = {}
    try:
        game2 = Game.objects.get(slug=gameID_slug)
        context_dict['game_name'] = game2.name
        context_dict['threads'] = Thread.objects.filter(game=game2)
        context_dict['game'] = game2
    except Game.DoesNotExist:
        pass
    return render(request, 'ourapp/forums.html', context_dict)
	
def gamesearch(request):
    category_list = Category.objects.order_by('name')
    game_list = {}
    for category in category_list:
		games = Game.objects.filter(category=category)
		game_list[category] = games
    context_dict = {'categories': category_list, 'games' : game_list}
	
    return render(request, 'ourapp/gamesearch.html', context_dict)