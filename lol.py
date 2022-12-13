import bisect
import copy

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
    
def intersect(line1, line2):
    return ccw(line1[0], line2[0], line2[1]) != ccw(line1[1], line2[0], line2[1]) \
            and ccw(line1[0], line1[1], line2[0]) != ccw(line1[0], line1[1], line2[1])

def calculateLineConstants(line):
    a = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0])
    b = (line[0][0] * line[1][1] - line[0][1] * line[1][0]) / (line[0][0] - line[1][0])
    return [a, b]

def intersectionPoint(line1, line2):
    const1 = calculateLineConstants(line1)
    const2 = calculateLineConstants(line2)

    x = - (const1[1] - const2[1]) / (const1[0] - const2[0])
    y = x*const1[0] + const1[1]

    return [x, y]

def yLine(a, b, x):
    return a*x + b


def intersectionExist(segments):
    # points przechowuje punkty w postaci [idx, [p.x, p.y]]
    points = [[i, point] for i, line in enumerate(segments) for point in line]
    # active[i] = true, jezeli i zawiera sie w broom
    active = [False for _ in range(len(segments))]
    # stan miotły, [idx, a, b], gdzie a i b to odpowiednio wspl kierunkowy i wyraz wolny
    broom = []

    # sortuje po x-owych
    points.sort(key=lambda x: x[1][0])

    # dla kazdego punktu
    for point in points:
        
        currIndex, currPoint= point[0], point[1]

        # jezeli currIndex nie jest w miotle
        if not active[currIndex]:
            active[currIndex] = True
            # znalezienie miejsca w miotle oraz obliczenie wspl kierunkowego i wyrazu wolnego
            index = bisect.bisect(broom, currPoint[1], key=lambda x: yLine(x[1], x[2], currPoint[0]))
            lineConstants = calculateLineConstants(segments[currIndex])
            broom.insert(index, [currIndex, lineConstants[0], lineConstants[1]])

            # czy przecina się z sąsiadem nad
            if index + 1 < len(broom) and intersect(segments[broom[index][0]], segments[broom[index + 1][0]]):
                return True
            
            # czy przecina sie z sąsiadem pod
            if index - 1 >= 0 and intersect(segments[broom[index][0]], segments[broom[index - 1][0]]):
                return True
        
        # jezeli jest to koncówka, to musimy go usunac z broom
        else:
            active[currIndex] = False
            # znalezienie indeksu punktu, który chcemy usunąć
            index = bisect.bisect_left(broom, currPoint[1], key=lambda x: yLine(x[1], x[2], currPoint[0]))
            for i in range(-1, 2):
                if broom[index + i][0] == currIndex:
                    index = index + i
                    break 

            if index + 1 < len(broom) and index - 1 >= 0 and \
                intersect(segments[broom[index - 1][0]], segments[broom[index + 1][0]]):
                
                return True
                
            broom.pop(index)
    return False