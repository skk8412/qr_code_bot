import segno
import telebot
import os
from segno import helpers

bot= telebot.TeleBot("5614074653:AAE63qqP_KlNJv8vtUV2BRVUhGg7_M0g43k")



@bot.message_handler(commands=['start'])
def start(message):
    f_name=message.from_user.first_name
    l_name=message.from_user.last_name
    bot.reply_to(message, "send /help to see all command")
    bot.send_message('@getnoti_abnh','New user from QR Code:{} {}'.format(f_name,l_name))


@bot.message_handler(commands=['help'])
def mainhelp(message):
    send = '''
    /normal -To create normal QR Code

    /color -To create colorful QR Code

    /wifi -To creat QR Code of WiFi

    /email -Create QR Code of email

    /geo -To creat loaction QR Code

    /mecard -Create MeCard QR Code

    /vcard -Create VCard QR Code

    /bgqr -Create QR Code with Image in Background

    /gifqr -Create QR Code with GIF in Background

    /logoqr -Create QR Code with logo in centre
    '''
    bot.reply_to(message, send)

@bot.message_handler(commands=['normal'])
def normal(message):
    bot.send_message(message.chat.id,"Enter the text/URL")
    bot.register_next_step_handler(message, get_text_message)

def get_text_message(message):
    text =message.text
    f_name=message.from_user.first_name
    try:
        qr= segno.make(text , error='h')
        qr.save('qr_code.png', scale=40)
        with open('qr_code.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        user_name = message.from_user.first_name
        chat_id = -1001843505894
        text = user_name + ' : new image normal'
        with open('qr_code.png', 'rb') as new:
            bot.send_photo(chat_id, new, caption=text)
        os.remove('qr_code.png')
    except Exception as e:
        bot.reply_to(message, "An error occurred: {}".format(e))



# color 

@bot.message_handler(commands=['color'])
def color(message):
    bot.send_message(message.chat.id, "Enter the text/URL")
    bot.register_next_step_handler(message, get_link)

def get_link(message):
    link = message.text
    bot.send_message(message.chat.id, "Enter the background color")
    bot.register_next_step_handler(message, get_bg_color, link=link)

def get_bg_color(message, link):
    bg_color = message.text
    bot.send_message(message.chat.id, "Enter the QR Code color")
    bot.register_next_step_handler(message, get_fg_color, link=link, bg_color=bg_color)

def get_fg_color(message, link, bg_color):
    fg_color = message.text
    # Use the link, bg_color, and fg_color to generate the QR code
    try:
        qr= segno.make(link , error='h')
        qr.save('qr_code.png', scale=40 ,dark=fg_color, light=bg_color)
        with open('qr_code.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        user_name = message.from_user.first_name
        chat_id = -1001843505894
        text = user_name + ' : new image color'
        with open('qr_code.png', 'rb') as new:
            bot.send_photo(chat_id, new, caption=text)
        os.remove('qr_code.png')
    except Exception as e:
        bot.reply_to(message, "An error occurred: {}".format(e))

# WIFI_CODE
@bot.message_handler(commands=['wifi'])
def wifi(message):
    bot.send_message(message.chat.id, "Enter the SSID")
    bot.register_next_step_handler(message, get_wifi_ssid)

def get_wifi_ssid(message):
    ssid = message.text
    bot.send_message(message.chat.id, "Enter the password")
    bot.register_next_step_handler(message, get_wifi_password, ssid=ssid)

def get_wifi_password(message, ssid):
    password = message.text
    bot.send_message(message.chat.id, "Enter the security type(/WEP/WPA/WPA2)")
    bot.register_next_step_handler(message, get_wifi_security, ssid=ssid, password=password)

def get_wifi_security(message, ssid, password):
    security = message.text
    bot.send_message(message.chat.id, "Enter the QR Code color")
    bot.register_next_step_handler(message, get_wifi_fg_color, ssid=ssid, password=password, security=security)

def get_wifi_fg_color(message, ssid, password, security):
    fg_color = message.text
    wifi_setting={
        'ssid': ssid,
        'password':password,
        'security':security
    }
    try:
        qr = helpers.make_wifi(**wifi_setting)
        qr.save('qr_code.png', scale=40, dark=fg_color)
        with open('qr_code.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        user_name = message.from_user.first_name
        chat_id = -1001843505894
        text = user_name + ' : new image wifi'
        with open('qr_code.png', 'rb') as new:
            bot.send_photo(chat_id, new, caption=text)
        os.remove('qr_code.png')
    except Exception as e:
        bot.reply_to(message, "An error occurred: {}".format(e))

# location script

@bot.message_handler(commands=['geo'])
def handle_geo(message):
    bot.send_message(message.chat.id, "Enter the latitude:")
    bot.register_next_step_handler(message, get_latitude)

def get_latitude(message):
    lat = message.text
    bot.send_message(message.chat.id, "Enter the longitude:")
    bot.register_next_step_handler(message, get_longitude, lat=lat)

def get_longitude(message, lat):
    lon = message.text
    bot.send_message(message.chat.id, "Enter the color for QR code ")
    bot.register_next_step_handler(message, get_qr_color, lat=lat, lon=lon)

def get_qr_color(message, lat, lon):
    bg_color = message.text
    try:
        qr_geo = helpers.make_geo(float(lat),float(lon))
        qr_geo.save('qr_code.png', scale=40, dark=bg_color)
        with open('qr_code.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        user_name = message.from_user.first_name
        chat_id = -1001843505894
        text = user_name + ' : new image geo'
        with open('qr_code.png', 'rb') as new:
            bot.send_photo(chat_id, new, caption=text)
        os.remove('qr_code.png')
    except Exception as e:
        bot.reply_to(message, "An error occurred: {}".format(e))



# vCard
@bot.message_handler(commands=['vcard'])
def handle_vcard(message):
    bot.send_message(message.chat.id, "Enter Name:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Enter Phone:")
    bot.register_next_step_handler(message, get_phone, name=name)

def get_phone(message, name):
    phone = message.text
    bot.send_message(message.chat.id, "Enter Email:")
    bot.register_next_step_handler(message, get_email, name=name, phone=phone)

def get_email(message, name, phone):
    email = message.text
    bot.send_message(message.chat.id, "Enter birhday(YYYY-MM-DD):")
    bot.register_next_step_handler(message, get_address, name=name, phone=phone, email=email)

def get_address(message, name, phone, email):
    birthday = message.text
    bot.send_message(message.chat.id, "Enter organization:")
    bot.register_next_step_handler(message, get_org, name=name, phone=phone, email=email, birthday=birthday)

def get_org(message, name, phone, email, birthday):
    org = message.text
    bot.send_message(message.chat.id, "Enter url:")
    bot.register_next_step_handler(message, get_url, name=name, phone=phone, email=email, birthday=birthday, org=org)

def get_url(message, name, phone, email, birthday, org):
    url = message.text
    try:
        qrcode_v=helpers.make_vcard(
                name=name,
                displayname=name,
                phone=phone,
                email=email,
                birthday= birthday,
                org=org,
                url=url
            )
        qrcode_v.save('qr_code.png', scale=40)
        with open('qr_code.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        user_name = message.from_user.first_name
        chat_id = -1001843505894
        text = user_name + ' : new image vcard'
        with open('qr_code.png', 'rb') as new:
            bot.send_photo(chat_id, new, caption=text)
        os.remove('qr_code.png')
    except Exception as e:
        bot.reply_to(message, "An error occurred: {}".format(e))



@bot.message_handler(commands=['mecard','bgqr','gifqr','logoqr','email'])
def all(message):
    bot.reply_to(message,"This feature will be available soon")



@bot.message_handler(func=lambda message: True)
def all(message):
    bot.reply_to(message, "Send /help to see all command") 

bot.polling()