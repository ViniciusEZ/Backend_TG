from django.core.management.base import BaseCommand, CommandError

from ... import models



class Command(BaseCommand):
    
    
    def add_arguments(self, parser):
        
        parser.add_argument('email')
        parser.add_argument('password')
    
    
    def handle(self, *args, **options):
        
        run(options)



def run(options):
    
    email = options['email']
    password = options['password']
    
    user = models.User(email=email)
    
    user.set_password(password)
    
    user.save()
    
    print('user pk', user.pk)