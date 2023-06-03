from django.shortcuts import render , redirect
from .models import*
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from .predictor import model_predict
from django.db.models import Q , Sum
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import logging

logger = logging.getLogger(__name__)



@login_required(login_url='login')
def shop(request): 
    if request.method == 'POST':
        medicine_image=request.FILES.get('medicine_image')   
        medicine_name = request.POST.get('medicine_name')
        medicine_description =request.POST.get('medicine_description')

        Medicine.objects.create(
            medicine_name = medicine_name,
            medicine_description = medicine_description,
            medicine_image=medicine_image
            )
        return redirect('/shop/')
    
    queryset = Medicine.objects.all()
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(medicine_name__icontains = search) |
            Q(medicine_description__icontains = search) |
            Q(medicine_price__icontains = search) 
            ).order_by('medicine_name').order_by('medicine_price')

    paginator = Paginator(queryset,10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'medicines': page_obj}

    return render(request ,'shop.html',context)


@login_required(login_url='login')
def medicines(request):
    if request.method == "POST":
        data = request.POST   # request for text frontend data to backend 
        
        medicine_image=request.FILES.get('medicine_image')   #for image
        medicine_name = data.get('medicine_name')
        medicine_price = float(data.get('medicine_price'))
        medicine_description =data.get('medicine_description')

        Medicine.objects.create(
            medicine_name = medicine_name,
            medicine_price = medicine_price,
            medicine_description = medicine_description,
            medicine_image=medicine_image
            )
        
        return redirect('/medicines/')
    
    queryset = Medicine.objects.all()
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(medicine_name__icontains = search) |
            Q(medicine_description__icontains = search) |
            Q(medicine_price__icontains = search) 
            ).order_by('medicine_name').order_by('medicine_price')

    paginator = Paginator(queryset,10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'medicines': page_obj}

    return render(request, 'medicines.html', context)







def home(request):
    return render(request , 'home.html')
    
    
@login_required(login_url="/login/")
def test(request):
    user = request.user
    return render(request, 'test.html', {'user': user})


@login_required(login_url="/login/")
def result(request):
    return render(request, 'result.html')


@login_required(login_url="/login/")
def predict(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("test"))
    # Retrieve user input from the form
    count=0
    age = request.POST.get('age')
    if not age:
        return HttpResponseRedirect(reverse("test"))

    weight = request.POST.get('weight')
    if not weight:
        return HttpResponseRedirect(reverse("test"))

    user_input = [
        1 if request.POST.get('cold') == 'yes' else 0 ,
        1 if request.POST.get('eyepain') == 'yes' else 0,
        1 if request.POST.get('fever') == 'yes' else 0,
        1 if request.POST.get('headache') == 'yes' else 0,
        1 if request.POST.get('stomachache') == 'yes' else 0,
        1 if request.POST.get('dizziness') == 'yes' else 0,
        1 if request.POST.get('vomiting') == 'yes' else 0,
        1 if request.POST.get('chestpain') == 'yes' else 0,
        1 if request.POST.get('jointpain') == 'yes' else 0,
        1 if request.POST.get('loosemotion') == 'yes' else 0,
        1 if request.POST.get('throatinfection') == 'yes' else 0,
        int(request.POST.get('age')),
        int(request.POST.get('gender')),
        int(request.POST.get('weight'))
    ]

    count = user_input.count(0) 

    if count >= 10:
        context = {}

    else:
        medicines = model_predict(str(user_input).lstrip('[').rstrip(']'))
        print(medicines)

    # predictor here
        context = {
            'medicine1': medicines[0][0],
            'medicine2': medicines[0][1],
            'medicine3': medicines[0][2],
        }

    return render(request, 'result.html', {
        'context': context, 'count': count,
    })


@login_required(login_url='/login/')
def delete_medicine(request, id):      #also regiser this rout to urls.py
    queryset = Medicine.objects.get(id=id)
    queryset.delete()
    return redirect('/medicines/')

    
@login_required(login_url='/login/')
def buy_medicine(request, id):      #also regiser this rout to urls.py
    queryset = Medicine.objects.get(id=id)
    try:
        host = request.get_host()
        
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': queryset.medicine_price,
            'item_name': queryset.medicine_name,
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': f'http://{host}{reverse("paypal-ipn")}',
            'return_url': f'http://{host}{reverse("paypal-return")}',
            'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        
        return render(request, 'buy.html', {context})
    except Exception as err:
        logger.exception("An error occurred during PayPal integration: %s", str(err))
        

def paypal_return(request):
    messages.success(request=request, message="Successful payment")
    return redirect('buy_medicine')

def paypal_cancel(request):
    messages.success(request=request, message="Payment failed")
    return redirect('buy_medicine')



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        
        user =authenticate(username = username, password = password)

        if user is None:    
            messages.info(request, "Invalid Password")
            return redirect('/login/')
        
        else:
            login(request,user)       # iska name(lgoin()) aur function ka name (login_page) diffrent hona chaiye 
                        # varna infiniite loop chlenga 
            return redirect('/test/')


    return render(request, 'login.html')



def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):

    if request.method != "POST":
        return render(request, 'register.html')
    


    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')




    user = User.objects.filter(username=username)


    if user.exists():
        messages.info(request, "Username Already Exists")
        return redirect('/register/')


    user = User.objects.create(
        first_name= first_name, 
        last_name= last_name,
        username=username,
        # password=password  we cant directly add password so we have encrypt it
        )

    user.set_password(password)    # this method is already thier in django
    user.save()
    messages.info(request, "Account created successfully")

    return redirect('/login/')






























