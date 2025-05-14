import exception

def _region(master_data, regions):
    if regions == "*":
        return master_data
    else:
        for region in regions:
            if region not in master_data['region_id'].unique():
                raise exception.RegionNotAvailable(region)
        return master_data[master_data['region_id'].isin(regions)]

def _topic(master_data, topics):
    if topics == "*":
        return master_data
    else: 
        for topic in topics:
            if topic not in master_data['topic'].unique():
                raise exception.TopicNotAvailable(topic)
        return master_data[master_data['topic'].isin(topics)]

def _source(master_data, sources):
    if sources == "*":
        return master_data
    else:
        for source in sources:
            if source not in master_data['source'].unique():
                raise exception.SourceNotAvailable(source)
        return master_data[master_data['source'].isin(sources)]