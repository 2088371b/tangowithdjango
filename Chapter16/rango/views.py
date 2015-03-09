from django.shortcuts import render
from rango.models import Category
from rango.models import UserProfile
from rango.models import Page
from django.http import HttpResponse
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from rango.bing_search import run_query
from django.shortcuts import redirect


def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response
	
def about(request):
	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0

	# remember to include the visit data
	return render(request, 'rango/about.html', {'visits': count})
def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)
	
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat,"category_name_slug":category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)

def restricted(request):
    return render(request, 'rango/restricted.html',)
# Use the login_required() decorator to ensure only those logged in can access the view.
def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})
	
def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)
def register(request):

    registered = False

    if request.method == 'POST':

        profile_form = UserProfileForm(data=request.POST)
		
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
				
            profile.save()
            registered = True

        else:
            print profile_form.errors

    else:
        profile_form = UserProfileForm()

    return render(request,
            'rango/profile_registration.html',
            {'profile_form': profile_form, 'registered': registered} )
def profile(request):
	
		if not request.user.is_authenticated():
			return HttpResponse("You are not logged in")
		
		context_dict = {}
		user = request.user

		try:
			user_profile = UserProfile.objects.get( user = user )
			context_dict['user_profile'] = user_profile
		except:
			return HttpResponse("Non-existent profile")
			
		if request.method == 'POST':
			form = UserProfileForm(request.POST)
			form.fields['website'].initial = user_profile.website
			context_dict['form'] = form
			context_dict['picture'] = user_profile.picture
			
			if form.is_valid():
			
				newp = form.save(commit=False)
				newp.user = request.user
				
				if 'picture' in request.FILES:
					newp.picture = request.FILES['picture']
					
				try:
					newp.save()
					
				except:
					user_profile.delete()
					newp.save()
					
			else:
				print profile_form.errors
					
		else:
			form = UserProfileForm()
			form.fields['website'].initial = user_profile.website
			context_dict['form'] = form
			context_dict['picture'] = user_profile.picture
		return render(request, 'rango/profile.html', context_dict)
	
def otherprofile(request, username): 

	if username == request.user.username: 
		return profile(request) 
		
	context_dict = {} 
	
	try:
		user = User.objects.get(username=username) 
	except:
		return HttpResponse("No such username")
	
	uprofile = UserProfile.objects.get(user = user) 
	context_dict['username'] = username 
	context_dict['email'] = user.email 
	context_dict['website'] = uprofile.website 
	context_dict['picture'] = uprofile.picture 
	return render(request, 'rango/otherprofile.html', context_dict)
	