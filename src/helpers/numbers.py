def shorten_number(value):
    """
    Shorten a number to a more readable format.
    """

    try:
        value = int(value)
        if value >= 1_000_000_000_000:
            formatted_value = value/1_000_000_000_000
            suffix = 'T'
        elif value >= 1_000_000_000:
            formatted_value = value/1_000_000_000
            suffix = 'B'
        elif value >= 1_000_000:
            formatted_value = value/1_000_000
            suffix = 'M'
        elif value >= 1_000:
            formatted_value = value/1_000
            suffix = 'K'
        else:
            return str(value)
        
        formatted_value = round(formatted_value, 1)

        if formatted_value.is_integer():
            return '{:.0f}{}'.format(formatted_value, suffix)
        else:
            return '{:.1f}{}'.format(formatted_value, suffix)
    except (ValueError, TypeError):
        return str(value)