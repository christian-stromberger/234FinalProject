# BUGS BUGS BUGS BUGS BUGS!!!!!
from planarutils import *
import math
import random

def tunnel_bug(polygons, start, end):
    return [start,end]

def bug0(polygons, start, end):
    x0 = start
    # start by moving in positive x until we hit an obstacle
    segments = generate_segments(polygons)

    path = [start]
    curr_point = path[-1]
    while curr_point != end:
        #find the segments that intersect with ideal path
        midline = (curr_point, end)
        intersections = []
        intersecting_segs = []
        for seg in segments:
            if SegmentCrossSegment(midline, seg):
                intersections.append(intersection(midline, seg))
                intersecting_segs.append(seg)
        
        #if we can see the goal directly just go to it
        if len(intersections) == 0:
            path.append(end)
            curr_point = end
            continue

        # now find closest intersection point to start and corresponding segment
        min_dist = 100000
        min_point = None
        min_seg = None
        print(intersecting_segs)
        for i in range(0, len(intersections)):
            dist = distance(intersections[i], curr_point)
            if dist < min_dist:
                min_dist = dist
                min_point = intersections[i]
                min_seg = intersecting_segs[i]

        path.append(min_point)

        # now we have the closest intersection point and the corresponding segment
        # now we need to figure out which polygon that segment belongs to
        for polygon in polygons:
            if min_seg[0] in polygon and min_seg[1] in polygon:
                curr_polygon = polygon
        print("curr_polygon", curr_polygon)
        print("minseggs", min_seg)

        path.append(min_seg[1])

        index = curr_polygon.index(min_seg[1])

        curr_point = path[-1]

        print("generated segments for curr polygon:", generate_segments(curr_polygon))
        
        print("yay")
        cant_move_on = True

        while cant_move_on:
            #what segments to loop over
            #see if any intersect with current point and goal
            #if so, add next segment to path and then try again
            #if not, break this loop
            curr_segments = generate_segments(curr_polygon)
            can_go_next = True
            for i in range(0,len(curr_segments)):
                if SegmentCrossSegment(((curr_point[0]+0.01,curr_point[1]), end),(curr_segments[i-1], curr_segments[i])):
                    can_go_next = False
            cant_move_on = not can_go_next

            if cant_move_on:
                index = index + 1
                if index == len(curr_polygon):
                    index = 0
                next_point = curr_polygon[index]
                path.append(next_point)
                curr_point = next_point

    return(path)


def bug1(polygons, start, end):
    # algorithm which implements bug 1
    # start by moving toward the goal until we hit an obstacle
    segments = generate_segments(polygons)
    
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

    # now figure out which polygon we are on and trace it
    for polygon in polygons:
            if min_seg[0] in polygon and min_seg[1] in polygon:
                curr_polygon = polygon
    
    # this is a left bug

    # find the closest point on the polygon to the intersection point min_point
    dis = 10000
    for i in range(0, len(curr_polygon)):
        if distance(min_point, curr_polygon[i]) < dis:
            dis = distance(min_point, curr_polygon[i])
            c_p = curr_polygon[i]

    index = curr_polygon.index(c_p)

    
    # now we want to go around the entire polygon and find the closest point to the goal
    # first add going around the polygon to the path
    for i in range(0, len(curr_polygon)+1):
        path.append(curr_polygon[index])
        index = (index + 1) % len(curr_polygon)


    # now find the closest point on the polygon to the goal
    min_dist, close_point, seg = closest_point_to_polygon(curr_polygon, end)
    print(close_point)
    # find the closest point on the polygon to the exit point close_point
    
    # dis = 10000
    # for i in range(0, len(curr_polygon)):
    #     if distance(close_point, curr_polygon[i]) < dis:
    #         dis = distance(close_point, curr_polygon[i])
    #         c_p = curr_polygon[i]

    # index2 = curr_polygon.index(c_p)

    # while index != index2:
    #     path.append(curr_polygon[index])
    #     index = (index + 1) % len(curr_polygon)
    print(dis)
    print(seg)

    while True:
        if(curr_polygon[index][0]==seg[1][0] and curr_polygon[index][1]==seg[1][1]):
            break
        path.append(curr_polygon[index])
        index = (index + 1) % len(curr_polygon)


    # for i in range(0, abs(index2-index)):
    #     path.append(curr_polygon[index])
    #     index = (index + 1) % len(curr_polygon)
    
    # now add the path to the closest point on the polygon
    # for now I am just going to add the point to the path

    path.append(close_point)

    # now we want to loop this until midline_intersections is empty
    while len(midline_intersections) > 0:
        curr_point = path[-1]
        curr_point = (curr_point[0]+0.01, curr_point[1])
        midline = (curr_point, end)
        intersections = []
        intersecting_segs = []
        for seg in segments:
            if SegmentCrossSegment(midline, seg):
                intersections.append(intersection(midline, seg))
                intersecting_segs.append(seg)
        
        #if we can see the goal directly just go to it
        if len(intersections) == 0:
            path.append(end)
            curr_point = end
            return path

        # now find closest intersection point to start and corresponding segment
        min_dist = 100000
        min_point = None
        min_seg = None
        # print(intersecting_segs)
        for i in range(0, len(intersections)):
            dist = distance(intersections[i], curr_point)
            if dist < min_dist:
                min_dist = dist
                min_point = intersections[i]
                min_seg = intersecting_segs[i]

        path.append(min_point)

        # now we have the closest intersection point and the corresponding segment
        # now we need to figure out which polygon that segment belongs to
        for polygon in polygons:
            if min_seg[0] in polygon and min_seg[1] in polygon:
                curr_polygon = polygon
        # print("curr_polygon", curr_polygon)
        # print("minseggs", min_seg)

        # find the closest point on the polygon to the intersection point min_point
        dis = 10000
        for i in range(0, len(curr_polygon)):
            if distance(min_point, curr_polygon[i]) < dis:
                dis = distance(min_point, curr_polygon[i])
                c_p = curr_polygon[i]

        index = curr_polygon.index(c_p)

        
        # now we want to go around the entire polygon and find the closest point to the goal
        # first add going around the polygon to the path
        for i in range(0, len(curr_polygon)+1):
            path.append(curr_polygon[index])
            index = (index + 1) % len(curr_polygon)

        
        # now find the closest point on the polygon to the goal
        min_dist, close_point, seg = closest_point_to_polygon(curr_polygon, end)
        # find the closest point on the polygon to the exit point close_point
        # dis = 10000
        # for i in range(0, len(curr_polygon)):
        #     if distance(close_point, curr_polygon[i]) < dis:
        #         dis = distance(close_point, curr_polygon[i])
        #         c_p = curr_polygon[i]

        # while True:
        #     path.append(curr_polygon[index])
        #     index = (index + 1) % len(curr_polygon)
        #     if(distance(curr_polygon[index], close_point) == dis):
        #         break


        while True:
            if(curr_polygon[index][0]==seg[1][0] and curr_polygon[index][1]==seg[1][1]):
                break
            path.append(curr_polygon[index])
            index = (index + 1) % len(curr_polygon)        

        

        # now add the path to the closest point on the polygon
        # for now I am just going to add the point to the path
            # find the closest point on the polygon to the exit point close_point
       
        

        path.append(close_point)



    return path
    
