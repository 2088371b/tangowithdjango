import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gamecrew.settings')
import django
django.setup()
from ourapp.models import Category, Game, Thread


def populate():
    fps_cat=add_cat("FPS")
    callofUK = add_game(cat=fps_cat,gameID=1,
       name="Call of Duty : Modern Warfare 2",server="UK",platform="Xbox 360")
    CSus = add_game(cat=fps_cat,gameID=2,
       name="Counter Strike : Global Offensive",server="US",platform="PC")
    add_thread(game = CSus, title="is there no one on this forum ?lol")
    moba_cat=add_cat("MOBA")
    lolEu = add_game(cat=moba_cat,gameID=3,
	   name="League of Legends",server="EU", platform="PC")
    add_thread(game = lolEu, title="is there no one on this forum ?lol")
    mmorpg_cat=add_cat("MMORPG")
    other_cat=add_cat("other")
    
    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Game.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_game(cat,gameID,name, views=0, server="World", platform= "PC"):
    g = Game.objects.get_or_create(category=cat,gameID=gameID, name=name, server=server, platform=platform)[0]
    g.views=views
    g.save()
    return g
def add_thread(game, title):
    t = Thread.objects.get_or_create(game=game,title=title)[0]
    return t
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()