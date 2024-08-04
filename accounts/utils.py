import random, string, re
from django.contrib.auth.models import User

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def create_username():
    while True:
        username = 'AccuKnox-' + ''.join(random.choices(string.digits + string.ascii_letters, k=16))
        if not User.objects.filter(username=username).exists():
            return username
        
def is_valid_email(email):
    return re.match(EMAIL_REGEX, email)