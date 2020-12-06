def get_seatID(line):
    row = line[:-3]
    column = line[-3:]

    #row = row.replace("F", "0").replace("B", "1")
    #column = column.replace("L", "0").replace("R", "1")

    bin_row = ""
    bin_column = ""

    for char in row:
        if char == "F":
            bin_row += "0"
        else:
            bin_row += "1"

    for char in column:
        if char == "L":
            bin_column += "0"
        else:
            bin_column += "1"


    row = int(bin_row, 2)
    column = int(bin_column, 2)
    seat_id = row * 8 + column
    return seat_id

with open("input.txt") as file:
    seats_ids = []
    for line in file:
        seat_id = get_seatID(line.rstrip())
        seats_ids.append(seat_id)

    print("Max Seat ID: {MAX_ID}".format(MAX_ID=int(max(seats_ids))))

    for seat in range(min(seats_ids), max(seats_ids) + 1):
        if seat not in seats_ids:
            print("Your seat ID: {SEAT_ID}".format(SEAT_ID=seat))