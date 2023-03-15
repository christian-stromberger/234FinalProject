import matplotlib.pyplot as plt
import numpy as np
import random
import time
from the_terrarium import *

from math          import pi, sin, cos, atan2, sqrt

(xmin, xmax) = (0, 14)
(ymin, ymax) = (0, 10)

class Node:
    # Initialize with coordinates.
    def __init__(self, x, y):
        # Define/remember the state/coordinates (x,y).
        self.x = x
        self.y = y

        # Clear any parent information.
        self.parent = None

    ############
    # Utilities:
    # In case we want to print the node.
    def __repr__(self):
        return ("<Point %5.2f,%5.2f>" % (self.x, self.y))

    # Compute/create an intermediate node.  This can be useful if you
    # need to check the local planner by testing intermediate nodes.
    def intermediate(self, other, alpha):
        return Node(self.x + alpha * (other.x - self.x),
                    self.y + alpha * (other.y - self.y))

    # Compute the relative distance to another node.
    def distance(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    # Return a tuple of coordinates, used to compute Euclidean distance.
    def coordinates(self):
        return (self.x, self.y)


######################################################################
#
#   Visualization
#
class Visualization:
    def __init__(self):
        # Clear the current, or create a new figure.
        plt.clf()

        # Create a new axes, enable the grid, and set axis limits.
        plt.axes()
        plt.grid(True)
        plt.gca().axis('on')
        plt.gca().set_xlim(xmin, xmax)
        plt.gca().set_ylim(ymin, ymax)
        plt.gca().set_aspect('equal')

        # Show the triangles.
        # for tr in triangles:
        #     plt.plot((tr[0][0], tr[1][0], tr[2][0], tr[0][0]),
        #              (tr[0][1], tr[1][1], tr[2][1], tr[0][1]),
        #              'k-', linewidth=2)

        # Show.
        self.show()

    def show(self, text = ''):
        # Show the plot.
        plt.pause(0.001)
        # If text is specified, print and wait for confirmation.
        if len(text)>0:
            input(text + ' (hit return to continue)')

    def drawNode(self, node, *args, **kwargs):
        plt.plot(node[0], node[1], *args, **kwargs)

    # def drawEdge(self, head, tail, *args, **kwargs):
    #     plt.plot((head.x, tail.x),
    #              (head.y, tail.y), *args, **kwargs)

    def drawEdge(self, p1, p2, color):
        plt.plot((p1[0],p2[0]),(p1[1], p2[1]), color=color)
    

    def drawPath(self, path, color,*args, **kwargs):
        for i in range(len(path)-1):
            # self.drawEdge(path[i], path[i+1], (0, min(1,i/6), 0))
            self.drawEdge(path[i], path[i+1], color=color)


######################################################################
#
#  Main Code
#
def main():
    # Create the figure.

    # triangles = ((( 2, 6), ( 3, 2), ( 4, 6)),
    #             (( 6, 5), ( 7, 7), ( 8, 5)),
    #             (( 6, 9), ( 8, 9), ( 8, 7)),
    #             ((10, 3), (11, 6), (12, 3)))
    course1 = [((0,0), (14,0), (14,10), (0,10)),(( 6, 4), ( 7, 7), ( 8, 5.5)), 
                (( 6, 9), ( 8, 9), ( 8, 7)), ((10, 3), (11, 6), (12, 3)), ((2,2),(2,6),(5,6),(5,2))]
    # course1 = [[( 0, 3), ( 0, 3)]]

    # course2 = [((2,9),(2,1),(11,1),(11,9),(10.5,9),(10.5,2),(8.5,2),(8.5,9),(7.5,9),(7.5,2),(5.5,2),(5.5,9),(4.5,9),(4.5,2),(2.5,2),(2.5,9))]
    # course2 = [((2,9),(2,1),(11,1),(11,9),(10.5,9),(10.5,2),(8.5,2),(8.5,9),(7.5,9),(7.5,2),(5.5,2),(5.5,9),(4.5,9),(4.5,2),(2.5,2),(2.5,9))]
    course2 = [((0,0), (14,0), (14,10), (0,10)),((2,1),(11,1),(11,9),(2,9),(2,8),(10,8),(10,2),(2,2))]
    # course2 = course2[:-1]

    # course 4
    course4 = [()]

    # generate a star course
    poly1 = []
    # generate a list of points to form a star using numpy array
    x = np.linspace(0,np.pi*2,25)
    for i in range(0,len(x)):
        if(i%2==0):
            poly1.append((5*np.cos(x[i])+7,5*np.sin(x[i])+5.01))
        else:
            poly1.append((2*np.cos(x[i])+7,2*np.sin(x[i])+5.01))
    
    course3 = [poly1,((0,0), (14,0), (14,10), (0,10))]
    # print(course2)

    # for i in range(1,10):
    #     course2.append([(i,1),(i,9)])
    # for i in range(1,10):
    #     course2.append([(1,i),(9,i)])

    

    (startx, starty) = ( 1, 5)
    (goalx,  goaly)  = (13, 5)


    visual = Visualization()

    # Create the start/goal nodes.
    startnode = (startx, starty)
    goalnode  = (goalx, goaly)

    # Show the start/goal nodes.
    visual.drawNode(startnode, color='r', marker='o')
    visual.drawNode(goalnode,  color='r', marker='o')

    # now draw the polygons

    for polygon in course3:
        for i in range(0,len(polygon)):
            visual.drawEdge(polygon[i-1], polygon[i], 'r')
    #visual.drawPath(bug0(course3, startnode, goalnode),color = (0,0,1))
    visual.drawPath(bouncy_ball_bug(course3, startnode, goalnode),color = (0,1,0))
    #visual.drawPath(bug1(course3, startnode, goalnode),color = (0,1,0))
    #visual.drawPath(bug2(course3, startnode, goalnode),color = (0,1,0))




    visual.show("Showing basic world")
    '''


    # Run the EST planner.
    print("Running EST...")
    (path, N) = est(startnode, goalnode, visual)

    # If unable to connect, show what we have.
    if not path:
        visual.show("UNABLE TO FIND A PATH")
        return

    # Show the path.
    print("PATH found after %d nodes" % N)
    visual.drawPath(path, color='r', linewidth=2)
    visual.show("Showing the raw path")


    # Post Process the path.
    PostProcess(path)

    # Show the post-processed path.
    visual.drawPath(path, color='b', linewidth=2)
    visual.show("Showing the post-processed path")
    '''

if __name__== "__main__":
    main()
