from django.conf import settings as conf
from django.core.management import BaseCommand
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from bot.bot import get_last, start


class Command(BaseCommand):
    help = 'Bot start polling.'

    def handle(self, *args, **kwargs):
        updater = Updater(token=conf.BOT_TOKEN)
        disp = updater.dispatcher

        disp.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CallbackQueryHandler(get_last))

        updater.start_polling()
        updater.idle()
