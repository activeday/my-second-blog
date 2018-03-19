from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
#from django.views.generic import TemplateView, ListView, DetailView
from django.views import generic
from mysite.core.forms import *
from .models import *
from mysite.core.tokens import account_activation_token
import time
import datetime
from .filters import apartment_filter


#@login_required
def home(request):
    template = loader.get_template('home.html')
    context = {"apartment_images": common_detail.objects.all()[:1],
                 #"today":datetime.datetime.now().date(),
                 #"hotel_list": hotel_details.objects.all()
                 }

    return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


@login_required
def baze_test(request):
    if request.method == 'POST':
        form = property_detail_form(request.POST, request.FILES)
        if form.is_valid():
            
            owner = request.user.username
            apartment_name = request.POST.get('apartment_name', '')
            apartment_type = request.POST.get('apartment_type', '')
            county = request.POST.get('county', '')
            rent = request.POST.get('rent', '')
            location = request.POST.get('location', '')
            phone = request.POST.get('phone', '')
            apartment_image = request.FILES['apartment_image']	 
            description = request.POST.get('description','')
            uploaded_at = request.POST.get('uploaded_at','')
            #image = None
            #if 'image' in request.FILES:
            
            aprt_obj = common_detail(owner=owner,apartment_name=apartment_name,apartment_type=apartment_type,county=county,rent=rent,
                                    location=location,phone=phone,apartment_image=apartment_image,
                                     description=description,uploaded_at=uploaded_at)
            aprt_obj.save()
            time.sleep(5)
            
        return redirect('home')
    else:
        form = property_detail_form()
        return render( request, 'test_form.html', {'form': form})
    

# apartment list view an detail view
def list_view(request):
    user_list = common_detail.objects.all()
    user_filter = apartment_filter(request.GET, queryset=user_list)
    return render(request, 'core/index.html', {'filter': user_filter})

class DetailsView(generic.DetailView):
    model = common_detail
    template_name = 'core/details.html'











#apartment list view function view 
def apartments_page(request):
    template = loader.get_template('offers.html')
    context = {"apartment_images": common_detail.objects.all(),
                 #"today":datetime.datetime.now().date(),
                 #"hotel_list": hotel_details.objects.all()
                 } 
    return HttpResponse(template.render(context, request))

#apartment listview using generic view
class IndexView(generic.ListView):
    
    # a name to refer to the object_list(to be used in the index.html)
    context_object_name = 'apartment_images'
    template_name = 'core/index.html'
    paginate_by = 9
 
    def get_queryset(self):
        return common_detail.objects.all()
