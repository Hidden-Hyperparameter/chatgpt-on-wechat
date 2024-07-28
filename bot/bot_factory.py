"""
channel factory
"""
from common import const


def create_bot(bot_type):
    """
    create a bot_type instance
    :param bot_type: bot type code
    :return: bot instance
    """
    if bot_type == const.CPHOS:
        from bot.CPHOS_bot.cphos_bot import CPHOSBot
        return CPHOSBot()

    raise RuntimeError
