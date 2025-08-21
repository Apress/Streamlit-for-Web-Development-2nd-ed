import time
from typing import Iterable

def yield_text(text: str) -> Iterable:
   for word in text.split(' '):
       yield  word + ' '
       time.sleep(0.01)
