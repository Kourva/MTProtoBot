<h1 align="center">
    <img align='left' src="https://github.com/Kourva/MTProtoBot/assets/118578799/8abb7f24-2547-4e6f-a119-86419fa92342" width=200 height=200/>
    <h2>MTProto Telegram Bot </h2>
  <p><b>Get frequently updated MTProto proxies from bot up to 20 at once!</b></p>
  <p><i>Also see information about each proxy which bot sends to you</i></p>
</h1>
<br><br>


# ▋Features
This bot can send from 5 - 20 proxies based on proxy index. [5, 10, 15, 20]
+ **/mtp** command to show proxy menu.

<br>

# ▋Clone Repository
To get started, first you need to **clone** this repository from github into your machine:
```bash
git clone https://github.com/Kourva/MTProtoBot
```
and if you dont have git you can install it from your package manager!

<br>

# ▋Install Requirements
Then you have to install requirements before running bot
1. Navigate to bot directory
2. Install requirements using pip
```bash
cd MTProtoBot
```
```bash
pip install -r requirements.txt
```
This will install **pyTelegamBotAPI** and **Requests** for you

<br>

# ▋Config your token
Now you have to get create bot from [BotFather](https://t.me/BotFather) **(If you don't have)** and take your **Token** to starts working with your bot.<br>
After getting **Token** from **BotFather** replace the Token in `utils.py` in line **10** as follows:
```python
# Bot token to use
Token = "6146793572:AAE7fbH29UPOKzlHlp0YDr9o06o_NdD4DBk"
```
> This is just an example Token. Use yours instead

<br>

# ▋Launch the bot
Now you are ready to launch your bot in polling mode inside your terminal using python
```bash
python main.py
```
You can also use **proxychains** to run your bot via **Tor** proxy
```bash
proxycahins python main.py
```
Or in quiet mode
```bash
proxychains -q python main.py
```
To install proxychains install `proxychains-ng` and then edit the config file in `/etc/proxychains.conf`.<br>
In config file comment the `strict_chain` and un-comment `dynamic_chain` and its ready to use.
<br>

# ▋TOR new IP address
If you got any denied requests that blocked your Ip address, you can renew your IP
```bash
sudo killall -HUP tor
```

<br>

# ▋Thanks
Give me a start if you made this bot helpful
