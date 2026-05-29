import sympy
from sympy import sqrt, cos, sin
import numpy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation

def animateSolution(k, m, c):
    t = sympy.Symbol("t")

    Q = sqrt(2)/2 * sympy.Matrix([[1, 1], [1, -1]])
    F = sympy.Matrix([
        [c[0]*cos(sqrt(k/m)*t) + c[1]*sin(sqrt(k/m)*t)],
        [c[2]*cos(sqrt(3*k/m)*t) + c[3]*sin(sqrt(3*k/m)*t)]
    ])
    Y = Q*F

    y1 = sympy.lambdify(t, Y[0])
    y2 = sympy.lambdify(t, Y[1])

    animationEnd = 50
    animationStep = 0.1
    T = numpy.arange(0, animationEnd, animationStep)

    ## Compute positions of masses
    m1Pos = y1(T)
    m2Pos = y2(T)

    ## Setup parameters for the plot objects
    springLen = 5
    springHeight = 0.2
    springCoils = 3
    massWidth = 2
    massHeight = 0.5
    systemHeight = 0.5
    frameInterval = 25          # Time between frames in ms

    ## Define and compute spring positions
    springResolution = 100
    s1x = numpy.zeros((len(T), springResolution+1))
    s1y = numpy.zeros((len(T), springResolution+1))
    s2x= numpy.zeros((len(T), springResolution+1))
    s2y = numpy.zeros((len(T), springResolution+1))
    s3x = numpy.zeros((len(T), springResolution+1))
    s3y= numpy.zeros((len(T), springResolution+1))

    for i in range(len(T)):
        startPoint = numpy.array([
            0,
            springLen + m1Pos[i] + massWidth/2,
            2*springLen + m2Pos[i] + massWidth/2
        ]).transpose()
        endPoint = numpy.array([
            springLen + m1Pos[i] - massWidth/2,
            2*springLen + m2Pos[i] - massWidth/2,
            3*springLen
        ]).transpose()
        length = endPoint - startPoint

        ## Sample points at a sine curve between each of the start- and endpoints
        s1x[i] = startPoint[0] + length[0]/springResolution*numpy.arange(0, springResolution+1)
        s1y[i] = systemHeight + springHeight*numpy.sin((s1x[i] - startPoint[0])*springCoils*2*numpy.pi/length[0])

        s2x[i] = startPoint[1] + length[1]/springResolution*numpy.arange(0, springResolution+1)
        s2y[i] = systemHeight + springHeight*numpy.sin((s2x[i] - startPoint[1])*springCoils*2*numpy.pi/length[1])

        s3x[i] = startPoint[2] + length[2]/springResolution*numpy.arange(0, springResolution+1)
        s3y[i] = systemHeight + springHeight*numpy.sin((s3x[i] - startPoint[2])*springCoils*2*numpy.pi/length[2])

        
    ## Start creating the plot
    fig, ax = plt.subplots()
    ax.set_xlim(0, 3*springLen)
    ax.set_ylim(0, 2*systemHeight)
    
    mass1 = Rectangle((springLen + m1Pos[0]-massWidth/2, systemHeight-massHeight/2), massWidth, massHeight)
    mass2 = Rectangle((2*springLen + m2Pos[0]-massWidth/2, systemHeight-massHeight/2), massWidth, massHeight)
    mass1.set_color('0.6')
    mass2.set_color('0.6')
    
    spring1 = Line2D(s1x[0], s1y[0])
    spring2 = Line2D(s2x[0], s2y[0])
    spring3 = Line2D(s3x[0], s3y[0])

    tLabel = ax.text(0.1*springLen, 0.1*systemHeight, "t = {:.1f}".format(T[0]))
    
    def animationInit():
        ax.add_patch(mass1)
        ax.add_patch(mass2)
        ax.add_line(spring1)
        ax.add_line(spring2)
        ax.add_line(spring3)
        return [mass1, mass2, spring1, spring2, spring3, tLabel]

    def animationUpdate(frame):
        mass1.set_xy([springLen + m1Pos[frame]-massWidth/2, systemHeight-massHeight/2])
        mass2.set_xy([2*springLen + m2Pos[frame]-massWidth/2, systemHeight-massHeight/2])
        
        spring1.set_xdata(s1x[frame])
        spring1.set_ydata(s1y[frame])
        
        spring2.set_xdata(s2x[frame])
        spring2.set_ydata(s2y[frame])
        
        spring3.set_xdata(s3x[frame])
        spring3.set_ydata(s3y[frame])

        tLabel.set_text("t = {:.1f}".format(T[frame]))
        return [mass1, mass2, spring1, spring2, spring3, tLabel]

    anim = FuncAnimation(fig,
                         animationUpdate,
                         init_func=animationInit,
                         frames=len(T),
                         interval=frameInterval)
    plt.show()
        
