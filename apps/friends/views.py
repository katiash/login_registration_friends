# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import User, UserManager
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
from checkuser import *

# Create your views here.
def main(request):   
    #@ensure_current_user
        # cannot do (if request.session["user_id"]) because python is unforgiving!
    if "user_id" in request.session:
        return redirect('friends:success')
    else: 
            #context={"my_message" : "Hello, I am your successesful login/registration request"}
        return render(request, 'friends/main.html')
         
def register(request):
    if request.method=='POST':
        print['****************in view method****************']
        print[request.POST]
        response_from_models = User.objects.validate_user(request.POST)
        print['****************back in view method****************']

        #on successful reg validation
        if response_from_models['status']:
            request.session['user_id']= response_from_models['user'].id
            return redirect('/friends')   
        #else return redirect ('/')
        else:
            #HOW MESSAGES WORK/PASSED BACK TO CLIENT:
            # The 'messages' object's methods also require the 'request'
            # object to be passed as a first parameter...
            # These messages are then going to be inside of that 'request' 
            # object to pass them back.

            # If errors in response_from_models is not a dictionary, but a list/array:
            # for error in response_from_models['errors']:
            #     messages.error(request, error)            

            # If errors in response_from_models IS a dictionary of tags and error messages:
            for tag, error in response_from_models['errors'].items():
                print tag, error
                messages.error(request, error, extra_tags=tag)
            return redirect('/')    
    else:
        # not a post, redirect to index method?
        return redirect('/') #our main.html template
    
def login(request):
    if request.method=='POST':
        print['****************in view method****************']
        print[request.POST]
        #invoke my method from the User model manager
        response_from_models = User.objects.validate_login(request.POST)
        print "************************* in login view method*************************"
        print response_from_models
        if response_from_models["status"]:
            request.session["user_id"]=response_from_models['user'].id
            #on successful login validation
            return redirect('/friends')
        else:
            #use the error message to display; will be just one string, so no need to loop through.
            messages.error(request, response_from_models['error'])
            return redirect('/')
    else:
        # not a post, redirect to index method?
        return redirect('friends:index') #our main.html template

def success(request):
    if "user_id" in request.session:
        print "************************* in login view method*************************"
        # context={"success_str" : "Hello, I am your successesful login/registration request"}
        print "user id of the logged in user is: ", request.session["user_id"]
        # me_id=User.objects.filter(id=request.session["user_id"]).values_list(flat=True)
        # friends_ids=User.objects.get(id=request.session["user_id"]).friends.all().values_list(flat=True)
        # all_users_ids=User.objects.all().values_list(flat=True)
        # not_friends_ids=all_users_ids.difference(me_id, friends_ids)

        me=User.objects.filter(id=request.session["user_id"])
        friends=User.objects.get(id=request.session["user_id"]).friends.all()
        all_users=User.objects.all()
        not_friends=all_users.difference(me, friends)
        print not_friends
        # <!-- Setting Relationships:
        # Comment.objects.create(blog=Blog.objects.get(id=1), comment="test") - create a new comment where the comment's blog points to Blog.objects.get(id=1). -->
        # Blog.objects.raw("SELECT * FROM {{app_name}}_{{class/table name}}") - performs a raw SQL query
        context = {
            'not_friends': not_friends,
            'friends' : friends,
            'me' : me[0]
        }
        return render(request, 'friends/friends.html', context)
    else:
        print request.session
        request.session.clear()
        return redirect ('/')

def profile(request, id):
    if "user_id" in request.session:
        print "*******************in Profile View**********************"
        user=User.objects.filter(id=id)
        if user:
            print "filter result: ", user
            print "user result: ", user[0]
        
            #pull up the info page on the provided user "id"
            return render(request, 'friends/profile.html', {"user":user[0]})
        else:
            print "Profile method decided there is no such ID in User table"
            return redirect('friends:success')
        return redirect('friends:index')
    else:
        return redirect('friends:logout')
        

def remove(request, id):
    print "Someone just called the 'remove' method"
    friend=get_object_or_404(User, id=id)
    # friend=User.objects.get(id=id)
    logged_user=User.objects.get(id=request.session["user_id"])
    #same for "this_user2
    rem_result=logged_user.friends.remove(friend)
    print rem_result
    #Need to clear that cookie/session dictionary/table =) !
    return redirect('friends:success' )
    
def add(request, id):
    print "Someone just called the 'add' method"
    to_friend=get_object_or_404(User, id=id)
    # to_friend=User.objects.get(id=id)
    logged_user=User.objects.get(id=request.session["user_id"])
    add_result=logged_user.friends.add(to_friend)
    print add_result
    return redirect('friends:success')

def logout(request):
    print "Someome just called the 'logout' method "
    #Need to clear that cookie/session dictionary/table =) !
    request.session.clear()
    return redirect('friends:index')
