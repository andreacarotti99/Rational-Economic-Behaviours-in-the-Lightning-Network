import logging
from src.Channel import Channel
from src.ChannelGraph import ChannelGraph
from src.equilibrium_game.utils.obtain_capacity_from_channels import obtain_capacity_from_channels


def open_given_channels(G: ChannelGraph, target_node: str, channels_to_open: [Channel]):
    for i in range(len(channels_to_open)):
        G.create_channel_bilateral(target_node,
                                   channels_to_open[i].dest,
                                   channels_to_open[i].is_announced,
                                   channels_to_open[i].capacity,
                                   channels_to_open[i].flags,
                                   channels_to_open[i].is_active,
                                   channels_to_open[i].last_update,
                                   channels_to_open[i].base_fee,
                                   channels_to_open[i].ppm,
                                   channels_to_open[i].cltv_delta,
                                   channels_to_open[i].htlc_min_msat,
                                   channels_to_open[i].htlc_max_msat,
                                   channels_to_open[i].short_channel_id,
                                   opposite_fee_mean=True)
        # print(f'|__KEEPING ch with {channels_to_open[i].dest[0:5]}, capacity: {channels_to_open[i].capacity} ch_id: {channels_to_open[i].short_channel_id}')
        # logging.debug('open ch with %s capacity: %d', channels_to_open[i].dest, channels_to_open[i].capacity)
        # obtain_capacity_from_channels(G=G, node=channels_to_open[i].dest, amt=channels_to_open[i].capacity // 2)
    return True
