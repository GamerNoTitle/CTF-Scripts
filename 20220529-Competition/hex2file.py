hexdata = '526172211A070100CF907300000D00000000000000C4527424943500300000002A0000000235B9F9B0530778B5541D3308C50020000000666C61672E747874B9BA0132357642F3AFC000B092C229D6E994167C055EA78708B271FFC042AE3D251E65536F9ADA5087C77406B67D0E631668476607A86E844DC81AA2C72C714A348D10C43D7B00400700E'
times = 1
for i in range(0,len(hexdata),2):
    data = hexdata[i:i+2]
    with open('bin.txt', 'at') as f:
        if times == 8:
            f.write(data+'\n')
            times = 1
        else:
            f.write(data+' ')
            times += 1