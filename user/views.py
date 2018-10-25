from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,reverse
import json
from datetime import datetime,timedelta
from user import models
from course.models import CourseComment
from course.models import CourseCommentLike
from utils.userlogin import *
from utils.token import *
from utils import token as toto
from user import models
from utils.userlogin import *
from utils.token import *
# from utils import token as toto
# from qiniu import Auth, put_file, etag
# import qiniu.config
from collections import OrderedDict
import uuid
import random
from course import models as course_models
from shop import models as shop_models
from datetime import datetime,timedelta
def index(request):
    # return render(request,'user_index.html')
    return HttpResponse('i am index')

def getUserById(request,myid):

    # return HttpResponse('i am login'+myid)
    url=reverse('user:index',kwargs={"id":myid})
    print(url)
    return  redirect(url)
def login(request):
    if request.method == "POST":
        user = json.loads(request.body)
        res=login_ser(user)
        resp=JsonResponse(res)
        # print(res)
        if res['code']=='201':
            token=makeToken(res['telephone'],res['user_id'])
            resp['token']=token
            resp["Access-Control-Expose-Headers"] = "token"
            return resp
        else:
            return JsonResponse(res)

def regist(request):
    try:
        if request.method == "POST":
            newuser = json.loads(request.body)
            res = regist_ser(newuser)
            print(res)
            if res and res['code'] == '203':
                resp = JsonResponse(res)
                token = makeToken(res['telephone'], res['user_id'])
                resp['token'] = token
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                return JsonResponse(res, safe=False)
    except Exception as ex:
        return JsonResponse({"code":"500"})

def changePassword(request):
    try:
        if request.method == "POST":
            user = json.loads(request.body)
            print(user)
            res = change_password(user)
            print(res)
            # print(res)
            if res and res['code'] == '203':
                resp = JsonResponse(res)
                # token = makeToken(res['id'],res['telephone'])
                token = makeToken(res['telephone'], res['user_id'])

                resp['token'] = token
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                return JsonResponse(res, safe=False)
    except Exception as ex:
       return JsonResponse({"code":"500"})

def userInfo(request):
    try:
        # if request.method=="POST":
        #     token=request.META.get("HTTP_TOKEN")
        #     res=toto.openToken(token)
        #     user_id=res['user_id']
        #     result=models.UserInfo.objects.filter()
        return JsonResponse({"code":"203"})
    except Exception as ex:
        return JsonResponse({"code":"404"})

def UpUser(request):
    try:
        if request.method=="POST":

            r=json.loads(request.body)
            token = r["token"]
            print(r)
            res=toto.openToken(token)
            user_id=res['user_id']
            print(user_id)
            # print(r['sex'])
            s=list(models.Sex.objects.filter(name=r['sex']).values())
            sex_id=s[0]['id']
            # A=models.Sex.objects.get(name=r['sex'])
            # print(type(A))
            # print(A)
            # print(sex_id)
            icon_id=1
            result=[]
            ss={
                "name":r['name'],
                "height":r['height'],
                "width":r['width'],
                "birth":r['birth'],
                "sex_id": sex_id,
                "icon_id":icon_id,
                "user_id":user_id
            }
            print(ss)
            try:
                models.UserInfo.objects.create(**ss)
                # print('****'+aa)
            except Exception as ex:
                print(ex)
        return JsonResponse({"code": "201"})
    except Exception as ex:
        return JsonResponse({"code":"404"})


def UserAddress(request):
    if request.method=='POST':
        try:
            address=json.loads(request.body)
            print(address)
            token = address['headers']['token']
            print(token)
            if token:
                res=openToken(token)
                print(res)
                if res:
                    user_id=res['user_id']
                    print(user_id)
                    ss={
                        "user_id":user_id,
                        "province":address['province'],
                        "city":address['city'],
                        "area":address['area'],
                        "detailaddress":address['detailaddress'],
                        "telephone":address['telephone'],
                        "youbian":address['youbian'],
                        "recievename":address['recievename']
                    }
                    print(ss)
                    try:
                        models.Address.objects.create(**ss)
                    except Exception as ex:
                        print(ex)
                    return JsonResponse({"code":"202"})
                else:
                    return JsonResponse({"code":"411"})
            else:
                return JsonResponse({"code": "411"})
        except Exception as ex:
            return JsonResponse({"code":"500"})

