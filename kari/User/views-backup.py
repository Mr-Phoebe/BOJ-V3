# coding: utf-8
from User.models import *
import Course.models
import django.contrib.sessions
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from User.forms import *
from common.err import Err
from django.core.paginator import Paginator
from django.contrib import messages
import logging

logger = logging.getLogger('django')

tpltrue = {'sp':True}
tplfalse = {'sp':False}

def showUserInfo(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
    except Err:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)
    else:
        return render(request, 'newtpl/user/userinfo.html', {'user':u, 'tpl':tpltrue})

def viewUserInfo(request, uid):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        utov = User.objects.get(pk=uid)
        if u == False:
            raise Err(request, 'not login')
        # elif u.priv != 'university':
        elif u.priv == 'student' and u.uid != utov.uid:
            raise Err(request, 'no priv')
        else:
            if utov.university != u.university:
                raise Err(request, 'no priv')
            return render(request, 'newtpl/user/viewuser.html', {'user':u, 'utov':utov, 'tpl':tpltrue})
    except Err:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE, {'errmsg':Err})
 
def showLoginPage(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        if 'uid' in request.session:
            u = User.getSessionUser(request.session)
            raise Err(request, 'logged in')
        else:
            form = LoginForm()
            return render(request, 'User/login.html', {'form':form, 'user':False})
    except Err as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE, {'errmsg': e})

def login(request):
    logger.info(str(request).replace("\n","\t"))
    if request.method != 'POST':
        return showLoginPage(request)
    form = LoginForm(request.POST)
    if form.is_valid():
        usname = form.cleaned_data['username']
        pswd = form.cleaned_data['passwd']
        try:
            u = User.getUserByRawUsername(usname)
        except:
            raise Exception(Const.LOGIN_FAIL)
        if u._chkPasswd(pswd):
            request.session['uid'] = u.uid
            return redirect('/user/')
        else:
            raise Exception(Const.LOGIN_FAIL)
    else:
        return render(request, 'User/login.html', {'form':form, 'user':False})

def logout(request):
    logger.info(str(request).replace("\n","\t"))
    if 'uid' not in request.session:
        return render(request, 'User/error.html', {'errmsg': Const.NOT_LOGGED_IN, 'user':False})
    else:
        request.session.flush()
        return redirect('/user/login')

