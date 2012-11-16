__author__ = "Keith Lee"
__email__ = "keithlee002@gmail.com"

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError, Http404
from models import *
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from forms import RecipeForm
from django.contrib import messages,sessions
import mimetypes
from django.conf import settings
import re
from boto.s3.connection import S3Connection
from boto.s3.key import Key


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    recipeList = Recipe.objects.all().order_by('id')
    # If not even number of recipes add a page so that flipbook can close properly
    even = False
    if len(recipeList)%2 == 0:
        even = True 
    
    return render_to_response('shakeapp/index.html',{'recipeList': recipeList, 'even': even, 'dev':settings.DEV}, context_instance = RequestContext(request) )

def add(request):
    def storeInS3(recipe_id, filename, content):
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        b = conn.create_bucket(settings.S3BUCKET)
        mime = mimetypes.guess_type(filename)[0]
        k = Key(b)
        k.key = 'recipe_id_'+str(recipe_id) +'_'+filename 
        k.set_metadata("Content_Type", mime)
        content.seek(0)
        k.set_contents_from_file(content)
        k.set_acl("public-read")
        
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES )
        recipeName = request.POST['name']
        if Recipe.objects.filter(name=recipeName).count() > 0:
            messages.add_message(request, messages.ERROR,"The recipe name "+recipeName+" has been taken. Please choose another name for your recipe.")
            return render(request, 'shakeapp/add.html')
        if form.is_valid():
            newRecipe = form.save(commit=False)
            pictureFile = form.cleaned_data['picture']
            newRecipe.picture.save(pictureFile.name, pictureFile)
            filename = pictureFile.name 
            
            storeInS3(newRecipe.id, filename, pictureFile.file)
            newRecipe.url = settings.S3URL+'recipe_id_'+str(newRecipe.id)+"_"+filename
            newRecipe.save()
            return HttpResponseRedirect("/shakeapp/")
        else:
            print
            print form.errors
            messages.add_message(request, messages.ERROR,"There has been an error in the form. Please make sure your inputs are correct.")
            return render(request, 'shakeapp/add.html')
    return render_to_response('shakeapp/add.html',context_instance = RequestContext(request) )

#    return render_to_response('shakeapp/index.html', {'itemList':itemList},
#        context_instance=RequestContext(request))

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/shakeapp/')

def detail(request, recipe_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/shakeapp/')
    p = get_object_or_404(Recipe, pk=recipe_id)
    return render_to_response('shakeapp/detail.html', {'recipe':p}, 
        context_instance=RequestContext(request))

def like(request):
    post = request.POST.copy()
    if not request.user.is_authenticated() or not request.POST: 
        return HttpResponseRedirect('/shakeapp/')
    
    recipeId= post['recipe_id']
    user = request.user
    likedAlready = True
    recipe=Recipe.objects.get(id=recipeId)
    if RecipeLikes.objects.filter(user=user.id,recipe=recipeId).count() > 0:
        return render_to_response('shakeapp/detail.html', {'likedAlready':likedAlready, 'recipe':recipe}, 
            context_instance=RequestContext(request))
    #Create Likes table that keeps track of recipes that the users have liked. 
    #Extra username and recipename is for non-relational database compatability
    RecipeLikes.objects.create(user=User.objects.get(id=user.id), recipe=Recipe.objects.get(id=recipeId))
    qset = Recipe.objects.filter(id=recipeId)
    recipe = qset[0]
    recipe.numLikes = recipe.numLikes + 1
    recipe.save()
    return render_to_response('shakeapp/detail.html', {'recipe':recipe}, 
        context_instance=RequestContext(request))
    
def delete(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/shakeapp/')
    post = request.POST.copy()
    recipeId= post['recipe_id']
    p = get_object_or_404(Recipe, pk=recipeId)
    # Delete image file from s3
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    b = conn.get_bucket(settings.S3BUCKET)
    # Get filename from the end of the recipe url
    filename =re.sub(settings.S3URL,'', p.url)
    print filename
    b.delete_key(filename)
    Recipe.objects.filter(id=recipeId).delete()
    
    return HttpResponse('Recipe has been deleted. Refresh the page to update the Recipebook')

def random(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/shakeapp/')    
    recipeList = Recipe.objects.all().order_by('id')
    # If not even number of recipes add a page so that flipbook can close properly
    even = False
    if len(recipeList)%2 == 0:
        even = True 
        
    if request.method == "POST":
        post = request.POST.copy()
        if post.has_key('ingredient'):
            ingredient = post['ingredient']
            q = Recipe.objects.filter(ingredients__icontains=ingredient)
            # Ingredient is in atleast one recipe added.
            if q.count() > 0:
                randomNum = randint(0, q.count()-1)
                p = q[randomNum]
                return render_to_response('shakeapp/index.html', {'recipeRandom':p, 'recipeList':recipeList,'even':even,'dev':settings.DEV}, 
                    context_instance=RequestContext(request))
            else:
                return HttpResponseNotFound('<h1>Sorry no recipe uses \"%s\" as an ingredient' % ingredient)
    else:
        randomNum = randint(0, recipeList.count()-1)
        p = recipeList[randomNum]
        return render_to_response('shakeapp/index.html', {'recipeRandom':p, 'recipeList':recipeList, 'even':even, 'dev':settings.DEV}, 
                context_instance=RequestContext(request))

