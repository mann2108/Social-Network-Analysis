import matplotlib
from django.http import HttpResponse
from django.shortcuts import render
#import scipy
from app.models import Tweeter, Relationship, Post, HistoryOfPost
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import networkx as nx

import random

'''To Avoid Extra Warnings'''


def index(request):
    if request.method == "POST":
        if request.POST.get('logout'):
            del request.session['session_user_name']
            request.session.modified = True

    if request.session.has_key('session_user_name'):
        for i in Tweeter.objects.all():
            if (i.user_name == request.session['session_user_name']):

                followingUsers = []

                for j in Relationship.objects.all():
                    if (j.who.user_name == request.session['session_user_name']):
                        followingUsers.append(j.whom)

                posts = []
                for j in followingUsers:
                    for k in Post.objects.all():
                        if k.who == j:
                            posts.append(k)

                posts = set(posts)
                posts = list(posts)
                random.shuffle(posts)

                context = {'object': i, 'rel': Relationship.objects.all(), 'post': posts}
                return render(request, 'app/blog-home.html', context)

    if request.method == "POST":
        if request.POST.get('email') and request.POST.get('password'):

            email_1 = request.POST.get('email')
            password_1 = request.POST.get('password')

            flag = False
            user = Tweeter()
            for obj in Tweeter.objects.all():
                if (obj.email == email_1 and obj.password == password_1):
                    flag = True
                    user = obj
                    break

            if flag:
                request.session['session_user_name'] = user.user_name
                followingUsers = []

                for i in Relationship.objects.all():

                    if (i.who.user_name == request.session['session_user_name']):
                        followingUsers.append(i.whom)

                posts = []
                for i in followingUsers:
                    for j in Post.objects.all():
                        if j.who == i:
                            posts.append(j)

                posts = set(posts)
                posts = list(posts)
                random.shuffle(posts)

                # return HttpResponse("Logged In Success")
                context = {'object': user, 'rel': Relationship.objects.all(), 'post': posts}

                return render(request, 'app/blog-home.html', context)
            else:
                # return HttpResponse("Logged In Failed")
                context = {'error_message': "Logging Failed !!"}
                return render(request, 'app/index.html', context)

    # temp=0
    # ls=[]
    #
    # while(temp!=200):
    #     user1=random.choice(Tweeter.objects.all())
    #     user2=random.choice(Tweeter.objects.all())
    #     if(user1!=user2 and (user1,user2) not in ls):
    #         ls.append((user1,user2))
    #         temp+=1
    # s=""
    # for i in ls:
    #     s+=str(i[0].user_name)+" "+str(i[1].user_name)+"<br>"
    #     rel = Relationship()
    #     rel.who=i[0]
    #     rel.whom=i[1]
    #     rel.save()
    #
    # return HttpResponse(s)
    return render(request, 'app/index.html')


def register(request):
    if request.method == "POST":

        name1 = request.POST.get('name')
        user_name1 = request.POST.get('user_name')
        email1 = request.POST.get('email')
        gender1 = request.POST.get('gender')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if (password1 != password2):
            error_message = "Password Not Matched"
            return render(request, 'app/register.html', {'error_message': error_message})
        for obj in Tweeter.objects.all():
            if (obj.user_name == user_name1):
                error_message = "User Name Already Taken !!"
                return render(request, 'app/register.html', {'error_message': error_message})
            if (obj.email == email1):
                error_message = "User Already Exist !!"
                return render(request, 'app/register.html', {'error_message': error_message})

        new_user = Tweeter()

        new_user.name = name1
        new_user.user_name = user_name1
        new_user.email = email1
        new_user.gender = gender1
        new_user.password = password1

        new_user.save()

        error_message = "User Registered Successfully !!"
        return render(request, 'app/register.html', {'error_message': error_message})
    return render(request, 'app/register.html')


def followers(request):
    if request.session.has_key('session_user_name'):
        current_user = Tweeter()
        for i in Tweeter.objects.all():
            if (i.user_name == request.session['session_user_name']):
                current_user = i
                break

        rel = []
        for i in Relationship.objects.all():
            if (i.whom == current_user):
                rel.append(i.who)
        rel = set(rel)
        context = {'object': current_user, 'rel': rel}
        return render(request, 'app/followers.html', context)
    return render(request, 'app/index.html')


