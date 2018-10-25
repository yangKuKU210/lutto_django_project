from shop import models
from user import models as user_models
from utils.shop import *
from collections import OrderedDict
import json
from django.http import HttpResponse, response, JsonResponse
from . import models
from django.db.models import Count
from utils.token import *
import datetime
# Create your views here.
def index(request):
    pass


def search(request):
    try:
        name=request.GET.get('name')
        index=request.GET.get('index')
        print(name)
        pagesize=5
        if index:
            index = int(index)
        else:
            index=1
        # print(name)
        G=[]
        if name:
            good=list(models.Goods.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values('kucun','name','intergal','gooddesc','goodbrand__name','goodclass__name','id'))
            if good:
                for g in good:
                    ss={
                        "goods_kuncun":g['kucun'],
                        "goods_name":g['name'],
                        "goods_intergal":g['intergal'],
                        "goods_gooddesc":g['gooddesc'],
                        "good_class_name":g['goodclass__name'],
                        "goods_id":g['id'],
                        "goods_band_name":g['goodbrand__name']
                    }
                    G.append(ss)
                    goods = Greatgoods(G)
            else:
                pass
            good=list(models.GoodClass.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values('goods__kucun','goods__name','goods__intergal','goods__gooddesc','goods__goodbrand__name','name','goods__id'))
            if good:
                print(good)
                for g in good:
                    ss={
                        "goods_kuncun":g['goods__kucun'],
                        "goods_name":g['goods__name'],
                        "goods_intergal":g['goods__intergal'],
                        "goods_gooddesc":g['goods__gooddesc'],
                        "good_class_name":g['name'],
                        "goods_id":g['goods__id'],
                        "goods_band_name":g['goods__goodbrand__name']
                    }
                    G.append(ss)
                    goods = Greatgoods(G)
            else:
                pass
            good=list(models.GoodBrand.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values('goods__kucun','goods__name','goods__intergal','goods__gooddesc','name','goods__goodclass__name','goods__id'))
            if good:
                for g in good:
                    ss={
                        "goods_kuncun":g['goods__kucun'],
                        "goods_name":g['goods__name'],
                        "goods_intergal":g['goods__intergal'],
                        "goods_gooddesc":g['goods__gooddesc'],
                        "good_class_name":g['goods__goodclass__name'],
                        "goods_id":g['goods__id'],
                        "goods_band_name":g['name']
                    }
                    G.append(ss)
                goods =Greatgoods(G)
            else:
                pass
        else:
            good = list(models.Goods.objects.filter()[pagesize * (index - 1):pagesize * index].values('kucun','name', 'intergal', 'gooddesc', 'goodbrand__name','goodclass__name','id'))
            if good:
                for g in good:
                    ss = {
                        "goods_kuncun": g['kucun'],
                        "goods_name": g['name'],
                        "goods_intergal": g['intergal'],
                        "goods_gooddesc": g['gooddesc'],
                        "good_class_name": g['goodclass__name'],
                        "goods_id": g['id'],
                        "goods_band_name": g['goodbrand__name']
                    }
                    G.append(ss)
                    goods = Greatgoods(G)
        return HttpResponse(json.dumps(Greatgoods(G), ensure_ascii=False))
    except Exception as ex:
        print(ex)


def account(request):
    name=request.GET.get('name')
    try:
        if name:
            len1 = models.Goods.objects.filter(name__icontains=name).aggregate(
                len1=Count('id'))
            len2=models.GoodClass.objects.filter(name__icontains=name).aggregate(
                len2=Count('goods__id'))
            len3=models.GoodBrand.objects.filter(name__icontains=name).aggregate(
                len3=Count('goods__id'))
            len=(len1['len1'])+(len2['len2'])+(len3['len3'])
        else:
            len4 = models.Goods.objects.filter(name__icontains=name).aggregate(
                len4=Count('id'))
            len=len4['len4']
        return JsonResponse({"acount":len})
    except Exception as ex:
        return JsonResponse({"code": "500"})

def addGoodToCar(request):
    if request.method=='POST':
        try:
            r=json.loads(request.body)
            token=r['token']
            res=openToken(token)
            if res:
                user_id=res['user_id']
                ss={
                    "good_id":r['good_id'],
                    "user_id":user_id
                }
                result=user_models.AddGood.objects.filter(user_id=user_id,good_id=r['good_id']).values_list()
                if result:
                    return JsonResponse({"code":"403"})
                else:
                    user_models.AddGood.objects.create(**ss)
                    return JsonResponse({"code":"206"})
        except Exception as ex:
            return JsonResponse({"code":"500"})


def delGood(request):
    if request.method=='POST':
        try:
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                ss = {
                    "good_id": r['good_id'],
                    "user_id": user_id
                }
                result = user_models.AddGood.objects.filter(user_id=user_id, good_id=r['good_id']).values_list()
                if result:
                    user_models.AddGood.objects.filter(good_id=r['good_id']).delete()
                    return JsonResponse({"code": "207"})
                else:
                    return JsonResponse({"code":"412"})
            else:
                return JsonResponse({"code":"411"})
        except Exception as ex:
            return JsonResponse({"code":"500"})


