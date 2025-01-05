def non_negative(number):
    if isinstance(number, str):
        try:
            # Try casting to int first
            number = int(number)
        except ValueError:
            try:
                # If int fails, try casting to float
                number = float(number)
            except ValueError:
                return False

    return number >= 0