import json
from instagrapi import Client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def follow_user(account_username, account_password, username_to_follow):
    try:
        cl = Client()
        cl.login(account_username, account_password)
        logger.info(f"Logged in as {account_username}")
        
        user_id_to_follow = cl.user_id_from_username(username_to_follow)
        cl.user_follow(user_id_to_follow)
        logger.info(f"Now following {username_to_follow}")
    except Exception as e:
        logger.error(f"Error with account {account_username}: {e}")
