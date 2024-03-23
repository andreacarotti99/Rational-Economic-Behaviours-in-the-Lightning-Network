from src.ChannelGraph import ChannelGraph

BASE_PATH = "YOUR_BASE_PATH"
path = BASE_PATH + "PreferentialPayment/snapshots/cosimo_19jan2023_converted.json"
channel_graph = ChannelGraph(path)

src = "02f3d9e33a2de53e128ae1821f0cff02f7e8c9b6872d949f0ebb0c8e388bad82ac"
dst = "035f5236d7e6c6d16107c1f86e4514e6ccdd6b2c13c2abc1d7a83cd26ecb4c1d0e"
chid = "837974095501328385"

channel = channel_graph.get_channel(src, dst, chid)

print(channel)
