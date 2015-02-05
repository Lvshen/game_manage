##############################################################################################################################
#Author : Sail (ZENGXING)
#2009 06 16 纪念1888年的今天《國際歌》誕生。 今天，接近完美的Makefile诞生了.
#编译COMMLIB库,定义MAKE规则,
#
#你无需再修改这个makefile,把.c,.cpp.h文件摔在目录下就可以了.依赖关系我会自己处理,
#这个Makefile已经对.h文件的依赖做了检查,是一个很酷的Makefile，你可以崇拜我.
#其实Makefile对于我，一致是一个旁门左道.我每次用改都会很痛苦,但是我希望证明的一点是，别人能做到的，我也可以.
#也许每一次使用都是一次进步，哈哈.
#所以鸣谢三篇Makefile文章的作者《GNU Make 指南》《跟我一起写 Makefile》《GNUMake 手册》,也像大叔表示敬意Richard Stallman,Roland McGrath
#
#另外，我没有使用GNUMake的默认依赖关系，我实在不喜欢那种方式，虽然ACE也用了这种关系,(或者说我还没有搞懂)
#
#Richard Stallman说：软件就像性，免费的比较好.
###############################################################################################################################


#你要定义输出文件,和PRGNAME的名称这两个变量
#PRGNAME表示你的程序名称，一般就是你的目录名称，当然希望目录名称不要重复，
#OUTFILE,最总输出的文件名称，为啥要定义这个呢，最后删除的时候可以统一
PRGNAME = rcmproto
# OUTFILE = $(PATH_BIN)/$(PRGNAME)
OUTFILE = lib$(PRGNAME).a


#如果你要编译EXECUTE文件，请定义EXEFILE=$(OUTFILE),
#EXEFILE = $(OUTFILE)
#如果你要编译DLL(.so)动态库，请在你的makefile定义DLLFILE=$(OUTFILE)
#DLLFILE = $(OUTFILE)
#如果你要编译LIB(.a)静态库，请在你的makefile定义LIBFILE=$(OUTFILE)
LIBFILE = $(OUTFILE)

#如果你使用预定头文件,请定义PREH_FILE,比如下面这样
#对应生成的GCH文件还只能放在当前目录下比较简单，放入其他目录很难保证其正常运行，打包源文件的脚本必须删除gch文件.
#如果你不适用预定头文件，可以屏蔽下面这个定义
# PREH_FILE = ./zone_predefine.h

PROTO_FILE = db_cache.proto diesystem.proto cardsystem.proto player_match.proto login.proto game_desk.proto action.proto \
			 gameshop.proto gameinfo.proto friend.proto mail.proto gm.proto pay.proto report.proto  rcm_error_code.proto \
			 rcm_cmd.proto activity.proto mission.proto rcminfo.proto
#这个里面定义所有的变量和定义,你自己看吧
include ../Makefile.macros

.PHONY :

#如果你想改变Mafile的规则，请在这个地方加入你自己的定义.


#这个定义其他所有的规则,还是你自己看吧
include ../Makefile.rule



