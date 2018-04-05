import click
import requests
import time
import json
import os

TELEGRAM_URL = 'https://api.telegram.org/botBOT_TOKEN/sendMessage?chat_id=CHAT_ID&text=TEXT'
VK_URL = 'https://api.vk.com/method/wall.get?v=5.52&domain=USER_NAME&access_token=TOKEN&count=100'
@click.command()
@click.option('--t_token', help='telegramm bot token', required=True)
@click.option('--channel', help='channel name', required=True)
@click.option('--user_name', help='vk user name to follow', required=True, multiple=True)
@click.option('--v_token', help='vk app token', required=True)
def main(t_token, channel, user_name, v_token):
    link = ''
    if not os.path.isfile('log.txt'):
        logFile = open('log.txt','w')
        logFile.close()
    #starting trace
    while True:
        logFile = open('log.txt','r+')
        posts_id = set([logFile.read().splitlines()])
        for un in user_name:
            req_ans = requests.get(VK_URL.replace('USER_NAME', un).replace('TOKEN', v_token)).content[::-1]
            vk_answer = json.loads(req_ans)
            for example in vk_answer['response']['items']:
                unique_id = '{}_{}_{}'.format(example['id'], example['from_id'], example['owner_id'])
                if unique_id not in posts_id:
                    requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token).replace('CHAT_ID', channel).replace('TEXT', example['text']))
                    for atch in example['attachments']:
                        if atch['type'] == 'photo':
                            phts = atch['photo']
                            dim = [int(d.replace('photo_','')) for d in phts.keys() if d.startswith('photo_')]
                            link = phts['photo_{}'.format(max(dim))] #getting photo with max dim
                    if link != '':
                        requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token).replace('CHAT_ID', channel).replace('TEXT', link))
                        link = ''
                    posts_id.add(unique_id)
                    logFile.write('{}\n'.format(unique_id))
        logFile.close()
        time.sleep(20)
if __name__ == '__main__':
    main()

