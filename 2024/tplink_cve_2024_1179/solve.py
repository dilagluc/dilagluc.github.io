import binascii

def logical(output):
    #output = b'1_l0v3_R3v3rsE_Eng1n33r1ng_dUd3!!!!'  # Desired output
    byte_sequence = bytearray(b'\x4b\x11\x4b\x7e\x5f\x54\x1d\x3b\x6b\x02\x5d\x6e\x14\x7b\x43\x3b\x6e\x53\x31\x31\x6f\x75\x02\x2d\x46\x42\x43\x2a\x6c\x56\x29\x5f\x09\x17\x44')  # Byte sequence used
    byte_sequence.reverse()
    #print(byte_sequence)

    input_bytes = bytearray(len(output))
    for i in range(len(output)):
        input_bytes[i] = output[i] ^ byte_sequence[i % len(byte_sequence)]

    input_string = input_bytes.decode()
    return input_bytes


def ceasar(output):
    input_bytes = bytearray(len(output))
    minus = list(map(lambda i: i - ord('\r'), output))
    plus = list(map(lambda i: i +13, output))
    final=[]
    
    for i in range(len(minus)):
        if ( (ord('`') < minus[i] < ord('{')) or (ord('@') < minus[i] < ord('['))):
            if( minus[i] < ord('n') and (minus[i]< ord('N') or ord('Z')< minus[i])):
                ## Minus fit the two conditions great it's definitely the minus one
                final.append(minus[i])
            else:
                # 
                if ( (ord('`') < output[i] < ord('{')) or (ord('@') < output[i] < ord('['))     ):
                    final.append(plus[i])
                    #print(chr(plus[i]))
                else:
                    final.append(output[i])
                    #print(chr(output[i]) )
        elif( ( ord('`') < plus[i] < ord('{')) or (ord('@') < plus[i] < ord('[') )):
                if ( (ord('`') < output[i] < ord('{')) or (ord('@') < output[i] < ord('['))     ):
                    final.append(plus[i])
                    #print(chr(plus[i]) + "___in")
                else:
                    final.append(output[i])
                    #print(chr(plus[i]) +"___out")
        else:
            #print(chr(output[i]))
            final.append(output[i])
    
    return bytearray(final)

'''def replace(output):
    input_length = len(output)
    input_bytes = bytearray(input_length)

    for i in range(input_length):
        input_bytes[i] = output[input_length - i - 1]

    return input_bytes
    #input_string = input_bytes.decode()'''

def replace(output):
    return output[::-1]
    #input_string = input_bytes.decode()

output = b'1_l0v3_R3v3rsE_Eng1n33r1ng_dUd3!!!!'  # Desired output


print(logical(output))
print(  ceasar(logical(output)))

print(  replace(ceasar(logical(output)) ) )