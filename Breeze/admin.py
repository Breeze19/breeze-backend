from django.contrib import admin
from .models import *
# Register your models here.

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'transaction_status', 'get_reg_name','nop', 'payable', 'college', 'get_event_category','get_email_id', 'get_reg_contact','get_event_name','get_contact_no')
    search_fields = ('registration_id', 'transaction_status', 'userId__profile__name', 'eventId__name','eventId__category')
    readonly_fields = ('created_at', 'updated_at')
    def get_reg_name(self, obj):
        return obj.userId.profile.name
    get_reg_name.short_description = 'User Name'
    get_reg_name.admin_order_field = 'userId'

    def get_reg_contact(self, obj):
        return obj.userId.profile.contact
    get_reg_contact.short_description = 'Phone'
    get_reg_contact.admin_order_field = 'userId'

    def get_event_name(self, obj):
        return obj.eventId.name
    get_event_name.short_description = 'Event Name'
    get_event_name.admin_order_field = 'eventId'
    
    def get_email_id(self,obj):
        return obj.userId.email
    get_email_id.short_description = 'Email id'
    get_email_id.admin_order_field = 'userId'
    
    def get_event_category(self,obj):
        if obj.eventId.category == 'c':
            return 'cultural'
        elif obj.eventId.category == 's':
            return 'sports'
        else:
            return 'technical'
    get_event_category.short_description = 'Category'
    get_event_category.admin_order_field = 'eventId'
    
    def get_contact_no(self,obj):
        return obg.userId.profile.contact

class AccomRegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'payable', 'transaction_status', 'get_reg_name','get_reg_contact','get_package_name')
    search_fields = ('registration_id', 'payable', 'transaction_status', 'userId__profile__name', 'packageId__name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_reg_name(self, obj):
        return obj.userId.profile.name
    get_reg_name.short_description = 'User Name'
    get_reg_name.admin_order_field = 'userId'

    def get_reg_contact(self, obj):
        return obj.userId.profile.contact
    get_reg_contact.short_description = 'Phone'
    get_reg_contact.admin_order_field = 'userId'

    def get_package_name(self, obj):
        return obj.packageId.name
    get_package_name.short_description = 'Package Name'
    get_package_name.admin_order_field = 'packageId'

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'get_user_name')

    def get_user_name(self, obj):
        return obj.user.email
    get_user_name.short_description = 'Email'

admin.site.register(Registration,RegistrationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AccPackage)
admin.site.register(Events)
admin.site.register(ForgetPass)
admin.site.register(AccomRegistration, AccomRegistrationAdmin)
