from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Custom registration form
class RegisterForm(UserCreationForm):

    class Meta:
        model = User

        # Fields to include in the form
        fields = ['username', 'email', 'password1', 'password2']

    # Customize form fields (add CSS classes)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop through all fields and add class for styling
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })