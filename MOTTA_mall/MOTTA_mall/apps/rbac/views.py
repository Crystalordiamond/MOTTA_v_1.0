from django.http.response import JsonResponse
from .models import User
from divices.models import divices, coordinate
from django.db.models import Q, F
from django.http import HttpResponse
import json


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
    if user:
        dict_data = {
            "user_id": user[0].id,
            "username": user[0].username,
            "grade": user[0].u_backup,
            "ip": ip_list,  # 查询用户关联的站点
            # 'token': Token.objects.create(user=user)
        }
        return JsonResponse(dict_data, safe=False)  # 转换为json字符串类型
    else:
        return JsonResponse("error", safe=False)
