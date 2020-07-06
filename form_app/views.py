from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from form_app.models import UserFormDetails
from django.contrib.auth.models import User
from .forms import RegisterForm, SignIn, UserForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@csrf_exempt
def signup(request):
    err = ''
    if request.method == 'POST':
        user = User.objects.all()
        form = RegisterForm(request.POST)
        email = form.data['email']
        if user.filter(email=email):
            err = 'User with this email already exist'
        elif form.data['psw'] == form.data['psw_repeat']:
            if form.is_valid():
                user = User.objects.create_user(first_name=form.data['first_name'], last_name=form.data['last_name'],
                                                username=form.data['username'], email=form.data['email'],
                                                password=form.data['psw_repeat'])
                user.save()
                return HttpResponseRedirect('/signin')
            else:
                err = 'Invalid login please try again'
        else:
            err = 'Password does not match please try again'
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form, 'err': err})


def change_pass(request):
    message = "Change Password"
    if request.method == 'GET':
        email = request.GET.get('email')
        password1 = request.GET.get('password1')
        password2 = request.GET.get('password2')
        print(password1, password2)
        try:
            if password1 == password2:
                u = User.objects.get(email=email)
                u.set_password(password1)
                u.save()
                return HttpResponseRedirect('/signin')
            else:
                message = "Passwords doesn't Match"
        except ObjectDoesNotExist:
            message = "E-mail not matched"
    return render(request, 'change_password.html', {'message': message})


@csrf_exempt
def signin(request):
    err = ''
    if request.method == 'POST':
        form = SignIn(request.POST)
        if authenticate(username=form.data['username'], password=form.data['psw']):
            user = User.objects.get(username=form.data['username'])
            if user.is_superuser:
                return HttpResponseRedirect('/admin_view/')
            return user_form(request)
        else:
            err = 'Invalid username or password'
    else:
        form = SignIn()
    return render(request, 'signin.html', {'form': form, 'err': err})


def user_form(request):
    form = UserForm()
    return render(request, 'base.html', context={'form': form, 'status': ''})


def return_response(request):
    return render(request, 'base.html', context={'status': 'Your form is submitted successfully'})


# form_details to update and save new forms
@csrf_exempt
def form_details(request):
    form = UserForm()
    details = UserFormDetails.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES) # taking forms from the POST method
        previous_details = details.filter(email=form.data['email']) # checking the form is already exist or not
        if len(form.data['contact']) == 10 and form.is_valid():

            # validating form and updating the results
            if previous_details.exists():
                user = previous_details.last()
                # taking names for files
                pdf_name = form.cleaned_data.get('upload_pdf').name
                img_name = form.cleaned_data.get('image').name

                # saving the form responses
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.contact = form.cleaned_data.get('contact')
                user.date_of_birth = form.cleaned_data.get('date_of_birth')
                user.submission_date = form.cleaned_data.get('submission_date')
                user.upload_pdf.save(pdf_name, form.cleaned_data.get('upload_pdf'))
                user.image.save(img_name, form.cleaned_data.get('image'))
                user.save()
                return return_response(request)
            elif form.data['first_name'] != '':
                # if the form is new the save it to database
                details = UserFormDetails(first_name=form.cleaned_data.get('first_name'),
                                          last_name=form.cleaned_data.get('last_name'),
                                          email=form.cleaned_data.get('email'), image=form.cleaned_data.get('image'),
                                          upload_pdf=form.cleaned_data.get('upload_pdf'),
                                          contact=form.cleaned_data.get('contact'),
                                          date_of_birth=form.cleaned_data.get('date_of_birth'),
                                          submission_date=form.cleaned_data.get('submission_date')
                                          )
                details.save()
                return return_response(request)
        else:
            return render(request, 'base.html', context={'form': form})
    elif request.method == 'GET':
        return render(request, 'base.html', context={'form': form})
    return render(request, 'base.html', context={'form': form, 'status': 'Invalid input'})


@csrf_exempt
def admin_view(request):
    items = UserFormDetails.objects.all()  # fetch all records from UserFormDetails table
    if request.method == 'GET':
        # getting the responses from GET method
        id = request.GET.get('id')
        notes = request.GET.get('note')
        u = request.GET.get('user')
        search = request.GET.get('csearch')
        try:
            user = User.objects.get(username=u)
            i = items.filter(id=id)
            # check if the user is superuser or not
            if user.is_superuser:
                if search is not None:
                    # querying the table to search records
                    search_values = items.filter(
                        Q(first_name=search) | Q(last_name=search) | Q(email=search) | Q(image=search)
                        | Q(upload_pdf=search) | Q(contact=search))
                    if search_values:
                        return render(request, 'admin.html', context={'items': search_values})
                    else:
                        return render(request, 'admin.html',
                                      context={'items': items, 'status': 'Search value not found'})

                # update the notes in the user details
                elif id and notes not in ('[object HTMLCollection]', '[object HTMLButtonElement]'):
                    i.update(notes=notes)
                    return JsonResponse({'url': '/admin_view/'})
                elif notes in ('[object HTMLCollection]', '[object HTMLButtonElement]'):

                    return JsonResponse({'url': '/admin_view/'})
                else:
                    return render(request, 'admin.html', context={'items': items})
        except ObjectDoesNotExist or TypeError:
            return render(request, 'admin.html', context={'items': items})

    return render(request, 'admin.html', context={'items': items})
