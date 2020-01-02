from django.http.response import JsonResponse
from .models import User, UserStatus
from divices.models import divices, coordinate
from django.db.models import Q, F
from django.http import HttpResponse
import json, random, time


# 用户登入验证
def post_login(request):
    # session_data = request.session.get('session_id', None)
    # # 如果是第一次登入，设置sessio
    # if not session_data:
    #     request.session['session_id'] = 'w532fdsy621=-dfsorelsgkldgkldk'
    # # 获取session
    # hello = request.session.get('session_id')
    # print(hello)

    json_str = request.body.decode()
    user_data = json.loads(json_str)
    user = User.objects.filter(Q(username=user_data["username"]) & Q(password=user_data["password"]))
    # 查询用户关联的站点
    ip_list = [i.divice_ip for i in user[0].divices_set.all()]
    u_flg = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 5))
    # print(u_flg)
    if user:
        # 1.将用户的登入信息存入数据表
        UserStatus.objects.create(
            u_username=user[0].username,
            u_grader=user[0].u_backup,
            u_logintime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            u_outtime='null',
            u_flg=u_flg

        )
        dict_data = {
            "user_id": user[0].id,
            "username": user[0].username,
            "grade": user[0].u_backup,
            "ip": ip_list,  # 查询用户关联的站点
            'u_flg': u_flg
        }
        return JsonResponse(dict_data, safe=False)  # 转换为json字符串类型
    else:
        return JsonResponse("error", safe=False)


# 保存用户退出信息
def out_put(request):
    json_str = request.body.decode()
    user_data = json.loads(json_str)
    print(user_data)
    user_data = UserStatus.objects.filter(u_username=user_data['user']).filter(u_flg=user_data['u_flg'])
    print(user_data)
    if user_data:
        user_data.update(
            u_outtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            u_flg=""
        )
    return JsonResponse("ok", safe=False)


# 查询用户信息
def userstatus_post(request):
    json_str = request.body.decode()
    user_data = json.loads(json_str)
    start_time = time.strptime(user_data['start_time'], "%Y-%m-%d %H:%M:%S")
    end_time = time.strptime(user_data['end_time'], "%Y-%m-%d %H:%M:%S")
    login_time = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
    out_time = time.strftime("%Y-%m-%d %H:%M:%S", end_time)
    print(login_time)
    user_status = UserStatus.objects.filter(Q(u_username=user_data['user']) & Q(
        u_logintime__gt=login_time) & Q(u_outtime__lt=out_time))
    print(user_status)
    user_list = []
    for i in user_status:
        data_dict = {
            "username": i.u_username,
            "grader": i.u_grader,
            "logintime": i.u_logintime,
            "outtime": i.u_outtime
        }
        user_list.append(data_dict)
    return JsonResponse(user_list, safe=False)


# 密码确认
def password_verily(request):
    json_str = request.body.decode()
    user_data = json.loads(json_str)
    user = User.objects.filter(Q(username=user_data["username"]) & Q(password=user_data["password"]))
    print('>>>>>>>>>>>>>>>',user_data)
    print('>>>>>>>>>>>>>>>',user)
    if user:
        return JsonResponse('ok', safe=False)
    else:
        return JsonResponse('wrong password', safe=False)
