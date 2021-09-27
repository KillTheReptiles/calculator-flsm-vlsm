###Calculator Functions### 
def listToFormat (list_in):
    contDot = 0
    formatString = ''
    numBin = ''
    for i in range(len(list_in)):
        numBin += list_in[i]
        contDot += 1
        if contDot == 8:
            formatString += str(int(numBin,2))
            formatString += '.'
            contDot = 0
            numBin = ''
    finale = formatString[0:-1]
    return finale
def ipToList (addressNet):
    aIP =  str("{0:b}".format(int(addressNet.split('.')[0])))
    bIP =  str("{0:b}".format(int(addressNet.split('.')[1])))
    cIP =  str("{0:b}".format(int(addressNet.split('.')[2])))
    dIP =  str("{0:b}".format(int(addressNet.split('.')[3])))
    ###Validation for less than eight###
    if len(aIP) < 8: aIP = aIP.zfill(8)
    if len(bIP) < 8: bIP = bIP.zfill(8)
    if len(cIP) < 8: cIP = cIP.zfill(8)
    if len(dIP) < 8: dIP = dIP.zfill(8)
    addressIPConca = aIP + bIP + cIP + dIP
    addressIPList = []
    for i in addressIPConca:
        addressIPList.append(i)#add each character of IP to a list
    return addressIPList
def is_255 (addressNet):
    first = ''
    for i in range(4-1, -1, -1):
        if addressNet.split('.')[i] == '255':
            a = addressNet.split('.')
            a[i] = '0'
            addressNet = '.'.join(a)
        else:
            a = addressNet.split('.') 
            a[i] = str(int(addressNet.split('.')[i])+1)
            first = '.'.join(a) 
            break
    return first 
def is_0 (broadcastDef):
    finale = ''
    for i in range(4-1, -1, -1):
        if broadcastDef.split('.')[i] == '0':
            a = broadcastDef.split('.')
            a[i] = '255'
            broadcastDef = '.'.join(a)
        else:
            a = broadcastDef.split('.')
            a[i] = str(int(broadcastDef.split('.')[i])-1)
            finale = '.'.join(a)
            break
    return finale
###Inputs### 
print('1. for FLSM \n2. for VLSM')
option = input()
print('What is the address IP?:')
addressNet = input()
print('What is Subnetwork(MASK)?: ')
subNetwork = input()
#########################
addressIPConca = ''.join(ipToList(addressNet))
subNetworkConca = ''.join(ipToList(subNetwork))
addressIPList = ipToList(addressNet)
addressIPListTemp = ipToList(addressNet)

if option == '1':
    print('What is the subnets?: ')#How many subnets you want calculate?
    numSubnets = input()
    numSubnetsBin = str("{0:b}".format(int(numSubnets)))

    prefixInitial = int(str(subNetworkConca.count('1')))
    prefix = prefixInitial + len(("{0:b}".format(int(numSubnets))))

    subNetworkList = ipToList(subNetwork)
    contSubNetwork = prefixInitial+1
    for i in range (1,len(subNetworkList)+1):
        if i == contSubNetwork:
            subNetworkList.insert(i-1, '1')
            contSubNetwork += 1
        if i == prefix:
            print('------------------------')
            print('SubNetwork Mask: ' + listToFormat(subNetworkList) + '/' + str(prefix))
            print('------------------------')
            break
    contSubNetwork = prefixInitial + 1
    subNetCont = 0
    for j in range(int(numSubnets)):
        addressIPListTemp = addressIPList
        contPositionSubnet = 0
        binSubnet = str("{0:b}".format(int(subNetCont)))
        if len(binSubnet) < 3:
            binSubnet = binSubnet.zfill(len(numSubnetsBin)) #fill with zeros if is missing the len = 3
        for i in range (1,len(addressIPList)+1):
            if i == contSubNetwork:
                addressIPListTemp[i-1] = binSubnet[contPositionSubnet]
                contPositionSubnet += 1
                contSubNetwork += 1
            if i == prefix:
                subNetCont += 1
                contPositionSubnet = 0
                contSubNetwork = prefixInitial + 1
                print('IP #'+ str(j+1)+': '+ listToFormat(addressIPListTemp))
                break
    print('------------------------')
if option == '2':
    print('How many host?')
    numHost = input()
    print('Write the host you want counting the 2 unusable')
    host = []
    for i in range(int(numHost)):
        host.append(int(input())) #Read the input host and save them in a List
    host.sort(reverse=True)
    conthost = 0
    contPower = 0
    maxHost = 0
    for i in range(len(host)):
        print('\n------------------------')
        print ('Address IP: ', addressNet)
        for i in range(32):
            if int(host[conthost]) <= 2**i:
                maxHost = 2**i
                break
            contPower += 1
        subNetworkBinStr = '1'*(32-int(contPower))
        subNetworkBinStr += '0'*contPower
        subNetworkBin = []
        for i in subNetworkBinStr: #add each character of mask or subnetwork in a list  
            subNetworkBin.append(i)
        prefix = 32-int(contPower)
        print('SubNetwork mask: : ' + listToFormat(subNetworkBin) + '/' + str(prefix) + '\nMaximum host: ' + str(maxHost))#Delete the last 'point' of string
        print('------------------------')
        first = '' #first usable
        last = '' #last usable
        broadcast = ipToList(addressNet)
        broadcastFinal = ''
        ##Find First Usable
        addressNetVLSM = addressNet
        print('First:', is_255(addressNet))
        ##Find Broadcast host
        contBroad = 0
        for i in range(32):
            if i == (32-int(contPower)+contBroad):
                broadcast[i] = '1'
                contBroad += 1
        contPower = 0
        print('Broadcast:', listToFormat(broadcast))
        broadcastFinal = str(listToFormat(broadcast))
        ##Increase the Address IP +1
        for i in range(4-1, -1, -1):
            if broadcastFinal.split('.')[i] == '255':
                a = broadcastFinal.split('.')
                a[i] = '0'
                addressNet = '.'.join(a)
            else:
                a = broadcastFinal.split('.') 
                a[i] = str(int(broadcastFinal.split('.')[i])+1)
                addressNet = '.'.join(a) 
                break
        ##Find Last Usable
        print('Latest:', is_0(broadcastFinal))
        conthost += 1
else:
    print('Option ', option, ' does not exist')