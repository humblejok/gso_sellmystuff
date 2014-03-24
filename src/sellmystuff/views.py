from django.shortcuts import render, redirect
from sellmystuff.models import Account, Advertisement, Attributes
from datetime import datetime
from django.http.response import HttpResponse
from django.contrib.auth.models import User
import simplejson

def index(request):
    account = None
    if request.user.is_authenticated and request.user.id!=None:
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
            # TODO: Handle naive datetime
            account.last_update = datetime.today()
            account.owner = User.objects.get(id=request.user.id)
            account.title = request.user.username
            account.type = Attributes.objects.get(identifier='ACCOUNT_TYPE_COMMON')
            account.save()
            redirect('/account_edition.html')
    context = {'account': account}
    return render(request, 'index.html', context)
    
def account_edition(request):
    # TODO: Handle bad access
    account = Account.objects.get(owner__id=request.user.id)
    all_ads = Advertisement.objects.filter(owner__id=account.id)
    context = {'account': account,'all_ads':all_ads}
    return render(request, 'account_edition.html', context)
    
def account_management(request):
    # TODO: Handle bad access
    account = Account.objects.get(owner__id=request.user.id)
    all_ads = Advertisement.objects.filter(owner__id=account.id)
    context = {'account': account,'all_ads':all_ads}
    return render(request, 'account_management.html', context)
    
def account_view(request):
    # TODO: Check user
    account = Account.objects.get(owner__id=request.user.id)
    all_ads = Advertisement.objects.filter(owner__id=account.id)
    context = {'account': account,'all_ads':all_ads}
    return render(request, 'account_view.html', context)

def advertisement_creation(request):
    # TODO: Check user
    account = Account.objects.get(owner__id=request.user.id)
    all_ads = Advertisement.objects.filter(owner__id=account.id)
    # TODO: Add limitation controls
    if len(all_ads)>=100:
        return HttpResponse('{"result": false, "message":"You''ve reached the maximum ads!"}', content_type="application/json")
    ad = Advertisement()
    ad.active = False
    # TODO: Determine default or prefered ad category
    ad.category = Attributes.objects.get(identifier='AD_CAT_GAMING_SOFT')
    ad.last_update = datetime.today()
    ad.sold = False
    ad.owner = account
    ad.sub_title = 'New ad...'
    ad.title = 'A brand new ad...'
    ad.type = Attributes.objects.get(identifier='AD_FIXED_PRICE')
    ad.save()
    context = {"current": ad}
    # TODO: Check if there is no more efficient way to do the inner rendition
    rendition = render(request, 'advertisement/advertisement_edition.html', context).content
    rendition = rendition.replace('\r','').replace('\n','').replace('\t','')
    return HttpResponse('{"result": true, "ad_id":' + str(ad.id) + ',"message":"Ad created without error", "rendition":"' + str(rendition) + '"}', content_type="application/json")

def advertisement_edition(request):
    None
    
def advertisement_view(request):
    None
    
def page_edition(request):
    None
    
def page_view(request):
    None
    
