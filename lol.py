import bisect
import copy

def figureToLines(figure):
    res = []
    for i in figure:
        res+=i.lines
    return res

def det(a, b, c):
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])
    
def intersect(line1, line2):
    return det(line1[0], line2[0], line2[1]) != det(line1[1], line2[0], line2[1]) \
            and det(line1[0], line1[1], line2[0]) != det(line1[0], line1[1], line2[1])

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


def intersectionExists(segments):
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

# jezeli seg1 przecina seg2, to dodaje przecięcie do event list 
# oraz do intersections
def addIntersection(eventList, intersections, segments, broom, idx1, idx2):
    b1, b2 = broom[idx1][0], broom[idx2][0]
    line1, line2 = segments[b1], segments[b2]
    intersection = intersectionPoint(line1, line2)
    b1, b2 = min(b1, b2), max(b1, b2)
    # dodanie do intersections
    if [b1, b2] not in intersections:
        intersections.append([b1, b2])
        # dodanie do eventList po najmniejszej wspl x-owej
        insertIndex = bisect.bisect(eventList, intersection[0], key= lambda x: x[1][0])
        eventList.insert(insertIndex, [-1, intersection, b1, b2])


def detectIntersections(segments):
    # przechowuje punkty w liście zawierającej punkty [idx, [p.x, p.y]]
    # jezeli idx = -1, to jest to punkt przecięcia oraz zawiera indeksy przecinających się odcinków
    points = [[i, point] for i, line in enumerate(segments) for point in line]
    active = [False for _ in range(len(segments))]
    intersections = []

    # lista zawierająca indeksy i wspl x-owe odcinków aktywnych
    broom = []

    # sortowanie punktów po x-owej współrzędnej
    points.sort(key=lambda x: x[1][0])

    # jako, że punkt przecięcia na pewno będzie znajdował się po prawej stronie od 
    # początku odcinka, to nie musimy się martwić o warunek pętli while
    while points:

        info = points.pop(0)
        currIndex = info[0]
        currPoint = info[1]

        # jezeli trafiliśmy na punkt przecięcia
        if currIndex == -1:            
            index = bisect.bisect_left(broom, currPoint[1], key=lambda x: yLine(x[1], x[2], currPoint[0]))
            flag1 = flag2 = False
            for i in range(-2, 2):
                if index + i >=0 and not flag1 and broom[index + i][0] == info[2]:
                    index1 = index + i
                    flag1 = True
                if index + i >=0 and not flag2 and broom[index + i][0] == info[3]:
                    index2 = index + i
                    flag2 = True
                if flag1 and flag2:
                    break

            broom[index1], broom[index2] = broom[index2], broom[index1]

            # sprawdzamy przeciecia z nowymi odcinkam:
            index1, index2 = min(index1, index2), max(index1, index2)
            if index1 - 1 >= 0 and intersect(segments[broom[index1 - 1][0]], segments[broom[index1][0]]):
                addIntersection(points, intersections, segments, broom, index1, index1 - 1)
            
            if index2 + 1 < len(broom) and intersect(segments[broom[index2][0]], segments[broom[index2 + 1][0]]):
                addIntersection(points, intersections, segments, broom, index2, index2 + 1)

        # jezeli currIndex nie jest w miotle
        elif not active[currIndex]:
            active[currIndex] = True
            # znalezienie miejsca w miotle oraz obliczenie wspl kierunkowego i wyrazu wolnego
            index = bisect.bisect(broom, currPoint[1], key=lambda x: yLine(x[1], x[2], currPoint[0]))
            lineConstants = calculateLineConstants(segments[currIndex])
            broom.insert(index, [currIndex, lineConstants[0], lineConstants[1]])

            # czy przecina się z sąsiadem nad
            if index + 1 < len(broom) and intersect(segments[broom[index][0]], segments[broom[index + 1][0]]):
                addIntersection(points, intersections, segments, broom, index, index + 1)
                
            # czy przecina sie z sąsiadem pod
            if index - 1 >= 0 and intersect(segments[broom[index][0]], segments[broom[index - 1][0]]):
                addIntersection(points, intersections, segments, broom, index, index - 1)
        
        # jezeli jest to prawy koniec odcinka, to musimy go usunac z miotły
        else:
            active[currIndex] = False
            # znalezienie indeksu punktu, który chcemy usunąć
            index = bisect.bisect_left(broom, currPoint[1], key=lambda x: yLine(x[1], x[2], currPoint[0]))
            for i in range(-1, 2):
                if broom[index + i][0] == currIndex:
                    index = index + i
                    break 

            if index + 1 < len(broom) and index - 1 >= 0 and intersect(segments[broom[index - 1][0]], segments[broom[index + 1][0]]):
                
                addIntersection(points, intersections, segments, broom, index - 1, index + 1)
                
            broom.pop(index)

    return intersections       

def getIntersectionPoints(lines):
    res = []
    for (idx1, idx2) in detectIntersections(lines):
        res.append(intersectionPoint(lines[idx1], lines[idx2]))
    return res     