def bug2(polygons, start, end):
    # algorithm which implements bug 2
    # start by moving toward the goal until we hit an obstacle
    segments = generate_segments(polygons)
    
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

def bouncy_ball_bug(polygons, start, end):
    path = [start]
    heading = random.randint(0,359)
    curr_point = start
    segments = generate_segments(polygons)
    tries = 0
    while not can_see_end(polygons, curr_point, end):
        midline = (curr_point, (curr_point[0]+math.cos(heading)*14, curr_point[1]+math.sin(heading)*10))
        intersections = []
        intersecting_segs = []
        for seg in segments:
            if SegmentCrossSegment(midline, seg):
                intersections.append(intersection(midline, seg))
                intersecting_segs.append(seg)

        if len(intersections) == 0:
            path.append(midline[1])
            print("No intersections?!?")
            break

        # now find closest intersection point to start and corresponding segment
        min_dist = 100000
        min_point = None
        min_seg = None
        for i in range(0, len(intersections)):
            dist = distance(intersections[i], curr_point)
            if dist < min_dist:
                min_dist = dist
                min_point = intersections[i]
                min_seg = intersecting_segs[i]

        path.append(min_point)

        # now we have the closest intersection point and the corresponding segment
        # now we need to figure out which polygon that segment belongs to
        for polygon in polygons:
            if min_seg[0] in polygon and min_seg[1] in polygon:
                curr_polygon = polygon

        #bouncy ball bug shines here
        # |
        # V
        
        heading = get_bounce_angle(min_seg, heading)
        tries = tries + 1
        print(tries)
        if tries>10:
            print("sad mode")
            break

    #path.append(end)
    return path

def can_see_end(polygons, curr_point, end):
    segments = generate_segments(polygons)
    midline = (curr_point, end)
    for seg in segments:
        if SegmentCrossSegment(midline, seg):
            return False
    return True

def get_bounce_angle(segment, ball_angle):
    wall_start = segment[0]
    wall_end  = segment[1]
    dx = wall_end[0] - wall_start[0]
    dy = wall_end[1] - wall_start[1]

    if dx == 0:
        # Wall is vertical
        bounce_angle = math.pi/2 - ball_angle
    else:
        wall_slope = dy / dx
        
        # Calculate the angle of the wall
        wall_angle = math.atan(wall_slope)
        
        # Calculate the angle of incidence
        incidence_angle = ball_angle - wall_angle
        
        # Calculate the angle of reflection
        reflection_angle = -incidence_angle
        
        # Calculate the angle of the bounce
        bounce_angle = wall_angle + reflection_angle
        
    return bounce_angle
    

        


