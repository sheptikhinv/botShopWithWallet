from configparser import ConfigParser

config = ConfigParser()


def get_token():
    try:
        file = open("settings.ini", "x")
    except:
        pass

    config.read("settings.ini")
    try:
        token = config["SETTINGS"]["TOKEN"]
    except:
        token = input("Введите токен вашего бота: ")
        if not "SETTINGS" in config:
            config.add_section("SETTINGS")
        config.set("SETTINGS", "TOKEN", token)
        with open("settings.ini", "w") as configfile:
            config.write(configfile)

    return token


def get_wallet_key():
    try:
        file = open("settings.ini", "x")
    except:
        pass

    config.read("settings.ini")
    try:
        token = config["SETTINGS"]["WALLET"]
    except:
        token = input("Введите ваш ключ от Wallet API: ")
        if not "SETTINGS" in config:
            config.add_section("SETTINGS")
        config.set("SETTINGS", "WALLET", token)
        with open("settings.ini", "w") as configfile:
            config.write(configfile)

    return token
