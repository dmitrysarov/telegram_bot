import click
import requests
import time
import json

TELEGRAM_URL = 'https://api.telegram.org/botBOT_TOKEN/sendMessage?chat_id=CHAT_ID&text=TEXT'
VK_URL = 'https://api.vk.com/method/wall.get?v=5.52&domain=USER_NAME&access_token=TOKEN&count=100'
@click.command()
@click.option('--t_token', help='telegramm bot token', required=True)
@click.option('--channel', help='channel name', required=True)
@click.option('--user_name', help='vk user name to follow', required=True, multiple=True)
@click.option('--v_token', help='vk app token', required=True)
def main(t_token, channel, user_name, v_token):
    print(t_token, channel, user_name, v_token)
    posts_id = set([])
    while True:
        for un in user_name:
            req_ans = requests.get(VK_URL.replace('USER_NAME', un).replace('TOKEN', v_token)).content
            vk_answer = json.loads(req_ans)
            for example in vk_answer['response']['items']:
                unique_id = '{}_{}_{}'.format(example['id'], example['from_id'], example['owner_id'])
                if unique_id not in posts_id:
                    requests.get(TELEGRAM_URL.replace('BOT_TOKEN', t_token).replace('CHAT_ID', channel).replace('TEXT', example['text']))
                    posts_id.add(unique_id)
        time.sleep(20)
if __name__ == '__main__':
    main()

