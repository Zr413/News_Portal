from django.views.generic.edit import CreateView
from .forms import SignUpForm
from news.models import Author

class SignUp(CreateView):
    model = Author
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'
