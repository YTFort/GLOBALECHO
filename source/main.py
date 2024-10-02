try:
    import configparser, threading, time, requests
    from nickname_generator import generate
    from rich.console import Console
    from rich_gradient import Gradient
    from logger import *
    console = Console()
except Exception as e:
    error(f"You haven't installed all the Python libraries!\nto fix errors: pip install -r requirements.txt\nError: {e}")
    exit(1)

try:
    from javascript import require, On
    mineflayer = require('mineflayer')
except Exception as e:
    error(f'You have not installed NodeJS or the mineflayer Library\nto fix the error: Install NodeJS and "npm install mineflayer" or "npm install" in the program folder\nError: {e}')
    exit(1)

try:
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="UTF-8")
except Exception as e:
    error(f'The problem with the config: {e}')
    exit(1)

def main():
    console.print(Gradient(
        r"""
  ______     __       _____      _____     _____     __         _____  _____   __   __    _____    
 /_/\___\   /\_\     ) ___ (   /\  __/\   /\___/\   /\_\      /\_____\/\ __/\ /\_\ /_/\  ) ___ (   
 ) ) ___/  ( ( (    / /\_/\ \  ) )(_ ) ) / / _ \ \ ( ( (     ( (_____/) )__\/( ( (_) ) )/ /\_/\ \  
/_/ /  ___  \ \_\  / /_/ (_\ \/ / __/ /  \ \(_)/ /  \ \_\     \ \__\ / / /    \ \___/ // /_/ (_\ \ 
\ \ \_/\__\ / / /__\ \ )_/ / /\ \  _\ \  / / _ \ \  / / /__   / /__/_\ \ \_   / / _ \ \\ \ )_/ / / 
 )_)  \/ _/( (_____(\ \/_\/ /  ) )(__) )( (_( )_) )( (_____( ( (_____\) )__/\( (_( )_) )\ \/_\/ /  
 \_\____/   \/_____/ )_____(   \/____\/  \/_/ \_\/  \/_____/  \/_____/\/___\/ \/_/ \_\/  )_____(                                                                                      
        """,
        colors=["#074891", "#4c0791"],
        justify="center" ))
    
    try:
        with open(config["server"]["serverlist"], 'r') as servers:
            count = sum(1 for line in servers)
        info(f'IP servers loaded: {count}')
    except Exception as e:
        error(f'The file with the servers could not be read: {e}')
        return

    info(f'Message: {config["text"]["message"]}')

    Start()

def connect(host, port, globalmessage):
    nickname = generate('en')

    bot = mineflayer.createBot({
      'host': host,
      'port': port,
      'username': nickname })
    
    @On(bot, "login")
    def login(this):
        bot.chat(f"/register H8yftdsF7d3 H8yftdsF7d3")
        bot.chat(f"/login H8yftdsF7d3")
        bot.chat(f"!{globalmessage}")

        @On(bot, 'chat')
        def handleMsg(this, sender, message, *args):
            errorleave = 0

            if sender and (sender != nickname):
                if errorleave <= 3:
                    errorleave += 1
                    bot.chat(f"!{globalmessage}")
                else:
                    bot.quit()
                    nosended(f'The message could not be sent to the server: {host}:{port}')
                    return
            else:
                bot.quit()
                sended(f'Successfully sent to the server: {host}:{port}')
                return
    
    @On(bot, "kicked")
    def kicked(this, reason, *a):
        bot.quit()
        nosended(f'The message could not be sent to the server: {host}:{port}')
        return
    
    @On(bot, "error")
    def error(err, *a):
        bot.quit()
        nosended(f'The message could not be sent to the server: {host}:{port}')
        return

def Start():
    threads = []

    with open(config["server"]["serverlist"], 'r') as servers:
        for line in servers:
            address = line.rstrip('\r\n')
            try:
                host, port = address.split(":")
            except:
                host = address
                port = 25565
            
            online = requests.get(f'https://api.mcsrvstat.us/3/{host}:{port}')
            data = online.json()

            if data['online']:
                try:
                    if str(data['protocol']['version']) == "-1" or str(data['protocol']['version']) == "0" or str(data['protocol']['version']) == "767":
                        nosended(f'The message could not be sent to the server: {host}:{port}')
                    else:
                        while threading.active_count() > int(config["server"]["maxtheards"]):
                            time.sleep(0.1)

                        ts = threading.Thread(target=connect, args=(host, port, config["text"]["message"], ))
                        ts.start()
                except:
                    nosended(f'The message could not be sent to the server: {host}:{port}')
            else:
                nosended(f'The message could not be sent to the server: {host}:{port}')

            continue

    for ts in threads:
        ts.join()
    
    info('Completed')

if __name__ == '__main__':
    main()