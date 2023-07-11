# Utils file for ChatGpt bot


# Libraries
import requests  # Make requests
import json      # Json function
import random    # Random functions
import datetime  # Datetime functions 


# Bot token to use
Token = "Your Token here"


# Escape markdown filter
def escape_markdown(string: str) -> str:
    """
    Function to escape markdown syntax
    
    Parameter:
        String to be escaped
    
    Returns:
        Filtered string
    """

    # Return escaped string
    return (
        string.replace("_", "\_").replace("*", "\*").replace("[", "\[")
        .replace("]", "\]").replace("(", "\(").replace(")", "\)")
        .replace("~", "\~").replace(">", "\>").replace("#", "\#")
        .replace("+", "\+").replace("-", "\-").replace("=", "\=")
        .replace("|", "\|").replace("{", "\{").replace("}", "\}")
        .replace(".", "\.").replace("!", "\!").replace(",", "\,")
    )


# Force private chat
def force_private(message: object) -> bool:
    """
    Function to force chat into private chat

    Parameter:
        Message object

    Returns:
        Boolean value
    """

    # Return Boolean statement
    if message.chat.type == "private":
        return True
    
    return False


# Get MTProto Proxies
def Get_MTProto_Proxy(length: int) -> tuple:
    """
    Function to get MTProto proxies from API
    You can get up to 20 proxies at once (If available)

    Parameter:
        Length of proxies (How much you want)
    """

    # Error handling
    try:

        # Base URL for target API
        url = "https://mtpro.xyz/api/?type=mtproto"

        # Fetch proxies from target URL
        result = requests.get(url, timeout=10).json()

        # Avoid getting more proxies if there are few
        # May user entered 50 in parameter for length
        # but we have just 20 proxies in index
        proxy_length = len(result)
        if length > proxy_length:
            length = proxy_length

        # Get random proxies from main result
        random_proxies = random.choices(result, k=length)

        # Set total results list and Add proxies
        results = []
        for proxy in random_proxies:
            results.append(
                [
                    proxy["host"],
                    proxy["port"],
                    proxy["secret"],
                    proxy["country"],
                    proxy["up"],
                    proxy["down"],
                    proxy["uptime"],
                    proxy["addTime"],
                    proxy["updateTime"],
                    proxy["ping"],
                ]
            )

        # Return True and results
        return True, results

    except:
        # Return False and error message
        return False, "Can not get proxies for now. Try again."


# Calculate X-time ago
def time_ago(timestamp: str) -> str:
    """
    Function to turn timestamp to X ago time

    Parameter:
        Timestamp
    """

    # Turn timestamp to integer
    TmSt = int(timestamp)

    # Get current time
    Crnt = datetime.datetime.now()

    # Format timestamp
    TdFr = Crnt - datetime.datetime.fromtimestamp(TmSt)

    # Get days and seconds from formatted time
    DaYs = TdFr.days
    ScNd = TdFr.seconds

    # Calculate the X time ago
    if DaYs > 0:
        FrmtEd = f"{DaYs} day(s) ago"
    elif ScNd >= 3600:
        hours = ScNd // 3600
        FrmtEd = f"{hours} hour(s) ago"
    elif ScNd >= 60:
        minutes = ScNd // 60
        FrmtEd = f"{minutes} minute(s) ago"
    else:
        FrmtEd = f"{ScNd} second(s) ago"

    # Return formatted time
    return FrmtEd