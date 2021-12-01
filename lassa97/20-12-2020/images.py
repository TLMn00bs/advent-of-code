import re

def parse_data(file):
    images = {}

    image_id = int(re.search(r'\d+', file[0]).group())
    image = []

    for line in file:
        if (line.startswith('Tile')):
            image_id = int(re.search(r'\d+', line).group())
            image = []
        elif (line != ''):
            image.append(line)
        else:
            images[image_id] = image

    images[image_id] = image

    return images

def get_borders(images):
    borders = {}

    for index, image in images.items():
        top_border = image[0]
        reversed_top_border = top_border[::-1]
        bottom_border = image[-1]
        reversed_bottom_border = bottom_border[::-1]

        left_border = ''
        right_border = ''
        for i in range(len(image)):
            left_border += image[i][0]
            right_border += image[i][len(image) - 1]

        reversed_left_border = left_border[::-1]
        reversed_right_border = right_border[::-1]

        if (top_border in borders.keys()):
            borders[top_border] += 1
        elif (reversed_top_border in borders.keys()):
            borders[reversed_top_border] += 1
        else:
            borders[top_border] = 1

        if (bottom_border in borders.keys()):
            borders[bottom_border] += 1
        elif (reversed_bottom_border in borders.keys()):
            borders[reversed_bottom_border] += 1
        else:
            borders[bottom_border] = 1
        
        if (left_border in borders.keys()):
            borders[left_border] += 1
        elif (reversed_left_border in borders.keys()):
            borders[reversed_left_border] += 1
        else:
            borders[left_border] = 1

        if (right_border in borders.keys()):
            borders[right_border] += 1
        elif (reversed_right_border in borders.keys()):
            borders[reversed_right_border] += 1
        else:
            borders[right_border] = 1
    
    return borders

def get_unique_borders(borders):
    unique_borders = []

    for border, count in borders.items():
        if (count == 1):
            unique_borders.append(border)

    return unique_borders

def search_1(unique_borders, images):
    corner_ids = []
    total = 1

    for border in unique_borders:
        for index, image in images.items():
            top_border = image[0]
            bottom_border = image[-1]
            left_border = ''
            right_border = ''
        
            for i in range(len(image)):
                left_border += image[i][0]
                right_border += image[i][len(image) - 1]

            if (border in [top_border, bottom_border, left_border, right_border]):
                if (index in corner_ids):
                    total *= index
                corner_ids.append(index)
                break

    return total


file = open('input.txt').read().splitlines()

images = parse_data(file)

borders = get_borders(images)

unique_borders = get_unique_borders(borders)

total = search_1(unique_borders, images)

print('The product of the corner IDs is: {TOTAL}'.format(TOTAL=total))

