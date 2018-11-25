#!/usr/bin/env python
# -*- coding: utf-8 -*-


from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram import InlineQueryResultArticle, ParseMode,InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from urllib import quote_plus
import requests, logging
from bs4 import BeautifulSoup



token = "YOURBOTTOKEN"



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


    
def help(bot, update):
    msg = "Usage: /book <keyword> and I will give you direct links to PDF :)\n"
    msg += "Powered by libgen.pw\n"
    msg += "https://github.com/joaovarelas/bookbot_telegram"
    update.message.reply_text(msg)


    
def book(bot, update):
    line = update["message"]["text"].split()
    
    if len(line) < 2:
        update.message.reply_text('Hey! I need a keyword >:(')
        return
  
    url = "https://libgen.pw"
    bookname = quote_plus(' '.join(line[1:]))
    query = url+"/search?q="+bookname
    print query
    r = requests.get(query)
    html = r.text
    soup = BeautifulSoup(html, "lxml")

    items = soup.find_all("div", {"class": "search-results-list__item"})[1:]
    msg = ""
    for i in items:
        author = i.find("div", {"class": "search-results-list__item-author"}).get_text().strip()
        div_title = i.find("div", {"class": "search-results-list__item-title"})
        title = div_title.get_text().strip()
        bookid =  div_title.find("a", href=True)["href"].split('/')[4]
        link = url + "/download/book/" + bookid
        #print "title %s\tauthor %s\tlink %s" % (title, author, link)
        msg += "%s\n%s\n%s\n\n" % (title, author, link)

    update.message.reply_text(msg)
    

    

    
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("book", book))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


    
if __name__ == '__main__':
    main()
