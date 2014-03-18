from django.shortcuts import render, redirect
from sellmystuff.models import Account, Advertisement, Attributes
from datetime import datetime

def index(request):
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(owner__id=request.user.id)
        except:
            # Create account
            account = Account()
            account.active = True
            account.creation_date = datetime.today()
            account.currency = Attributes.objects.get(identifier='CURR_EUR')
            account.country = Attributes.objects.get(identifier='ISO2_COUNTRY_FR')
            account.expiry_date = None
            account.last_update = datetime.today()
            account.owner = request.user
            account.title = request.user.username
            account.type = Attributes.objects.get(identifier='ACCOUNT_TYPE_COMMON')
            account.save()
            redirect('/account_edition.html')
    context = {'account': account}
    return render(request, 'index.html', context)
    
def account_edition(request):
    # TODO Handle bad access
    account = Account.objects.get(owner__id=request.user.id)
    context = {'account': account}
    return render(request, 'account_edition.html', context)
    
def account_management(request):
    None
    
def account_view(request):
    # TODO Check user
    account = Account.objects.get(owner__id=request.user.id)
    all_ads = Advertisement.objects.filter(owner__id=account.id)
    context = {'account': account,'all_ads':all_ads}
    return render(request, 'account_view.html', context)
    
def advertisement_edition(request):
    None
    
def advertisement_view(request):
    None
    
def page_edition(request):
    None
    
def page_view(request):
    None
    
