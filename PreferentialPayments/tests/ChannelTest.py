from src.ChannelGraph import ChannelGraph
import path

channel_graph = ChannelGraph(snapshot_path)

src = "035e4ff418fc8b5554c5d9eea66396c227bd429a3251c8cbc711002ba215bfc226"
dst = "03551c1ea860c957949a642e66943179692cd874a5a6d23948edf59ef579a0532f"
chid = "771400865411039232"

print(channel_graph.get_channel(src, dst, chid))

