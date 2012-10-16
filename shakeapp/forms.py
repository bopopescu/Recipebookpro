from django.forms import ModelForm
from models import User
from shakeapp.models import Recipe
from django.template.loader import *

class RecipeForm(ModelForm):    
    class Meta:
        model = Recipe
        fields = ('name', 'picture', 'ingredients', 'instruction', 'cookHour', 'cookMin')
#    def as_p(self):
#         return render_to_string('forms/form.html')