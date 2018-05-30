import click
import requests
import time
import json
import os
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s ::: %(name)s: %(message)s (%(filename)s:%(lineno)d)',
                                        datefmt='%Y-%m-%d %H:%M:%S')
TELEGRAM_URL = 'https://api.telegram.org/botBOT_TOKEN/sendMessage?'
TELEGRAM_SEND_PHOTO_URL = 'https://api.telegram.org/botBOT_TOKEN/sendPhoto?'
TELEGRAM_URL_CHECK = 'https://api.telegram.org/botBOT_TOKEN/getUpdates'
VK_URL = 'https://api.vk.com/method/wall.get?'


@click.command()
@click.option('--t_token', help='telegramm bot token', required=True)
@click.option('--channel', help='channel name', required=True)
@click.option('--user_name', help='vk user name to follow', required=True, multiple=True)
@click.option('--v_token', help='vk app token', required=True)
def main(t_token, channel, user_name, v_token):

    def bot_action(input_text, chat_id, output_text = ''):
        if input_text == 'ping':
            requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token), params = {'chat_id': chat_id, 'text': 'I am alive and full of health!'})
        if input_text == 'last':
            requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token), params = {'chat_id': chat_id, 'text': output_text})

    link = ''
    if not os.path.isfile('log.txt'):
        logFile = open('log.txt','w')
        logFile.close()
    if not os.path.isfile('updates_log.txt'):
        updatesLogFile = open('updates_log.txt','w')
        updatesLogFile.close()
    #starting trace
    while True:
        try:
            #trace walls
            logFile = open('log.txt','r+')
            posts_id = set(logFile.read().splitlines())
            for un in user_name:
                req_ans = requests.get(VK_URL, params = {'v': '5.52', 'domain': un, 'access_token': v_token, 'count': 20, 'filter': 'owner'}).content
                vk_answer = json.loads(req_ans)
                for example in vk_answer['response']['items'][::-1]:
                    unique_id = '{}_{}_{}'.format(example['id'], example['from_id'], example['owner_id'])
                    if unique_id not in posts_id:
                        if 'attachments' in example:
                            for atch in example['attachments']:
                                if atch['type'] == 'photo':
                                    phts = atch['photo']
                                    dim = [int(d.replace('photo_','')) for d in phts.keys() if d.startswith('photo_')]
                                    link = phts['photo_{}'.format(max(dim))] #getting photo with max dim
                        if link != '':
                            requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token), params = {'chat_id': channel, 'text': un+'\n'+example['text']})
                            requests.get(TELEGRAM_SEND_PHOTO_URL.replace('BOT_TOKEN', t_token), params = {'chat_id': channel, 'photo': link})
                            link = ''
                        else:
                            requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token), params = {'chat_id': channel, 'text': un+'\n'+example['text']})

                        posts_id.add(unique_id)
                        logFile.write('{}\n'.format(unique_id))
            logFile.close()
            #updates handle of telegram
            updatesLogFile = open('updates_log.txt','r+')
            updates_id = set(updatesLogFile.read().splitlines())
            updates_answer = requests.get(TELEGRAM_URL_CHECK.replace('BOT_TOKEN', t_token)).json()
            for upd in updates_answer['result']:
                if str(upd['update_id']) not in updates_id:
                    if 'message' in upd:
                        tmp_key = 'message'
                    elif 'channel_post' in upd:
                        tmp_key = 'channel_post'
                    else:
                        continue
                    bot_action(upd[tmp_key]['text'], upd[tmp_key]['chat']['id'], output_text = un+'\n'+example['text'])
                    updates_id.add(str(upd['update_id']))
                    updatesLogFile.write('{}\n'.format(upd['update_id']))
            updatesLogFile.close()
        except Exception as e:
            logging.info(str(e))
        time.sleep(300)

if __name__ == '__main__':
    main()