def delAddress(request):
    if request.method=='POST':
        try:
            r = json.loads(request.body)
            print(r)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                result=models.Address.objects.filter(id=r['id']).values_list()
                if result:
                    models.Address.objects.filter(id=r['id']).delete()
                    return JsonResponse({"code": "208"})
                else:
                    return JsonResponse({"code":"413"})
            else:
                return JsonResponse({"code":"411"})
        except Exception as ex:
            return JsonResponse({"code":"500"})

def GetNameByTel(request):
    try:
        if request.method=="POST":
            # print('this is getnamebytel')
            r=json.loads(request.body)
            token=r['headers']['token']
            # print(token)
            res=openToken(token)
            # print(res)
            if res:
                user_id=res['user_id']
                name=list(models.UserInfo.objects.filter(user_id=user_id).values('name','sex','height','width','icon__icon_url','birth'))
                if name:
                    user_year = str(name[0]['birth']).split('-')[0]
                    now_year = str(datetime.now()).split('-')[0]
                    age = int(now_year) - int(user_year)
                    userinfo = []
                    ss = {
                        "name": name[0]['name'],
                        "sex": name[0]['sex'],
                        "height": name[0]['height'],
                        "width": name[0]['width'],
                        "icon_url": name[0]['icon__icon_url'],
                        "age": age
                    }
                    # print(ss)
                    userinfo.append(ss)
                    return HttpResponse(json.dumps(userinfo,ensure_ascii=False))
                else:
                    return JsonResponse({"code":"415"})
            else:
                return JsonResponse({"code":"411"})
    except Exception as ex:
        return JsonResponse({"code":"500"})

def GetAddress(request):
    if request.method=='POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            if token:
                res = openToken(token)
                if res:
                    user_id = res['user_id']
                    print(user_id)
                    address=list(models.Address.objects.filter(user_id=user_id).values())
                    if address:
                        pass
                    else:
                        return JsonResponse({"code":"419"})
            return HttpResponse(json.dumps(address,ensure_ascii=False))
        except Exception as ex:
            return JsonResponse({"code":"500"})


