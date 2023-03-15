def get_bounce_angle(segment, ball_angle):
    # takes in wall segement and ball angle and returns new ball angle
    # ball angle is in radians
    # segment is a tuple of two points


    # get the angle of the wall segment
    wall_angle = math.atan2(segment[1][1] - segment[0][1], segment[1][0] - segment[0][0])

    # get the angle between the wall and the ball
    angle_between = wall_angle - ball_angle
    
    # get the new ball angle
    new_ball_angle = wall_angle + angle_between
