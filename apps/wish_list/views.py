
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
	if request.session.get('errors')==None:
		request.session['errors'] =[]
	return render(request, 'wish_list/index.html')

def login(request):
	errors = User.objects.login_validation(request.POST)

	if len(errors) != 0:
		request.session['errors'] = errors
		print errors
		return redirect('/')
	else:
		user= User.objects.login(request.POST)
		print 'Hello, '+user.name
		request.session['user_id'] = user.id
		request.session['name'] = user.name
		return redirect('/dashboard')

def register(request):
	errors = User.objects.registration_validation(request.POST)

	if len(errors) != 0:
		request.session['errors'] = errors
		print errors
		return redirect('/')
	else:
		user = User.objects.register(request.POST)
		print 'Hello, '+user.name
		request.session['user_id'] = user.id
		request.session['name'] = user.name
		return redirect('/dashboard')

def dashboard(request):
	user = User.objects.get(id=request.session['user_id'])
	exclude =[]
	context = {
      "user" : user,
      "myItems" : user.wantedItem.all(),
      "mylisteditems" : Item.objects.filter(listedBy=user),
      "otherItems" : Item.objects.exclude(listedBy=user).exclude(userWant=user),
    }
	
	return render(request, 'wish_list/dash.html', context)


def iteminfo(request):
	item = Item.objects.get(id=request.POST['item_id'])
 	context = {
 		"iteminfo" : item,
 		"moreinfo" : item.listedBy
 	}
	
	return render(request, 'wish_list/item.html', context)

def add(request):
	item = Item.objects.get(id=request.POST['item_id'])
 	user = User.objects.get(id=request.session['user_id'])
	item.userWant.add(user)
	print 'item added'
	return redirect('/dashboard')

def remove(request):
	item = Item.objects.get(id=request.POST['item_id'])
 	user = User.objects.get(id=request.session['user_id'])
	item.userWant.remove(user)
	print 'item removed'
	return redirect('/dashboard')

def delete(request):
	item = Item.objects.get(id=request.POST['item_id'])
	item.delete()
	print 'item deleted'
	return redirect('/dashboard')

def additem(request):
	return render(request, 'wish_list/create.html')


def create(request):
	errors = Item.objects.item_validation(request.POST)

	if len(errors) != 0:
		request.session['errors'] = errors
		print errors
		print 'So Many Errors'
		return redirect('/additem')
	else:
		item= Item.objects.addItem(request.POST,request.session['user_id'])
		print 'success'
		return redirect('/dashboard')


def logout(request):
	request.session.clear()
	return redirect('/')