def following(request):
    current_user = Tweeter()
    whom_to = Tweeter()
    if request.method == "POST":

        for i in Tweeter.objects.all():
            if (i.user_name == request.POST.get('rmedge')):
                whom_to = i
                break
        for i in Tweeter.objects.all():
            if (i.user_name == request.session['session_user_name']):
                current_user = i
                break
        rel = Relationship()
        rel.who = current_user
        rel.whom = whom_to
        for i in Relationship.objects.all():
            if (i == rel):
                i.delete()
                break

    if request.session.has_key('session_user_name'):
        current_user = Tweeter()
        for i in Tweeter.objects.all():
            if (i.user_name == request.session['session_user_name']):
                current_user = i
                break

        rel = []
        for i in Relationship.objects.all():
            if (i.who == current_user):
                rel.append(i.whom)
        rel = set(rel)
        strr = str(current_user.user_name) + " " + str(whom_to.user_name) + "<br>"
        context = {'object': current_user, 'rel': rel, 'debug': strr}
        return render(request, 'app/following.html', context)
    return render(request, 'app/index.html')


def recommended_users(request):
    if request.method == "POST":
        current_user = Tweeter()
        whom_to = Tweeter()
        for i in Tweeter.objects.all():
            if (i.user_name == request.POST.get('mkedge')):
                whom_to = i
                break
        for i in Tweeter.objects.all():
            if (i.user_name == request.session['session_user_name']):
                current_user = i
                break
        rel = Relationship()
        rel.who = current_user
        rel.whom = whom_to
        if rel not in Relationship.objects.all():
            rel.save()

    if request.session.has_key('session_user_name'):
        users_i_follows = []
        current_user = Tweeter()
        for i in Tweeter.objects.all():
            if (i.user_name == request.session['session_user_name']):
                current_user = i
                break
        for i in Relationship.objects.all():
            if i.who == current_user:
                users_i_follows.append(i.whom)

        recommended_users_list = []

        for i in users_i_follows:
            for j in Relationship.objects.all():
                if j.whom == i or j.who == i:
                    if j.who == i or j.who == current_user or (j.who in recommended_users_list):
                        pass
                    else:
                        recommended_users_list.append(j.who)

        users_i_follows = []

        for i in Relationship.objects.all():
            if i.who == current_user:
                users_i_follows.append(i.whom)

        users_i_follows = set(users_i_follows)
        recommended_users_list = set(recommended_users_list)

        recommended_users_list = recommended_users_list - users_i_follows

        mp = {i: 0 for i in Tweeter.objects.all()}

        for i in Relationship.objects.all():
            mp[i.whom] += 1

        most_popular = None

        var = -1

        for i in Tweeter.objects.all():
            if (mp[i] > var):
                var = mp[i]
                most_popular = i

        flag = False
        if (len(recommended_users_list) == 0):
            flag = True
        context = {'object': current_user, 'rel': recommended_users_list, 'most_popular': most_popular, 'flag': flag}
        return render(request, 'app/recommended_users.html', context)


