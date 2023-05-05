from django import forms
from .models import Question

# use forms.Modelform so that we don't have to manually define the fields and widgets
class QuestionForm(forms.ModelForm):
    # form to handle user submitting answers
    class Meta:
        model = Question
        fields = ['question', 'opt1', 'opt2', 'opt3', 'opt4']
                #   'ans']
        widgets = {
            'question': forms.TextInput(attrs={'readonly': True}),
            'opt1': forms.RadioSelect(),
            'opt2': forms.RadioSelect(),
            'opt3': forms.RadioSelect(),
            'opt4': forms.RadioSelect(),
        }
