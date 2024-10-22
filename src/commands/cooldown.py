import time
from collections import defaultdict
import logging
from config import COOLDOWN_TIME

last_response_time = defaultdict(float)

def is_on_cooldown(user_id: int) -> bool:
    on_cooldown = time.time() - last_response_time[user_id] < COOLDOWN_TIME
    logging.debug(f"User {user_id} is {'on' if on_cooldown else 'not on'} cooldown.")
    return on_cooldown

def update_cooldown(user_id: int) -> None:
    last_response_time[user_id] = time.time()
    logging.debug(f"Updated cooldown for user {user_id}.")
