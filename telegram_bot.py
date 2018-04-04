import click
import requests
import time

@click.command()
@click.option('--token', help='bot token')
@click.option('--channel', help='channel name')
def main(token, channel):
    URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token, channel, 'test')
    answer = requests.get(URL)
if __name__ == '__main__':
    main()

