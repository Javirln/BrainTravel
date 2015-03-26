from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.MainViews.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signin/$', 'principal.views.UserViews.sign_in'),
    url(r'^logout/$', 'principal.views.UserViews.system_logout'),
    url(r'^search', 'principal.views.TripViews.search_trip'),
    #Para indicar en las URLs un metodo que se encuentra dentro de un archivo .py
    # url(r'^<nombre_url>$', '<app>.<paquete>.<archivo>.<metodo>'),
    # url(r'^<nombre_url>$', 'principal.views.ViewsModel1.method1')
    url(r'^register_traveller/$', 'principal.views.UserViews.create_traveller'),
    url(r'^confirm_account/$', 'principal.views.UserViews.confirm_account'),
    url(r'^public_trip_details/(?P<trip_id>[0-9]+)$', 'principal.views.TripViews.public_trip_details'),
    url(r'^administrator/trip/list/$', 'principal.views.TripViews.list_trip_administrator'),
    url(r'^administrator/trip/update/(?P<trip_id>[0-9]+)$', 'principal.views.TripViews.update_state'),
    url(r'^Coin/list/$', 'principal.views.Coinviews.list_coin_traveller'),
    url(r'^Trip/MyList/(?P<optional>.*)$', 'principal.views.TripViews.list_all_by_traveller'),
    url(r'^Trip/edit/(?P<trip_id>[0-9]+)$$', 'principal.views.TripViews.trip_edit'),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^Trip/create/$', 'principal.views.TripViews.trip_create'),
    url(r'^judge/(?P<trip_id>[0-9]+)/(?P<like>[0-1])', 'principal.views.JudgeViews.judge'),
    url(r'^profile/(?P<traveller_id>[0-9]+)$', 'principal.views.TravellerViews.profile_details'),
    url(r'^profile/edit/$', 'principal.views.TravellerViews.profile_edit'),
    url(r'^profile/edit/password/$', 'principal.views.TravellerViews.profile_edit_password'),
    url(r'^Trip/draft/$', 'principal.views.TripViews.list_all_by_traveller_draft'),
    url(r'^public_trip_details/comment/', 'principal.views.TripViews.comment_trip'),
    url(r'^public_trip_details/rate/', 'principal.views.TripViews.send_assessment'),
    url(r'^auth_request/$', 'principal.views.FoursquareViews.foursquare_request'),
    url(r'^trip/list/(?P<profile_id>[0-9]+)$$', 'principal.views.TripViews.list_trip_approved_by_profile'),
    #paypal urls
    url(r'^test_paypal/$', 'principal.views.PayPalViews.test_paypal_view'),
    (r'^something/paypal/', include('paypal.standard.ipn.urls')),
)
