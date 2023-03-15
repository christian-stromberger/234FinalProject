import math


def closest_point_to_polygon(polygon, point):
    # find the closest point on a polygon to the given point
    # the closest point may be on an edge
    # polygon is a list of points
    # point is a tuple (x,y)
    # return the closest point on the polygon

    # first find the closest point on each edge
    min_dist = 100000
    min_point = None
    for i in range(0, len(polygon)):
        seg = (polygon[i], polygon[(i+1) % len(polygon)])
        dist, closest_point = closest_point_to_segment(seg, point)
        if dist < min_dist:
            min_dist = dist
            min_point = closest_point
    
    return min_dist, min_point
    
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
    

# unit tests for closest_point_to_polygon
print(closest_point_to_polygon([(0,0), (1,0), (1,1), (0,1)], (2,2)))
