# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rcm_error_code.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rcm_error_code.proto',
  package='rcm',
  serialized_pb='\n\x14rcm_error_code.proto\x12\x03rcm\"\xec\"\n\x07RCM_RET\"\xe0\"\n\tErrorCode\x12 \n\x13\x46\x41IL_INTERNAL_ERROR\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x0b\n\x07SUCCESS\x10\x00\x12\x15\n\x10\x45RR_COMMON_BEGIN\x10\x88\'\x12\x1d\n\x18\x45RR_COMMON_ENCODE_FAILED\x10\x89\'\x12\x1d\n\x18\x45RR_COMMON_DECODE_FAILED\x10\x8a\'\x12\x13\n\x0e\x45RR_COMMON_END\x10\x8fN\x12\x14\n\x0e\x45RR_ZONE_BEGIN\x10\x80\xf1\x04\x12\x16\n\x10\x45RR_STORE_SYSTEM\x10\x81\xf1\x04\x12\x15\n\x0f\x45RR_STORE_PRICE\x10\x82\xf1\x04\x12\x17\n\x11\x45RR_STORE_PAYTYPE\x10\x83\xf1\x04\x12\x17\n\x11\x45RR_STORE_BALANCE\x10\x84\xf1\x04\x12\x1e\n\x18\x45RR_STORE_GOOD_NOT_EXIST\x10\x85\xf1\x04\x12\x13\n\rERR_STORE_SEX\x10\x86\xf1\x04\x12\x1e\n\x18\x45RR_STORE_TOO_MUCH_GOODS\x10\x87\xf1\x04\x12*\n$ERR_STORE_PRESENT_RECEIVER_NOT_TNTER\x10\x88\xf1\x04\x12\x1c\n\x16\x45RR_STORE_PRESENT_SELF\x10\x89\xf1\x04\x12\x1b\n\x15\x45RR_STORE_CREATE_BILL\x10\x8a\xf1\x04\x12%\n\x1f\x45RR_STORE_PRESENT_GAME_CURRENCY\x10\x8b\xf1\x04\x12$\n\x1e\x45RR_STORE_PRESENT_RECEIVER_SEX\x10\x8c\xf1\x04\x12 \n\x1a\x45RR_STORE_CAN_NOT_RECHARGE\x10\x8d\xf1\x04\x12\x16\n\x10\x45RR_PORTAL_PRICE\x10\x95\xf1\x04\x12\x18\n\x12\x45RR_PORTAL_PROVIDE\x10\x96\xf1\x04\x12\x1a\n\x14\x45RR_PORTAL_NOT_EXIST\x10\x97\xf1\x04\x12\x17\n\x11\x45RR_PORTAL_FREEZE\x10\x98\xf1\x04\x12\x15\n\x0f\x45RR_PORTAL_LOSS\x10\x99\xf1\x04\x12\x18\n\x12\x45RR_PORTAL_BALANCE\x10\x9a\xf1\x04\x12\x19\n\x13\x45RR_PORTAL_PAYLIMIT\x10\x9b\xf1\x04\x12\x19\n\x13\x45RR_PORTAL_DAYLIMIT\x10\x9c\xf1\x04\x12\x1d\n\x17\x45RR_PORTAL_TOTAL_ENOUGH\x10\x9d\xf1\x04\x12!\n\x1b\x45RR_PORTAL_NOT_FRIENDS_7DAY\x10\x9e\xf1\x04\x12\x1c\n\x16\x45RR_PORTAL_OTHER_ERROR\x10\x9f\xf1\x04\x12\x1f\n\x19\x45RR_EXCHANGE_ID_NOT_EXIST\x10\xa8\xf1\x04\x12!\n\x1b\x45RR_EXCHANGE_MODE_NOT_EXIST\x10\xa9\xf1\x04\x12\x1e\n\x18\x45RR_EXCHANGE_LEVEL_LIMIT\x10\xaa\xf1\x04\x12(\n\"ERR_EXCHANGE_NEED_GOODS_NOT_ENOUGH\x10\xab\xf1\x04\x12\"\n\x1c\x45RR_EXCHANGE_ADD_ITEM_FAILED\x10\xac\xf1\x04\x12\x1b\n\x15\x45RR_EXCHANGE_GP_LIMIT\x10\xad\xf1\x04\x12\x19\n\x13\x45RR_PACKAGE_IS_FULL\x10\xb2\xf1\x04\x12 \n\x1a\x45RR_PACKAGE_ITEM_NOT_EXIST\x10\xb3\xf1\x04\x12!\n\x1b\x45RR_PACKAGE_ITEM_NOT_ENOUGH\x10\xb4\xf1\x04\x12\x1f\n\x19\x45RR_TITAN_PARAMETER_ERROR\x10\xc6\xf1\x04\x12&\n ERR_TITAN_PACKAGE_ITEM_NOT_EXIST\x10\xc7\xf1\x04\x12\x31\n+ERR_TITAN_PACKAGE_SAMALL_CRYSTAL_NOT_ENOUGH\x10\xc8\xf1\x04\x12.\n(ERR_TITAN_PACKAGE_BIG_CRYSTAL_NOT_ENOUGH\x10\xc9\xf1\x04\x12+\n%ERR_TITAN_PACKAGE_CATALYST_NOT_ENOUGH\x10\xca\xf1\x04\x12)\n#ERR_TITAN_PACKAGE_SHIELD_NOT_ENOUGH\x10\xcb\xf1\x04\x12 \n\x1a\x45RR_TITAN_GOODS_TYPE_WRONG\x10\xcc\xf1\x04\x12\x1c\n\x16\x45RR_TITAN_LEVEL_IS_MAX\x10\xcd\xf1\x04\x12\x1e\n\x18\x45RR_TITAN_UPGRADE_FAILED\x10\xce\xf1\x04\x12\x1e\n\x18\x45RR_TITAN_INSERT_ALREADY\x10\xcf\xf1\x04\x12\x1b\n\x15\x45RR_TITAN_REMOVE_NONE\x10\xd0\xf1\x04\x12*\n$ERR_TITAN_UPGRADE_FAILED_AND_DEGRADE\x10\xd1\xf1\x04\x12\x1f\n\x19\x45RR_TITAN_GOLD_NOT_ENOUGH\x10\xd2\xf1\x04\x12\x1f\n\x19\x45RR_TITAN_UPGRADE_CAN_NOT\x10\xd3\xf1\x04\x12\x18\n\x12\x45RR_LOGIN_NOPLAYER\x10\xdb\xf1\x04\x12\x15\n\x0f\x45RR_LOGIN_CLOSE\x10\xdc\xf1\x04\x12\x1c\n\x16\x45RR_LOGIN_SERVER_CLOSE\x10\xdd\xf1\x04\x12 \n\x1a\x45RR_LOGIN_LOADPLAYERFAILED\x10\xde\xf1\x04\x12\x19\n\x13\x45RR_LOGIN_AREA_FULL\x10\xdf\xf1\x04\x12\x1a\n\x14\x45RR_LOGIN_SYSTEM_ERR\x10\xe0\xf1\x04\x12\x17\n\x11\x45RR_LOGIN_NO_AREA\x10\xe1\xf1\x04\x12\x13\n\rERR_LOGIN_BAN\x10\xe2\xf1\x04\x12 \n\x1a\x45RR_LOGIN_AREA_AUTO_CHANGE\x10\xe3\xf1\x04\x12\x1e\n\x18\x45RR_LOGIN_SERVER_STOPPED\x10\xe4\xf1\x04\x12\x1f\n\x19\x45RR_ACTIVITY_ID_NOT_EXIST\x10\x97\xf2\x04\x12\x1a\n\x14\x45RR_ACTIVITY_OVERDUE\x10\x98\xf2\x04\x12\x1d\n\x17\x45RR_ACTIVITY_NOT_ACCORD\x10\x99\xf2\x04\x12#\n\x1d\x45RR_ACTIVITY_FILL_LIMIT_ENTRY\x10\x9a\xf2\x04\x12#\n\x1d\x45RR_ACTIVITY_NOT_ENOUGH_GOODS\x10\x9b\xf2\x04\x12&\n ERR_ACTIVITY_DEDUCT_GOODS_FAILED\x10\x9c\xf2\x04\x12#\n\x1d\x45RR_ACTIVITY_ADD_GOODS_FAILED\x10\x9d\xf2\x04\x12\x1c\n\x16\x45RR_ACTIVITY_HAD_PLANT\x10\x9e\xf2\x04\x12\x1a\n\x14\x45RR_ACTIVITY_NO_SEED\x10\x9f\xf2\x04\x12\x1d\n\x17\x45RR_ACTIVITY_NO_HARVEST\x10\xa0\xf2\x04\x12\'\n!ERR_ACTIVITY_HARVEST_OVER_ENDTIME\x10\xa1\xf2\x04\x12#\n\x1d\x45RR_WAREHOUSE_NO_REFRESH_ITEM\x10\xc9\xf2\x04\x12&\n ERR_WAREHOUSE_ITEM_HAS_EXCHANGED\x10\xca\xf2\x04\x12#\n\x1d\x45RR_WAREHOUSE_EXCHANGE_ID_ERR\x10\xcb\xf2\x04\x12$\n\x1e\x45RR_QQ_FRIEND_INVITE_NUM_LIMIT\x10\xad\xf3\x04\x12\'\n!ERR_QQ_INVITE_AWARD_NUM_NOT_REACH\x10\xae\xf3\x04\x12*\n$ERR_QQ_INVITE_AWARD_ALREADY_RECEIVED\x10\xaf\xf3\x04\x12+\n%ERR_QQ_INVITE_AWARD_INVITEE_NOT_EXIST\x10\xb0\xf3\x04\x12\x12\n\x0c\x45RR_ZONE_END\x10\x8f\xbf\x05\x12\x15\n\x0f\x45RR_MATCH_BEGIN\x10\x80\xe2\t\x12!\n\x1b\x45RR_MATCH_START_LEVEL_LIMIT\x10\x81\xe2\t\x12 \n\x1a\x45RR_MATCH_START_QUEUE_FULL\x10\x82\xe2\t\x12\x1c\n\x16\x45RR_MATCH_START_QUEUED\x10\x83\xe2\t\x12\x1e\n\x18\x45RR_MATCH_CANCEL_MATCHED\x10\x84\xe2\t\x12\x1e\n\x18\x45RR_MATCH_RESULT_TIMEOUT\x10\x85\xe2\t\x12\x1f\n\x19\x45RR_MATCH_START_NOT_BEGIN\x10\x86\xe2\t\x12\x13\n\rERR_MATCH_END\x10\x8f\xb0\n\x12\x15\n\x0f\x45RR_GUILD_BEGIN\x10\xb0\xcc\x0b\x12\x1b\n\x15\x45RR_GUILD_LEVEL_LIMIT\x10\xb1\xcc\x0b\x12\x18\n\x12\x45RR_GUILD_NO_MEDAL\x10\xb2\xcc\x0b\x12\x1a\n\x14\x45RR_GUILD_NAME_EXIST\x10\xb3\xcc\x0b\x12\x18\n\x12\x45RR_GUILD_NONEXIST\x10\xb4\xcc\x0b\x12\x14\n\x0e\x45RR_GUILD_FULL\x10\xb5\xcc\x0b\x12\x1a\n\x14\x45RR_GUILD_ALREADY_IN\x10\xb6\xcc\x0b\x12\x1b\n\x15\x45RR_GUILD_CANNOT_EXIT\x10\xb7\xcc\x0b\x12\x16\n\x10\x45RR_GUILD_NOT_IN\x10\xb8\xcc\x0b\x12\x1e\n\x18\x45RR_GUILD_NO_SUCH_PLAYER\x10\xb9\xcc\x0b\x12\x1b\n\x15\x45RR_GUILD_TITLE_LIMIT\x10\xba\xcc\x0b\x12\x1e\n\x18\x45RR_GUILD_GET_NEW_ID_ERR\x10\xbb\xcc\x0b\x12\x1b\n\x15\x45RR_GUILD_NO_GUILD_ID\x10\xbc\xcc\x0b\x12\x1c\n\x16\x45RR_GUILD_GET_INFO_ERR\x10\xbd\xcc\x0b\x12\x1e\n\x18\x45RR_GUILD_REJECT_TO_JOIN\x10\xbe\xcc\x0b\x12\x1a\n\x14\x45RR_GUILD_SYSTEM_ERR\x10\xbf\xcc\x0b\x12\x1e\n\x18\x45RR_GUILD_TITLE_TYPE_ERR\x10\xc0\xcc\x0b\x12\x1f\n\x19\x45RR_GUILD_ACCEPT_TYPE_ERR\x10\xc1\xcc\x0b\x12!\n\x1b\x45RR_GUILD_HAS_BEEN_DISSOLVE\x10\xc2\xcc\x0b\x12\x17\n\x11\x45RR_GUILD_NO_NAME\x10\xc3\xcc\x0b\x12\x1d\n\x17\x45RR_GUILD_NAME_TOO_LONG\x10\xc4\xcc\x0b\x12$\n\x1e\x45RR_GUILD_DECLARATION_TOO_LONG\x10\xc5\xcc\x0b\x12#\n\x1d\x45RR_GUILD_INVITE_ALEADY_EXIST\x10\xc6\xcc\x0b\x12\x1f\n\x19\x45RR_GUILD_INVITE_TOO_MUCH\x10\xc7\xcc\x0b\x12\'\n!ERR_GUILD_NOT_PROCESSING_TRANSFER\x10\xc8\xcc\x0b\x12\'\n!ERR_GUILD_NOT_PROCESSING_DISSOLVE\x10\xc9\xcc\x0b\x12%\n\x1f\x45RR_GUILD_OPERATION_ON_CHAIRMAN\x10\xca\xcc\x0b\x12&\n ERR_GUILD_ALEADY_IN_APPROVE_LIST\x10\xcb\xcc\x0b\x12\"\n\x1c\x45RR_GUILD_NOT_IN_INVITE_LIST\x10\xcc\xcc\x0b\x12\x1c\n\x16\x45RR_GUILD_VICE_IS_FULL\x10\xcd\xcc\x0b\x12\x1d\n\x17\x45RR_GUILD_ELDER_IS_FULL\x10\xce\xcc\x0b\x12!\n\x1b\x45RR_GUILD_HAS_BEEN_TRANSFER\x10\xcf\xcc\x0b\x12\x1c\n\x16\x45RR_GUILD_CHAT_ILLEGAL\x10\xd0\xcc\x0b\x12\x1c\n\x16\x45RR_GUILD_NAME_ILLEGAL\x10\xd1\xcc\x0b\x12#\n\x1d\x45RR_GUILD_DECLARATION_ILLEGAL\x10\xd2\xcc\x0b\x12$\n\x1e\x45RR_GUILD_ANNOUNCEMENT_ILLEGAL\x10\xd3\xcc\x0b\x12#\n\x1d\x45RR_GUILD_NOT_IN_APPROVE_LIST\x10\xd6\xcc\x0b\x12\x1b\n\x15\x45RR_GUILD_DATA_INLOAD\x10\xd7\xcc\x0b\x12 \n\x1a\x45RR_GUILD_APPROVE_TOO_MUCH\x10\xd8\xcc\x0b\x12 \n\x1a\x45RR_GUILD_QUIT_IN_HALF_DAY\x10\xd9\xcc\x0b\x12\x13\n\rERR_GUILD_END\x10\xbf\x9a\x0c\x12\x14\n\x0e\x45RR_GAME_BEGIN\x10\xc0\x9a\x0c\x12%\n\x1f\x45RR_GAME_CANT_GET_CARD_SELFKILL\x10\xc1\x9a\x0c\x12*\n$ERR_GAME_CANT_GET_CARD_TEAM_SELFKILL\x10\xc2\x9a\x0c\x12&\n ERR_GAME_NO_ENOUGH_NPC_GAME_TICK\x10\xc3\x9a\x0c\x12%\n\x1f\x45RR_GAME_CANT_GET_CARD_NO_MONEY\x10\xc4\x9a\x0c\x12\'\n!ERR_GAME_CANT_GET_CARD_SYSTEM_ERR\x10\xc5\x9a\x0c\x12\x12\n\x0c\x45RR_GAME_END\x10\xdf\xa7\x12')



