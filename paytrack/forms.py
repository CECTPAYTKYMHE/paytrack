from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from Calendar.models import Profile

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Login',
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',
        }))
    
    class Meta:
        fields = ('username', 'password')
        
    def __init__(self, *args, **kwargs):
        super(UserLoginForm,self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
            
class UserRegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))
    telegram_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите id телеграмм',
                                                                'maxlength': "10",}))
    captcha = CaptchaField()

    
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        
    def clean_email(self):
    # Get the email
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует")
        return email
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm,self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
    
    

class UserForms(forms.ModelForm):
    
    class Meta:
        model = User
        
        fields = ('username', 'email', )
        widgets = {
            'username' : forms.TextInput(attrs={'class':"form-control",
                                                'disabled':'',
                                                'readonly':'',
                                                }),
            'email' : forms.TextInput(attrs={'class':"form-control",
                                                'disabled':'',
                                                'readonly':''
                                                })
        }
        
class ProfileForms(forms.ModelForm):
    
    class Meta:
        model = Profile
        
        fields = ('telegram_id', )
        widgets = {
            'telegram_id' : forms.TextInput(attrs={'class':"form-control",
                                                   'maxlength': "10",
                                                }),
            
        }
        
        
    
    
