from datetime import datetime

def to_dd_mm_yyyy(date_str):
    try:
        if "-" not in date_str:
            raise ValueError("Unsupported date format")

        # Try YYYY-MM-DD
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # If that fails, try DD-MM-YYYY
            dt = datetime.strptime(date_str, "%d-%m-%Y")

        return dt.strftime("%d-%m-%Y")

    except Exception as e:
        print(f"Invalid date: {date_str} ({e})")
        return None