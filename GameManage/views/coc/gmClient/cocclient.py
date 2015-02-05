from socket import *
from struct import *
import ctypes
import  binascii
import string
import sys,os
from google.protobuf import text_format
from socketclient import CTcpClient

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gmClient/protopy'))
import gm_pb2
#import friend_pb2

def SerializeMessage(v, p, msg):  
    nlen = len(msg)+6
    str1 = pack("!BBBBBBBB", (nlen >> 8) & 0xff, nlen & 0xff, (v >> 8) & 0xff, v & 0xff, (p >> 24) & 0xfff, (p >> 16) & 0xff, (p >> 8) & 0xff, p & 0xff)
    str1 += str(msg)
    #print str1
    return str1


def ParseMessage(message): 
    mFormat = "!BBBBBBBB" + str(len(message) - 8) + "s"
    a, b, c, d, e, f, g, h, ansStr = unpack(mFormat, message)
    v = c << 8 | d
    cmdid = (e << 24) | (f << 16) | (g << 8) | h 
    #print v, cmdid
    return (ansStr, cmdid)

#using in queryPlayerDataQeq
def totalQueryPlayerData(serverip, playerid):
    #ll = ctypes.cdll.LoadLibrary 
    #p_lib = ll("/home/shenj/data/Web/game_manage/GameManage/views/coc/gmClient/pack.so") 
    serverip = str(serverip)
    playerid = int(playerid)
    tcpClient = CTcpClient()
    tcpClient.Init(serverip, 8888)
    queryPlayer = gm_pb2.QueryPlayerDataReq()
    queryPlayer.player_id = playerid;
    str1 = queryPlayer.SerializeToString()
    #sendBuff = SerializeMessage(str1, 0x4100, playerid)
    sendBuff = SerializeMessage(1, 2001, str1)
    revBuff = tcpClient.SendAndRecv(sendBuff)
    ansStr, hCmd = ParseMessage(revBuff);
    #print ('~~~~~~~~~~~~~~', hCmd, ansStr)
    receive = ParseQueryPlayerDataRsp(ansStr)
    tcpClient.Fini()
    print receive
    return receive


def ParseQueryPlayerDataRsp(str):
    queryPlayerRsp = gm_pb2.QueryPlayerDataRsp()
    queryPlayerRsp.ParseFromString(str)
    return queryPlayerRsp

#using in sendmailans
def totalSendMailToPlayer(serverip, receiver, context, template_id, attachmentSet):
    serverip = str(serverip)
    receiver = int(receiver)
    template_id = int(template_id)
    tcpClient = CTcpClient()
    tcpClient.Init(serverip, 10000)
    sendmailReq = gm_pb2.MailToPlayerReq()
    sendmailReq.mail.serial = 0;
    sendmailReq.mail.receiver = receiver
    if(context != ""):
        sendmailReq.mail.context  = context
    if(template_id != -1):
        sendmailReq.mail.template_id = template_id
    for thisAttachment in reversed(attachmentSet):
        attach = sendmailReq.mail.attachments.add()
        prop_id = thisAttachment["prop_id"]
        attach.prop_id = prop_id
        if("prop_amount" in thisAttachment):
            prop_amount = thisAttachment["prop_amount"]
            attach.prop_amount = prop_amount
        if("prop_param" in thisAttachment):
            prop_param = thisAttachment["prop_param"]
            attach.prop_param = prop_param
    sendmailReq.player_id = receiver
    message = sendmailReq.SerializeToString()

    sendBuff = SerializeMessage(str(message), 0x4116, receiver)
    revBuff = tcpClient.SendAndRecv(sendBuff)
    tcpClient.Fini()

    ansStr, hCmd = ParseMessage(revBuff)
    if(hCmd == 0x4117):
        print "warning:hCmd is wrong!!!"
    
    return ParseSendMailRsp(ansStr)

def ParseSendMailRsp(str):
    queryPlayerRsp = gm_pb2.MailToPlayerRsp()
    queryPlayerRsp.ParseFromString(str)
    return queryPlayerRsp.ret_code


#using in modified_player
#def totalModifyPlayerData(serverip, player_id, flag, marbel_change, goldcoin_change, energy_change, ticket_count, ticket_type, lvl_change, exp_change, point_change,deleteCardid):
#def totalModifyPlayerData(serverip, player_id, flag, marbel_change, goldcoin_change, energy_change, ticket, lvl_change, exp_change, present_points_change, point_change, deleteCardid):
def totalModifyPlayerData(serverip, player_id, flag, water_change, goldcoin_change, lvl_change, exp_change, point_change, gem_change):
    serverip = str(serverip)
    player_id = int(player_id)
    flag = int(flag)
    lvl_change = int(lvl_change)
    exp_change = int(exp_change)
    #present_points_change = int(present_points_change)
    point_change = int(point_change)
    water_change = int(water_change)
    goldcoin_change = int(goldcoin_change)
    gem_change = int(gem_change)
    #energy_change = int(energy_change)
    tcpClient = CTcpClient()
    tcpClient.Init(serverip, 8888)
    queryPlayer = gm_pb2.ModifyPlayerDataReq()
    queryPlayer.player_id = player_id
    queryPlayer.flag = flag
    if(water_change != -1):
        queryPlayer.water_change = water_change
    if(goldcoin_change != -1):
        queryPlayer.goldcoin_change = goldcoin_change
    #if(energy_change != -1):
    #    queryPlayer.energy_change = energy_change

    if(lvl_change != -1):
        queryPlayer.lvl_change = lvl_change
    #if(present_points_change != -1):
    #    queryPlayer.present_points_change = present_points_change
    if(point_change != -1):
        queryPlayer.point_change = point_change
    if(exp_change !=-1):
        queryPlayer.exp_change = exp_change
    if(gem_change !=-1):
        queryPlayer.gem_change = gem_change
    '''
    for item in deleteCardid:
        chandChange = queryPlayer.card_change.add()
        chandChange.card_id = int(item)
        chandChange.change_type = gm_pb2.Remove

    for item in ticket.keys() :
        ticketChange = queryPlayer.ticket_change.add()
        ticketChange.ticket_type = int(item)
        ticketChange.ticket_count = int(ticket[item])
    '''
    message = queryPlayer.SerializeToString()
    sendBuff = SerializeMessage(1, 2003, str(message))
    revBuff = tcpClient.SendAndRecv(sendBuff)
    tcpClient.Fini()

    ansStr, hCmd = ParseMessage(revBuff);
    
    return ParseModifyPlayerDataRsp(ansStr)

    