def closest_point_to_polygon(polygon, point):
    # find the closest point on a polygon to the given point
    # the closest point may be on an edge
    # polygon is a list of points
    # point is a tuple (x,y)
    # return the closest point on the polygon

    # first find the closest point on each edge
    min_dist = 100000
    min_point = None
    min_seg = None
    for i in range(0, len(polygon)):
        seg = (polygon[i], polygon[(i+1) % len(polygon)])
        dist, closest_point = closest_point_to_segment(seg, point)
        if dist < min_dist:
            min_seg = seg
            min_dist = dist
            min_point = closest_point
    
    return min_dist, min_point, min_seg
    
def closest_point_to_segment(segment, point):
    # find the closest point on a segment to the given point
    # the closest point may be on an edge
    # segment is a tuple of tuples ((x1,y1), (x2,y2))
    # point is a tuple (x,y)
    # return the closest point on the segment

    # what if the segement is vertical?
    # then the perpendicular line is horizontal
    # so we need to handle that case separately

    if segment[0][0] == segment[1][0]:
        # the segment is vertical
        # find the intersection point of the segment and the perpendicular line
        x = segment[0][0]
        y = point[1]

        # check if the intersection point is on the segment
        if x >= min(segment[0][0], segment[1][0]) and x <= max(segment[0][0], segment[1][0]) and y >= min(segment[0][1], segment[1][1]) and y <= max(segment[0][1], segment[1][1]):
            return distance((x,y), point), (x,y)
        else:
            # the intersection point is not on the segment
            # so the closest point is one of the endpoints
            if distance(segment[0], point) < distance(segment[1], point):
                return distance(segment[0], point), segment[0]
            else:
                return distance(segment[1], point), segment[1]

    # first find the slope of the segment
    m = (segment[1][1] - segment[0][1]) / (segment[1][0] - segment[0][0])

    # find the y-intercept of the segment
    b = segment[0][1] - m * segment[0][0]

    # what if the slope is 0?
    # then the segment is horizontal
    # and the perpendicular line is vertical
    # so we need to handle that case separately

    if m == 0:
        # the segment is horizontal
        # find the intersection point of the segment and the perpendicular line
        x = point[0]
        y = b

        # check if the intersection point is on the segment
        if x >= min(segment[0][0], segment[1][0]) and x <= max(segment[0][0], segment[1][0]) and y >= min(segment[0][1], segment[1][1]) and y <= max(segment[0][1], segment[1][1]):
            return distance((x,y), point), (x,y)
        else:
            # the intersection point is not on the segment
            # so the closest point is one of the endpoints
            if distance(segment[0], point) < distance(segment[1], point):
                return distance(segment[0], point), segment[0]
            else:
                return distance(segment[1], point), segment[1]

    # find the slope of the perpendicular line
    m_perp = -1 / m

    # find the y-intercept of the perpendicular line
    b_perp = point[1] - m_perp * point[0]

    # find the intersection point of the segment and the perpendicular line
    x = (b_perp - b) / (m - m_perp)
    y = m * x + b

    # check if the intersection point is on the segment
    if x >= min(segment[0][0], segment[1][0]) and x <= max(segment[0][0], segment[1][0]) and y >= min(segment[0][1], segment[1][1]) and y <= max(segment[0][1], segment[1][1]):
        return distance((x,y), point), (x,y)
    else:
        # the intersection point is not on the segment
        # so the closest point is one of the endpoints
        if distance(segment[0], point) < distance(segment[1], point):
            return distance(segment[0], point), segment[0]
        else:
            return distance(segment[1], point), segment[1]
       

    
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def intersection(seg1, seg2):
    # find the intersection point of two segments
    # assume the segements are known to intersect
    # seg1 and seg2 are tuples of tuples
    # seg1 = ((x1,y1), (x2,y2))

    # what if one of the segments is vertical?
    # then the intersection point is easy to find
    if seg1[0][0] == seg1[1][0]:
        # seg1 is vertical
        # find the slope of seg2
        m2 = (seg2[1][1] - seg2[0][1]) / (seg2[1][0] - seg2[0][0])

        # find the y-intercept of seg2
        b2 = seg2[0][1] - m2 * seg2[0][0]

        # find the intersection point
        x = seg1[0][0]
        y = m2 * x + b2

        return (x,y)
    
    if seg2[0][0] == seg2[1][0]:
        # seg2 is vertical
        # find the slope of seg1
        m1 = (seg1[1][1] - seg1[0][1]) / (seg1[1][0] - seg1[0][0])

        # find the y-intercept of seg1
        b1 = seg1[0][1] - m1 * seg1[0][0]

        # find the intersection point
        x = seg2[0][0]
        y = m1 * x + b1

        return (x,y)


    # find the slope of each segment
    m1 = (seg1[1][1] - seg1[0][1]) / (seg1[1][0] - seg1[0][0])
    m2 = (seg2[1][1] - seg2[0][1]) / (seg2[1][0] - seg2[0][0])

    # find the y-intercept of each segment
    b1 = seg1[0][1] - m1 * seg1[0][0]
    b2 = seg2[0][1] - m2 * seg2[0][0]

    # find the intersection point
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    return (x,y)
    

def generate_segments(polygons):
    # generate list of segments
    segments = []
    for polygon in polygons:
        for i in range(0, len(polygon)):
            segments.append((polygon[i-1], polygon[i]))
    return segments