import random
from src.Channel import Channel
from src.ChannelGraph import ChannelGraph
from src.continuative_game.changing_both.utils.generate_custom_exponential import generate_custom_exponential
from src.equilibrium_game.utils.open_all_given_channels_randomly import get_nodes_to_connect_to


def open_given_channels_with_new_fee(G: ChannelGraph, target_node: str, channels_to_open: [Channel], opening_strategy, max_fee) -> [Channel]:
    opened_channels = []
    all_nodes = set(G.network.nodes) - {target_node}
    for channel in channels_to_open:
        if opening_strategy == "SINGLE_FUNDED":
            eligible_nodes = get_nodes_to_connect_to(G, channel, all_nodes)
            selected_node = random.choice(eligible_nodes)

            channel_created_chid = G.create_channel_bilateral(target_node, selected_node, channel.is_announced,
                                                              channel.capacity // 2,
                                                              channel.flags, channel.is_active, channel.last_update,
                                                              channel.base_fee,
                                                              channel.ppm,
                                                              channel.cltv_delta, channel.htlc_min_msat,
                                                              channel.htlc_max_msat,
                                                              str(channel.short_channel_id) + '_2',
                                                              opposite_fee_mean=True)



            new_fee_value = generate_custom_exponential(scale=50, upper_limit=max_fee)

            if G.edit_channel(target_node, selected_node, channel_created_chid, 'fee', new_fee_value):
                opened_channels.append(G.get_channel(target_node, selected_node, channel_created_chid))
            else:
                print(f'Channel from {target_node[0:5]} --> {selected_node[0:5]} - ID: {channel_created_chid} not edited')
    return opened_channels
