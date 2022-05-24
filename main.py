import json
import time
#import pyodbc
import psycopg2
import psycopg2.extras
import requests
import random
from threading import Thread

TOKEN = #the token of telegram bot goes here, check botFather
URL = f'https://api.telegram.org/bot{TOKEN}/'
USERNAME_BOT = "supremeWaiffuBot"
MAX_NUM_WAIFFUS = 5#updates in the database
GROUP = "-999999999"


# usou o metodo get, a resposta é um json, ele traduz o conteudo do json com decode
def get_url(url):
    resposta = requests.get(url)
    conteudo = resposta.content.decode("utf8")
    return conteudo


def get_json_from_url(url):
    conteudo = get_url(url)
    js = json.loads(conteudo)
    return js


def get_updates(url_bot):
    url = url_bot + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    numero_updates = len(updates["result"])
    ultimo_update = numero_updates - 1
    text = updates["result"][ultimo_update]["message"]["text"]
    chat_id = updates["result"][ultimo_update]["message"]["chat"]["id"]
    user_name = updates["result"][ultimo_update]["message"]["from"]["first_name"]
    return text, chat_id, user_name


def send_message(text, chat_id, id):
    conn = psycopg2.connect(
        dbname="xxxxxxxxxxxxxx",
        user="xxxxxxxxxxxxxx",
        password="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        host="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )
    if text == '/protecc':
        print('is correct')
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(f'select * from waiffus')
        waiffu = []
        waiffu = cursor.fetchall()
        # envia mensagem waiffu

        nome = waiffu[id]['waiffu_name']
        anime = waiffu[id]['waiffu_anime']
        url = URL + "sendMessage?text={}&chat_id={}".format(f'UWU Voce pretegeu a {nome} de {anime}, Ela agora faz parte do seu harém ❤️', chat_id)
        get_url(url)
        conn.commit()
        conn.close()
        cursor.close()
    elif text == '/help':
        url = URL + "sendMessage?text={}&chat_id={}".format("use os comandos protecc pra proteger as waiffus", chat_id)
        get_url(url)
        conn.commit()
        conn.close()
    else:
        url = URL + "sendMessage?text={}&chat_id={}".format(">.< Hmm... não é isso", chat_id)
        get_url(url)
        conn.commit()
        conn.close()
    # envia o comando get pra enviar essa requisição



#def send_photo(text,chat_id, link):


def send_photo(chat_id, link):
    parameters= {
        "chat_id": "-999999999",
        "photo": link,
        "caption": "😍 Uma Waiffu apareceu! digite /protecc e o nome dessa waiffu para adicioná-la no seu harém"
    }
    resp = requests.get(URL+"sendPhoto", parameters)
    #print(resp.text)


def get_waiffu():
    #numero primo: 317, 331, 997, 691, 881, 383
    #timer = 317
    timer = 17
    while timer > 0:
        timer -= 1
        print(f'tempo para a proxima waiffu={timer}')
        time.sleep(1)

    waiffu_ind = random.randint(1,MAX_NUM_WAIFFUS-1)
    print(waiffu_ind)
    conn = psycopg2.connect(
        dbname="xxxxxxxxxxxxxx",
        user="xxxxxxxxxxxxxxx",
        password="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        host="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )
    """cursor = conn.cursor()
    cursor.execute('select waiffu_image_link  from waiffus where waiffuid = 1')
    print(cursor.fetchone())"""

    # usando um dicionario, como uma coluna ao inves de uma linha da tabela
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f'select * from waiffus where waiffuID={waiffu_ind}')

    waiffu = []
    waiffu = cursor.fetchall()
    print(waiffu)
    #anime_waiffu = cursor.fetchone()['waiffuid']
    # print(waiffu[1]['waiffu_image_link'])
    link = waiffu[0]['waiffu_image_link']
    send_photo(GROUP, link)

    conn.commit()
    cursor.close()
    conn.close()

    #envia mensagem waiffu
    nome = waiffu[0]['waiffu_name']
    anime = waiffu[0]['waiffu_show']
    #send_message(f'UWU vc protegeu {nome} de {anime}, agora ela faz parte do seu harem', chat_id, nome)

    '''conn.commit()
    cursor.close()
    conn.close()'''
    return waiffu_ind