def analysis(request):



    nodes = []




    G = nx.DiGraph()
    for i in Tweeter.objects.all():
        G.add_node(i.user_name)

    rel = []

    for i in Relationship.objects.all():
        frm = i.who.user_name
        to = i.whom.user_name
        flag1 = True
        flag2 = True
        for j in nodes:
            if j[0] == frm and flag1:
                frm = j[1]
                flag = False
            if j[0] == to and flag2:
                to = j[1]
                flag = False
            if ((not flag1) and (not flag2)):
                break
        rel.append((frm, to))

    for i in rel:
        G.add_edge(i[0], i[1])
    d = dict(G.degree)

    nx.draw_kamada_kawai(G, with_labels='True', nodelist=list(d.keys()), node_size=[v * 50 for v in list(d.values())])
    information=[str(G.number_of_edges()),str(G.is_directed()), str(G.number_of_nodes())]

    plt.grid(axis='both', alpha=1)
    plt.savefig('app/static/GraphNetwork.png')
    plt.close()
    #nx.draw_
    y = nx.degree_histogram(G)
    x = [i + 1 for i in range(len(y))]

    plt.bar(x, y)

    plt.grid(axis='both', alpha=0.9)

    plt.title("Degree Distribution of Social Network")

    plt.xlabel("# of People")
    plt.ylabel("# of Followers+Following")

    plt.savefig('app/static/DegreeHistogram.png')
    #plt.show()
    plt.close()

    CC=nx.strongly_connected_components(G)

    iid = [120, 123, 384]

    # x=[[],[],[]]
    # y=[[],[],[]]
    #
    viralPost = []


    x=['ViralMeme1.png','ViralMeme2.png','ViralMeme3.png']
    cnt=0

    for i in iid:
        for j in Post.objects.all():
            if j.id == i:
                viralPost.append((j,x[cnt]))
                cnt+=1


    # for i in
    #
    # for i in HistoryOfPost.objects.all():
    #

    viralMemex1 = []
    viralMemey1 = []

    viralMemex2 = []
    viralMemey2 = []

    viralMemex3 = []
    viralMemey3 = []



    s = ""
    iid = [120, 123, 384]

    mp={120:[],123:[],384:[]}



    for i in HistoryOfPost.objects.all():
        if i.post.id in iid:
            mp[i.post.id].append((i.likes,i.dislikes))

    for i in iid:
        for j in mp[i]:
            s+=str(j)+" "
        s+="<br>"

    x1 = [i for i in range(1,6)]
    y1 = [i[0] for i in mp[120]]
    for i in range(5):
        if(y1[i]>20000):
            y1[i]+=20000

    s1_likes = ""
    for i in range(5):
        s1_likes+="Day "+str(i+1)+": -"+str(y1[i])+"\n"


    x2 = [i for i in range(1,6)]
    y2 = [i[0] for i in mp[123]]
    s2_likes = ""
    for i in range(5):
        s2_likes += "Day " + str(i + 1) + ": -" + str(y2[i]) + "\n"

    x3 = [i for i in range(1,6)]
    y3 = [i[0] for i in mp[384]]
    s3_likes = ""
    for i in range(5):
        s3_likes += "Day " + str(i + 1) + ": -" + str(y3[i]) + "\n"

    x11 = [i for i in range(1, 6)]
    y11 = [i[1] for i in mp[120]]
    s1_dislikes = ""
    for i in range(5):
        s1_dislikes += "Day " + str(i + 1) + ": -" + str(y11[i]) + "\n"

    x22 = [i for i in range(1, 6)]
    y22 = [i[1] for i in mp[123]]
    s2_dislikes = ""
    for i in range(5):
        s2_dislikes += "Day " + str(i + 1) + ": -" + str(y22[i]) + "\n"


    x33 = [i for i in range(1, 6)]
    y33 = [i[1] for i in mp[384]]

    s3_dislikes = ""
    for i in range(5):
        s3_dislikes += "Day " + str(i + 1) + ": -" + str(y33[i]) + "\n"

    plt.plot(x11,y11,color='blue',linestyle='dashed',marker='o',markerfacecolor='red',markersize=10,label='Likes')

    plt.plot(x1, y1, color='brown', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10, label='Dislikes')
    plt.legend()
    plt.title("Meme Virality Analysis")
    plt.xlabel("DAYS")
    plt.ylabel("LIKES")
    plt.savefig('app/static/ViralMeme1.png')
    plt.close()

    plt.plot(x2, y2, color='blue', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10,
             label='Likes')
    plt.plot(x22, y22, color='brown', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10,
             label='Dislikes')
    plt.title("Meme Virality Analysis")
    plt.legend()
    plt.xlabel("DAYS")
    plt.ylabel("LIKES")
    plt.savefig('app/static/ViralMeme2.png')
    plt.close()

    plt.plot(x3, y3, color='blue', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10,
             label='Likes')
    plt.plot(x33, y33, color='brown', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10,
             label='Dislikes')
    plt.legend()

    plt.title("Meme Virality Analysis")
    plt.xlabel("DAYS")
    plt.ylabel("LIKES")

    plt.savefig('app/static/ViralMeme3.png')
    plt.close()

    track_data = [(s1_likes,s1_dislikes),(s2_likes,s2_dislikes),(s3_likes,s3_dislikes)]
    viralPost[0][0].dislikes+=20000
    x=G.number_of_nodes()
    context = {'p': (x, y),'cc':CC,'viralPost':viralPost,'information':information,'mp':mp,'track_data':track_data,'x':x}

    return render(request, 'app/insurance.html', context)

def add_post(request):
    s=""
    return HttpResponse(s)