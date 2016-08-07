# coding: utf-8
# Create your views here.

from django.shortcuts import render, redirect
from kari.const import Const
from common.err import Err
from User.models import User
from Contest.models import Contest, ContestProblem
from Submission.models import Submission
from Cheat.models import Cheat
from Cheat.forms import ChooseProbForm
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from Submission.general_forms import addGeneralForm, generalListForm
from Submission.forms import addSubmissionForm, submissionListForm

def addRecord(request, cid):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, err='not login')

        c = Contest.getById(cid)
        try:
            c.canBeManaged(u)
        except:
            raise Err(request, err='no priv')

        cp = c.getContestProblem()

        if request.method == 'POST':
            form = ChooseProbForm(cp, request.POST) 
            if form.is_valid():
                Cheat.addRecord(cp_set=form.cleaned_data['contest_problem'])
                Cheat.antiCheat()
                return redirect('Cheat:show_cheat_result', cid=c.cid)
            else:
                raise Err(request, err='unknown err')
        else:
            form = ChooseProbForm(cp)
            return render(request, 'newtpl/cheat/addRecord.html', {'tpl':{'sp':True,}, 'contest':c, 'form':form,})
    except Exception as e:
        return render(request, Err.ERROR_PAGE)

def addRecord2(request, cid):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, err='not login')

        c = Contest.getById(cid)
        try:
            c.canBeManaged(u)
        except:
            raise Err(request, err='no priv')

        cp = c.getContestProblem()
        Cheat.addRecord(cp_set=cp)
        Cheat.antiCheat()
        return redirect('Cheat:show_cheat_result', cid=c.cid)
    except Exception as e:
        return render(request, Err.ERROR_PAGE)
 
def showResult(request, cid, page='1'):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, err='not login')

        c = Contest.getById(int(cid))
        try:
            c.canBeManaged(u)
        except:
            raise Err(request, err='no priv')

        if ('threshold' in request.GET) and request.GET['threshold']:
            threshold = float(request.GET['threshold'])
        else:
            threshold = Const.CHEAT_DEFAULT_THRESHOLD
        
#------------form-------------
        idxList = [(cp.problem_index, cp.problem_index) for cp in c.getContestProblem()]
        langList = [('gcc','GNU C'), ('g++','GNU C++'), ('java','java')]
        form = submissionListForm(idxList, langList, request.GET)
        if form.is_valid():
            if form.cleaned_data['problem_index']:
                try:
                    contestProb = ContestProblem.getBy( c, form.cleaned_data['problem_index'])
                except:
                    contestProb=None
                    # raise Exception(u'contest problem not found')
            else:
                contestProb=None
        else:
            raise Err( request, err='example err', 
                    log_format=( 'form invalid', ''), 
                    user_format=( u'输入的内容不合法', '')
                    )

#------------form--------------


        cheatList = Cheat.getCheatList(contest=c, threshold=0)
        
#------------filter------------
        if contestProb:
            cheatList = cheatList.filter(contest_problem=contestProb)
        if form.cleaned_data['username']:
            cheatList1 = cheatList.filter(sub1__user__username__icontains=form.cleaned_data['username'])
            cheatList2 = cheatList.filter(sub2__user__username__icontains=form.cleaned_data['username'])
            cheatList = cheatList1 | cheatList2
#------------filter------------

        paginator = Paginator(cheatList, Const.CHEAT_PER_PAGE)
        page = min(max(int(page), 1), paginator.num_pages)

        cl = paginator.page(page)
        ipa = []
        ipb = []
        for idx, element in enumerate(cl):
            info_a = eval(element.sub1.other_info)
            info_b = eval(element.sub2.other_info)
            #cl[idx] = {'c': element, 'ip_a': info_a['submit_ip'], 'ip_b': info_b['submit_ip']}
            ipa.append(info_a['submit_ip'])
            ipb.append(info_b['submit_ip'])
        
        return render(request, 'newtpl/cheat/showResult.html', {'tpl':{'sp':True,}, 'contest':c, 'cheat_list':cl, 'ipa':ipa,'ipb':ipb, 'form':form })
    except Exception as e:
        return render(request, Err.ERROR_PAGE)

