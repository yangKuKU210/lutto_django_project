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
import math


# Create your views here.
def index(request):
    pass


def search(request):
    try:
        name = request.GET.get('name')
        index = request.GET.get('index')
        print(name)
        pagesize = 5
        if index:
            index = int(index)
        else:
            index = 1
        # print(name)
        G = []
        if name:
            good = list(
                models.Goods.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values(
                    'kucun', 'name', 'intergal', 'gooddesc', 'goodbrand__name', 'goodclass__name', 'id'))
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
            else:
                pass
            good = list(
                models.GoodClass.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values(
                    'goods__kucun', 'goods__name', 'goods__intergal', 'goods__gooddesc', 'goods__goodbrand__name',
                    'name', 'goods__id'))
            if good:
                print(good)
                for g in good:
                    ss = {
                        "goods_kuncun": g['goods__kucun'],
                        "goods_name": g['goods__name'],
                        "goods_intergal": g['goods__intergal'],
                        "goods_gooddesc": g['goods__gooddesc'],
                        "good_class_name": g['name'],
                        "goods_id": g['goods__id'],
                        "goods_band_name": g['goods__goodbrand__name']
                    }
                    G.append(ss)
                    goods = Greatgoods(G)
            else:
                pass
            good = list(
                models.GoodBrand.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values(
                    'goods__kucun', 'goods__name', 'goods__intergal', 'goods__gooddesc', 'name',
                    'goods__goodclass__name', 'goods__id'))
            if good:
                for g in good:
                    ss = {
                        "goods_kuncun": g['goods__kucun'],
                        "goods_name": g['goods__name'],
                        "goods_intergal": g['goods__intergal'],
                        "goods_gooddesc": g['goods__gooddesc'],
                        "good_class_name": g['goods__goodclass__name'],
                        "goods_id": g['goods__id'],
                        "goods_band_name": g['name']
                    }
                    G.append(ss)
                goods = Greatgoods(G)
            else:
                pass
        else:
            good = list(models.Goods.objects.filter()[pagesize * (index - 1):pagesize * index].values('kucun', 'name',
                                                                                                      'intergal',
                                                                                                      'gooddesc',
                                                                                                      'goodbrand__name',
                                                                                                      'goodclass__name',
                                                                                                      'id'))
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
    name = request.GET.get('name')
    try:
        if name:
            len1 = models.Goods.objects.filter(name__icontains=name).aggregate(
                len1=Count('id'))
            len2 = models.GoodClass.objects.filter(name__icontains=name).aggregate(
                len2=Count('goods__id'))
            len3 = models.GoodBrand.objects.filter(name__icontains=name).aggregate(
                len3=Count('goods__id'))
            len = (len1['len1']) + (len2['len2']) + (len3['len3'])
        else:
            len4 = models.Goods.objects.filter(name__icontains=name).aggregate(
                len4=Count('id'))
            len = len4['len4']
        return JsonResponse({"acount": len})
    except Exception as ex:
        return JsonResponse({"code": "500"})


# 添加购物车
def addGoodToCar(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            if 'token' in r.keys():
                res = openToken(r['token'])
                if res:
                    uu = user_models.AddGood.objects.filter(user_id=res['user_id'],
                                                            good_id=r['good_id']).values().first()
                    if uu:
                        user_models.AddGood.objects.filter(id=uu['id']).update(num=r['num'])
                    else:
                        user_id = res['user_id']
                        ss = {
                            "good_id": r['good_id'],
                            "user_id": user_id,
                            "num": r['num']
                        }
                        result = user_models.AddGood.objects.filter(user_id=user_id, good_id=r['good_id']).values_list()
                        if result:
                            return JsonResponse({"code": "403"})
                        else:
                            user_models.AddGood.objects.create(**ss)

                else:
                    return JsonResponse({"code": "411"})
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "206"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


def delGood(request):
    if request.method == 'POST':
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
                    return JsonResponse({"code": "412"})
            else:
                return JsonResponse({"code": "411"})
        except Exception as ex:
            return JsonResponse({"code": "500"})


def getGoodById(request):
    try:
        good_id = request.GET.get('gid')
        print(good_id)
        goods = []
        good = list(
            models.Goods.objects.filter(id=good_id).values('kucun', 'name', 'intergal', 'gooddesc', 'goodbrand__name',
                                                           'goodclass__name'))
        # print(goods)
        url = list(models.GoodPicture.objects.filter(good_id=good_id).values('url', 'size'))
        # print(url)
        url_size_1 = []
        url_size_3 = []
        for u in url:
            if u:
                if u['size'] == '1':
                    url_size_1.append(u)
                else:
                    url_size_3.append(u)
        url1 = []
        url3 = []
        for i in range(len(url_size_1)):
            url1.append(url_size_1[i]['url'])
        for j in range(len(url_size_3)):
            url3.append(url_size_3[j]['url'])
        G = good[0]['gooddesc']
        good_name = G.split('@')
        aa = []
        for g in good_name:
            if g:
                if '店铺' in g or '价位' in g:
                    pass
                else:
                    aa.append(g)
        # print(aa)
        ss = {
            "name": good[0]['name'],
            "good_kucun": good[0]['kucun'],
            "intergal": good[0]['intergal'],
            "gooddesc": aa,
            "goodbrand_name": good[0]['goodbrand__name'],
            "goodclass_name": good[0]['goodclass__name'],
            "url_size_1": url1,
            "url_size_3": url3,
        }
        # print(ss)
        goods.append(ss)
        # print(goods)
        return HttpResponse(json.dumps(goods, ensure_ascii=False))
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "500"})


def GoodIndex(request):
    try:
        goods = []
        good = list(
            models.Goods.objects.all().values('name', 'intergal', 'gooddesc', 'goodbrand__name', 'goodclass__name',
                                              'id'))
        for i in range(0, len(good)):
            goods_id = good[i]['id']
            res = list(models.GoodPicture.objects.filter(good=goods_id, size='1').values('good_id', 'url'))
            b = OrderedDict()
            for item in res:
                b.setdefault(item['good_id'], {**item, })
            b = list(b.values())
            goods_comment = models.GoodComment.objects.filter(good_id=goods_id).aggregate(
                goods_comment=Count('content'))
            ss = {
                "name": good[i]['name'],
                "intergla": good[i]['intergal'],
                "good_url": b[0]['url'],
                "goodbrand_name": good[i]['goodbrand__name'],
                "goodclass_name": good[i]['goodclass__name'],
                "good_id": good[i]['id'],
                "good_comment": goods_comment['goods_comment']
            }
            goods.append(ss)
        return HttpResponse(json.dumps(goods, ensure_ascii=False))
    except Exception as ex:
        print(ex)


# 商品评论
#商品评论
#商品评论
def GoodComment(request):
    if request.method=='POST':
        try:
            r=json.loads(request.body)
            token = r['headers']['token']
            data = r['data']
            good_id = r['good_id']
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res = openToken(token)
            if res:
                user_id = res['user_id']
                print(user_id)
                ss = {
                    "user_id": user_id,
                    "good_id": good_id,
                    "content": data,
                    "time": dt
                }
                models.GoodComment.objects.create(**ss)
                jf = list(user_models.Intergral.objects.filter(user_id=res['user_id']).values('intergral'))
                jifen = jf[0]['intergral']
                user_jifen = int(jifen) + 1
                user_models.Intergral.objects.filter(user_id=res['user_id']).update(intergral=user_jifen)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "210"})
        except Exception as ex:
            return JsonResponse({"code":"500"})




# 删除商品评论
def DelComment(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = request.META.get("HTTP_TOKEN")
            comment_id = r['comment_id']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                print(user_id)
                comment = models.GoodComment.objects.filter(user_id=user_id, id=comment_id)
                if comment:
                    models.GoodComment.objects.filter(user_id=user_id, id=comment_id).delete()
                else:
                    return JsonResponse({"code": "418"})
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "211"})
        except Exception as ex:
            return JsonResponse({"code": "500"})


# 收藏商品
def LoveGood(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            good_id = r['good_id']
            token = r['headers']['token']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                print(user_id)
                love = models.loveGood.objects.filter(good_id=good_id).values()
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
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "212"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 购物车

# 查看购车的商品
def GetCart(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            # print(r)
            if 'token' in r.keys():
                GOOD = []
                TT = r['token']
                # print(TT)
                res = openToken(TT)
                if res:
                    good = list(user_models.AddGood.objects.filter(user_id=res['user_id']).values('good_id'))
                    if good:
                        for i in range(len(good)):
                            good_id = good[i]['good_id']
                            goods = list(
                                models.Goods.objects.filter(id=good_id).values('kucun', 'name', 'intergal', 'gooddesc',
                                                                               'goodbrand__name', 'goodclass__name',
                                                                               'id', 'addgood__num'))
                            urls = list(
                                models.GoodPicture.objects.filter(good_id=good_id, size=1).values('url', 'good_id'))
                            b = OrderedDict()
                            for item in urls:
                                b.setdefault(item['good_id'], {**item, })
                            b = list(b.values())
                            ss = {
                                "good_id": good_id,
                                "good_url": b[0]['url'],
                                "good_name": goods[0]['name'],
                                "good_intergal": goods[0]['intergal'],
                                "num": goods[0]['addgood__num']
                            }
                            GOOD.append(ss)
                    else:
                        return JsonResponse({"code": "423"})
                else:
                    return JsonResponse({"code": "411"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(GOOD, ensure_ascii=False))
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 收藏商品
def OrderGood(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            # print(r)
            token = r['token']
            res = openToken(token)
            if res:
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ss = {
                    "user_id": res['user_id'],
                    "good_id": r['good_id'],
                    "status": 1,
                    "time": dt,
                    "goodcounts": r['goodcounts'],
                    "total": r['total']
                }
                models.Order.objects.create(**ss)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "217"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 删除收藏的商品
def DelOrder(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                order = models.Order.objects.filter(id=r['order_id'], user_id=res['user_id']).values()
                if order:
                    models.Order.objects.filter(id=r['order_id'], user_id=res['user_id']).delete()
                else:
                    return JsonResponse({"code": "426"})
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "218"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 用户完成交易
def DealOrder(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                intergal = list(user_models.Intergral.objects.filter(user_id=res['user_id']).values('intergral'))
                user_intergal = int(intergal[0]['intergral'])
                total = list(models.Order.objects.filter(id=r['order_id']).values('total'))
                order_intergal = total[0]['total']
                if user_intergal < order_intergal:
                    return JsonResponse({"code": "427"})
                else:
                    new_intergal = user_intergal - order_intergal
                    user_models.Intergral.objects.filter(user_id=res['user_id']).update(intergral=new_intergal)
                    status = list(models.Order.objects.filter(id=r['order_id']).values('status'))
                    if status[0]['status'] == 1:
                        models.Order.objects.filter(id=r['order_id']).update(status=2)
                    else:
                        order = list(models.Order.objects.filter(id=r['order_id']).values())
                        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ss = {
                            "user_id": res['user_id'],
                            "status": 2,
                            "good_id": order[0]['good_id'],
                            "goodcounts": order[0]['goodcounts'],
                            "total": order[0]['total'],
                            "time": dt
                        }
                        models.Order.objects.create(**ss)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "219"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 显示评论
def GetGoodComment(request):
    try:
        good_id = request.GET.get('good_id')
        comment = list(
            models.GoodComment.objects.filter(good_id=good_id).values('content', 'id', 'good_id', 'user_id', 'likes'))
        print(comment)
        return HttpResponse(json.dumps(comment, ensure_ascii=False))
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "500"})


# 商品评论点赞
def likeComment(request):
    try:
        r = json.loads(request.body)
        token = r['token']
        comment_id = r['comment_id']
        res = openToken(token)
        if res:
            comment = models.GoodComment.objects.filter(id=comment_id).values()
            if comment:
                result = models.ShopCommentLike.objects.filter(comment_id=comment_id, user_id=res['user_id']).values()
                # print(result)
                if result:
                    models.ShopCommentLike.objects.filter(comment_id=comment_id, user_id=res['user_id']).delete()
                    likenum = list(models.GoodComment.objects.filter(id=comment_id).values('likes'))
                    print(likenum)
                    res = likenum[0]['likes'] - 1
                    models.GoodComment.objects.filter(id=comment_id).update(likes=res)
                    return JsonResponse({"code": "214"})
                else:
                    ss = {
                        'comment_id': comment_id,
                        'user_id': res['user_id'],
                    }
                    models.ShopCommentLike.objects.create(**ss)
                    likenum = list(models.GoodComment.objects.filter(id=comment_id).values('likes'))
                    print(likenum)
                    res = likenum[0]['likes'] + 1
                    models.GoodComment.objects.filter(id=comment_id).update(likes=res)
                    return JsonResponse({"code": "215"})
            else:
                return JsonResponse({"code": "425"})
        else:
            return JsonResponse({"code": "411"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "500"})


# 回复评论
def ReturnComment(requset):
    if requset.method == 'POST':
        try:
            r = json.loads(requset.body)
            token = r['token']
            res = openToken(token)
            if res:
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ss = {
                    "content": r['data'],
                    "user_id": res['user_id'],
                    "comment_id": r['comment_id'],
                    "time": dt
                }
                # print(ss)
                models.ShopCommentReply.objects.create(**ss)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "216"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 查看我的订单（商品）
def GetOrder(request):
    if request.method == 'POST':
        try:
            ORDER = []
            r = json.loads(request.body)
            print(r)
            # token=request.META('HTTP_TOKEN')
            token = r['headers']['token']
            # print(token)
            res = openToken(token)
            if res:
                order = list(models.Order.objects.filter(user_id=res['user_id'], status=r['good_status']).values())
                if order:
                    for o in order:
                        res = list(
                            models.GoodPicture.objects.filter(good=o['good_id'], size='1').values('good_id', 'url'))
                        b = OrderedDict()
                        for item in res:
                            b.setdefault(item['good_id'], {**item, })
                        b = list(b.values())
                        good = list(models.Goods.objects.filter(id=o['good_id']).values('name'))
                        time = str(o['time'])
                        # print(time)
                        tt = time.split('.' or '+')[0]
                        import time
                        time_array = time.strptime(tt, "%Y-%m-%d %H:%M:%S")
                        timestamp = time.mktime(time_array)
                        old_time = int(timestamp) + 28800
                        now_time = int(time.time())
                        time = now_time - old_time
                        min = math.ceil(time / 60)
                        # print(min)
                        if min < 60:
                            order_time = str(min) + '分之前'
                        else:
                            hour = math.ceil(min / 60)
                            if hour < 24:
                                order_time = str(hour) + '小时前'
                            else:
                                day = math.ceil(hour / 24)
                                if day <= 3:
                                    order_time = str(day) + '天前'
                                else:
                                    order_time = tt.split(' ')[0]
                        ss = {
                            "order_id": o['id'],
                            "order_time": order_time,
                            "order_status": o['status'],
                            "order_goodcounts": o['goodcounts'],
                            "order_total": o['total'],
                            "good_name": good[0]['name'],
                            "good_url": b[0]['url']
                        }
                        ORDER.append(ss)
                else:
                    return JsonResponse({"code": "426"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(ORDER, ensure_ascii=False))
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})
