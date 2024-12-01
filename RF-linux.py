import os
import socket
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from multiprocessing.pool import ThreadPool

BOT_TOKEN = 'BOT_TOKEN'

def start(update, context):
    try:
        username = os.getlogin()
    except OSError:
        username = "Unknown User"

    kernal_version = os.uname().release
    ip_address = socket.gethostbyname(socket.gethostname())

    welcome_message = f"Welcome to the Linux File Access Bot, {username}! :)\n\n"
    welcome_message += f"System Details:\n"
    welcome_message += f"  Username: {username}\n"
    welcome_message += f"  Kernel Version: {kernal_version}\n"
    welcome_message += f"  IP Address: {ip_address}\n\n"

    instructions = "Available commands:\n"
    instructions += "/start - Display welcome message and instructions\n"
    instructions += "/ls - List files in the current directory\n"
    instructions += "/cat <filename> - Read the content of a file\n"
    instructions += "/get <filename> - Download a file\n"
    instructions += "/get_dir_zip <directory> - Download an entire directory as a ZIP\n"
    instructions += "/get_dir <directory> - Download an entire directory recursively\n"
    instructions += "/structure - Display the directory structure\n"
    instructions += "/cdx - Go up one directory\n"
    instructions += "/cd <directory> - Go into the specified directory\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message + instructions)

def list_files(update, context):
    files = os.listdir()
    file_list = '\n'.join(files)
    context.bot.send_message(chat_id=update.effective_chat.id, text=file_list)

def read_file(update, context):
    file_name = ' '.join(context.args)
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            context.bot.send_message(chat_id=update.effective_chat.id, text=content)
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="File not found.")

def get_file(update, context):
    file_name = ' '.join(context.args)
    try:
        with open(file_name, 'rb') as file:
            context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="File not found.")

def get_dir_zip(update, context):
    directory = ' '.join(context.args)
    try:
        zip_file_name = f"{directory}.zip"
        os.system(f"zip -r {zip_file_name} {directory}")

        with open(zip_file_name, 'rb') as zip_file:
            context.bot.send_document(chat_id=update.effective_chat.id, document=zip_file)

        os.remove(zip_file_name)

    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Directory not found.")

def get_dir(update, context):
    directory = ' '.join(context.args)
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as file:
                    context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Directory not found.")

def display_directory_structure(update, context):
    structure = os.walk('.')
    structure_str = ''
    for root, dirs, files in structure:
        structure_str += f"{root}:\n"
        structure_str += f"  Directories: {', '.join(dirs)}\n"
        structure_str += f"  Files: {', '.join(files)}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=structure_str)

def go_up_directory(update, context):
    os.chdir('..')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Moved up one directory.")

def go_into_directory(update, context):
    directory = ' '.join(context.args)
    try:
        os.chdir(directory)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Moved into directory: {directory}")
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Directory not found.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ls', list_files))
    dp.add_handler(CommandHandler('cat', read_file, pass_args=True))
    dp.add_handler(CommandHandler('get', get_file, pass_args=True))
    dp.add_handler(CommandHandler('get_dir_zip', get_dir_zip, pass_args=True))
    dp.add_handler(CommandHandler('get_dir', get_dir, pass_args=True))
    dp.add_handler(CommandHandler('structure', display_directory_structure))
    dp.add_handler(CommandHandler('cdx', go_up_directory))
    dp.add_handler(CommandHandler('cd', go_into_directory, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