def update(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')

        if request.method == 'GET':
            return render(request, 'newtpl/user/update.html', {'tpl':tpltrue})
	
        nickname = request.POST['nickname']
        passwd1 = request.POST['passwd']
        passwd2 = request.POST['passwd2']
        email = request.POST['email']
        gender = request.POST['gender']

        if email == '':
            email = None
        if passwd1 != passwd2:
            raise Err(request, 'passwd diff')
        try:
            if passwd1 != '':
                u.update(nickname, passwd1, email, gender)
            else:
                u.updateNoPass(nickname, email, gender)
        except Exception as e:
            print e
            raise Err(request, 'email illegal')
        return redirect('/user/')
    except Err as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def addMultiUser(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')

        if request.method == 'GET':
            return render(request, 'newtpl/user/addmultiuser.html', {'univ_name':u.university.name, 'schools':School.objects.all(), 'tpl':tpltrue})
        else:
            schoolname = request.POST['school']
            school = School.objects.get(name=schoolname)
            txt = request.POST['usernames']
            #ulist = txt.replace('\r', '').split('\n')
            ulist = txt.splitlines()
            prefix = u.university.name + '#'
            succ = {}
            fail = {}
            for it in ulist:
                item = it.split()
                if len(item) < 1:
                    continue

                uname = item[0].strip().lower()

                if len(item) > 1:
                    passwd = item[1].strip()
                    if passwd == '*':
                        passwd = prefix+uname
                else:
                    passwd = User._genRandPasswd()

                if len(item) > 2:
                    nickname = item[2].strip()
                else:
                    nickname = item[0].strip()

                try:
                    nu = User.addUser(uname, passwd, u.university, 'student', nickname)
                    nu.school = school
                    nu.save()
                except Exception, e:
                    if 'unique' in unicode(e):
                        fail[prefix+uname] = Err(request, 'username dup').user_msg
                    else:
                        fail[prefix+uname] = Err(request, unicode(e)).user_msg
                else:
                    succ[prefix+uname] = passwd
            return render(request, 'newtpl/user/addresult.html',
                     {'succ':succ,
                     'succcnt':len(succ),
                     'fail':fail,
                     'failcnt':len(fail),
                     'user':u,
                     'tpl':tplfalse,
                     })
    except Err as e:
        logger.error(str(e).replace("\n","\t"))
        return render(reqeust, Err.ERROR_PAGE)

def addAdmin(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)

        if not u:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')

        if request.method == 'GET':
            schools = School.objects.filter(university=u.university)
            return render(request, 'newtpl/user/addadmin.html', {'univ_name':u.university.name, 'tpl':tpltrue, 'schools':schools})

        uname = request.POST['username']
        password1 = request.POST['passwd']
        password2 = request.POST['passwd2']
        if password1 != password2:
            raise Err(request, 'passwd diff')
        else:
            password = password1
        priv = request.POST['priv']
        schid = request.POST['school']
        sch = School.getById(schid)
        try:
            ad = u.addAdmin(uname, password, priv)
            ad.school = sch
            ad.save()
        except Exception, e:
            if 'unique' in unicode(e):
                raise Err(request, 'username dup')
            elif 'username' in unicode(e):
                raise Err(request, 'username illegal')
            elif 'no priv' in unicode(e):
                raise Err(request, 'no priv')
            else:
                raise Err(request, 'unknown err')
        return redirect('/user/manage/admin/')

    except Err as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)
            

def listAdmin(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')
 
        alladmin = User.objects.filter(university=u.university).exclude(priv='student')
        return render(request, 'newtpl/user/alladmin.html', {'alladmin':alladmin, 'tpl':tpltrue})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def listStudent(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')

        allstudent = User.objects.filter(university=u.university, priv='student')
        return render(request, 'newtpl/user/allstudent.html', {'allstudent':allstudent, 'tpl':tpltrue})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def manageSchool(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not (u.priv == 'university' or u.priv == 'school'):
            raise Err(request, 'no priv')
    
        schlist = School.objects.filter(university=u.university)
        if u.priv == 'university':
            can_manage = True
        else:
            schlist = schlist.filter(admin=u)
            can_manage = False
        return render(request, 'newtpl/user/manageschool.html', {'school_list':schlist, 'tpl':{'sp':True, 'can_manage':can_manage,},})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def addSchool(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')
 
        if request.method == 'GET':
            form = AddSchoolForm()
            return render(request, 'newtpl/user/addschool.html', {'form':form, 'user':u, 'tpl':tpltrue})

        form = AddSchoolForm(request.POST)
        if form.is_valid():
            school_abbr = form.cleaned_data['schoolabbr']
            school_name = form.cleaned_data['schoolname']
            try:
                School.addSchool(school_abbr, school_name, u.university)
            except Exception as e:
                raise Err(request, 'school info illegal')
            return redirect('/user/manage/school/')
        else:
            return render(request, 'newtpl/error.html', {'errmsg':form._errors, 'user':u})
    except Err as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def modifySchool(request, school_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')

        try:
            sch = School.objects.get(pk=school_id)
        except:
            raise Err(request, 'school not exist')
        if sch.university != u.university:
            raise Err(request, 'no priv')
        if request.method == 'GET':
            admin_cddt = [x for x in User.objects.filter(priv='school',university=u.university)]
            return render(request, 'newtpl/user/modifyschool.html', {'user':u, 'admin_cddt':admin_cddt, 'school':sch, 'tpl':tpltrue})

        schoolname = request.POST['schoolname']
        schoolabbr = request.POST['schoolabbr']
        admin_uid = request.POST['admin']
        if School.validSchoolname(schoolname):
            sch.fullname = schoolname
        else:
            raise Err(request, 'schoolname illegal')
        if School.validSchoolabbr(schoolabbr):
            sch.name = schoolabbr
        else:
            raise Err(request, 'schoolabbr illegal')

        sch.admin = User.objects.get(pk=admin_uid)
        sch.save()
        return redirect('/user/manage/school')
    except Err as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def manageGroup(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')

        group_list = Group.objects.filter(school__university=u.university).order_by("-id")
        for g in group_list:
            g.cnt = g.users.count()
        #[(x,x.users.count()) for x in Group.objects.all() if x.school.university == u.university]
        return render(request, 'newtpl/user/managegroup.html', {'groups':group_list, 'tpl':{'sp':True}})
    except Err:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def addGroup(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')
 
        if request.method == 'GET':
            school_cddt = School.objects.filter(university=u.university)
            admin_cddt = User.objects.filter(priv='group',university=u.university)
            return render(request, 'newtpl/user/addgroup.html', {'school_cddt':school_cddt, 'user':u, 'admin_cdt':admin_cddt, 'tpl':tpltrue})

        group_name = request.POST['groupname']
        school_id = request.POST['school']
        try:
            Group.addGroup(group_name, School.objects.get(pk=school_id))
        except:
            raise Err(request, 'groupname illegal')
        return redirect('/user/manage/group/')
    except Err:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def modifyGroup(request, group_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')

        try:
            g = Group.objects.get(pk=group_id)
        except:
            raise Err(request, 'group not exist')
        if g.school.university != u.university:
            raise Err(request, 'no priv')

        schs = School.objects.filter(university=u.university)
        if request.method == 'GET':
            init = {'name':g.name, 'school':g.school}
            form = ModifyGroupForm(schs, init)
            return render(request, 'newtpl/user/modifygroup.html', {'form':form, 'group':g, 'users':g.allMembers(), 'schools':schs, 'tpl':tpltrue})
        else:
            form = ModifyGroupForm(schs, request.POST)
            if form.is_valid():
                g.name = form.cleaned_data['name']
                g.school = form.cleaned_data['school']
                g.save()
                return redirect('/user/manage/group/')
            else:
                return render(request, 'newtpl/user/modifygroup.html', {'form':form, 'group':g, 'users':g.allMembers(), 'schools':schs, 'tpl':tpltrue})
    except Err:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)
 
def delMember(request, group_id, user_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')
 
        g = Group.objects.get(pk=group_id)
        utodel = User.objects.get(pk=user_id)
        if g.school.university != u.university:
            raise Err(request, 'no priv')
        if utodel.university != u.university:
            raise Err(request, 'no priv')
        g.delMember(utodel)
        return redirect('/user/modify/group/'+group_id)
    except Err:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def addMember(request, group_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')

        try:
            g = Group.objects.get(pk=group_id)
        except:
            raise Err(reqeust, 'group not exist')

        if request.method == 'GET':
            return render(request, 'newtpl/user/addmember.html', {'user':u,  'group_id':g.id, 'tpl':tpltrue})
        else:
            txt = request.POST['usernames']
            prefix = u.university.name + '#'
            studs_to_add = [prefix+n for n in txt.replace('\r', '').strip().split('\n') if len(n) > 0]
            for uname in studs_to_add:
                try:
                    utoadd = User.objects.get(username=uname)
                except:
                    return render(request, 'newtpl/error.html', {'errmsg':uname + ': ' + Const.USERNAME_NOT_EXIST})
                if not utoadd in g.allMembers():
                    g.users.add(utoadd)
            return redirect('/user/modify/group/'+group_id)
    except Err:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def showSchool(request, school_id, page_id = '1'):
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show School
    """
    tpl = {'sp':True}
    school_id = int(school_id)
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err( request, err = 'not login')
        try:
            sc = School.getById( school_id)
        except:
            raise Err( request, err='no school', 
                    log_format=( '{0}'.format( school_id), ''), 
                    user_format=( u'{0}'.format( school_id), u'艾玛！'),
                    )

        if not ( sc.university.isAdmin( u) or sc.isAdmin( u)):
            raise Err( request, err = 'no priv')

        if u.priv == 'university':
            tpl['can_modify'] = True

        courses = Course.models.Course.getBySchool(sc)

        paginator = Paginator( courses, Const.PROBLEM_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        return render(request, 'newtpl/user/show_school.html',
                { 'course_list': paginator.page(page_id), 'school': sc, 'tpl': tpl,} )
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def ResetPasswd(request, uid):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not u.priv == 'university':
            raise Err(request, 'no priv')
    
        try:
            utoreset = User.getById(uid)
        except:
            raise Err(request, 'no such user')

        if u.university != utoreset.university:
            raise Err(request, 'no priv')
            
        if request.method == 'GET':
            return render(request, 'newtpl/user/resetone.html', {'tpl':tpltrue, 'user':utoreset})

        passwd1 = request.POST['passwd1']
        passwd2 = request.POST['passwd2']
        if passwd1 == passwd2:
            utoreset.passwd = passwd1
            utoreset._encPasswd()
            utoreset.save()
        else:
            raise Err(request, 'passwd diff')

        messages.add_message(request, messages.SUCCESS, u'Complete!')
        return redirect('/user/viewuser/%d' % (utoreset.uid,))
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def resetGroupMemberPasswd(request, group_id, mode='random'):
    logger.info(str(request).replace("\n","\t"))
    try:
        try:
            g = Group.getById(group_id)
        except:
            raise Err(request, 'group not exist')
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not (u.priv == 'university' and u.university == g.school.university):
            raise Err(request, 'no priv')
        
        succ = {}
        for u in g.allMembers():
            newpasswd = u.ResetPasswd(mode)
            succ[u.username] = newpasswd
        return render(request, 'newtpl/user/resetresult.html', {'group':g, 'succ':succ, 'tpl':tpltrue})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def resetGroupMemberPasswdHomepage(request, group_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        try:
            g = Group.getById(group_id)
        except:
            raise Err(request, 'group not exist')
        u = User.getSessionUser(request.session)
        if u == False:
            raise Err(request, 'not login')
        if not (u.priv == 'university' and u.university == g.school.university):
            raise Err(request, 'no priv')

        return render(request, 'newtpl/user/resethomepage.html', {'group':g, 'tpl':tpltrue})
    except Err as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)
