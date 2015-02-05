from struct import *
def _pack(v, p, msg):
    buffer = []
    #'''
    buffer.insert(0, (v >> 8) & 0xff)
    buffer.insert(1, v & 0xff)
    buffer.insert(2, (p >> 24) & 0xfff)
    buffer.insert(3, (p >> 16) & 0xff)
    buffer.insert(4, (p >> 8) & 0xff)
    buffer.insert(5, p & 0xff)
    buffer.insert(6, msg)
    '''
    buffer[0] = (v >> 8) & 0xff
    buffer[1] = v & 0xff
    buffer[2] = (p >> 24) & 0xff
    buffer[3] = (p >> 16) & 0xff
    buffer[4] = (p >> 8) & 0xff
    buffer[5] = p & 0xff
    buffer[6] = msg
    print buffer[6]
    '''
    str1 = pack("!BBBBBB", (v >> 8) & 0xff, v & 0xff, (p >> 24) & 0xfff, (p >> 16) & 0xff, (p >> 8) & 0xff, p & 0xff);
    str1 += str(msg)
    print str1
    return str1

    
_pack(1,2003, "saf")