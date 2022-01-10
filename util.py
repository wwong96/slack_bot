import os
import requests
import json
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen



class Parser:
    def __init__(self, client, channel):
        self.client = client
        self.channel = channel
        print("Parser inited")

    def post_message(self, text):
        response = self.client.chat_postMessage(
            channel=self.channel,
            text=text)
        return None

    def post_image(file, title):
        response = self.client.files_upload(
            channels=self.channel,
            file=file,
            title=title
        )
        return None

    def Egg(self, query_list):
        self.post_message("...")
        return None

    def TicTacToe(self, query_list):
        if query_list[1] =='시작':
            return

    def Corona(self, query_list):
        url = 'http://ncov.mohw.go.kr/'
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            num = soup.select_one(".occur_graph > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(5) > span:nth-child(1)")
            num = int(num.get_text().replace(',',''))
            self.post_message(f"오늘의 코로나 확진자 수는 {num}명입니다.")
        else:
            self.post_message(f"홈페이지 접속에 문제가 있습니다. - {response.status_code}")

    def Choice(self, query_list):
        if len(query_list) == 1:
            self.post_message("선택지가 없습니다")
            return None
        ans = random.choice(query_list[1:])
        self.post_message(ans)
        return None


    def DevTodo(self, query_list):
        with open('res/deb.json', 'r') as f:
            deb_todo = json.load(f)
        if len(query_list) == 1:
            self.post_message("[!help 개발문의]를 참고해주세요")
            return None
        elif len(query_list) == 2:
            cmd = query_list[1]
            if cmd == "목록":
                answer = ''
                for c in deb_todo.keys():
                    answer += (c + ', ')
                answer = answer[:-2]
                self.post_message(answer)
                return None
            elif cmd not in deb_todo.keys():
                self.post_message("현재 개발문의 목록에 없는 명령어입니다.")
                return None
            else:
                self.post_message(f"{cmd} : {deb_todo[cmd]}")
                return None
        elif len(query_list) >= 3:
            if query_list[1] == '개발완료':
                cmd = query_list[2]
                if cmd not in deb_todo.keys():
                    self.post_message("개발문의 목록에 없는 명령어입니다")
                    return None
                del deb_todo[query_list[2]]
                with open('res/deb.json', 'w') as f:
                    f.write(json.dumps(deb_todo, ensure_ascii=False, indent=4))
                self.post_message(f"{cmd} 명령어가 개발 완료되어 개발문의 목록에서 삭제되었습니다. !help {cmd}를 참고해주세요")
                return None
            else:
                cmd = query_list[1]
                deb_todo[cmd] = ' '.join(query_list[2:])
                with open('res/deb.json', 'w') as f:
                    f.write(json.dumps(deb_todo, ensure_ascii=False, indent=4))
                self.post_message(f"{cmd} 명령어가 개발 문의 목록에 추가되었습니다. !개발문의 {cmd}로 확인해보세요")
                return None
        else:
            self.post_message("[!help 개발문의]를 참고해주세요")
            return None

    def Help(self, query_list):
        with open('command.json') as f:
            json_data = json.load(f)
        command_list = json_data['command_list']
        help_list = json_data['help']
        if len(query_list) == 1:
            answer = '현재 존재하는 명령어 : '
            for c in command_list.keys():
                answer = answer +  c + ', '
            answer = answer[:-2]
            self.post_message(answer)
            return answer

        elif len(query_list) == 2:
            command = query_list[1]
            if command not in help_list.keys():
                self.post_message("존재하지 않는 명령어입니다.")
                return None
            answer = command + ' : ' + help_list[command]
            self.post_message(answer)
            return answer

        else:
            self.post_message('올바르지 않은 사용법입니다')
            return None


    def Hello(self, query_list):
        print("Hello")
        self.post_message("안녕!")
        return None


    def APOD(self, query_list):
        self.post_message("현재 버그로 기능 중지되었습니다.")
        return None
        """
        root = 'https://apod.nasa.gov/'
        webpage = requests.get('https://apod.nasa.gov/')
        soup = BeautifulSoup(webpage.content, "html.parser")
        img = soup.find_all('img')

        if len(img) < 1:
            self.post_message("APOD 사진을 찾을 수 없습니다.")
            return None
        else:
            image = root + img[0]['src']
            with urlopen(image) as f:
                if os.path.isfile('res/apod.jpg'):
                    os.remove('res/apod.jpg')
                with open('res/apod.jpg', 'wb') as h:  # w - write b - binary
                    img = f.read()
                    h.write(img)
            self.post_image('res/apod.jpg', 'APOD.jpg')
        return None
        """


