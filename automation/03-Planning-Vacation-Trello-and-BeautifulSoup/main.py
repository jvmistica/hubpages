from modules.scraper import get_holidays, get_free_time
from modules.trello import create_board, create_list, create_card


area = "malaysia"
holidays = get_holidays(area)
long_weekends, all_free_time = get_free_time(holidays)

board_id = create_board("Holidays")

# Spread the vacation days across different Trello boards
first_four = create_list(board_id, "Jan - Apr", 1)
second_four = create_list(board_id, "May - Aug", 2)
third_four = create_list(board_id, "Sep - Dec", 3)

for from_date, to_date in long_weekends:
    vacation_days = (to_date - from_date).days + 1
    start = from_date.strftime("%m/%d")
    end = to_date.strftime("%m/%d")
    content = f"{vacation_days} days: {start} - {end}"

    if from_date.month <= 4:
        create_card(first_four, content)
    elif 5 <= from_date.month <= 8:
        create_card(second_four, content)
    else:
        create_card(third_four, content)

# Get suggestions on when to file vacation leaves
suggestions = []
for ndx, free_time in enumerate(all_free_time):
    from_date, to_date = free_time
    try:
        leaves = (all_free_time[ndx + 1][0] - to_date).days
        if leaves <= 5:
            vacation_days = (to_date - from_date).days + (all_free_time[ndx + 1][1] - all_free_time[ndx + 1][0]).days + leaves
            if vacation_days - leaves > 1:
                suggestions.append((vacation_days + 1, leaves, from_date.strftime("%m/%d"), \
                                    all_free_time[ndx + 1][1].strftime("%m/%d")))
    except IndexError:
        pass

suggestions.sort(reverse=True)
suggestions_list = create_list(board_id, "Suggested Leaves", 4)
for suggestion in suggestions:
    create_card(suggestions_list, "{0} days: {2} - {3} | {1} VL".format(*suggestion))