def ParseModifyPlayerDataRsp(str):
    queryPlayerRsp = gm_pb2.ModifyPlayerDataRsp()
    queryPlayerRsp.ParseFromString(str)
    return queryPlayerRsp.ret_code


#using in banPlayerAns
def totalBanPlayer(serverip, player_id, bandays):
    serverip = str(serverip)
    player_id =int(player_id)
    bamdaus = int(bandays)
    tcpClient = CTcpClient()
    tcpClient.Init(serverip, 8888)
    banPlayerMsg = gm_pb2.BanPlayerReq()
    banPlayerMsg.player_id = player_id
    banPlayerMsg.ban_days = bandays
    message = banPlayerMsg.SerializeToString()

    sendBuff = SerializeMessage(str(message), 0x4112, player_id)
    revBuff = tcpClient.SendAndRecv(sendBuff)
    tcpClient.Fini()

    ansStr, hCmd = ParseMessage(revBuff)
    if(hCmd != 0x4113):
        print "Warning:hCmd is Wrong!!!"

    return ParseBanPlayerDataRsp(ansStr)


def ParseBanPlayerDataRsp(str):
    banPlayerRsp = gm_pb2.BanPlayerRsp()
    banPlayerRsp.ParseFromString(str)
    return banPlayerRsp.ret_code


#using in unbanPlayerAns
def totalUnBanPlayer(serverip, player_id):
    serverip = str(serverip)
    player_id = int(player_id)
    tcpClient = CTcpClient()
    tcpClient.Init(serverip, 8888)
    unbanPlayerMsg = gm_pb2.UnBanPlayerReq()
    unbanPlayerMsg.player_id = player_id
    message = unbanPlayerMsg.SerializeToString()

    sendBuff = SerializeMessage(str(message), 0x4114, player_id)
    revBuff = tcpClient.SendAndRecv(sendBuff)
    tcpClient.Fini()

    ansStr, hCmd = ParseMessage(revBuff)

    return unParseBanPlayerDataRsp(ansStr)


def unParseBanPlayerDataRsp(str):
    unbanPlayerRsp = gm_pb2.UnBanPlayerRsp()
    unbanPlayerRsp.ParseFromString(str)
    return unbanPlayerRsp.ret_code


def ResetServerStatusReq(serverip, type):
    serverip = str(serverip)
    tcpClient = CTcpClient()
    tcpClient.Init(serverip, 10000)
    ServerStatusReq = gm_pb2.ResetServerStatusReq()
    ServerStatusReq.type = type
    message = ServerStatusReq.SerializeToString()

    sendBuff = SerializeMessage(str(message), 0x4108, 0, 2)
    revBuff = tcpClient.SendAndRecv(sendBuff)
    tcpClient.Fini()

    ansStr, hCmd = ParseMessage(revBuff)

    return unParseResetServerStatusReq(ansStr)


def unParseResetServerStatusReq(str):
    ServerStatusRsp = gm_pb2.ResetServerStatusRsp()
    ServerStatusRsp.ParseFromString(str)
    return ServerStatusRsp.ret_code

#using in refreshfriendans
'''
def totalRefreshFriendReq(serverip, player_id):
    serverip = str(serverip)
    tcpClient = CTcpClient()
    tcpClient.Init(serverip, 10000)

    refreshFriendMsg = friend_pb2.C2S_ResetFrinedInfo_Req()
    refreshFriendMsg.roleid.extend(player_id)
    message = refreshFriendMsg.SerializeToString()

    sendBuff = SerializeMessage(str(message), 0x4120, player_id[0])
    revBuff = tcpClient.SendAndRecv(sendBuff)
    tcpClient.Fini()

    ansStr, hCmd = ParseMessage(revBuff)
    if(hCmd != 0x4121):
        print "Warning:hCmd is Wrong!!!"

    return ParseRefreshFriendRsp(ansStr)


def ParseRefreshFriendRsp(str):
    refreshFriendRsp = friend_pb2.C2S_ResetFrinedInfo_Rsp()
    refreshFriendRsp.ParseFromString(str)
    return refreshFriendRsp.retcode
'''

if __name__=="__main__":
    print("main")
    #ll = ctypes.cdll.LoadLibrary 
    #p_lib = ll("/home/shenj/data/Web/game_manage/GameManage/views/coc/gmClient/pack.so") 

    
