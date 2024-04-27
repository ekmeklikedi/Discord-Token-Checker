import requests
import time
import pyfiglet
import threading

print(pyfiglet.figlet_format("XWİ FORUM DEDE TOKEN CHECKER ;)\n"))

# Kullanıcıdan iş parçacığı sayısını alın
num_threads = int(input("Ne kadar hız istiyorsunuz? (Örnek 120):  "))

def check_discord_tokens(tokens, valid_tokens_file, invalid_tokens_file):
    for token in tokens:
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token.strip(),
            'origin': 'null',
            'sec-ch-ua': '"Opera GX";v="89", "Chromium";v="103", "_Not:A-Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Campaign 34)'
        }

        response = requests.get('https://discordapp.com/api/v8/users/@me', headers=headers)
        if response.status_code == 200:
            print("--+ ÇALIŞAN TOKEN : " + token.strip() + " + --")
            valid_tokens_file.write(token)  # Çalışan tokenleri valid_tokens.txt dosyasına yaz
            valid_tokens_file.flush()  # Buffer'i temizle
        elif response.status_code == 401:
            print("Çalışmayan token: " + token.strip())
            invalid_tokens_file.write(token)  # Çalışmayan tokenleri invalid_tokens.txt dosyasına yaz
            invalid_tokens_file.flush()  # Buffer'i temizle
        else:
            print("Error occurred:", response.text)

        # Saniyede 15 token kontrol edecek şekilde bekleyin
        time.sleep(1 / 15)

def start_token_checking(tokens, valid_tokens_file, invalid_tokens_file, num_threads):
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=check_discord_tokens, args=(tokens[i::num_threads], valid_tokens_file, invalid_tokens_file))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

# Tokenleri içeren dosyanın adını ve yolunu buraya girin
token_file_path = "tokens.txt"
valid_tokens_file_path = "calisan_tokenler.txt"
invalid_tokens_file_path = "calismayan_tokenler.txt"

# Token dosyasını okuyun
tokens = open(token_file_path, 'r').readlines()

# Her bir token için token kontrolü yapın
start_token_checking(tokens, open(valid_tokens_file_path, 'a'), open(invalid_tokens_file_path, 'a'), num_threads)

# Programın kapanmaması için input ekleyin
input("Programı kapatmak için herhangi bir tuşa basın...")