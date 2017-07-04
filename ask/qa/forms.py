from models import Answer, Question

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# class AskForm(ModelForm):
#
#     class Meta:
#         model = Question
#         fields = ['title', 'text']
#
#
# class AnswerForm(ModelForm):
#
#     class ModelChoiceFieldTitle(forms.ModelChoiceField):
#
#         def label_from_instance(self, obj):
#             return obj.title
#
#     question = ModelChoiceFieldTitle(queryset=Question.objects.all())
#
#     class Meta:
#         model = Answer
#         fields = ['question', 'text']


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea, max_length=128)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        user, _ = User.objects.get_or_create(username='x', defaults={'password': 'y'})

        q = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'], author=user)
        q.save()
        return q

    def clean(self):
        return self.cleaned_data


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Question.objects.all())

    def save(self):
        user, _ = User.objects.get_or_create(username='x', defaults={'password': 'y'})

        ans = Answer(text=self.cleaned_data['text'], question=self.cleaned_data['question'], author=user)
        ans.save()
        return ans

    def clean(self):
        pass


class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoggingForm(forms.Form):

    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': "Please enter a correct username and password.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        super(LoggingForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user:
                if self.user.is_active:
                    return self.cleaned_data
                else:
                    raise forms.ValidationError(
                        self.error_message['inactive'],
                        code='inactive',
                    )
            raise forms.ValidationError(
                self.error_message['invalid_login'],
                code='invalid_login',
            )

    def get_user(self):
    	return self.user
