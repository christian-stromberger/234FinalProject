# BUGS BUGS BUGS BUGS BUGS!!!!!
from planarutils import *
import math
import random



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