def getGoodById(request):
    try:
        good_id=request.GET.get('gid')
        print(good_id)
        goods=[]
        good=list(models.Goods.objects.filter(id=good_id).values('kucun','name','intergal','gooddesc','goodbrand__name','goodclass__name'))
        # print(goods)
        url=list(models.GoodPicture.objects.filter(good_id=good_id).values('url','size'))
        # print(url)
        url_size_1=[]
        url_size_3=[]
        for u in url:
            if u:
                if u['size']=='1':
                    url_size_1.append(u)
                else:
                    url_size_3.append(u)
        url1=[]
        url3=[]
        for i in range(len(url_size_1)):
            url1.append(url_size_1[i]['url'])
        for j in range(len(url_size_3)):
            url3.append(url_size_3[j]['url'])
        G=good[0]['gooddesc']
        good_name=G.split('@')
        aa=[]
        for g in good_name:
            if g:
                if '店铺' in g or '价位' in g:
                    pass
                else:
                    aa.append(g)
        # print(aa)
        ss={
            "name":good[0]['name'],
            "good_kucun": good[0]['kucun'],
            "intergal":good[0]['intergal'],
            "gooddesc":aa,
            "goodbrand_name":good[0]['goodbrand__name'],
            "goodclass_name":good[0]['goodclass__name'],
            "url_size_1":url1,
            "url_size_3":url3,
        }
        # print(ss)
        goods.append(ss)
        # print(goods)
        return HttpResponse(json.dumps(goods,ensure_ascii=False))
    except Exception as ex:
        print(ex)
        return JsonResponse({"code":"500"})


def GoodIndex(request):
    try:
        goods=[]
        good = list(models.Goods.objects.all().values('name', 'intergal', 'gooddesc', 'goodbrand__name','goodclass__name','id'))
        for i in range(0,len(good)):
            goods_id=good[i]['id']
            res = list(models.GoodPicture.objects.filter(good=goods_id,size='1').values('good_id','url'))
            b = OrderedDict()
            for item in res:
                b.setdefault(item['good_id'], {**item, })
            b = list(b.values())
            goods_comment=models.GoodComment.objects.filter(good_id=goods_id).aggregate(goods_comment=Count('content'))
            ss={
                "name":good[i]['name'],
                "intergla":good[i]['intergal'],
                "good_url":b[0]['url'],
                "goodbrand_name":good[i]['goodbrand__name'],
                "goodclass_name":good[i]['goodclass__name'],
                "good_id":good[i]['id'],
                "good_comment":goods_comment['goods_comment']
            }
            goods.append(ss)
        return HttpResponse(json.dumps(goods,ensure_ascii=False))
    except Exception as ex:
        print(ex)

#商品评论
def GoodComment(request):
    if request.method=='POST':
        try:
            r=json.loads(request.body)
            token= request.META.get("HTTP_TOKEN")
            data=r['data']
            good_id=r['good_id']
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res=openToken(token)
            if res:
                user_id=res['user_id']
                print(user_id)
                ss={
                    "user_id":user_id,
                    "good_id":good_id,
                    "content":data,
                    "time":dt
                }
                models.GoodComment.objects.create(**ss)
            else:
                return JsonResponse({"code":"411"})
            return JsonResponse({"code":"210"})
        except Exception as ex:
            return JsonResponse({"code":"500"})

#删除商品评论
def DelComment(request):
    if request.method=='POST':
        try:
            r=json.loads(request.body)
            token= request.META.get("HTTP_TOKEN")
            comment_id=r['comment_id']
            res=openToken(token)
            if res:
                user_id=res['user_id']
                print(user_id)
                comment=models.GoodComment.objects.filter(user_id=user_id,id=comment_id)
                if comment:
                    models.GoodComment.objects.filter(user_id=user_id,id=comment_id).delete()
                else:
                    return JsonResponse({"code":"418"})
            else:
                return JsonResponse({"code":"411"})
            return JsonResponse({"code":"211"})
        except Exception as ex:
            return JsonResponse({"code":"500"})

# 收藏商品
def LoveGood(request):
    if request.method=='POST':
        try:
            r=json.loads(request.body)
            good_id=r['good_id']
            token=r['headers']['token']
            res=openToken(token)
            if res:
                user_id=res['user_id']
                print(user_id)
                love=models.loveGood.objects.filter(good_id=good_id).values()
                print(love)
                if love:
                    return JsonResponse({"code": "417"})
                else:
                    ss = {
                        "user_id": user_id,
                        "good_id": good_id
                    }
                    models.loveGood.objects.create(**ss)
            else:
                return JsonResponse({"code":"411"})
            return JsonResponse({"code":"212"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code":"500"})


# 购物车