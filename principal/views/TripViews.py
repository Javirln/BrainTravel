# -*- coding: latin-1 -*-

from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from principal.forms import TripEditForm, CommentForm, AssessmentForm
from principal.forms import TripUpdateStateForm
from principal.models import Judges, Assessment, Day, Venue, VenueDay, Feedback, Traveller, CoinHistory
from principal.models import Trip, Comment
from principal.services import TripService, TravellerService, CommentService, LikeService
from principal.services.TravellerService import save
from principal.utils import BrainTravelUtils


def search_trip(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
        else:
            title = request.GET.get('title')

        trips = TripService.searchTrip(title)
        paginator = Paginator(trips, 2)
        page = request.GET.get('page')
        try:
            trips = paginator.page(page)
        except PageNotAnInteger:
            trips = paginator.page(1)
        except EmptyPage:
            trips = paginator.page(paginator.num_pages)
        return render_to_response('search.html', {'trip_result': trips, 'title_search': title}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


def public_trip_details(request, trip_id):
    try:
        # Variable que hace que se muestre el modal de las valoraciones
        modal = False

        # Obtener el viaje
        trip = Trip.objects.get(id=trip_id, planified=False)
        assert trip.traveller.id == request.user.id or trip.state == 'ap' or request.user.has_perm('principal.administrator')

        # Obtener todos los comentarios de un viaje
        comments = Comment.objects.filter(trip=trip_id).order_by('-date')

        # Paginacion para la lista de comentarios
        paginator = Paginator(comments, 10)
        page = request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        # Obtener todos los 'judges' realizados por un viajero a un viaje
        judges = Judges.objects.filter(trip_id=trip_id, traveller_id=request.user.id)
        if len(judges) == 0:
            judge = None
        else:
            judge = list(judges)[0]

        # Obtener todos los 'assessment' realizados por un viajero a un viaje
        assessment = Assessment.objects.filter(scorable_id=trip_id, traveller_id=request.user.id)
        if len(assessment) == 0:
            assessment = None
        else:
            assessment = list(assessment)[0]

        if request.POST:
            assert request.user.has_perm('principal.traveller')
            # Validacion del comentario
            if 'comment_name' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = CommentService.construct_comment(request.user.id, comment_form)
                    CommentService.save(request.user.id, comment)
                    BrainTravelUtils.save_success(request, _('Comment successfully'))
                    return HttpResponseRedirect("/public_trip_details/" + str(comment.trip.id))
            else:
                comment_form = CommentForm(initial={'id_trip': trip.id})
            # Validacion de la valoracion
            if 'assessment_name' in request.POST:
                assessment_form = AssessmentForm(request.POST)
                if assessment_form.is_valid():
                    TripService.construct_assessment(request.user.id, assessment_form)
                    BrainTravelUtils.save_success(request, _('Your vote has been saved!'))
                    return HttpResponseRedirect("/public_trip_details/" + str(trip.id))
                else:
                    modal = True
            else:
                assessment_form = AssessmentForm(initial={'id_trip': trip.id})

        else:
            comment_form = CommentForm(initial={'id_trip': trip.id})
            assessment_form = AssessmentForm(initial={'id_trip': trip.id})

        form = TripUpdateStateForm(initial={'id': trip.id, 'state': trip.state})
        return render_to_response('public_trip_details.html', {'trip': trip, 'comments': comments, 'judge': judge, 'form': form, 'comment_form': comment_form, 'assessment_form': assessment_form, 'assessment': assessment, 'modal': modal}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@login_required()
def list_trip_administrator(request):
    try:
        trips = TripService.list_trip_administrator(request.user)
        paginator = Paginator(trips, 10)
        page = request.GET.get('page')
        try:
            trips = paginator.page(page)
        except PageNotAnInteger:
            trips = paginator.page(1)
        except EmptyPage:
            trips = paginator.page(paginator.num_pages)
        return render_to_response('trip_list.html', {'trips': trips, 'create_trip': True, 'title_list': _('Trips')}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@permission_required('principal.traveller')
def planned_trips(request):
    try:
        trips = TripService.find_planed_trips_by_traveller(request.user.id)
        if trips is not False:
            paginator = Paginator(trips, 10)
            page = request.GET.get('page')
            try:
                trips = paginator.page(page)
            except PageNotAnInteger:
                trips = paginator.page(1)
            except EmptyPage:
                trips = paginator.page(paginator.num_pages)
        return render_to_response('trip_planned_list.html', {'trips': trips, 'create_trip': False, 'title_list': _('My planned trips')}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@login_required()
@permission_required('principal.administrator')
def update_state(request, trip_id):
    try:
        if request.POST:
            trip_form = TripUpdateStateForm(request.POST)
            if trip_form.is_valid():
                trip = TripService.update_state(request.user, trip_form)
                assert str(trip.scorable_ptr_id) == trip_id
                TripService.save(trip)
                BrainTravelUtils.save_success(request, _('Trip successfully updated'))
                return redirect(list_trip_administrator)
        else:
            return redirect(public_trip_details(request, trip_id))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@login_required()
def list_all_by_traveller(request):
    try:
        trips = TripService.list_my_trip(request.user.id)
        if trips is not False:
            paginator = Paginator(trips, 10)
            page = request.GET.get('page')
            try:
                trips = paginator.page(page)
            except PageNotAnInteger:
                trips = paginator.page(1)
            except EmptyPage:
                trips = paginator.page(paginator.num_pages)
        return render_to_response('trip_list.html', {'trips': trips, 'create_trip': True, 'title_list': _('My trips')}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@login_required()
def list_all_by_traveller_draft(request):
    try:
        trips = TripService.list_trip_draft(request.user.id)
        if trips is not False:
            paginator = Paginator(trips, 10)
            page = request.GET.get('page')
            try:
                trips = paginator.page(page)
            except PageNotAnInteger:
                trips = paginator.page(1)
            except EmptyPage:
                trips = paginator.page(paginator.num_pages)
            return render_to_response('trip_list.html', {'trips': trips, 'create_trip': True, 'title_list': _('My draft trips')}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@login_required()
def trip_create(request):
    try:
        user_id = request.user.id
        if request.POST:
            form = TripEditForm(request.POST)
            if form.is_valid():
                trip_new = TripService.create(form, user_id)
                if "save" in request.POST:
                    trip_new.state = "df"
                    TripService.save_secure(trip_new)
                    BrainTravelUtils.save_success(request, _("Action completed successfully"))
                    return HttpResponseRedirect("/trip/draft/")
                elif "publis" in request.POST:
                    trip_new.state = "pe"
                    TripService.save_secure(trip_new)
                    BrainTravelUtils.save_success(request, _("Your trip must be accepted by an administrator"))
                    return HttpResponseRedirect("/trip/mylist/")
                BrainTravelUtils.save_error(request)
                return HttpResponseRedirect("/trip/mylist/")
        else:
            data = {}
            form = TripEditForm(initial=data)

        return render_to_response('trip_edit.html', {"form": form, "create": True},  context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@login_required()
@permission_required('principal.traveller')
def trip_edit(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id)
        assert trip.traveller.id == request.user.id
        if request.POST:
            form = TripEditForm(request.POST)
            if form.is_valid():
                trip.publishedDescription = form.cleaned_data['publishedDescription']
                trip.city = form.cleaned_data['city']
                trip.startDate = form.cleaned_data['startDate']
                trip.endDate = form.cleaned_data['endDate']
                trip.country = form.cleaned_data['country']
                if 'save' in request.POST:
                    trip.state = "df"
                    TripService.save_secure(trip)
                    BrainTravelUtils.save_success(request, _("Action completed successfully"))
                    return HttpResponseRedirect("/trip/draft/")
                elif 'publis' in request.POST:
                    trip.state = "pe"
                    TripService.save_secure(trip)
                    BrainTravelUtils.save_success(request, _("Your trip must be accepted by an administrator"))
                    return HttpResponseRedirect("/trip/mylist/")

            if 'delete' in request.POST:
                TripService.delete(request, trip)
                BrainTravelUtils.save_success(request, _("Trip deleted successfully"))
                return HttpResponseRedirect("/trip/mylist/")

        else:
            data = {'city': trip.city, 'publishedDescription': trip.publishedDescription, 'country': trip.country, 'startDate': trip.startDate, 'endDate': trip.endDate, 'name': trip.name}
            form = TripEditForm(initial=data)

        return render_to_response('trip_edit.html', {"form": form, "trip": trip, "can_delete": True, "create": False}, context_instance=RequestContext(request))
    except:
        # print(traceback.format_exc())
        return render_to_response('error.html', context_instance=RequestContext(request))


@permission_required('principal.traveller')
def change_venue(request):
    try:
        trip = Trip.objects.get(id=request.POST['trip'])
        assert trip.traveller.id == request.user.id
        day = Day.objects.get(id=request.POST['day'])
        oldVenue = Venue.objects.get(id=request.POST['oldVenue'])
        newVenue = Venue.objects.get(id=request.POST['newVenue'])
        
        venue_day = VenueDay.objects.get(Q(venue=oldVenue) & Q(day=day))
        venue_day.venue = newVenue
        venue_day.save()
        
        trip.possible_venues.remove(newVenue)
        trip.possible_venues.add(oldVenue)
        
        return HttpResponseRedirect("/show_planning/" + str(trip.id))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))
        

@login_required()
def list_trip_approved_by_profile(request, profile_id):
    try:
        traveller = TravellerService.find_one(profile_id)
        trips = TripService.list_trip_approved(traveller.id)
        paginator = Paginator(trips, 10)
        page = request.GET.get('page')
        try:
            trips = paginator.page(page)
        except PageNotAnInteger:
            trips = paginator.page(1)
        except EmptyPage:
            trips = paginator.page(paginator.num_pages)
        return render_to_response('trip_list.html', {'trips': trips, 'create_trip': True}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@login_required()
def send_feedback(request):
    try:
        user_id = request.user.id
        description = request.POST['text-description']
        venue_id = request.POST['venue-id']
        
        
        lead_time = request.POST['lead-time-value'] if request.POST['lead-time-value'] else None 
        duration_time = request.POST['duration-time-value'] if request.POST['duration-time-value'] else None
        
        
        url = request.path.split("/")
        TripService.send_feedback(user_id, venue_id, lead_time, duration_time, description)
        BrainTravelUtils.save_success(request, _("Thanks for the feedback, you are awesome!"))
        return HttpResponseRedirect("/" + url[1] + "/" + venue_id)
    except Exception:
        msg_errors = [_("Something went wrong...")]
        return HttpResponseRedirect("/" + url[1] + "/" + venue_id, {'msg_errors': msg_errors})


@login_required()
def value_tip(request, id_venue, id_tip):
    try:
        url = request.path.split("/")
        current_traveller = Traveller.objects.get(id=request.user.id)
        feedback_instance = Feedback.objects.get(id=id_tip)
        
        if LikeService.can_vote(current_traveller.id, feedback_instance.id):
            new_useful_count = feedback_instance.usefulCount + long(1)
            
            if (new_useful_count % 2) == 0:
                #Recompensa de monedas
                tip_owner = feedback_instance.traveller
                tip_owner.coins += long(2)
                save(tip_owner)
                new_entry = CoinHistory(
                    amount=2,
                    date=datetime.now(),
                    concept="Gift for useful tips",
                    traveller=tip_owner
                )
                new_entry.save()
            
            TripService.value_tip(feedback_instance, current_traveller)
            BrainTravelUtils.save_success(request, _("Thanks for the feedback, you are awesome!"))
            return HttpResponseRedirect("/" + url[1] + "/" + id_venue)
        else:
            BrainTravelUtils.save_info(request, _("You voted this tip already."))
            return HttpResponseRedirect("/" + url[1] + "/" + id_venue)
    except:
        msg_errors = ["Something went wrong..."]
        return HttpResponseRedirect("/" + url[1] + "/" + id_venue, {'msg_errors': msg_errors})


@login_required()
def stats(request):
    try:
        result = TripService.stats()
        return render_to_response('stats.html', {'travellers_travelling': result['travellers_travelling'],  'most_visited_venues': result['most_visited_venues'], 'most_liked_trips': result['most_liked_trips'], 'most_useful_tips': result['most_useful_tips']}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))
