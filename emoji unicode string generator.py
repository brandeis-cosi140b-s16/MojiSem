__author__ = 'hannahprovenza'



'''
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]+',
'''
output = []
# for x in range(2600, 5631):
  #  output.append(chr(x))

for x in range(127744, 128591):
    output.append(chr(x).encode("unicode_escape"))

for x in range(128640, 128709):
    output.append(chr(x))

for x in range(9728, 10175):
    output.append(chr(x))


print(output[0:401])