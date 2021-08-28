def paginator(data, current_page, limit):
    return data[limit * (current_page - 1): current_page * limit]
