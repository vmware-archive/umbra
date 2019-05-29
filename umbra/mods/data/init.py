async def run(hub, flows):
    '''
    Take the flows that we want to run and start monitoring the respective data pipelines
    '''
    for pipe in flows:
        hub.tools.loop.ensure_future('data.init.flow', pipe, flows[pipe])


async def flow(hub, pipe, config):
    '''
    Execute the data processing for the given pipe
    '''
    mod = config['data']
    if pipe not in hub.P:
        hub.P[pipe] = {
            'tmap': [],
            'words': {},
            'r_words': {},
            'data': [],
            'tmap_populated': False,
            'first': False}
    # TODO: Make the flow stop if the ingress gets exhausted
    while True:
        data = await hub.UP[pipe]['data'].get()
        cond = await hub.tools.ref.last(f'data.{mod}.prepare')(pipe, data)
        await hub.UP[pipe]['model'].put(cond)


def word_map(hub, word, words, r_words):
    '''
    Take a word and build it into the dict map. Modify the words dicts in place and then
    return the int that represents the given word
    '''
    if word in words:
        return words[word]
    num = len(words) + 1
    words[word] = num
    r_words[num] = word
    return num