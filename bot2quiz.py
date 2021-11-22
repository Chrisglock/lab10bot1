import logging
import random
from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a predefined poll"""
    count=0
    pool=[0,1,2,3,4,5,6,7,8,9,10,11]
    for i in range(0,6,1):
        
    
      questions = [
                  ["push", "pull", "commit"],
                   ["git track","git add","git push"]
                   ,["git log","git status","git commits"]
                   ,["verificar cambios antes de traerlos a tu repositorio","usar github","ninguna de las anteriores"],
                   ["git combine","git mix","git merge"],
                   ["git developers","git check","git blame"],
                  ["lenguaje de programacion","sistema de control de versiones","una pagina web"],
                  ["una version alterna del proyecto","un comando especial","una forma especial de commit"],
                  ["git download","git clone","git copy local"],
                  ["fetch y merge","cherrypick y combine","cherry-pick y merge"],
                  ["todos los archivos de trackean","git hooks","archivos .txt"],
                  ["desarrollo NO lineal entre ramas","desarrollo lineal entre ramas","ninguna de las anteriores",]
                   ]
      enunciados = ["como mandas tu progreso a tus compañeros en git?",
                    "como trackeamos un nuevo archivo en el repositorio?",
                    "como comprobamos el registro de commits?",
                    "cual seria una ventaja de hacer un pull request sobre solo hacer pull en github?",
                    "como combinas los cambios hechos en dos branches distintas?",
                    "como identificas el autor de los cambios hechos en el codigo?",
                    "que es git?",
                    "en git un una rama o branch es?",
                    "que comando sirva para traer a tu pc un repositorio en github?",
                    "git pull es una combinacion de?",
                    "que tipo de archivos no son trackeados por git?",
                    "el merge de tipo fast-fordward se da en?",]
      
      numran=random.randint(0, len(pool)-1)
      correctas = [0,1,0,0,2,2,1,0,1,0,1,1]
      nopregunta=pool[numran]
      
      question=questions[nopregunta]
      enunciado=enunciados[nopregunta]
      correcta=correctas[nopregunta]
      pool.remove(nopregunta)
      message = update.effective_message.reply_poll(
          enunciado, question, type=Poll.QUIZ, correct_option_id=correcta,
            is_anonymous=False
      )
      
      # Save some info about the poll the bot_data for later use in receive_quiz_answer
      payload = {
          message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
      }
      context.bot_data.update(payload)
      
      


def receive_quiz_answer(update: Update, context: CallbackContext) -> None:
    """el quiz de cierra despues de responder"""
    # the bot can receive closed poll updates we don't care about
    #print("id del correcto: " + str(update.poll.correct_option_id))
    #if update.poll.correct_option_id == option
    print("update.poll.correct_option_id")
    if update.poll.is_closed:
        return
    if update.poll.total_voter_count == 3:
        try:
            quiz_data = context.bot_data[update.poll.id]
        # this means this poll answer update is from an old poll, we can't stop it then
        except KeyError:
            return
        context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])
    


def preview(update: Update, context: CallbackContext) -> None:
    """Ask user to create a poll and display a preview of it"""
    # using this without a type lets the user chooses what he wants (quiz or poll)
    button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
    message = "Press the button to let the bot generate a preview for your poll"
    # using one_time_keyboard to hide the keyboard
    update.effective_message.reply_text(
        message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
    )


def receive_poll(update: Update, context: CallbackContext) -> None:
    """On receiving polls, reply to it by a closed poll copying the received poll"""
    actual_poll = update.effective_message.poll
    # Only need to set the question and options, since all other parameters don't matter for
    # a closed poll
    update.effective_message.reply_poll(
        question=actual_poll.question,
        options=[o.text for o in actual_poll.options],
        # with is_closed true, the poll/quiz is immediately closed
        is_closed=True,
        reply_markup=ReplyKeyboardRemove(),
    )


def help_handler(update: Update, context: CallbackContext) -> None:
    """Display a help message"""
    update.message.reply_text("Use /quiz, /poll or /preview to test this bot.")


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2126135673:AAEzEGBJJdRmOoiA7NzVzPnyQZwXntMhMuc")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(PollHandler(receive_quiz_answer))
    dispatcher.add_handler(CommandHandler('preview', preview))
    dispatcher.add_handler(MessageHandler(Filters.poll, receive_poll))
    dispatcher.add_handler(CommandHandler('help', help_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
