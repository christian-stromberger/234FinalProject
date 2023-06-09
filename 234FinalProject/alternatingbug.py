from bugutils import *
import random


def alter_bug(polygons, start, end):
    # algorithm which implements split bug
    # start by moving toward the goal until we hit an obstacle
    segments = generate_segments(polygons)
    Odd = True
    path = []
    path.append(start)

    # check intersection with segment start/end
    midline = (start,end)
    midline_intersections = []
    midline_seggs = []
    for seg in segments:
        if SegmentCrossSegment(midline, seg):
            midline_intersections.append(intersection(midline, seg))
            midline_seggs.append(seg)
    
    # now find closest intersection point to start and corresponding segment
    min_dist = 100000
    min_point = None
    min_seg = None
    
    for i in range(0, len(midline_intersections)):
        dist = distance(midline_intersections[i], start)
        if dist < min_dist:
            min_dist = dist
            min_point = midline_intersections[i]
            min_seg = midline_seggs[i]
    
    # now we know that first step of our path
    path.append(min_point)

    # figure out the current polygon
    for polygon in polygons:
            if min_seg[0] in polygon and min_seg[1] in polygon:
                curr_polygon = polygon


    # need to check if min_seg[0] or min_seg[1] is the closest point to the start
    # if(distance(min_seg[0], start) < distance(min_seg[1], start)):
    #     path.append(min_seg[0])
    #     index = curr_polygon.index(min_seg[0])
    # else:
    #     path.append(min_seg[1])
    #     index = curr_polygon.index(min_seg[1])

    # path.append(min_seg[0])

    # index = curr_polygon.index(min_seg[0])
    
    # generate a random number between 0 and 1
    # if it is less than 0.5, we want to go counterclockwise
    # otherwise, we want to go clockwise
    # if(random.random() < 0.5):

    if(Odd):
        index = curr_polygon.index(min_seg[0])
        path.append(min_seg[0])
        # now we want to traverse around the polygon until we hit the midline
        for i in range(0, len(curr_polygon)+1):
            # if the segment from the last point to the current point intersects the midline
            if(SegmentCrossSegment((path[-1], curr_polygon[index]),(midline))):
                p = intersection((path[-1], curr_polygon[index]),(midline))
                path.append(p)
                break
            path.append(curr_polygon[index])
            index = (index - 1) % len(curr_polygon)
            # print("index: " + str(index))
    else:
        index = curr_polygon.index(min_seg[1])
        
        # now we want to traverse around the polygon until we hit the midline
        for i in range(0, len(curr_polygon)+1):
            # if the segment from the last point to the current point intersects the midline
            if(SegmentCrossSegment((path[-1], curr_polygon[index]),(midline))):
                p = intersection((path[-1], curr_polygon[index]),(midline))
                path.append(p)
                break
            path.append(curr_polygon[index])
            index = (index + 1) % len(curr_polygon)


        # print("index: " + str(index))
    
    # # print distances 
    # print("dis1: " + str(dis1))
    # print("dis2: " + str(dis2))
    # # path = old_path
    # if(dis1 < dis2):
    #     index = curr_polygon.index(min_seg[0])
    #     # now we want to traverse around the polygon until we hit the midline
    #     for i in range(0, len(curr_polygon)+1):
    #         # if the segment from the last point to the current point intersects the midline
    #         if(SegmentCrossSegment((curr_polygon[index], curr_polygon[index-1]),(midline))):
    #             p = intersection((curr_polygon[index], curr_polygon[index-1]),(midline))
    #             path.append(p)
    #             break
    #         path.append(curr_polygon[index])
    #         index = (index - 1) % len(curr_polygon)
    #         # print("index: " + str(index))
    # else:
    #     index = curr_polygon.index(min_seg[1])
    #     for i in range(0, len(curr_polygon)+1):
    #         index = (index + 1) % len(curr_polygon)
    #         if(SegmentCrossSegment((curr_polygon[index-1], curr_polygon[index]),(midline))):
    #             p = intersection((curr_polygon[index-1], curr_polygon[index]),(midline))
    #             path.append(p)
    #             break
    #         path.append(curr_polygon[index])
    #         index = (index + 1) % len(curr_polygon)
    #         # print("index: " + str(index))

    # this is a left bug
    # last_branch_point = path[-1]
    # now we want to go into a loop until we can see the end point
    print(path[-1])
    j = 0
    print("about to enter loop")
    while(j < 10):
        print("in loop")
        curr_point = path[-1]
        curr_point = [curr_point[0]+.01, curr_point[1]]
        midline = (curr_point, end)
            # check intersection with segment start/end
        midline_intersections = []
        midline_seggs = []
        for seg in segments:
            if SegmentCrossSegment(midline, seg):
                midline_intersections.append(intersection(midline, seg))
                midline_seggs.append(seg)
        
        if(len(midline_intersections) == 0):
            path.append(end)
            return path

        # now find closest intersection point to start and corresponding segment
        min_dist = 100000
        min_point = None
        min_seg = None
        
        for i in range(0, len(midline_intersections)):
            dist = distance(midline_intersections[i], start)
            if dist < min_dist:
                min_dist = dist
                min_point = midline_intersections[i]
                min_seg = midline_seggs[i]
        
        # now we know that first step of our path
        path.append(min_point)

        # figure out the current polygon
        for polygon in polygons:
                if min_seg[0] in polygon and min_seg[1] in polygon:
                    curr_polygon = polygon


        # need to check if min_seg[0] or min_seg[1] is the closest point to the start
        # if(distance(min_seg[0], start) < distance(min_seg[1], start)):
        #     path.append(min_seg[0])
        #     index = curr_polygon.index(min_seg[0])
        # else:
        #     path.append(min_seg[1])
        #     index = curr_polygon.index(min_seg[1])
        Odd = not Odd
        dis1 = 0
        if(Odd):
            index = curr_polygon.index(min_seg[0])
            path.append(min_seg[0])
            # now we want to traverse around the polygon until we hit the midline
            for i in range(0, len(curr_polygon)+1):
                # if the segment from the last point to the current point intersects the midline
                if(SegmentCrossSegment((path[-1], curr_polygon[index]),(midline))):
                    p = intersection((path[-1], curr_polygon[index]),(midline))
                    path.append(p)
                    break
                path.append(curr_polygon[index])
                index = (index - 1) % len(curr_polygon)
                # print("index: " + str(index))
        else:
            path.append(min_seg[1])

            index = curr_polygon.index(min_seg[1])
            
            # now we want to traverse around the polygon until we hit the midline
            for i in range(0, len(curr_polygon)+1):
                # if the segment from the last point to the current point intersects the midline
                if(SegmentCrossSegment((path[-1], curr_polygon[index]),(midline))):
                    p = intersection((path[-1], curr_polygon[index]),(midline))
                    path.append(p)
                    break
                path.append(curr_polygon[index])
                index = (index + 1) % len(curr_polygon)

        last_branch_point = path[-1]

        

        j = j + 1
        
    return path