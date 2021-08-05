from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():
        #conectam modelul si fields
        model = Post
        fields = ('author','title','text')

        #ADAUGAM WIDGETS - ESTE UN DICTIONAR
        #EX SA ADAUG UN BORDER ROSU PT 'text'
        #ASA SE CONECTEAZA LA O CSS -> IN CLASA META

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
            #VOR FI CONECTATE LA O CLASA CSS -> postcontent va fi propirul nostru class + textinputclass
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

    #LA FEL CA LA POST - widgets
    widgets = {
        'author':forms.TextInput(attrs={'class':'textinputclass'}),
        'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
    }
