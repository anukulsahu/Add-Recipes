from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login-page")
def recipes_home(request):
  if request.method == "POST":
    recipe_name = request.POST.get('recipe_name')
    recipe_description  =request.POST.get('recipe_description')
    recipe_image = request.FILES.get('recipe_image')

    Recipe.objects.create(
    recipe_name  =recipe_name,
    recipe_description = recipe_description,
    recipe_image = recipe_image
    )
    return redirect('/recipes-home')
  queryset = Recipe.objects.all()
  
  if request.GET.get('search'):
    queryset  = queryset.filter(recipe_name__icontains = request.GET.get('search'))

  context = {'recipes':queryset}
  return render(request,"recipe_home.html",context)  


def delete_recipe(request,id):
  queryset = Recipe.objects.get(id=id)
  queryset.delete()
  return redirect('/recipes-home')

@login_required(login_url="/login-page")
def update_recipe(request,id):
  queryset = Recipe.objects.get(id=id)
  if request.method == "POST":
    recipe_name = request.POST.get('recipe_name')
    recipe_description = request.POST.get('recipe_description')
    recipe_image = request.FILES.get('recipe_image')

    queryset.recipe_name = recipe_name
    queryset.recipe_description = recipe_description

    if(recipe_image):
      queryset.recipe_image = recipe_image
    queryset.save()
    return redirect('/recipes-home')

  context = {'recipe':queryset}
  return render(request, "update_recipe.html",context)


def login_page(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not User.objects.filter(username=username).exists() :
      messages.error(request,"Invalid username")
      return redirect('/login-page')
    
    user = authenticate(username=username,password=password)

    if user is None:
      messages.error(request,"Invalid Password")
      return redirect('/login-page')
    else:
      login(request,user)
      return redirect('/recipes-home')  
  return render(request,"login_page.html")

def logout_page(request):
  logout(request)
  return redirect('/login-page')


def register_page(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = User.objects.filter(username =username)
    if user.exists():
      messages.info(request, "Username already taken, try different username")
      return redirect('/register-page')

    user = User.objects.create(
      first_name=first_name,
      last_name=last_name,
      username=username
    )

    user.set_password(password)
    user.save()
    messages.info(request,"Account created successfully!")

  return render(request,"register_page.html")