from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import Question, Answer, Comment

class SignupForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username','email','password1','password2')

	def save(self, commit=True):
		user = super(UserCreationForm,self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class LoginForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ('username','password')


class EditDetailForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('email',)


class ChangePasswordForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('password1','password2')




class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('text',)


class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ('text',)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)



