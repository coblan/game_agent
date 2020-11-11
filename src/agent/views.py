from django.shortcuts import render,HttpResponse
from .models import AgentUser
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json

def player_regist(request,regist_code):
    agent_user = AgentUser.objects.get(regist_code=regist_code)
    dc = {
        'qq':agent_user.qq,
        'regist_code':regist_code,
    }
    return render(request, 'agent/regist.html',context=dc)

@csrf_exempt
def postregister(request):
    account = request.POST.get('account')
    pwd = request.POST.get('pwd')
    code = request.POST.get('code')
    agent = request.POST.get('regist_code')
    dc = {}
    if not code:
        dc['error']='请填写验证码' 
    elif not pwd:
        dc['error']='必须填写密码' 
    else:
        dc ['success']= True
    return HttpResponse(json.dumps(dc), content_type="application/json")