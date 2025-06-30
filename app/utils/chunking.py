def split_list_chunks(data_list, chunk_size=500):
    for i in range(0, len(data_list), chunk_size):
        yield data_list[i:i + chunk_size]

def split_text_chunks(text, chunk_size=50000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
