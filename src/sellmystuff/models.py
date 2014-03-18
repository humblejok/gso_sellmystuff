from django.db import models
import logging
from django.contrib.auth.models import User

LOGGER = logging.getLogger(__name__)

class CoreModel(models.Model):

    def get_editable_fields(self):
        values = []
        for field in self.get_fields():
            if self._meta.get_field(field).get_internal_type()!='ManyToManyField':
                values.append(field)
        return values
        
    def get_associable_field(self):
        values = []
        for field in self.get_fields():
            if self._meta.get_field(field).get_internal_type()=='ManyToManyField':
                values.append(field)
        return values        

    def get_fields(self):
        return []
    
    def get_identifier(self):
        return 'name'
    
    def list_values(self):
        values = []
        for field in self.get_fields():
            LOGGER.debug(self.__class__.__name__ + ' * ' + field)
            if field in self._meta.get_all_field_names():
                if self._meta.get_field(field).get_internal_type()=='ManyToManyField' and getattr(self,field)!=None:
                    values.append(str([e.list_values() for e in list(getattr(self,field).all())]))
                elif self._meta.get_field(field).get_internal_type()=='ForeignKey' and getattr(self,field)!=None:
                    values.append(getattr(self,field).get_value())
                else:
                    values.append(str(getattr(self,field)))
            else:
                # Generic foreign key
                values.append(getattr(self,field).get_value())
        return values
    
    def get_value(self):
        if self.get_identifier()!=None:
            return getattr(self, self.get_identifier())
        else:
            return None
        
    def __unicode__(self):
        return unicode(self.get_value())
    
    class Meta:
        ordering = ['id']
    
class Attributes(CoreModel):
    identifier = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=32)
    type = models.CharField(max_length=64)
    active = models.BooleanField()
    
    def get_fields(self):
        return ['identifier','name','short_name','type','active']
    
    class Meta:
        ordering = ['name']


class Account(CoreModel):
    owner = models.ForeignKey(User, related_name='account_owner_rel')
    title = models.TextField(max_length=128)
    type = models.ForeignKey(Attributes, limit_choices_to={'type':'account_type'}, related_name='account_type_rel')
    creation_date = models.DateTimeField()
    last_update = models.DateTimeField()
    expiry_date = models.DateTimeField(null=True, blank=True)
    currency = models.ForeignKey(Attributes, limit_choices_to={'type':'currency'}, related_name='account_currency_rel')
    active = models.BooleanField()

    def get_fields(self):
        return ['owner','title','type','creation_date','last_update','expiry_date','currency','active']
    
    class Meta:
        ordering = ['title']

class Comment(CoreModel):
    content = models.TextField()
    type = models.ForeignKey(Attributes, limit_choices_to={'type':'comment_type'}, related_name='comment_type_rel')
    reference = models.ForeignKey("Comment", related_name='reference_comment_rel', null=True)
    publish_date = models.DateTimeField()
    last_update = models.DateTimeField()
    active = models.BooleanField()
    
    owner = models.ForeignKey(Account, related_name='comment_owner_rel')

class Media(CoreModel):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(Attributes, limit_choices_to={'type':'media_type'}, related_name='media_type_rel')
    identifier = models.CharField(max_length=512)
    last_update = models.DateTimeField()
    active = models.BooleanField()
        
    owner = models.ForeignKey(Account, related_name='media_owner_rel')
    
    def get_fields(self):
        return ['title','description','type','identifier','last_update']
    
    class Meta:
        ordering = ['title']

class Advertisement(CoreModel):
    title = models.CharField(max_length=256)
    sub_title = models.CharField(max_length=128, null=True, blank=True)
    publish_date = models.DateTimeField()
    last_update = models.DateTimeField()
    type = models.ForeignKey(Attributes, limit_choices_to={'type':'ad_type'}, related_name='ad_type_rel')
    category = models.ForeignKey(Attributes, limit_choices_to={'type':'ad_cat_type'}, related_name='ad_cat_type_rel')
    medias = models.ManyToManyField("Media", related_name='ad_media_rel', null=True)
    comments = models.ManyToManyField("Comment", related_name='ad_comment_rel', null=True)
    price = models.FloatField(null=True, blank=True)
    
    sold = models.BooleanField()
    buyer = models.ForeignKey(Account, related_name='ad_buyer_rel')
    active = models.BooleanField()
    owner = models.ForeignKey(Account, related_name='ad_owner_rel')
    
    def get_fields(self):
        return ['title','sub_title','publish_date','last_update','type','category','medias','comments','price','sold','buyer','active']
    
    class Meta:
        ordering = ['title']
        
class Offer(CoreModel):
    owner = models.ForeignKey(Account, related_name='offer_owner_rel')
    advertisement = models.ForeignKey(Advertisement, related_name='offer_ad_rel')
    publish_date = models.DateTimeField()
    last_update = models.DateTimeField()
    price = models.FloatField(null=True, blank=True)
    
    def get_fields(self):
        return ['owner','advertisement','publish_date','last_update','price']
    
    class Meta:
        ordering = ['publish_date']