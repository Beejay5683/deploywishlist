
from __future__ import unicode_literals

from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):

	def login_validation(self, form_data):
		errors = []
		user = User.objects.filter(username = form_data['username']).first()
		if user:
			pw = str(form_data['password'])
			user_password = str(user.password)
			pw_check = bcrypt.hashpw(pw.encode(), user_password.encode())
			if not user_password == pw_check:
				errors.append('Ivalid Password')
		else: 
			errors.append('Invalid Username')

		return errors

	def registration_validation(self, form_data):
		errors = []

		if len(form_data['name']) < 2:
			errors.append('Name Required')
		if len(form_data['username']) < 2:
			errors.append('Username Required')
		if len(form_data['password']) < 8:
			errors.append('password should be more than 8 characters')
		if form_data['confirm_password'] <8:
			errors.append('confirmed password should be more than 8 characters')
		if form_data['password'] != form_data['confirm_password']:
			errors.append('Passwords do not match')
		duplicate = User.objects.filter(username = form_data['username'])
		if len(duplicate) == 1:
			errors.append('Username already exisits')
		if len(form_data['hireDate']) == 0:
			errors.append('Must Provide Hire Date')

		return errors

	def register(self, form_data):
		pw = str(form_data['password'])
		h_pw = bcrypt.hashpw(pw, bcrypt.gensalt())

		user = User.objects.create(
			name = form_data['name'],
			username = form_data['username'],
			password = h_pw,
			hireDate= form_data['hireDate'],
		)
		return user

	def login(self, form_data):
		user = User.objects.filter(username= form_data['username'])[0]
		return user

class ItemManager(models.Manager):

	def item_validation(self, form_data):
		errors = []

		if len(form_data['item']) < 3:
			errors.append('Item Required')
		return errors

	def addItem(self, form_data, user_id):
		item = Item.objects.create(
			item = form_data['item'],
			listedBy = User.objects.get(id=user_id),
		)
		return item

class User(models.Model):
	name = models.CharField(max_length=45)
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	hireDate = models.DateField()
	created_at = models.DateField(auto_now_add=True)
  	updated_at = models.DateField(auto_now=True)
  	objects = UserManager()

	def __unicode__(self):
		return "id: " + str(self.id)+", Name: "+self.name+", Username: "+ self.username+", password: " + self.password

class Item(models.Model):
	item = models.CharField(max_length=45)
	listedBy = models.ForeignKey(User, related_name="listedItem")
	userWant = models.ManyToManyField(User, related_name="wantedItem")
	created_at = models.DateTimeField(auto_now_add=True)
  	updated_at = models.DateTimeField(auto_now=True)
  	objects = ItemManager()

  	def __unicode__(self):
		return "id: " + str(self.id)+", Item: "+self.item


