#!/usr/bin/env python3

input = [[elem for elem in line.strip()] for line in open("input").readlines()]

def closest_neighbours(x,y,arr):
    adjacents = ""
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if x+i>=0 and y+j>=0:
                try:
                    if i==j==0: continue
                    adjacents+=arr[x+i][y+j]
                except IndexError:
                    pass
    return adjacents

def visible_neighbours(x,y,arr):
    adjacents = ""
    for v in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            try:
                l = 1
                while arr[ x+l*v[0] ][ y+l*v[1] ]==".":
                    l+=1
                if x+l*v[0]>=0 and y+l*v[1]>=0:
                    adjacents+=arr[ x+l*v[0] ][ y+l*v[1] ]
            except IndexError:
                pass
    return adjacents

def next_state(arr, min_occupied_seats_to_become_empty=4, first_visible_seat=False):
    new_arr = [ r[:] for r in arr ] # copy array (list of lists)
    neighbours = visible_neighbours if first_visible_seat else closest_neighbours
    for r,row in enumerate(arr):
        for c,column in enumerate(row):
            if arr[r][c]=="L" and neighbours(r,c,arr).count("#")==0:
                new_arr[r][c]="#"
            elif arr[r][c]=="#" and neighbours(r,c,arr).count("#")>=min_occupied_seats_to_become_empty:
                new_arr[r][c]="L"
    return new_arr



prev_state = input
curr_state = next_state(input)

while prev_state!=curr_state:
    prev_state = curr_state
    curr_state = next_state(prev_state)

print(sum(r.count('#') for r in curr_state))



prev_state = input
curr_state = next_state(input, 5, first_visible_seat=True)

while prev_state!=curr_state:
    prev_state = curr_state
    curr_state = next_state(prev_state, 5, first_visible_seat=True)

print(sum(r.count('#') for r in curr_state))