_RCM_RET_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='rcm.RCM_RET.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FAIL_INTERNAL_ERROR', index=0, number=-1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_COMMON_BEGIN', index=2, number=5000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_COMMON_ENCODE_FAILED', index=3, number=5001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_COMMON_DECODE_FAILED', index=4, number=5002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_COMMON_END', index=5, number=9999,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ZONE_BEGIN', index=6, number=80000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_SYSTEM', index=7, number=80001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_PRICE', index=8, number=80002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_PAYTYPE', index=9, number=80003,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_BALANCE', index=10, number=80004,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_GOOD_NOT_EXIST', index=11, number=80005,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_SEX', index=12, number=80006,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_TOO_MUCH_GOODS', index=13, number=80007,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_PRESENT_RECEIVER_NOT_TNTER', index=14, number=80008,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_PRESENT_SELF', index=15, number=80009,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_CREATE_BILL', index=16, number=80010,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_PRESENT_GAME_CURRENCY', index=17, number=80011,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_PRESENT_RECEIVER_SEX', index=18, number=80012,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_STORE_CAN_NOT_RECHARGE', index=19, number=80013,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_PRICE', index=20, number=80021,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_PROVIDE', index=21, number=80022,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_NOT_EXIST', index=22, number=80023,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_FREEZE', index=23, number=80024,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_LOSS', index=24, number=80025,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_BALANCE', index=25, number=80026,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_PAYLIMIT', index=26, number=80027,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_DAYLIMIT', index=27, number=80028,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_TOTAL_ENOUGH', index=28, number=80029,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_NOT_FRIENDS_7DAY', index=29, number=80030,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PORTAL_OTHER_ERROR', index=30, number=80031,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_EXCHANGE_ID_NOT_EXIST', index=31, number=80040,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_EXCHANGE_MODE_NOT_EXIST', index=32, number=80041,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_EXCHANGE_LEVEL_LIMIT', index=33, number=80042,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_EXCHANGE_NEED_GOODS_NOT_ENOUGH', index=34, number=80043,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_EXCHANGE_ADD_ITEM_FAILED', index=35, number=80044,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_EXCHANGE_GP_LIMIT', index=36, number=80045,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PACKAGE_IS_FULL', index=37, number=80050,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PACKAGE_ITEM_NOT_EXIST', index=38, number=80051,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_PACKAGE_ITEM_NOT_ENOUGH', index=39, number=80052,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_PARAMETER_ERROR', index=40, number=80070,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_PACKAGE_ITEM_NOT_EXIST', index=41, number=80071,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_PACKAGE_SAMALL_CRYSTAL_NOT_ENOUGH', index=42, number=80072,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_PACKAGE_BIG_CRYSTAL_NOT_ENOUGH', index=43, number=80073,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_PACKAGE_CATALYST_NOT_ENOUGH', index=44, number=80074,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_PACKAGE_SHIELD_NOT_ENOUGH', index=45, number=80075,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_GOODS_TYPE_WRONG', index=46, number=80076,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_LEVEL_IS_MAX', index=47, number=80077,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_UPGRADE_FAILED', index=48, number=80078,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_INSERT_ALREADY', index=49, number=80079,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_REMOVE_NONE', index=50, number=80080,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_UPGRADE_FAILED_AND_DEGRADE', index=51, number=80081,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_GOLD_NOT_ENOUGH', index=52, number=80082,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_TITAN_UPGRADE_CAN_NOT', index=53, number=80083,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_NOPLAYER', index=54, number=80091,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_CLOSE', index=55, number=80092,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_SERVER_CLOSE', index=56, number=80093,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_LOADPLAYERFAILED', index=57, number=80094,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_AREA_FULL', index=58, number=80095,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_SYSTEM_ERR', index=59, number=80096,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_NO_AREA', index=60, number=80097,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_BAN', index=61, number=80098,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_AREA_AUTO_CHANGE', index=62, number=80099,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_LOGIN_SERVER_STOPPED', index=63, number=80100,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_ID_NOT_EXIST', index=64, number=80151,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_OVERDUE', index=65, number=80152,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_NOT_ACCORD', index=66, number=80153,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_FILL_LIMIT_ENTRY', index=67, number=80154,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_NOT_ENOUGH_GOODS', index=68, number=80155,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_DEDUCT_GOODS_FAILED', index=69, number=80156,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_ADD_GOODS_FAILED', index=70, number=80157,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_HAD_PLANT', index=71, number=80158,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_NO_SEED', index=72, number=80159,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_NO_HARVEST', index=73, number=80160,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ACTIVITY_HARVEST_OVER_ENDTIME', index=74, number=80161,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_WAREHOUSE_NO_REFRESH_ITEM', index=75, number=80201,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_WAREHOUSE_ITEM_HAS_EXCHANGED', index=76, number=80202,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_WAREHOUSE_EXCHANGE_ID_ERR', index=77, number=80203,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_QQ_FRIEND_INVITE_NUM_LIMIT', index=78, number=80301,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_QQ_INVITE_AWARD_NUM_NOT_REACH', index=79, number=80302,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_QQ_INVITE_AWARD_ALREADY_RECEIVED', index=80, number=80303,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_QQ_INVITE_AWARD_INVITEE_NOT_EXIST', index=81, number=80304,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_ZONE_END', index=82, number=89999,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_BEGIN', index=83, number=160000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_START_LEVEL_LIMIT', index=84, number=160001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_START_QUEUE_FULL', index=85, number=160002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_START_QUEUED', index=86, number=160003,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_CANCEL_MATCHED', index=87, number=160004,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_RESULT_TIMEOUT', index=88, number=160005,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_START_NOT_BEGIN', index=89, number=160006,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_MATCH_END', index=90, number=169999,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_BEGIN', index=91, number=190000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_LEVEL_LIMIT', index=92, number=190001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NO_MEDAL', index=93, number=190002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NAME_EXIST', index=94, number=190003,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NONEXIST', index=95, number=190004,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_FULL', index=96, number=190005,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_ALREADY_IN', index=97, number=190006,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_CANNOT_EXIT', index=98, number=190007,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NOT_IN', index=99, number=190008,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NO_SUCH_PLAYER', index=100, number=190009,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_TITLE_LIMIT', index=101, number=190010,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_GET_NEW_ID_ERR', index=102, number=190011,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NO_GUILD_ID', index=103, number=190012,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_GET_INFO_ERR', index=104, number=190013,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_REJECT_TO_JOIN', index=105, number=190014,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_SYSTEM_ERR', index=106, number=190015,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_TITLE_TYPE_ERR', index=107, number=190016,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_ACCEPT_TYPE_ERR', index=108, number=190017,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_HAS_BEEN_DISSOLVE', index=109, number=190018,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NO_NAME', index=110, number=190019,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NAME_TOO_LONG', index=111, number=190020,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_DECLARATION_TOO_LONG', index=112, number=190021,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_INVITE_ALEADY_EXIST', index=113, number=190022,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_INVITE_TOO_MUCH', index=114, number=190023,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NOT_PROCESSING_TRANSFER', index=115, number=190024,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NOT_PROCESSING_DISSOLVE', index=116, number=190025,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_OPERATION_ON_CHAIRMAN', index=117, number=190026,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_ALEADY_IN_APPROVE_LIST', index=118, number=190027,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NOT_IN_INVITE_LIST', index=119, number=190028,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_VICE_IS_FULL', index=120, number=190029,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_ELDER_IS_FULL', index=121, number=190030,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_HAS_BEEN_TRANSFER', index=122, number=190031,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_CHAT_ILLEGAL', index=123, number=190032,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NAME_ILLEGAL', index=124, number=190033,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_DECLARATION_ILLEGAL', index=125, number=190034,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_ANNOUNCEMENT_ILLEGAL', index=126, number=190035,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_NOT_IN_APPROVE_LIST', index=127, number=190038,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_DATA_INLOAD', index=128, number=190039,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_APPROVE_TOO_MUCH', index=129, number=190040,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_QUIT_IN_HALF_DAY', index=130, number=190041,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GUILD_END', index=131, number=199999,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GAME_BEGIN', index=132, number=200000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GAME_CANT_GET_CARD_SELFKILL', index=133, number=200001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GAME_CANT_GET_CARD_TEAM_SELFKILL', index=134, number=200002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GAME_NO_ENOUGH_NPC_GAME_TICK', index=135, number=200003,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GAME_CANT_GET_CARD_NO_MONEY', index=136, number=200004,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GAME_CANT_GET_CARD_SYSTEM_ERR', index=137, number=200005,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERR_GAME_END', index=138, number=299999,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=42,
  serialized_end=4490,
)


_RCM_RET = _descriptor.Descriptor(
  name='RCM_RET',
  full_name='rcm.RCM_RET',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RCM_RET_ERRORCODE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=30,
  serialized_end=4490,
)

_RCM_RET_ERRORCODE.containing_type = _RCM_RET;
DESCRIPTOR.message_types_by_name['RCM_RET'] = _RCM_RET

class RCM_RET(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RCM_RET

  # @@protoc_insertion_point(class_scope:rcm.RCM_RET)


# @@protoc_insertion_point(module_scope)
