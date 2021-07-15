from django.shortcuts import render,redirect

from .models import SUser
from .doctor_confirm import clean_session, login_confirm
import patients.views as p_views
# Create your views here.


def user_login(request):
    # 清除登录session
    clean_session(request)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        res = SUser.objects.filter(username=username, password=password).values()
        if len(res) == 0:
            print('账号或密码错误！')
            return render(request, 'login.html', context={'login_flag': True})
        else:
            print('登录成功！')
            # print(res[0]['name'])
            # 保存登录session
            login_confirm(request, res[0]['id'], username)
            return redirect('/patients/get_patient_by_search')
    else:
        return render(request, 'login.html', context={'login_flag': False})


