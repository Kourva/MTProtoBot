#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# MTProto telegram bot
# Developed by Kourva
# Source code: https://github.com/Kourva/MTProtoBot


# Libraries
import telebot  # Bot API Library
import requests  # Internet requests
import utils  # Bot Utilities
import time # Time functions
import json  # Json function
import os  # OS functions
from telebot import types, util # Bot utilities
from telebot.util import quick_markup  # Markup generator
from utils import Get_MTProto_Proxy  # MTProto function


# Connect to bot
# Token placed in utils.py file. You can change it with your token
MTPbot = telebot.TeleBot(utils.Token)
print(f"The Bot is online (id: {MTPbot.get_me().id})...")


# Start message handler
@MTPbot.message_handler(commands=["start", "restart"])
def start_command_handler(message: object) -> None:
    """
    Function   to   handle /start  & /restart  command
    Creates account for user and sends welcome message
    """

    # Search for user account that is exist or not
    if (ufile := f"{message.from_user.id}") in os.listdir("Accounts/"):
        # Send welcome back message to user
        MTPbot.send_chat_action(chat_id=message.chat.id, action="typing")
        MTPbot.reply_to(
            message=message,
            text=f"Welcome Back {message.from_user.first_name}.\nLet's chat! (Use /mtp for mtp menu).",
        )

    # Continue if user is new member and create account for user
    else:
        # Send welcome message to new user
        MTPbot.send_chat_action(chat_id=message.chat.id, action="typing")
        MTPbot.reply_to(
            message=message,
            text=f"Welcome Dear {message.from_user.first_name}.\nLet's chat! (Use /mtp for mtp menu).",
        )

        # Initialize user account's files
        os.mkdir(f"Accounts/{ufile}")  # User account


# MTproto command handler
@MTPbot.message_handler(commands=["mtp"])
def mtproto_command_handler(message: object) -> None:
    """
    Function to handle /mtp command
    Send MTProto Proxies up to 20 at once
    Use Mtproto button in main menu options to see usage
    """

    # Force chat type to private. Skip if user is Owner
    if utils.force_private(message):

        # Send indexing message to user
        MTPbot.send_chat_action(chat_id=message.chat.id, action="typing")
        mtp_menu_msg = MTPbot.send_message(
            chat_id=message.chat.id,
            text=f"Indexing Proxies for you... It can take up to minutes based on our internet speed!",
        )

        # Get proxies index (How many proxies are available)
        # and make buttons based on result (up to 20)
        proxy_length = len(
            requests.get("https://mtpro.xyz/api/?type=mtproto", stream=True).json()
        )
        Markups = types.InlineKeyboardMarkup()
        if proxy_length >= 1 and proxy_length < 5:
            Markups.add(
                (types.InlineKeyboardButton("Get 1", callback_data=f"GetMTProto_1")),
                (
                    types.InlineKeyboardButton(
                        "Get All", callback_data=f"GetMTProto_{proxy_length}"
                    )
                ),
                (types.InlineKeyboardButton("Close", callback_data=f"Close")),
                row_width=2,
            )
        elif proxy_length >= 5 and proxy_length < 10:
            Markups.add(
                (types.InlineKeyboardButton("Get 1", callback_data=f"GetMTProto_1")),
                (types.InlineKeyboardButton("Get 5", callback_data=f"GetMTProto_5")),
                (types.InlineKeyboardButton("Close", callback_data=f"Close")),
                row_width=2,
            )
        elif proxy_length >= 10 and proxy_length < 20:
            Markups.add(
                (types.InlineKeyboardButton("Get 1", callback_data=f"GetMTProto_1")),
                (types.InlineKeyboardButton("Get 5", callback_data=f"GetMTProto_5")),
                (types.InlineKeyboardButton("Get 10", callback_data=f"GetMTProto_10")),
                row_width=2,
            )
            Markups.add(
                (types.InlineKeyboardButton("Close", callback_data=f"Close")),
            )
        elif proxy_length >= 20:
            Markups.add(
                (types.InlineKeyboardButton("Get 1", callback_data=f"GetMTProto_1")),
                (types.InlineKeyboardButton("Get 5", callback_data=f"GetMTProto_5")),
                (types.InlineKeyboardButton("Get 10", callback_data=f"GetMTProto_10")),
                (types.InlineKeyboardButton("Get 20", callback_data=f"GetMTProto_20")),
                (types.InlineKeyboardButton("Close", callback_data=f"Close")),
                row_width=2,
            )

        # Edit previous message and show buttons
        MTPbot.edit_message_text(
            text=f"Currently {proxy_length} proxies are available.",
            chat_id=message.chat.id,
            message_id=mtp_menu_msg.message_id,
            reply_markup=Markups,
        )


