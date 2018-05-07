import sys, pprint
import librun
"""
print("len: "+str(len(sys.argv)))
ali=[]
adi={}

abali = []
asi = " ".join(sys.argv)
bdi={}
while "--" in asi:
    abali = asi.split(" ")
    for n in range(len(abali)):
        if "--" == abali[n][0:2]:
            bsi = abali.pop(n).replace("--","")
            print("bsi:"+bsi)
            if "=" in bsi:
                bli=bsi.split("=")
                print(bli[0]+" : "+bli[1])
                bdi.update({ bli[0] : bli[1] })
                asi = " ".join(abali)
                break
print("bdi: "+pprint.pformat(bdi))

adali = []
adali = asi.split(" ")
for n in range(len(adali)):
    if adali[n][0] == '-':
        ali.append(n)

print("ali: "+pprint.pformat(ali))
for n in ali:
    if ali.index(n) == len(ali)-1:
        bli = adi.get(adali[n],[])
        bli.extend(adali[n+1:len(adali)])
        adi.update({ adali[n] : bli })
        print(adali[n]+": "+pprint.pformat(adali[n+1:len(adali)]))
    else:
        bli = adi.get(adali[n],[])
        bli.extend(adali[n+1:ali[ali.index(n)+1]])
        adi.update({ adali[n] : bli })
        # print(str(ali[ali.index(n)+1]))
        print(adali[n]+": "+pprint.pformat(adali[n+1:ali[ali.index(n)+1]]))
        # print(adali[n]+": "+str(ali.index(n))+", "+str(len(ali)))
print("adi: "+pprint.pformat(adi))
"""
Ano = librun.loggi()
print("Ano.dicodi:\n"+pprint.pformat(Ano.dicodi,compact=True))
""""""
