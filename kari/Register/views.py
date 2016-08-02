# coding: utf-8
from Register.models import Contestant, Team
from Register.forms import TeamRegisterForm, TeamLoginForm, ContestantForm
from Register.const import Const
import django.contrib.sessions
from django.shortcuts import render, redirect
from django.contrib import messages
from common.utils import referer
import logging

logger = logging.getLogger('django')

def mainPage(request):
    return render(request, 'newtpl/register/index.html', {})
    #return HttpResponseRedirect('http://www.saikr.com/bupt/acm')

def endedPage(request):
    return render(request, 'newtpl/register/ended.html', {})

def teamLogin(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        if request.method != 'POST':
            return render(request, 'newtpl/register/team_login.html', {})
        name = request.POST['name']
        passwd = request.POST['passwd']
        t = Team.getByName(name)
        t.matchPasswd(passwd)

        # Success
        request.session['team_id'] = t.pk
        messages.add_message(request, messages.SUCCESS, u'登录成功！')
        return redirect('Register:team_info', tid = t.pk)
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, u'用户名或密码错误')
        return render(request, 'newtpl/register/team_login.html', {})

def teamLogout(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        try:
            team = Team.getSessionTeam(request.session)
        except:
            raise Exception(u'您尚未登入！')
        request.session['team_id'] = None
        messages.add_message(request, messages.SUCCESS, u'已登出！')
        return redirect('Register:team_login')
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:home')

def teamRegister(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        if request.method != 'POST':
            return render(request, 'newtpl/register/team_register.html', {})
        form = TeamRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            passwd1 = form.cleaned_data['passwd1']
            passwd2 = form.cleaned_data['passwd2']
            if passwd1 != passwd2:
                raise Exception(u'两次密码不一致！')
            team = Team.addTeam(name, passwd1)

            # Success
            messages.add_message(request, messages.SUCCESS, u'%s队伍注册成功！请登录后添加队员信息' % name)
            request.session['team_id'] = team.pk
            return redirect('Register:team_info', team.pk) # TO BE FIXED
        else:
            raise Exception('Invalid Informations')        
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return render(request, 'newtpl/register/team_register.html', {})

def teamInfo(request, tid):
    logger.info(unicode(request).replace('\n', '\t'))
    tid = int(tid)
    try:
        team = Team.getSessionTeam(request.session)
    except Exception as e:
        messages.add_message(request, messages.INFO, u'请先登录！')
        return redirect('Register:team_login')
    try:
        if team.pk != tid:
            raise Exception(u'您没有查看该队伍信息的权限！')
        target_team = Team.getById(tid)
        members = Contestant.getTeamContestant(target_team)
        full = True if len(members) >= 3 else False
        return render(request, 'newtpl/register/team_info.html', {'target_team': target_team, 'members': members, 'full': full})
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:team_info', team.pk)

def addTeamMember(request, tid):
    logger.info(unicode(request).replace('\n', '\t'))
    tid = int(tid)
    try:
        team = Team.getSessionTeam(request.session)
    except Exception as e:
        request.session['team_id'] = None
        messages.add_message(request, messages.INFO, u'请先登录！')
        return redirect('Register:team_login')

    try:
        if team.pk != tid:
            raise Exception(u'您没有查看该队伍信息的权限！')
        
        target_team = Team.getById(tid)
        if request.method != 'POST':
            return render(request, 'newtpl/register/add_member.html', {'target_team': target_team, 'gender_choices': Const.GENDER_CHOICES, 'school_choices': Const.SCHOOL_CHOICES, 'grade_choices': Const.GRADE_CHOICES})

        form = ContestantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            grade = form.cleaned_data['grade']
            mobile = form.cleaned_data['mobile']
            student_id = form.cleaned_data['student_id']
            class_id = form.cleaned_data['class_id']
            school = form.cleaned_data['school']
            Contestant.addContestant(name, gender, grade, email, mobile, student_id, class_id, school, target_team)
        else:
            raise Exception(u'输入的内容不合法！')

        # Success
        messages.add_message(request, messages.SUCCESS, u'添加队员%s成功！请等待管理员审核' % name)
        target_team.status = '等待审核'
        target_team.updateStatus('Pending')
        return redirect('Register:team_info', tid)
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:team_info', team.pk)

def modifyTeamMember(request, cid):
    logger.info(unicode(request).replace('\n', '\t'))
    cid = int(cid)
    try:
        team = Team.getSessionTeam(request.session)
    except Exception as e:
        request.session['team_id'] = None
        messages.add_message(request, messages.INFO, u'请先登录！')
        return redirect('Register:team_login')

    try:
        contestant = Contestant.getById(cid)
        belong_team = contestant.team
        if team.pk != belong_team.pk:
            raise Exception(u'您没有查看该队伍信息的权限！')
        
        if request.method != 'POST':
            return render(request, 'newtpl/register/modify_member.html', {'gender_choices': Const.GENDER_CHOICES, 'school_choices': Const.SCHOOL_CHOICES, 'grade_choices': Const.GRADE_CHOICES, 'contestant': contestant})

        form = ContestantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            grade = form.cleaned_data['grade']
            mobile = form.cleaned_data['mobile']
            student_id = form.cleaned_data['student_id']
            class_id = form.cleaned_data['class_id']
            school = form.cleaned_data['school']
            contestant.modifyContestant(name, gender, grade, email, mobile, student_id, class_id, school, belong_team)
        else:
            raise Exception(u'输入的内容不合法！')

        # Success
        messages.add_message(request, messages.SUCCESS, u'修改队员%s成功！请等待管理员审核' % name)
        belong_team.updateStatus('Pending')
        return redirect('Register:team_info', belong_team.pk)
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:modify_member', cid)

def resetPasswd(request, tid):
    logger.info(unicode(request).replace('\n', '\t'))
    tid = int(tid)
    try:
        team = Team.getSessionTeam(request.session)
    except Exception as e:
        messages.add_message(request, messages.INFO, u'请先登录！')
        return redirect('Register:team_login')
    try:
        if team.pk != tid:
            raise Exception(u'您没有相关的权限！')
        target_team = Team.getById(tid)
        if request.method != 'POST':
            return render(request, 'newtpl/register/reset_passwd.html', {'target_team': target_team})

        passwd1 = request.POST['passwd1']
        passwd2 = request.POST['passwd2']
        if passwd1 != passwd2:
            raise Exception(u'两次密码不一致！')

        target_team.resetPasswd(passwd1)
        # Success
        messages.add_message(request, messages.SUCCESS, u'修改密码成功！')
        return redirect('Register:team_info', tid)
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:reset_passwd', team.pk)

def viewAllTeams(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        admin = request.session.get('admin', None)
        if not admin:
            messages.add_message(request, messages.INFO, unicode('Invalid Key'))
            return redirect('Register:admin_login')

        team_list = Team.getAllTeams()
        pending = team_list.filter(status = 'Pending').count()
        accepted = team_list.filter(status = 'Accepted').count()
        failed = team_list.filter(status = 'Failed').count()
        skipped = team_list.filter(status = 'Skipped').count()

        teams = []
        for team in team_list:
            members = Contestant.getTeamContestant(team)
            teams.append({'info': team, 'members': members})
        return render(request, 'newtpl/register/view_teams.html', {'teams': teams, 'pending': pending, 'accepted': accepted, 'failed': failed, 'skipped': skipped})

    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:view_teams')

def viewAcceptedTeams(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        admin = request.session.get('admin', None)
        if not admin:
            messages.add_message(request, messages.INFO, unicode('Invalid Key'))
            return redirect('Register:admin_login')

        all_team_list = Team.getAllTeams()
        ac_team_list = all_team_list.filter(status = 'Accepted')
        #ac_team_list = all_team_list.filter(status = 'Finals')
        #ac_team_list = all_team_list.filter(status = 'Bronze')

        teams = []
        for team in ac_team_list:
            members = Contestant.getTeamContestant(team)
            teams.append({'info': team, 'members': members})
        return render(request, 'newtpl/register/view_accepted_teams.html', {'teams': teams})

    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:view_accepted_teams')

def adminLogin(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        if request.method != 'POST':
            return render(request, 'newtpl/register/enter_admin.html', {})

        key = request.POST['key']
        if key != Const.ADMIN_KEY:
            raise Exception('Invalid Key')
        request.session['admin'] = True
        return redirect('Register:view_teams')
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect(referer(request))
        return redirect('Register:admin_login')

def adminLogout(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        request.session['admin'] = None
        raise Exception('Admin logout Successfully')
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:admin_login')

def judgeTeam(request, tid = 1):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        admin = request.session.get('admin', None)
        if not admin:
            messages.add_message(request, messages.INFO, u'Not admin!')
            return redirect('Register:admin_login')

        tid = int(tid)
        team = None
        while True:
            try:
                team = Team.getById(tid)
            except:
                raise Exception('No Pending Teams!')
            if team.status == 'Skipped' or team.status == 'Pending':
                break
            tid += 1
       
        team_list = Team.getAllTeams()
        pending = team_list.filter(status = 'Pending').count()
        accepted = team_list.filter(status = 'Accepted').count()
        failed = team_list.filter(status = 'Failed').count()
        skipped = team_list.filter(status = 'Skipped').count()
        members = Contestant.getTeamContestant(team)
        return render(request, 'newtpl/register/judge_team.html', {'team': team, 'members': members, 'pending': pending, 'accepted': accepted, 'failed': failed, 'skipped': skipped, 'admin': True})

    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.INFO, unicode(e))
        return redirect('Register:view_teams')

def judgeTeamResult(request, tid, result):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        admin = request.session.get('admin', None)
        if not admin:
            messages.add_message(request, messages.INFO, u'Not admin!')
            return redirect('Register:admin_login')

        valid_result = False
        for status in Const.TEAM_STATUS:
            if status == result:
                valid_result = True
                break
        if not valid_result:
            raise Exception('Invalid Result')

        tid = int(tid)
        team = Team.getById(tid)
        team.updateStatus(result)
        return redirect('Register:judge_team')
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.WARNING, unicode(e))
        return redirect(referer(request))

def showContest(request):
    logger.info(unicode(request).replace('\n', '\t'))
    try:
        pass
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.add_message(request, messages.WARNING, unicode(e))
        return redirect(referer(request))