# Callback query handler for buttons used in MTProto Menu
@MTPbot.callback_query_handler(func=lambda call: True)
def callback_query(call: object) -> None:
    """
    This function will handle the inline keyboards callback
    Show    results   and    Answer  the  callback  queries
    """

    # Initialize the IDs (User ID), (Chat ID), (Message ID)
    try:
        uid = call.from_user.id
    except:
        pass

    try:
        cid = call.message.chat.id
    except:
        pass

    try:
        mid = call.message.message_id
    except:
        pass

    # Callback handler for MTProto proxies
    if call.data.startswith("GetMTProto_"):
        
        # Error handling
        try:

            # Get the generator length from argument
            length = int(call.data.split("_")[1])

            # Fetch condition and result
            cond, result = Get_MTProto_Proxy(length)

            # If condition is false, send error result
            if not cond:
                MTPbot.answer_callback_query(call.id, result, show_alert=True)

            # Otherwise (If condition is true) send results
            else:
                # Make Buttons for each proxy and result
                keyboard = []
                for proxy in result:
                    (
                        host,
                        port,
                        secret,
                        country,
                        up,
                        down,
                        uptime,
                        addTime,
                        updateTime,
                        ping,
                    ) = proxy

                    # Shortened the proxy host if its long
                    shortened_host = host[:12] + "..." if len(host) > 15 else host

                    # Shortened the proxy secret
                    shortened_secret = (
                        secret[:12] + "..." if len(secret) > 15 else secret
                    )

                    # Make proxy URL to connect
                    proxy_url = f"tg://proxy?server={host}&port={port}&secret={secret}"

                    # Generate Connect & More Info button for each proxy
                    Markups = types.InlineKeyboardMarkup()
                    Markups.add(
                        (types.InlineKeyboardButton("Connect", url=proxy_url)),
                        (
                            types.InlineKeyboardButton(
                                "More Info",
                                callback_data=f"MtpInfo_{country}_{up}_{down}_{uptime}_{addTime}_{updateTime}_{ping}",
                            )
                        ),
                        row_width=2,
                    )

                    # Send the proxy to user
                    MTPbot.send_chat_action(chat_id=cid, action="typing")
                    MTPbot.send_message(
                        chat_id=cid,
                        text=f"▋Host: {shortened_host}\n▋Port: {port}\n▋Secret: {shortened_secret}",
                        reply_markup=Markups,
                    )

                    # Wait 1 second for each send (Telegram limitations)
                    # The limit is 1 second for each
                    time.sleep(1)

                # Delete the previous message
                MTPbot.delete_message(chat_id=cid, message_id=mid)

        except Exception as e:
            print(e) # Error
            # Show error message
            MTPbot.answer_callback_query(
                call.id, "Could not do this operation for now :("
            )

    # Callback handler for MTProto proxy information
    elif call.data.startswith("MtpInfo_"):
        # Error handling
        try:

            # Unpack the MTProto data from callback data
            (country, up, down, uptime, addTime, updateTime, ping) = call.data.split(
                "_"
            )[1:]

            # Shows the MTproto proxy information
            MTPbot.answer_callback_query(
                call.id,
                f"▋Ping: {ping}\n"
                f"▋Country: {country}\n"
                f"▋Upload: {up}\n"
                f"▋Download: {down}\n"
                f"▋Uptime: {uptime}\n"
                f"▋Add: {utils.time_ago(addTime)}\n"
                f"▋Update: {utils.time_ago(updateTime)}\n",
                show_alert=True,
            )

        except Exception as e:
            print(e) # Error
            # Show error message
            MTPbot.answer_callback_query(
                call.id, "Could not do this operation for now :("
            )

    # Callback handler for Close option
    elif call.data == "Close":
        # Error handling
        try:
            # Delete the message (Close)
            MTPbot.delete_message(chat_id=cid, message_id=mid)

        except:
            # Show error message
            MTPbot.answer_callback_query(
                call.id, "Could not do this operation for now :("
            )


# Connect to  bot in  infinite polling mode
# Make   bot  connection       non     stop
# Skip      old    messages,  don't  update
if __name__ == "__main__":
    # Error handling
    try:
        MTPbot.infinity_polling(
            skip_pending=True,
            none_stop=True,
        )

    # Except any error
    except:
        print("Lost connection!")