# 七牛云token
def qiniuToken(request):
    try:
        if request.method=='POST':
            r=json.loads(request.body)
            token=r['headers']['token']
            res=openToken(token)
            if res:
                access_key = 'Ib28fQUwpKMw82G4NNw-TAdDooGGrRWOdadnuamM'
                secret_key = 'evfP2KZpTRrP3rqO39I7Sc5n18_QxCbvFgSuArxc'
                # 构建鉴权对象
                q = Auth(access_key, secret_key)
                # 要上传的空间
                bucket_name = 'Lotto'
                # 上传到七牛后保存的文件名
                file = r['key']
                print(file)
                key = str(uuid.uuid4()) + '.' + file.split('.')[-1]
                # 生成上传 Token，可以指定过期时间等 一天
                token = q.upload_token(bucket_name, key, 3600)
                return JsonResponse({"token": token, "filename": key})
            else:
                return JsonResponse({"code":"411"})
    except Exception as ex:
        return JsonResponse({"code":"500"})

    try:
        fname=request.GET.get('fname')
        user_id=request.GET.get('user_id')
        obj = models.Icon.objects.create(icon_url=fname)
        # 当前插入图片的ID为obj.id
        # 修改用户的头像
        count = models.UserInfo.objects.filter(user_id=user_id).update(icon_id=obj.id)
        return JsonResponse({"res": "修改成功"}, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        return JsonResponse({"res": "修改失败"}, json_dumps_params={'ensure_ascii': False})

def upload(requset):
    if requset.method=='POST':
        try:
            user_id=requset.POST.get('userid')
            print(user_id)
            file=requset.FILES.get('usericon')
            fname=str(uuid.uuid4())+'.'+file.name.split('.')[1]
            print(fname)
            with open(fname,'wb+') as fp:
                for c in file.chunks():
                    fp.write(c)
            return JsonResponse({"code": "200"})
        except Exception as ex:
            return JsonResponse({"code": "500"})


def Getaction(request):
    if request.method=='POST':
        try:
            courses=[]
            r=json.loads(request.body)
            print('this is getaction')
            # print(r)
            token=r['headers']['token']
            print('this is token'+token)
            res=openToken(token)
            if res:
                user_id=res['user_id']
                print(user_id)
                courseid=list(models.AddCourse.objects.filter(user_id=user_id).values('course_id'))
                print(courseid)
                if courseid:
                    for i in range(len(courseid)):
                        course_id=courseid[i]['course_id']
                        course=course_models.Course.objects.filter(id=course_id).values('name','level__level','picture__url','type__type_name','machine__name','id').first()
                        courses.append(course)
                else:
                    return JsonResponse({"code":"466"})
            else:
                return JsonResponse({"code":"411"})
            return HttpResponse(json.dumps(courses,ensure_ascii=False))
        except Exception as ex:
            return JsonResponse({"code":"555"})

def DelAction(request):
    if request.method=='POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                course = list(models.AddCourse.objects.filter(user_id=user_id).values())
                if course:
                    models.AddCourse.objects.filter(user_id=user_id,course_id=r['id']).delete()
                    return JsonResponse({"code":"209"})
                else:
                    return JsonResponse({"code":"466"})
            else:
                return JsonResponse({"code": "411"})
        except Exception as ex:
            return JsonResponse({"code":500})

# 给课程添加评论
def addComment(request):
    try:
        if request.method=="POST":
            data = json.loads(request.body.decode('utf-8'))
            content=data['content']

            course_id = int(data['cid'])
            data = data['headers']
            token=data['token']
            res=toto.openToken(token)
            # result=models.AddCourse.objects.filter(course_id=course_id,user_id=res['user_id']).values()
            if res:
                addcomment = {
                    'course_id': course_id,
                    'user_id': res['user_id'],
                    'content':content,
                }
                CourseComment.objects.create(**addcomment)
                # print(res['user_id'])
                return JsonResponse({"code":"210"})
            else:
                return JsonResponse({"code":"没登陆"})

    except Exception as ex:
        print(ex)
        return JsonResponse({"code":"404"})

# 给课程评论点赞
def likeComment(request):
    try:
        if request.method=="POST":
            data = json.loads(request.body.decode('utf-8'))

            # print('oooo')
            # print(data)
            commentid = int(data['commentid'])
            # print(commentid)

            # data = data['headers']
            token=data['headers']['token']

            # print(token)
            res=openToken(token)
            # print(res)
            if res:
                result=CourseCommentLike.objects.filter(comment_id=commentid,user_id=res['user_id']).values()
                if result:
                    CourseCommentLike.objects.filter(comment_id=commentid,user_id=res['user_id']).delete()
                    likenum = CourseComment.objects.filter(id=commentid).values('likes')[0]['likes']
                    res = likenum - 1
                    CourseComment.objects.filter(id=commentid).update(likes=res)
                    return JsonResponse({"code": "410"})
                else:
                    addcomment = {
                        'comment_id': commentid,
                        'user_id': res['user_id'],
                    }
                    CourseCommentLike.objects.create(**addcomment)
                    likenum=CourseComment.objects.filter(id=commentid).values('likes')[0]['likes']
                    res=likenum+1
                    CourseComment.objects.filter(id=commentid).update(likes=res)

                    return JsonResponse({"code": "210"})
            else:
                return JsonResponse({"code": "没登陆"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code":"404"})


def GetLove(request):
    if request.method=='POST':
        try:
            goods=[]
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                print(user_id)
                love = list(shop_models.loveGood.objects.filter(user_id=user_id).values('good_id'))
                print(love)
                if love:
                    for i in range(len(love)):
                        good_id=love[i]['good_id']
                        good_url=list(shop_models.GoodPicture.objects.filter(good_id=good_id,size=1).values('url','good_id','good__name','good__intergal'))
                        b = OrderedDict()
                        for item in good_url:
                            b.setdefault(item['good_id'], {**item, })
                        b = list(b.values())
                        ss={
                            "good_id":b[0]['good_id'],
                            "good_name":b[0]['good__name'],
                            "good_intergal":b[0]['good__intergal'],
                            "good_url":b[0]['url']
                        }
                        goods.append(ss)
                else:
                    return JsonResponse({"code": "421"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(goods,ensure_ascii=False))
        except Exception as ex:
            print(ex)
            return JsonResponse({"code":"500"})

def DelLove(request):
    if request.method=='POST':
        try:
            r=json.loads(request.body)
            print(r)
            token=r['headers']['token']
            good_id=r['good_id']
            res=openToken(token)
            if res:
                user_id=res['user_id']
                good=shop_models.loveGood.objects.filter(user_id=user_id,good_id=good_id).values()
                if good:
                    shop_models.loveGood.objects.filter(user_id=user_id,good_id=good_id).delete()
                else:
                    return JsonResponse({"code":"422"})
            else:
                return JsonResponse({"code":"411"})
            return JsonResponse({"code":"213"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code":"500"})