from .channel import ChannelMiddleware
from loader import dp
print("mid")
if __name__=="middleware":
    print("d")
    dp.middleware.setup(ChannelMiddleware())