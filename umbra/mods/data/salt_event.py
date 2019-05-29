'''
Take the data from a salt event stream and prepare it to be loaded into an
AI/ML model
'''


async def prepare(hub, pipe, inbound):
    '''
    Takes the raw data loaded from a salt event stream, this data is transformed
    into data that can be loaded in to the model and we save the string map dicts
    for future translation
    '''
    ret = []
    d_count = 0
    for event in inbound:
        if not hub.P[pipe]['tmap_populated']:
            for key in event['data']:
                if not isinstance(event['data'][key], str):
                    # TODO: Make this able to handle mroe than just strings
                    continue
                if key == '_stamp':
                    continue
                hub.P[pipe]['tmap'].append(key)
            hub.P[pipe]['tmap_populated'] = True
        x = [0 for n in hub.P[pipe]['tmap']]
        for key in event['data']:
            if not isinstance(event['data'][key], str):
                # TODO: Be able to handle more than just strings here
                continue
            if key == '_stamp':
                continue
            x[hub.P[pipe]['tmap'].index(key)] = hub.data.init.word_map(
                event['data'][key],
                hub.P[pipe]['words'],
                hub.P[pipe]['r_words'])
        ret.append(x)
    return ret


async def refine(hub, pipe, data, preds):
    '''
    Take the data from the model and refine it back into salt event format
    '''
    dmap = hub.P[pipe]
    rets = []
    for ind in range(len(preds)):
        if not preds[ind]:
            continue
        ret = {}
        for t_ind in range(len(dmap['tmap'])):
            ret[dmap['tmap'][t_ind]] = dmap['r_words'][data[ind][t_ind]]
        rets.append(ret)
    return rets