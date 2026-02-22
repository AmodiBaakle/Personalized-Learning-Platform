from django.shortcuts import render,HttpResponse,redirect
from home.models import interface_data
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.decorators import login_required
from home import recommend
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
import json
import csv
import pandas as pd
from .models import interface_data
from django.http import JsonResponse
# Create your views here.

global username, preferences

@login_required(login_url='login')
def  index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):
    if request.method == "POST":
        print("in the if loop")
        goal=request.POST.get('goal')
        language=request.POST.get('language')
        level = request.POST.get('level')
        platform  = request.POST.get('platform')
        content_type = request.POST.get('content-type')
        if platform == 'GFG': pref_gfg, pref_w3, pref_yb = 1, 0, 0
        elif platform == 'W3Schools': pref_gfg, pref_w3, pref_yb = 0, 1, 0
        else: pref_gfg, pref_w3, pref_yb = 0, 0, 1
        global username
        idd = interface_data.objects.get(user=username)
        if idd.total_interactions == 0:
            idd.goal = goal
            idd.language = language
            idd.level = level
            idd.platform = platform
            idd.content_type = content_type
            idd.preference_gfg = pref_gfg
            idd.preference_w3school = pref_w3
            idd.preference_youtube = pref_yb
            print(goal,language,level,platform,content_type)
            idd.save()
        
        return redirect(analysis)
    df = pd.read_csv('./static/updated_content.csv')
    levels = df['Sub-topics'].tolist()
    return render(request, 'dashboard.html', {'levels': levels})

def signUpPage(request):
    if request.method=="POST":
        user_name = request.POST.get("username")
        email= request.POST.get("email")
        pw1 = request.POST.get("password1")
        pw2 = request.POST.get("password2")

        if pw1!=pw2:
            return HttpResponse("Your Password and Confirm Password are not same.")
        else:
            my_user = User.objects.create_user(user_name, email ,pw1)
            my_user.save()
            return  redirect('login')
    return render(request,'signup.html')

def loginPage(request):
    if request.method=='POST':
        global username
        global usern
        usern=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=usern,password=pass1)
        if user is not None : 
            login(request,user)
            username=user.id
            try: idd = interface_data.objects.get(user=username)
            except: 
                us =  User.objects.get(username=usern)
                idd = interface_data.objects.create(user=us)
                idd.save()
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect.")
    return render(request,'login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def analysis(request):
    topics = {}
    with open('./static/updated_content.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            topic = row['Topics']
            sub_topic = row['Sub-topics']
            if topic not in topics:
                topics[topic] = []
            topics[topic].append(sub_topic)
    idd = interface_data.objects.get(user=username)
    idd.total_interactions += 1
    idd.self_assess_visit += 1
    idd.self_assess_stay += 1
    idd.save()
    ques = dict()
    ques['question_remember'] = idd.question_remember
    ques['question_understanding'] = idd.question_understanding
    ques['question_application'] = idd.question_application
    ques['question_analysis'] = idd.question_analysis
    ques['question_evaluation'] = idd.question_evaluation
    return render(request, 'analysis.html', {'topics': topics, 'questions':ques, 'first_name': usern})

@login_required(login_url='login')
def results(request, sub_topic):
    global username, sub 
    sub = sub_topic
    if request.method=='POST':
        data = json.loads(request.body) 
        name = data.get('name')
        print(name)
        idd = interface_data.objects.get(user=username)
        if name == 'GFG': 
            idd.content_stay_gfg += 1
            idd.content_visit_gfg += 1
        elif name == 'W3Schools':
            idd.content_stay_w3school += 1
            idd.content_visit_w3school += 1
        elif name == 'Youtube':
            idd.content_stay_youtube += 1
            idd.content_visit_youtube += 1
        idd.save()
        return JsonResponse({'status': 'success'})
    idd = interface_data.objects.get(user=username)
    idd.total_interactions += 1
    idd.save()
    user = get_object_or_404(User, username=usern)
    pid = model_to_dict(get_object_or_404(interface_data, user=user))
    global preferences
    preferences = recommend.main(pid, username)
    print(preferences)
    context = {
        'Pref1': {'img_url': f'/static/{preferences[0]}.png', 'pref1': preferences[0], 'subtopic': sub_topic},
        'Pref2': {'img_url': f'/static/{preferences[1]}.png', 'pref1': preferences[1], 'subtopic': sub_topic},
        'Pref3': {'img_url': f'/static/{preferences[2]}.png', 'pref1': preferences[2], 'subtopic': sub_topic}
    }
    return render(request, 'results.html', context)

@login_required(login_url='login')
def page1(request):
    global preferences
    global sub
    context = recommend.recom(preferences, sub)
    print(context['pref1']['content'])
    return render(request, 'page1.html', context)

    