def user_waiffu(indice_atual):
    conn = psycopg2.connect(
        dbname="xxxxxxxxxxxxxx",
        user="xxxxxxxxxxxxxx",
        password="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        host="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    chat, text, user = get_last_chat_id_and_text(get_updates(URL))
    cursor.execute(f'insert into harens(userName, waiffuID) values (\'{user}\',{indice_atual});')

    cursor.close()
    conn.commit()
    conn.close()



def send_message_protecc(text_new, chat_new, indice_atual):
    conn = psycopg2.connect(
        dbname="xxxxxxxxxxxxxx",
        user="xxxxxxxxxxxxx",
        password="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        host="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f'select * from waiffus where waiffuid={indice_atual};')
    waiffu = []
    waiffu = cursor.fetchall()
    print(waiffu)
    nome = waiffu[0]["waiffu_name"]
    nome2 = waiffu[0]["waiffu_name2"]
    full_name = waiffu[0]["waiffu_total_name"]
    show = waiffu[0]["waiffu_show"]

    resposta_certa = "/protecc " + nome
    resposta_certa2 = "/protecc " + nome2
    print(f'{resposta_certa2} {resposta_certa}')

    if text_new == resposta_certa or text_new == resposta_certa2:
        print('sucesso!')
        user_waiffu(indice_atual)
        message_sucess = f'UWU Vc protegeu {full_name}! de {show} e agora ela faz parte do seu Harém'
        url = URL + 'sendMessage?text={}&chat_id={}'.format(message_sucess, "-999999999")
        get_url(url)
        return True
    else:
        return False


def wait_protection(url, text, chat, indice_atual):
    timer = 300
    last_textchat = (text, chat)
    while timer>0:
        print(f'aguardando proteção {timer}')
        timer -=1
        text_new, chat_new, qualquer = get_last_chat_id_and_text(get_updates(url))
        if (text_new, chat_new) != last_textchat:
            if send_message_protecc(text_new, chat_new, indice_atual) == True:
                return
            else:
                print("falha")

        last_textchat = (text_new, chat_new)
        time.sleep(0.25)
    url = URL + "sendMessage?text={}&chat_id={}".format(">´o`> Não! a Waiffu já se foi", "-999999999")
    get_url(url)


def show_harem(user):
    conn = psycopg2.connect(
        dbname="xxxxxxxxxxxxxx",
        user="xxxxxxxxxxxxxx",
        password="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        host="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f'select waiffuID from harens where userName=\'{user}\';')
    waiffus = []
    waiffus = cursor.fetchall()
    print(waiffus)
    cursor.execute(f'select * from waiffus;')
    lista_total_waiffus = cursor.fetchall()
    lista_waiffus = f'harem de {user}'
    for waiffu in waiffus:
        lista_waiffus += lista_total_waiffus[int(waiffu)] + '\n'

    url = URL + 'sendMessage?text={}&chat_id={}'.format(lista_waiffus, "-999999999")
    get_url(url)


def answer_comands():
    last_textchat = (None, None)
    while True:
        text, chat, user = get_last_chat_id_and_text(get_updates(URL))
        if (text, chat) != last_textchat:
            if text == "/harem":
                show_harem(user)
            '''elif text == "/ranking":
                show_ranking(user)'''
        last_textchat = (text, chat)
        time.sleep(0.5)



def main(url):
    last_textchat = (None, None)
    indice_atual = 0
    while True:
        text, chat, user = get_last_chat_id_and_text(get_updates(url))
        if (text, chat) != last_textchat:
            # send_message(text, chat)
            Thread(target=get_waiffu).start()
            Thread(target=answer_comands).start()
            #indice_atual = get_waiffu()
            wait_protection(url, text, chat, indice_atual)
            print(indice_atual)
            #send_message(text,chat,indice_atual)

        last_textchat = (text, chat)
        time.sleep(0.5)


if __name__ == '__main__':
    main(URL)