# def codeDiff(request, ctid):
#     try:
#         u = User.getSessionUser(request.session)
#         if not u:
#             raise Err(request, err='not login')
#         ct = Cheat.objects.select_related('sub1__user', 'sub2__user').get(ctid=ctid)
# 
#         try:
#             ct.contest.canBeManaged(u)
#         except:
#             raise Err(request, err='no priv')
# 
#         return render(request, 'newtpl/cheat/codeDiff.html', {'tpl':{'sp':True,}, 'sub1':ct.sub1, 'sub2':ct.sub2})
# 
# 
#     except Exception as e:
#         return render(request, Err.ERROR_PAGE)
    """
    try:
        cheat_list = Cheat.getCheatList()
        cheat_user_list = []
        for cl in cheat_list:
            cheat_user = []
            cheat_user.append(cl.user1)
            cheat_user.append(cl.user2)
            cheat_user.append(cl.contest_problem)
            cheat_user.append(cl.ratio)
            cheat_user_list.append(cheat_user)

        return render_to_response("newtpl/Cheat/showResult.html", {'cheat_list':cheat_user_list})
    except Exception as e:
        #return render( request, 'error.html','errmsg'=str(e))
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e), })
    """

def showCodeDiff(request, ct_id):
    """
    show codes of the two diffed submission
    """
    try:
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')

        ct_id = int( ct_id)
        ct = Cheat.objects.select_related('sub1__user', 'sub2__user').get(ctid=ct_id)

        # try:
        #     ct.contest.canBeManaged(u)
        # except:
        #     raise Err(request, err='no priv')

        s_a = ct.sub1
        s_b = ct.sub2
        #sid_a = int( sid_a)
        #sid_b = int( sid_b)

        #try:
        #    s_a = Submission.getById( sid_a)
        #except:
        #    raise Err( request, err='no submission',
        #            log_format=( '{0}'.format( sid_a), ''),
        #            user_format=( u'{0}'.format( sid_a), u'不要搞笑！！'),
        #            )

        #try:
        #    s_b = Submission.getById( sid_b)
        #except:
        #    raise Err( request, err='no submission',
        #            log_format=( '{0}'.format( sid_b), ''),
        #            user_format=( u'{0}'.format( sid_b), u'不要搞笑！！'),
        #            )

        if not Submission.canViewCode( s_a, u):
            raise Err( request, err = 'no priv')

        if not Submission.canViewCode( s_b, u):
            raise Err( request, err = 'no priv')

        info_a = eval( s_a.other_info)
        info_b = eval( s_b.other_info)

        ip_a = info_a['submit_ip']
        ip_b = info_b['submit_ip']

        brush_a = Const.BRUSH[s_a.code_language]
        brush_b = Const.BRUSH[s_b.code_language]

        # brush_a = s_a.code_language
        # brush_b = s_b.code_language

        # info['status_cn'] = Const.STATUS_CN[info['status']]
        #if 'case_result' in info:
        #    for seq in info['case_result']:
        #        seq['res_cn'] = JUDGE_RES_CN[seq['res']]

        return render( request, 'newtpl/cheat/code_diff.html', { 'ct_obj': ct, 'sub_a': s_a, 'sub_b': s_b, 'code_a': default_storage.open(s_a.code_file).read().decode('utf-8', 'ignore'), 'code_b': default_storage.open(s_b.code_file).read().decode('utf-8', 'ignore'), 'tpl': { 'sp': True },  'brush_a': brush_a, 'brush_b': brush_b, 'ip_a': ip_a, 'ip_b': ip_b})

    except Exception as e:
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )
