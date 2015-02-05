# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gmClient/protocol'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gmClient'))

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from gmClient.cocclient import *


def queryPlayer(request):
    dict1 = {}
    template = "coc/playerinfo.html"
    return render_to_response(template, dict1)


def queryPlayerDataQeq(request):
    serverip = str(request.POST.get("serverip",''))
    player_id = str(request.POST.get("player_id",''))
    if(serverip == '' or player_id == ''):
        return HttpResponseNotFound('<h1>Please select server and input player_id!!!</h1>')

    recv = totalQueryPlayerData(serverip, string.atoi(request.POST["player_id"]));
    parg = {}
    parg['message'] = recv
    parg['serverip'] = serverip
    parg['player_id'] = player_id
    '''
    parg['gamedata0'] = recv.player_data.game_record[0]
    parg['gamedata1'] = recv.player_data.game_record[1]
    parg['gamedata2'] = recv.player_data.game_record[2]
    parg['gamedata3'] = recv.player_data.game_record[3]
    print parg['gamedata0']
    '''
    template = "coc/playerinfoans.html"
    return render_to_response(template,parg);


def modified_player(request):
    flag = 0 
    serverip = str(request.POST.get('serverip',''))
    player_id = str(request.POST.get('player_id',''))
    if(serverip == '' or player_id == ''):
        return HttpResponseNotFound('<h1>Please select server and input player_id!!!</h1>')

    isLVL = request.POST.get('isLVL','')
    lvl_change = -1
    if(isLVL == "on"):
        lvl_change = request.POST.get('lvl_change','-1')
    if(lvl_change != -1):
        flag |= 0x00000200

    isExp = request.POST.get('isExp','')
    exp_change = -1
    if(isExp == "on"):
        exp_change = request.POST.get('exp_change','-1')
    if(exp_change != -1):
        flag |= 0x00000008
    '''
    ispresentPoint = request.POST.get('ispresentPoint','')
    present_point_change = -1
    if(ispresentPoint == "on"):
        present_point_change = request.POST.get('present_point_change','-1')
    if(present_point_change != -1):
        flag |= 0x00002000
    '''
    isPoint = request.POST.get('isPoint','')
    point_change = -1
    if(isPoint == "on"):
        point_change = request.POST.get('point_change','-1')
    if(point_change != -1):
        flag |= 0x00000100

    isWater = request.POST.get('isWater','-1')
    water_change = -1
    if(isWater == 'on'):
        water_change = int(request.POST.get('water_change','-1'))
    if(water_change != -1):
        flag |= 0x00000001
    
    isGoldcoin = request.POST.get('isGoldcoin','')
    goldcoin_change = -1
    if(isGoldcoin == 'on'):
        goldcoin_change = int(request.POST.get('goldcoin_change','-1'))
    if(goldcoin_change != -1):
        flag |= 0x00000002
    isGem = request.POST.get('isGem','')
    gem_change = -1
    if(isGem == 'on'):
        gem_change = int(request.POST.get('gem_change','-1'))
    if(gem_change != -1):
        flag |= 0x00000004
    #print lvl_change, exp_change, point_change, water_change, goldcoin_change, gem_change 
    #print isLVL, isExp, isPoint, isWater, isGoldcoin, isGem 
    '''
    isEnergy = request.POST.get('isEnergy','')
    energy_change = -1
    if(isEnergy == 'on'):
        energy_change = int(request.POST.get('energy_change','-1'))
    if(energy_change != -1):
        flag |= 0x00000004

    isTicket = request.POST.get('isTicket','')
    ticket = {}
    isDeleteTicketOk = False
    if(isTicket == 'on'):
        for i in range(-1,50):
            strKey = "TicketType"+str(i)
            strNum = "TicketNum"+str(i)
            strKeyType = str(request.POST.get(strKey,''))
            if(strKeyType != ''):
                isDeleteTicketOk = True
                ticket_num = int(request.POST.get(strNum))
                ticket[strKeyType] = ticket_num

    if(isDeleteTicketOk):
        flag |= 0x00000010


    isDeleteCard = request.POST.get('isDeleteCard','')
    deleteCardid = []
    isDeleteCardOk = False
    isDeleteCard = str(request.POST.get('isDeleteCard',''))
    maxCardId = int(request.POST.get('maxCardId','-1'))
    if(isDeleteCard == 'on' and maxCardId != -1):
        for i in range(1,maxCardId+1):
            strKey = "isDeleteCardCheck" + str(i)
            strKeyCheck = str(request.POST.get(strKey,''))
            if(strKeyCheck == "on"):
                isDeleteCardOk = True
                deleteCardid.append(i)
    print deleteCardid

    if(isDeleteCardOk == True):
        flag  |= 0x00000040
    '''               
    recv = totalModifyPlayerData(serverip, player_id, flag, water_change, goldcoin_change, lvl_change, exp_change, point_change, gem_change)

    if(recv != 0):
        ret_code = 0
    else:
        ret_code = 1
    template = "coc/ret.html"
    parg = {}
    parg['ret'] = ret_code
    return render_to_response(template, parg)


def sendmail(request):
    dict1 = {}
    template = "coc/sendmail.html"
    return render_to_response(template, dict1)
    

def sendmailans(request):
    serverip = str(request.POST.get('serverip',''))
    receiver = str(request.POST.get('receiver',''))
    if(serverip == '' or receiver == ''):
        return HttpResponseNotFound('<h1>serverip and receiver must not be NULL!!!</h1>')
    context = request.POST.get('context','').encode('utf8')

    attachmentSet = []
    template_id = -1
    isTemplate_id = str(request.POST.get('isTemplate_id',''))
    if isTemplate_id == "on":
        template_id = int(request.POST.get('template_id','-1'))

    PROP_TYPE_MARBLE = str(request.POST.get('PROP_TYPE_MARBLE',''))
    if PROP_TYPE_MARBLE == "on":
        marble_num = int(request.POST.get('marble_num','0'))
        attachment = {}
        attachment["prop_id"] = 1 #PROP_TYPE_MARBLE
        attachment["prop_amount"] = marble_num
        attachmentSet.append(attachment)

    PROP_TYPE_GOLDCOIN = str(request.POST.get('PROP_TYPE_GOLDCOIN','0'))
    if PROP_TYPE_GOLDCOIN == "on":
        goldcoin_num = int(request.POST.get('goldcoin_num','0'))
        attachment = {}
        attachment["prop_id"] = 2 #PROP_TYPE_GOLDCOIN
        attachment["prop_amount"] = goldcoin_num
        attachmentSet.append(attachment)

    PROP_TYPE_ENERGY = str(request.POST.get('PROP_TYPE_ENERGY',''))
    if PROP_TYPE_ENERGY == "on":
        energy_value = string.atoi(request.POST["energy_value"])
        attachment = {}
        attachment["prop_id"] = 3 #PROP_TYPE_ENERGY
        attachment["prop_amount"] = energy_value
        attachmentSet.append(attachment)

    PROP_TYPE_CARD = request.POST.get('PROP_TYPE_CARD','')
    if PROP_TYPE_CARD == "on":
        card_uuid = int(request.POST.get('card_uuid'))
        if(card_uuid < 1 or card_uuid > 605):
            return HttpResponseNotFound('<h1>card_uuid out of range!!!</h1>')

        attachment = {}
        attachment["prop_id"] = 4 #PROP_TYPE_CARD
        attachment["prop_amount"] = 1#todo   card default is 1
        attachment["prop_param"] = card_uuid
        attachmentSet.append(attachment)

    PROP_TYPE_CARDHODLER = str(request.POST.get('PROP_TYPE_CARDHODLER',''))
    if PROP_TYPE_CARDHODLER == "on":
        #cardHodlerNum = int(request.POST.get('cardHodlerNum','0'))
        cardHodlerType = int(request.POST.get('cardHodlerType','-1'))
            #for i in range(0, cardHodlerNum+1):
        attachment = {}
        attachment["prop_id"] = 5 #PROP_TYPE_CARDHODLER
        attachment["prop_amount"] = 1
        attachment["prop_param"] = cardHodlerType
        attachmentSet.append(attachment)


    PROP_TYPE_TICKET = str(request.POST.get('PROP_TYPE_TICKET',''))
    if PROP_TYPE_TICKET == "on":
        ticket_num = int(request.POST.get('ticket_num','0'))
        ticket_type = int(request.POST.get('ticket_type'))
        attachment = {}
        attachment["prop_id"] = 7 #PROP_TYPE_TICKET
        attachment["prop_amount"] = ticket_num
        attachment["prop_param"] = ticket_type
        attachmentSet.append(attachment)

    print attachmentSet
    
    ret = totalSendMailToPlayer(serverip, receiver, context, template_id, attachmentSet)
            
    dict = {}
    if(ret != 0):
        ret_code = 0
    else:
        ret_code = 1
    template = "coc/ret.html"
    parg = {}
    parg['ret'] = ret_code
    return render_to_response(template, parg)


def unbanPlayer(request):
    dict1 = {}
    template = "coc/unbanplayer.html"
    return render_to_response(template, dict1)


def unbanPlayerAns(request):
    serverip = str(request.POST.get('serverip',''))
    player_id = str(request.POST.get('player_id',''))
    if(serverip == '' or player_id == ''):
        return HttpResponseNotFound('<h1>serverip and player_id must not be NULL!!!</h1>')

    ret = totalUnBanPlayer(serverip, player_id);
    dict1 = {}
    if(ret != 0):
        ret_code = 0
    else:
        ret_code = 1
    template = "coc/ret.html"
    parg = {}
    parg['ret'] = ret_code
    return render_to_response(template, parg)


def banPlayer(request):
    dict1 = {}
    template = "coc/banplayer.html"
    return render_to_response(template, dict1)


def banPlayerAns(request):
    serverip = str(request.POST.get('serverip',''))
    player_id = str(request.POST.get('player_id',''))
    bandays = request.POST.get('bandays','')
    if(serverip == '' or player_id == '' or bandays == ''):
        return HttpResponseNotFound('<h1>serverip,player_id and bandays must not be NULL!!!</h1>')

    ret = totalBanPlayer(serverip, player_id, int(bandays))
    dict = {}
    if(ret != 0):
        ret_code = 0
    else:
        ret_code = 1
    template = "coc/ret.html"
    parg = {}
    parg['ret'] = ret_code
    return render_to_response(template, parg)


def resetserverstatus(request):
    dict1 = {}
    template = "coc/resetserverstatus.html"
    return render_to_response(template, dict1)


def resetserverstatusAns(request):
    serverip = str(request.POST.get("serverip",''))
    type1 = request.POST.get('type','')
    if(serverip == '' or type1 == ''):
        print "type not found!!!"
        return HttpResponseNotFound('<h1>Please select server and input type!!!</h1>')
    recv = ResetServerStatusReq(serverip, int(type1))

    if(recv !=0):
        ret_code = 0
    else:
        ret_code = 1
    template = "coc/ret.html"
    parg = {}
    parg['ret'] = ret_code
    return render_to_response(template, parg)

def refreshfriend(request):
    dict1 = {}
    template = "coc/refreshfriend.html"
    return render_to_response(template, dict1)

def refreshfriendAns(request):
    serverip = str(request.POST.get("serverip",''))
    player_id_list = str(request.POST.get('player_id',''))
    player_id = []
    for item in player_id_list.split(u','):
        item = item.strip(u'')
        player_id.append(int(item))
    if(serverip == '' or player_id.__len__() == 0):
        return HttpResponseNotFound('<h1>serverip and player_id must not be NULL!!!</h1>')
    recv = totalRefreshFriendReq(serverip, player_id)
    if recv != 0 :
        ret_code = 0
    else:
        ret_code = 1
    template = "coc/ret.html"
    parg = {}
    parg['ret'] = ret_code
    return render_to_response(template, parg)


