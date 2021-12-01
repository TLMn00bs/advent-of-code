def search_1(timestamp, lines):
    time = timestamp
    buses = list(filter((1).__ne__, lines))
    while True:
        for bus in buses:
            if (time % bus) == 0:
                return (time - timestamp), bus
        time += 1

def search_2(lines):
    time = 0
    offset = lines[0]
    for pos, line in enumerate(lines):
        if (pos == 0):
            continue
        if (line != 1):
            while ((time + pos) % line != 0):
                time += offset
            offset *= line

    return time



file = open('input.txt').read().splitlines()
timestamp, buses = int(file[0]), file[1].split(',')

lines = []

for bus in buses:
    lines.append(int(bus.replace('x', '1')))

time, bus = search_1(timestamp, lines)
print('Total: {TOTAL}'.format(TOTAL=time * bus))

time = search_2(lines)

print('Time: {TIME}'.format(TIME=time))