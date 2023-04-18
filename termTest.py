from cmu_112_graphics import *
import math
import string

class mainMenu(Mode):
    def appStarted(app):
        app.box1X = 200 #boxlength = 500, boxheight = 150
        app.box1Y = 350
        app.box2X = 900
        app.box2Y = 350
        app.box3X = 200
        app.box3Y = 550
        app.box4X = 900
        app.box4Y = 550
        app.mainMenuText = "Welcome to my Physics Simulator!"
        app.authorText = "Made by: David Bautista"
        app.pickText = "Pick a physics scenario to experiment with the simulation!"
        app.orbitText = "Newton's Law of Gravitation"
        app.pendulumText = "Pendulum Motion"
        app.projText = "Projectile Motion"
        app.inelasticText1 = "Conservation of Momentum"
        app.inelasticText2 = "(Perfectly Inelastic Collision)"

    def mousePressed(app, event):
        if (app.box1X < event.x < app.box1X + 500) and (app.box1Y < event.y < app.box1Y+150):
            app.app.setActiveMode(app.app.orbitMenu)
        if (app.box2X < event.x < app.box2X + 500) and (app.box2Y < event.y < app.box2Y+150):
            app.app.setActiveMode(app.app.pendulumMenu)
        if (app.box3X < event.x < app.box3X + 500) and (app.box3Y < event.y < app.box3Y+150):
            app.app.setActiveMode(app.app.projectileMenu)
        if (app.box4X < event.x < app.box4X + 500) and (app.box4Y < event.y < app.box4Y+150):
            app.app.setActiveMode(app.app.inelasticMenu)

    def redrawAll(app, canvas):
        canvas.create_text(app.width//2,100,text=app.mainMenuText,font="Times 16 bold")
        canvas.create_text(app.width//2,130,text=app.authorText,font="Times 14 bold")
        canvas.create_text(app.width//2,150,text=app.pickText,font="Times 14 bold")
        canvas.create_rectangle(app.box1X,app.box1Y,app.box1X+500,app.box1Y+150,fill="royal blue")
        canvas.create_rectangle(app.box2X,app.box2Y,app.box2X+500,app.box2Y+150,fill="SpringGreen3")
        canvas.create_rectangle(app.box3X,app.box3Y,app.box3X+500,app.box3Y+150,fill="firebrick3")
        canvas.create_rectangle(app.box4X,app.box4Y,app.box4X+500,app.box4Y+150,fill="MediumOrchid3")
        canvas.create_text(450,425,text=app.orbitText,font="Times 16 bold")
        canvas.create_text(1150,425,text=app.pendulumText,font="Times 16 bold")
        canvas.create_text(450,625,text=app.projText,font="Times 16 bold")
        canvas.create_text(1150,610,text=app.inelasticText1,font="Times 16 bold")
        canvas.create_text(1150,640,text=app.inelasticText2,font="Times 16 bold")

class orbitMenu(Mode):
    def appStarted(app):
        ####################NEWTON'S LAW OF GRAVITATION OBJECTS#####################
        ##########ATTRIBUTES#############
        app.gravitationalConstant = 6.67408 * 10**-20 
        #in "gigameters", only used to not go outisde of the canvas
        app.ball1Radius = 50
        app.ball1CX = 900
        app.ball1CY = 400 
        app.ball1Mass = 1.99 * 10**30 * 10**-4
        app.ball2Radius = 12.5
        app.ball2CY = 400
        app.ball3CY = 400
        app.ball4CY = 400
        app.vx1 = 0
        app.vx2 = 0
        app.vx3 = 0
        app.dt = 0.005
        app.timerDelay = -100
        app.elapsedTime = 0
        app.v = 0
        app.vScale = 1
        app.vList = []
        app.orbitText = '''As you can see, the tangential (orbital) speed of a planet/moon is constant because the mass that a planet/moon is orbiting around (star/planet)
is pulling on the planet/moon with a constant, gravitational force:

F = (Gm1m2)/(r**2),
G: gravitational constant, m1: Object 1 mass,
m2: Object 2 Mass, r = distance from Object 2 to Object 1

Of course this is in ideal conditions where the orbit is not elliptical. So we can apply circular motion equations like centripetal acceleration and circular velocity:

a = v**2/r, v: velocity
v = 2πr/T, T: period of motion/orbit

Additionally, because F is a force we can equate this to F = mass*acceleration. We find that that orbital speed essentially depends on distance of between two objects!
The orbital speed is inversely proportional to the square root of the distance:

v = sqrt(Gm1/r), m1: mass of star/planet

One thing to note is that the mass of the orbiting planet/moon doesn't actually matter!
'''
        #################################
        ##########USER INPUT############# 
        app.userBalls = ["","",""]
        app.dummyUserBallsCX = [None,None,None]
        app.userPlanetCounts = ""
        app.planetCounts = 0
        app.textBox1Bool = False
        app.textBox1X = 10
        app.textBox1Y = 160
        app.textBox2Bool = False
        app.textBox2X = 10
        app.textBox2Y = 230
        app.textBox3Bool = False
        app.textBox3X = 10
        app.textBox3Y = 300
        app.textBox4Bool = False
        app.textBox4X = 10
        app.textBox4Y = 370
        app.emptyStringBool1 = False
        app.emptyStringBool2 = False
        app.emptyStringBool3 = False
        app.lapCount1 = 0
        app.lapCount2 = 0
        app.lapCount3 = 0
        app.timesUp = False
        app.play1 = False
        app.infoOn = False
        #################################

    def timerFired(app):
        if app.play1:
            app.doStep()

    def mousePressed(app, event):
        if app.play1 == False and app.timesUp == False:
            if (app.textBox1X < event.x < app.textBox1X + 180) and (app.textBox1Y < event.y < app.textBox1Y+25):
                app.textBox1Bool = True
            else: app.textBox1Bool = False
            if (app.textBox2X < event.x < app.textBox2X + 180) and (app.textBox2Y < event.y < app.textBox2Y+25) and app.planetCounts >= 1:
                app.textBox2Bool = True
            else: app.textBox2Bool = False
            if (app.textBox3X < event.x < app.textBox3X + 180) and (app.textBox3Y < event.y < app.textBox3Y+25) and app.planetCounts >= 2:
                app.textBox3Bool = True
            else: app.textBox3Bool = False
            if (app.textBox4X < event.x < app.textBox4X + 180) and (app.textBox4Y < event.y < app.textBox4Y+25) and app.planetCounts == 3:
                app.textBox4Bool = True
            else: app.textBox4Bool = False
        if app.timesUp == True:
            if (100 < event.y < 230) and (1450 < event.x < 1600):
                app.infoOn = not app.infoOn
    def keyPressed(app, event):
        if event.key == "r":
            app.appStarted()
        if event.key == "q":
            app.appStarted()
            app.app.setActiveMode(app.app.mainMenu)
        if app.play1 == False and app.timesUp == False:
            if app.textBox1Bool:
                if event.key in string.digits: 
                    if len(app.userPlanetCounts) < 1:
                        app.userPlanetCounts += event.key
                elif event.key == "Backspace": app.userPlanetCounts = app.userPlanetCounts[:-1]
                elif event.key == "Enter":
                    if app.userPlanetCounts == "":
                        app.emptyStringBool1 = True
                    else:
                        app.emptyStringBool1 = False
                        if float(app.userPlanetCounts) > 3 or float(app.userPlanetCounts) < 1:
                            app.userPlanetCounts = ""
                        else:    
                            app.planetCounts = int(app.userPlanetCounts)

            if app.textBox2Bool:
                if event.key in string.digits or event.key == ".": 
                    if (app.userBalls[0].count(".") <= 1) and (len(app.userBalls[0]) <= 18):
                        app.userBalls[0] += event.key
                elif event.key == "Backspace": app.userBalls[0] = app.userBalls[0][:-1]
                elif event.key == "Enter":
                    if app.userBalls[0] != "":
                        if float(app.userBalls[0]) > 837.5 or float(app.userBalls[0]) < 213:
                            app.userBalls[0] = ""
                        else:    
                            app.dummyUserBallsCX[0] = float(app.userBalls[0])
                            app.ball2CX = app.dummyUserBallsCX[0]
                            app.initial2CY = app.ball2CY
                            app.initial2CX = app.ball2CX
                            app.Distance1 = math.sqrt((app.ball2CX-app.ball1CX)**2+(app.ball2CY-app.ball1CY)**2)
                            app.permDistance1 = app.Distance1
                            app.vy1 = math.sqrt(app.gravitationalConstant*app.ball1Mass/app.Distance1)
                            #app.vy1 = app.Distance1/math.sqrt((app.Distance1**3)/(app.gravitationalConstant*app.ball1Mass))
                            app.vyi = app.vy1
                            app.period1 = 2*math.pi*math.sqrt((app.permDistance1**3)/(app.gravitationalConstant*app.ball1Mass))

            if app.textBox3Bool:
                if event.key in string.digits or event.key == ".": 
                    if (app.userBalls[1].count(".") <= 1) and (len(app.userBalls[1]) <= 18):
                        app.userBalls[1] += event.key
                elif event.key == "Backspace": app.userBalls[1] = app.userBalls[1][:-1]
                elif event.key == "Enter":
                    if app.userBalls[1] == "":
                        app.emptyStringBool3 = True
                    else:
                        app.emptyStringBool3 = False
                        if float(app.userBalls[1]) > 837.5 or float(app.userBalls[1]) < 213:
                            app.userBalls[1] = ""
                        else:
                            app.dummyUserBallsCX[1] = float(app.userBalls[1])
                            app.ball3CX = app.dummyUserBallsCX[1]
                            app.initial3CY = app.ball3CY
                            app.initial3CX = app.ball3CX
                            app.Distance2 = math.sqrt((app.ball3CX-app.ball1CX)**2+(app.ball3CY-app.ball1CY)**2)
                            app.permDistance2 = app.Distance2
                            app.vy2 = app.Distance2/math.sqrt((app.Distance2**3)/(app.gravitationalConstant*app.ball1Mass))
                            app.period2 = 2*math.pi*math.sqrt((app.permDistance2**3)/(app.gravitationalConstant*app.ball1Mass))

            if app.textBox4Bool:
                if event.key in string.digits or event.key == ".": 
                    if (app.userBalls[2].count(".") <= 1) and (len(app.userBalls[2]) <= 18):
                        app.userBalls[2] += event.key
                elif event.key == "Backspace": app.userBalls[2] = app.userBalls[2][:-1]
                elif event.key == "Enter":
                    if app.userBalls[2] == "":
                        app.emptyStringBool4 = True
                    else:
                        app.emptyStringBool4 = False
                        if float(app.userBalls[2]) > 837.5 or float(app.userBalls[2]) < 213:
                            app.userBalls[2] = ""
                        else:
                            app.dummyUserBallsCX[2] = float(app.userBalls[2])
                            app.ball4CX = app.dummyUserBallsCX[2]
                            app.initial4CY = app.ball4CY
                            app.initial4CX = app.ball4CX
                            app.Distance3 = math.sqrt((app.ball4CX-app.ball1CX)**2+(app.ball4CY-app.ball1CY)**2)
                            app.permDistance3 = app.Distance3
                            app.vy3 = app.Distance3/math.sqrt((app.Distance3**3)/(app.gravitationalConstant*app.ball1Mass))
                            app.period3 = 2*math.pi*math.sqrt((app.permDistance3**3)/(app.gravitationalConstant*app.ball1Mass))
        
            if (None not in app.dummyUserBallsCX[:app.planetCounts]) and (app.planetCounts != 0):
                app.play1 = True
                app.textBox1Bool = False
                app.textBox2Bool = False
                app.textBox3Bool = False
                app.textBox4Bool = False

    def doStep(app):
        if app.planetCounts == 1:
            app.maxPeriod = app.period1
        if app.planetCounts == 2:
            app.maxPeriod = (app.period1+app.period2)/2
        if app.planetCounts == 3:
            app.maxPeriod = (app.period1+app.period2+app.period3)/3
        if app.elapsedTime > app.maxPeriod:
            app.play1 = False
            app.timesUp = True

        updatedTime = 50*app.elapsedTime
        if updatedTime < 900:
            if app.vyi >= 350:
                app.vScale = 1/2
            elif app.vyi < 50:
                app.vScale = 5
            app.v = math.sqrt(((app.vx1)**2)+((app.vy1)**2))
            app.vList.append((updatedTime,app.v*app.vScale))
        
        "PLANET 1"
        app.Distance1 = math.sqrt((app.ball2CX-app.ball1CX)**2+(app.ball2CY-app.ball1CY)**2)
        app.xDistance1 = (app.ball1CX-app.ball2CX)/app.Distance1
        #r_xhat = (r2_x - r1_x)/r
        app.yDistance1 = (app.ball1CY-app.ball2CY)/app.Distance1
        #r_yhat = (r2_y - r1_y)/r
        app.xGravity1 = (app.gravitationalConstant*app.ball1Mass*app.xDistance1)/(app.Distance1**2)
        #g_x = -(GM)(r_x)/(r**2)
        app.yGravity1 = (app.gravitationalConstant*app.ball1Mass*app.yDistance1)/(app.Distance1**2)
        #g_y = -(GM)(r_y)/(r**2)
        app.ball2CX = app.ball2CX + app.vx1*app.dt + 0.5*app.xGravity1*(app.dt**2)
        #x_f = x_i + (vx_i * t) + 0.5*(g_x * t**2)
        app.vx1 = app.vx1 + app.xGravity1*app.dt #vx_f = vx_i + gx*t
        app.ball2CY = app.ball2CY + app.vy1*app.dt + 0.5*app.yGravity1*(app.dt**2)
        #y_f = y_i + (vy_i * t) + 0.5*(g_y * t**2)
        app.vy1 = app.vy1 + app.yGravity1*app.dt #vy_f = vy_i + gy*t
        #g_y = -(GM)(r_y)/(r**2)
        if app.planetCounts >= 2:
            "PLANET 2"
            app.Distance2 = math.sqrt((app.ball3CX-app.ball1CX)**2+(app.ball3CY-app.ball1CY)**2)
            app.xDistance2 = (app.ball1CX-app.ball3CX)/app.Distance2
            app.yDistance2 = (app.ball1CY-app.ball3CY)/app.Distance2
            app.xGravity2 = (app.gravitationalConstant*app.ball1Mass*app.xDistance2)/(app.Distance2**2)
            app.yGravity2 = (app.gravitationalConstant*app.ball1Mass*app.yDistance2)/(app.Distance2**2)
            app.ball3CX = app.ball3CX + app.vx2*app.dt + 0.5*app.xGravity2*(app.dt**2)
            app.vx2 = app.vx2 + app.xGravity2*app.dt
            app.ball3CY = app.ball3CY + app.vy2*app.dt + 0.5*app.yGravity2*(app.dt**2)
            app.vy2 = app.vy2 + app.yGravity2*app.dt
        if app.planetCounts == 3:
            "PLANET 3"
            app.Distance3 = math.sqrt((app.ball4CX-app.ball1CX)**2+(app.ball4CY-app.ball1CY)**2)
            app.xDistance3 = (app.ball1CX-app.ball4CX)/app.Distance3
            app.yDistance3 = (app.ball1CY-app.ball4CY)/app.Distance3
            app.xGravity3 = (app.gravitationalConstant*app.ball1Mass*app.xDistance3)/(app.Distance3**2)
            app.yGravity3 = (app.gravitationalConstant*app.ball1Mass*app.yDistance3)/(app.Distance3**2)
            app.ball4CX = app.ball4CX + app.vx3*app.dt + 0.5*app.xGravity3*(app.dt**2)
            app.vx3 = app.vx3 + app.xGravity3*app.dt
            app.ball4CY = app.ball4CY + app.vy3*app.dt + 0.5*app.yGravity3*(app.dt**2)
            app.vy3 = app.vy3 + app.yGravity3*app.dt

        app.elapsedTime += app.dt
        
    def redrawAll(app, canvas):
        ###ANIMATION###
        canvas.create_rectangle(0,0,200,800,fill="royal blue",width=3)
        if app.timesUp:
            canvas.create_rectangle(250,50,1250,500,width=3)
            canvas.create_line(300,500,300,100,width=2)
            canvas.create_line(300,450,1200,450,width=2)
            for i in range(len(app.vList)):
                if (app.vList[i][1] < 350):
                    canvas.create_oval(300+app.vList[i][0]-2,450-app.vList[i][1]-2,300+app.vList[i][0]+2,450-app.vList[i][1]+2,fill="blue")
            canvas.create_text(375,90,text="Blue Velocity ('gigameters'/second)",font="Times 12 bold")
            canvas.create_text(750,460,text="Time (seconds)",font="Times 12 bold")
            canvas.create_rectangle(1450,100,1600,230,fill="green",width=3)
            canvas.create_text(1525,150,text="MORE",font="Times 14 bold")
            canvas.create_text(1525,180,text="INFO",font="Times 14 bold")

            if app.infoOn:
                canvas.create_rectangle(350,200,1450,600,fill="white",width=3)
                canvas.create_text(900,400,text=app.orbitText,font="Times 12")
        ##############
        ###SIDE MENU###
        canvas.create_text(100,10,text="Click white boxes to type a number.")
        canvas.create_text(100,25,text="Press Backspace to delete a character.")
        canvas.create_text(100,40,text="Press Enter when you type a number.")
        canvas.create_text(100,55,text="Your range of input will be the")
        canvas.create_text(100,70,text="x-coordinates of the center of")
        canvas.create_text(100,85,text="the planet(s) (213 to 837).")
        canvas.create_text(100,100,text="Each pixel is purposefully scaled")
        canvas.create_text(100,115,text="to be 10 to the ninth meters.")
        canvas.create_text(100,130,text="Have fun!")
        canvas.create_text(100,425,text="Press 'r' to restart anything.")
        canvas.create_text(100,450,text="Press 'q' to go back to main menu.")
        "PLANET COUNT BUTTON"
        canvas.create_text(100,145,text="Amount of planets (1-3):")
        canvas.create_rectangle(app.textBox1X,app.textBox1Y,app.textBox1X+180,app.textBox1Y+25,fill="white",width=2)
        canvas.create_text(100,172,text=f"{app.userPlanetCounts}")
        "PLANET 1"
        if app.planetCounts >= 1:
            canvas.create_text(100,200,text=f"Enter an x-coordinate for")
            canvas.create_text(100,215,text=f"Planet 1.")
            canvas.create_rectangle(app.textBox2X,app.textBox2Y,app.textBox2X+180,app.textBox2Y+25,fill="white",width=2)
            canvas.create_text(100,242,text=f"{app.userBalls[0]}")
            if app.play1:
                canvas.create_oval(app.ball1CX-app.ball1Radius,app.ball1CY-app.ball1Radius,app.ball1CX+app.ball1Radius,app.ball1CY+app.ball1Radius,fill="Yellow")
                canvas.create_oval(app.ball2CX-app.ball2Radius,app.ball2CY-app.ball2Radius,app.ball2CX+app.ball2Radius,app.ball2CY+app.ball2Radius,fill="blue")

        "PLANET 2"
        if app.planetCounts >= 2:
            canvas.create_text(100,270,text=f"Enter an x-coordinate for")
            canvas.create_text(100,285,text=f"Planet 2.")
            canvas.create_rectangle(app.textBox3X,app.textBox3Y,app.textBox3X+180,app.textBox3Y+25,fill="white",width=2)
            canvas.create_text(100,312,text=f"{app.userBalls[1]}")
            if app.play1:
                canvas.create_oval(app.ball3CX-app.ball2Radius,app.ball3CY-app.ball2Radius,app.ball3CX+app.ball2Radius,app.ball3CY+app.ball2Radius,fill="orange red")

        "PLANET 3"
        if app.planetCounts == 3:
            canvas.create_text(100,340,text=f"Enter an x-coordinate for")
            canvas.create_text(100,355,text=f"Planet 3.")
            canvas.create_rectangle(app.textBox4X,app.textBox4Y,app.textBox4X+180,app.textBox4Y+25,fill="white",width=2)
            canvas.create_text(100,382,text=f"{app.userBalls[2]}")
            if app.play1:
                canvas.create_oval(app.ball4CX-app.ball2Radius,app.ball4CY-app.ball2Radius,app.ball4CX+app.ball2Radius,app.ball4CY+app.ball2Radius,fill="SpringGreen3")

class projectileMenu(Mode):
    def appStarted(app):
        #########################PROJECTILE MOTION ATTRIBUTES#######################
        ##########ATTRIBUTES############
        app.ballX = 75+200
        app.ballSize = 25
        app.dt = 0.05
        app.g = 9.8
        app.elapsedTime = 0
        app.timerDelay = 0
        app.positionList = []
        app.velocityList = []
        app.vScale = 1
        app.yScale = 1
        app.text = '''In most projectile motion problems, we like to ignore any external force on the projectile. So gravity
is really the only force active in this scenario. To start off, acceleration is the rate at which velocity changes. It is
important to highlight that acceleration has direction. Because of this, if there's vertical acceleration, there shouldn't be any
change to horizontal velocity (because velocity also has a direction). And as we know, g, the acceleration due to gravity, is
equal to -9.8 and is completely vertical, meaning any upward velocity will decrease and any downward velocity will increase.
What I previously said is the concept of a falling object. And as you know from before, the horizontal velocity is constant!
Using the fact that acceleration is equal to change of velocity over time and that velocity is displacement over time, we get these
kinematic equations:

(final x-velocity) = (initial x-velocity)
(final y-velocity) = (initial y-velocity) + (y-acceleration)*(time)
(final y-position) = (initial y-position) + (initial y-velocity)*(time) + 0.5*(y-acceleration)*((time)**2)
(final x-position) = (initial x-position) + (initial x-velocity)*(time)

Additionally, if the projectile is being thrown at an angle from the horizontal, we know that:

(x-velocity) = (magnitude of velocity)*cos(angle)
(y-velocity) = (magnitude of velocity)*sin(angle)

By manipulating equations, we find that the horizontal distance travelled by the projectile depends on the height at which it's
being thrown, velocity, angle, and of course the acceleration due to gravity. Same goes for the time of flight and maximum height.
'''
        #################################
        ##########USER INPUT############# 
        app.userBallHeight = ""
        app.userAngle = ""
        app.userV = ""
        app.dummyUserBallHeight = None
        app.dummyUserAngle = None
        app.dummyUserV = None 
        app.textBox1Bool = False
        app.textBox2Bool = False
        app.textBox3Bool = False
        app.textBox1X = 10
        app.textBox1Y = 160
        app.textBox2X = 10
        app.textBox2Y = 230
        app.textBox3X = 10
        app.textBox3Y = 300
        app.play3 = False
        app.timesUp = False
        app.infoOn = False
        #################################

    def timerFired(app):
        if app.play3 == True:
            app.doStep()

    def mousePressed(app, event):
        if app.timesUp == False  and app.play3 == False:
            if (app.textBox1X < event.x < app.textBox1X + 180) and (app.textBox1Y < event.y < app.textBox1Y+25):
                app.textBox1Bool = True
            else: app.textBox1Bool = False
            if (app.textBox2X < event.x < app.textBox2X + 180) and (app.textBox2Y < event.y < app.textBox2Y+25):
                app.textBox2Bool = True
            else: app.textBox2Bool = False
            if (app.textBox3X < event.x < app.textBox3X + 180) and (app.textBox3Y < event.y < app.textBox3Y+25):
                app.textBox3Bool = True
            else: app.textBox3Bool = False
        if app.timesUp == True:
            if (1450 < event.x < 1600) and (510 < event.y < 540):
                app.infoOn = not app.infoOn

    def keyPressed(app, event):
        #######PROJECTILE MOTION#########
        if app.timesUp == False  and app.play3 == False:
            if app.textBox1Bool:
                if event.key in string.digits or event.key == ".": 
                    if (app.userBallHeight.count(".") <= 1) and (len(app.userBallHeight) <= 18):
                        app.userBallHeight += event.key
                elif event.key == "Backspace": app.userBallHeight = app.userBallHeight[:-1]
                elif event.key == "Enter":
                    if app.userBallHeight != "":
                        app.dummyUserBallHeight = float(app.userBallHeight)
                        app.ballY = app.height - app.dummyUserBallHeight - app.ballSize
                        app.buildingHeight = app.ballY

            if app.textBox2Bool:
                if event.key in string.digits or event.key == ".": 
                    if (app.userAngle.count(".") <= 1) and (len(app.userAngle) <= 18):
                        app.userAngle += event.key
                elif event.key == "Backspace": app.userAngle = app.userAngle[:-1]
                elif event.key == "Enter":
                    if float(app.userAngle) >= 0.5 or float(app.userAngle) < 0:
                        app.userAngle = ""
                    elif app.userAngle != "":
                        app.dummyUserAngle = float(app.userAngle)
                        app.angle = app.dummyUserAngle*math.pi

            if app.textBox3Bool:
                if event.key in string.digits or event.key == ".": 
                    if (app.userV.count(".") <= 1) and (len(app.userV) <= 18):
                        app.userV += event.key
                elif event.key == "Backspace": app.userV = app.userV[:-1]
                elif event.key == "Enter":
                    if app.userV != "":
                        app.dummyUserV = float(app.userV)
                        app.ballV = app.dummyUserV

            if (app.dummyUserBallHeight != None) and (app.dummyUserAngle != None) and (app.dummyUserV != None):
                app.textBox1Bool = False
                app.textBox2Bool = False
                app.textBox3Bool = False
                app.play3 = True
                app.vx = app.ballV*math.cos(app.angle)
                app.vy = -app.ballV *math.sin(app.angle)
                app.vyi = app.vy
                app.actualBallY = -1*(app.ballY-app.height+app.ballSize)
                if app.angle == 0:
                    TiMe = math.sqrt(2*app.actualBallY/app.g)
                    app.dx = app.vx*TiMe
                else:
                    app.dx = ((app.ballV**2)*math.sin(2*app.angle)/(2*app.g))*(1+math.sqrt(1+(2*app.g*app.actualBallY)/(app.ballV*math.sin(app.angle))**2))
                    #app.dx = Horizontal Distance covered = [(v_i**2)sin(2θ)/2g][1+sqrt(1+(2gy_i)/(v_i*sin(θ))**2)]
        if event.key == "r":
            app.appStarted()
        if event.key == "q":
            app.appStarted()
            app.app.setActiveMode(app.app.mainMenu)

    def doStep(app):
    #######PROJECTILE MOTION##########
        updatedTime = 50*app.elapsedTime
        if updatedTime < 900:
            if app.vyi > 800:
                app.vScale = 1/5
            elif app.vyi < 50:
                app.vScale = 5
            if app.actualBallY > 800:
                app.yScale = 1/5
            elif app.actualBallY < 50:
                app.yScale = 5
            app.positionList.append((updatedTime,-1*(app.ballY-app.height+app.ballSize)*app.yScale))
            app.velocityList.append((updatedTime,-app.vy*app.vScale))

        app.ballX = app.ballX + app.vx*app.dt # x_f = x_i + (vx_i * t)

        if app.ballX < 0:
            app.ballX = 0
            app.vx = -app.vx

        app.ballY = app.ballY + app.vy*app.dt + 0.5*app.g*(app.dt)**2 
        # y_f = y_i + (v_i * t) + 0.5*(g * t**2)
        app.vy = app.vy + app.g*app.dt
        # vy_f = vy_i + (g * t)

        if app.ballY > app.height - app.ballSize:
            app.ballY = app.height - app.ballSize
            app.play3 = False
            app.timesUp = True

        app.elapsedTime += app.dt

    def drawBallandBuilding(app, canvas):
        canvas.create_rectangle(200,app.buildingHeight+app.ballSize,300,800, fill="gray", width=3)
        canvas.create_oval(app.ballX,
                                app.ballY,
                                app.ballX + app.ballSize,
                                app.ballY + app.ballSize,
                                fill="blue")

    def tupleMax(app,L):
        newL = []
        for i in range(len(L)):
            newL.append(L[i][1])
        return max(newL)

    def drawResults(app, canvas):
        if app.ballY == app.height - app.ballSize:
            canvas.create_rectangle(1250,50,1475,450,fill="white",width=3)
            canvas.create_text(1362,60,text="Horizontal Distance Travelled",font="Times 12 bold")
            canvas.create_text(1270,80, text="Actual:",font="Times 10")
            canvas.create_text(1320,80,text=f"{round(app.ballX-75-200,3)}",font="Times 10")
            canvas.create_text(1280,100, text="Theoretical:",font="Times 10")
            canvas.create_text(1350,100,text=f"{round(app.dx,3)}",font="Times 10")
            canvas.create_text(1362,120,text="Maximum Height",font="Times 12 bold")
            canvas.create_text(1270,140, text="Actual:",font="Times 10")
            canvas.create_text(1320,140,text=f"{round(app.actualBallY+abs(app.actualBallY-app.tupleMax(app.positionList)),3)}",font="Times 10")
            canvas.create_text(1280,160, text="Theoretical:",font="Times 10")
            canvas.create_text(1350,160,text=f"{round(app.actualBallY+((app.ballV*math.sin(app.angle))**2)/(2*app.g),3)}",font="Times 10")


    def redrawAll(app, canvas):
        #########PROJECTILE MOTION#######
        ###ANIMATION###
        if app.play3:
            app.drawBallandBuilding(canvas)
        if app.timesUp:
            app.drawResults(canvas)
            canvas.create_rectangle(250,50,1250,750,width=3)
            canvas.create_line(300,750,300,100,width=2)
            canvas.create_line(1200,750,1200,100,width=2)
            canvas.create_line(300,450,1200,450,width=2)
            canvas.create_rectangle(650,60,660,70,fill="red")
            canvas.create_text(690,65,text="= Position")
            canvas.create_rectangle(890,60,900,70,fill="blue")
            canvas.create_text(930,65,text="= Velocity")
            for i in range(len(app.positionList)):
                if (app.positionList[i][1] < 350):
                    canvas.create_oval(300+app.positionList[i][0]-2,450-app.positionList[i][1]-2,300+app.positionList[i][0]+2,450-app.positionList[i][1]+2,fill="red")
            for i in range(len(app.velocityList)):
                if (app.velocityList[i][1] > -300) and (app.velocityList[i][1] < 350):
                    canvas.create_oval(300+app.velocityList[i][0]-2,450-app.velocityList[i][1]-2,300+app.velocityList[i][0]+2,450-app.velocityList[i][1]+2,fill="blue")
            canvas.create_text(310,90,text="Position (meters)",font="Times 12 bold")
            canvas.create_text(1120,90,text="Vertical Velocity (meters/second)",font="Times 12 bold")
            canvas.create_text(750,460,text="Time (seconds)",font="Times 12 bold")
            canvas.create_rectangle(1450,460,1600,590,fill="green",width=3)
            canvas.create_text(1525,510,text="MORE",font="Times 14 bold")
            canvas.create_text(1525,540,text="INFO",font="Times 14 bold")

            if app.infoOn:
                canvas.create_rectangle(500,185,1300,600,fill="white",width=3)
                canvas.create_text(900,400,text=app.text,font="Times 12")
        ##############
        ###SIDE MENU###
        canvas.create_rectangle(0,0,200,800,fill="firebrick3",width=3)
        canvas.create_rectangle(app.textBox1X,app.textBox1Y,app.textBox1X+180,app.textBox1Y+25,fill="white",width=2)
        canvas.create_rectangle(app.textBox2X,app.textBox2Y,app.textBox2X+180,app.textBox2Y+25,fill="white",width=2)
        canvas.create_rectangle(app.textBox3X,app.textBox3Y,app.textBox3X+180,app.textBox3Y+25,fill="white",width=2)
        canvas.create_text(100,10,text="Click white boxes to type a number.")
        canvas.create_text(100,25,text="Press Backspace to delete a character.")
        canvas.create_text(100,40,text="Press Enter when you type a number.")
        canvas.create_text(100,55,text="Have fun!")
        canvas.create_text(100,425,text="Press 'r' to restart anything.")
        canvas.create_text(100,450,text="Press 'q' to go back to main menu.")
        "HEIGHT"
        canvas.create_text(100,145,text="Enter ball height:")
        canvas.create_rectangle(app.textBox1X,app.textBox1Y,app.textBox1X+180,app.textBox1Y+25,fill="white",width=2)
        canvas.create_text(100,172,text=f"{app.userBallHeight}")
        "ANGLE"
        canvas.create_text(100,200,text="Enter constant that'll be multiplied")
        canvas.create_text(100,215,text="by pi (0 - 0.49)")
        canvas.create_rectangle(app.textBox2X,app.textBox2Y,app.textBox2X+180,app.textBox2Y+25,fill="white",width=2)
        canvas.create_text(100,242,text=f"{app.userAngle}")
        "VELOCITY"
        canvas.create_text(100,270,text="Enter a velocity:")
        canvas.create_text(100,285,text="(10m/s to 99999m/s)")
        canvas.create_rectangle(app.textBox3X,app.textBox3Y,app.textBox3X+180,app.textBox3Y+25,fill="white",width=2)
        canvas.create_text(100,312,text=f"{app.userV}")

class inelasticMenu(Mode):
    def appStarted(app):
        #########################INELASTIC ATTRIBUTES#######################
        ##########ATTRIBUTES############
        app.box1CX = 400
        app.box1CY = 650
        app.box1R = 50
        app.box2CX = 1000
        app.box2CY = 600
        app.box2R = 100 
        app.dt = 0.01
        app.elapsedTime = 0
        app.collisionTime = 0
        app.timerDelay = 0
        app.redBoxList = []
        app.blueBoxList = []
        app.scale1 = 1
        app.scale2 = 1
        app.text = '''This scenario uses one of the most fundamental concepts of physics: conservation of momentum.
First, momentum is a measurement of an object's motion. Mathematically, it is simply defined as

(momentum) = (mass)*(velocity)

Of course, momentum has a direction and magnitude. In a closed system (no external forces acted on objects in
system), momentum is never created nor destroyed. Knowing this, this scenario involves 2 objects that will stick
to each other once they collide--an inelastic collision. After they collide, they will both have the same velocity
and the two object will be basically one big mass, by conservation of momentum:

(momentum1) + (momentum2) = (mass1)(velocity1) + (mass2)(velocity2) = (mass3)(velocity3) = (mass1+mass2)(velocity3)
        '''
        #################################
        ##########USER INPUT############# 
        app.userBox1V = ""
        app.userBox2V = ""
        app.userBox1Mass = ""
        app.userBox2Mass = ""
        app.dummyUserBox1V = None
        app.dummyUserBox2V = None
        app.dummyUserBox1Mass = None
        app.dummyUserBox2Mass = None
        app.textBox1Bool = False
        app.textBox2Bool = False
        app.textBox3Bool = False
        app.textBox4Bool = False
        app.textBox1X = 10
        app.textBox1Y = 160
        app.textBox2X = 10
        app.textBox2Y = 230
        app.textBox3X = 10
        app.textBox3Y = 300
        app.textBox4X = 10
        app.textBox4Y = 370
        app.collision = False
        app.play4 = False
        app.timesUp = False
        app.infoOn = False
        #################################

    def timerFired(app):
        if app.play4 == True:
            app.doStep()

    def mousePressed(app, event):
        if app.timesUp == False  and app.play4 == False:
            if (app.textBox1X < event.x < app.textBox1X + 180) and (app.textBox1Y < event.y < app.textBox1Y+25):
                app.textBox1Bool = True
            else: app.textBox1Bool = False
            if (app.textBox2X < event.x < app.textBox2X + 180) and (app.textBox2Y < event.y < app.textBox2Y+25):
                app.textBox2Bool = True
            else: app.textBox2Bool = False
            if (app.textBox3X < event.x < app.textBox3X + 180) and (app.textBox3Y < event.y < app.textBox3Y+25):
                app.textBox3Bool = True
            else: app.textBox3Bool = False
            if (app.textBox4X < event.x < app.textBox4X + 180) and (app.textBox4Y < event.y < app.textBox4Y+25):
                app.textBox4Bool = True
            else: app.textBox4Bool = False

        if (app.timesUp == True):
            if (1450 < event.x < 1600) and (100 < event.y  < 230):
                app.infoOn = not app.infoOn

    def keyPressed(app, event):
    #######INELASTIC#########
        if app.timesUp == False  and app.play4 == False:
            if app.textBox1Bool:
                if event.key in string.digits or event.key == "." or event.key == "-": 
                    if app.userBox1V.count(".") <= 1 and app.userBox1V.count("-") <= 1 and (len(app.userBox1V) <= 18):
                        app.userBox1V += event.key
                elif event.key == "Backspace": app.userBox1V = app.userBox1V[:-1]
                elif event.key == "Enter":
                    if abs(float(app.userBox1V)) > 450:
                        app.userBox1V = ""
                    if app.userBox1V != "":
                        app.dummyUserBox1V = float(app.userBox1V)
                        app.box1V = app.dummyUserBox1V

            if app.textBox2Bool:
                if event.key in string.digits or event.key == "." or event.key == "-": 
                    if app.userBox2V.count(".") <= 1 and app.userBox2V.count("-") <= 1 and (len(app.userBox2V) <= 18):
                        app.userBox2V += event.key
                elif event.key == "Backspace": app.userBox2V = app.userBox2V[:-1]
                elif event.key == "Enter":
                    if abs(float(app.userBox2V)) > 450:
                        app.userBox2V = ""
                    elif app.userBox2V != "":
                        app.dummyUserBox2V = float(app.userBox2V)
                        app.box2V = app.dummyUserBox2V

            if app.textBox3Bool:
                if event.key in string.digits or event.key == ".": 
                    if app.userBox1Mass.count(".") <= 1 and (len(app.userBox1Mass) <= 18):
                        app.userBox1Mass += event.key
                elif event.key == "Backspace": app.userBox1Mass = app.userBox1Mass[:-1]
                elif event.key == "Enter":
                    if float(app.userBox1Mass) <= 0:
                        app.userBox1Mass = "" 
                    elif app.userBox1Mass != "":
                        app.dummyUserBox1Mass = float(app.userBox1Mass)
                        app.box1Mass = app.dummyUserBox1Mass
            
            if app.textBox4Bool:
                if event.key in string.digits or event.key == ".": 
                    if app.userBox2Mass.count(".") <= 1 and (len(app.userBox2Mass) <= 18):
                        app.userBox2Mass += event.key
                elif event.key == "Backspace": app.userBox2Mass = app.userBox2Mass[:-1]
                elif event.key == "Enter":
                    if float(app.userBox2Mass) <= 0:
                        app.userBox2Mass = "" 
                    elif app.userBox2Mass != "":
                        app.dummyUserBox2Mass = float(app.userBox2Mass)
                        app.box2Mass = app.dummyUserBox2Mass

            if (app.dummyUserBox2V != None) and (app.dummyUserBox2V != None) and (app.dummyUserBox1Mass != None) and (app.dummyUserBox2Mass != None):
                app.textBox1Bool = False
                app.textBox2Bool = False
                app.textBox3Bool = False
                app.textBox4Bool = False
                app.play4 = True

        if event.key == "q":
            app.appStarted()
            app.app.setActiveMode(app.app.mainMenu)            

        if event.key == "r":
            app.appStarted()

    def doStep(app):
        #######INELASTIC##########
        if app.collisionTime > 3:
            app.play4 = False
            app.timesUp = True
        Time = 500*app.elapsedTime/3
        if Time < 950:
            if abs(app.box1V) >= 300:
                app.scale1 = 1/2
            if abs(app.box1V) < 50:
                app.scale1 = 5
            if abs(app.box2V) >= 300:
                app.scale2 = 1/2
            if abs(app.box2V) < 50:
                app.scale2 = 5
            app.redBoxList.append((Time,abs(app.box1V)*app.scale1))
            app.blueBoxList.append((Time,abs(app.box2V)*app.scale2)) 

            

        app.box1CX = app.box1CX + app.box1V*app.dt
        app.box2CX = app.box2CX + app.box2V*app.dt

        if (app.box1CX + app.box1R > app.box2CX - app.box2R) and (app.collision == False):
            app.box1CX = app.box2CX - app.box2R - app.box1R
            app.v = (app.box1Mass*app.box1V + app.box2Mass*app.box2V) / (app.box1Mass + app.box2Mass)
            app.box1V = app.v
            app.box2V = app.v
            app.collision = True
        
        if (not app.collision) and (app.box1CX < 200 + app.box1R):
            app.box1V = -app.box1V
        
        if (not app.collision) and (app.box2CX > app.width - app.box2R):
            app.box2V = -app.box2V

        if (app.collision) and (app.box1CX < 200 + app.box1R):
            app.box1V = -app.box1V
            app.box2V = -app.box2V
        
        if (app.collision) and (app.box2CX > app.width - app.box2R):
            app.box1V = -app.box1V
            app.box2V = -app.box2V
        if app.collision:
            app.collisionTime += app.dt
        app.elapsedTime += app.dt

    def drawFloorAndBoxes(app, canvas):
        canvas.create_rectangle(200,700,1600,800,fill="gray",width=2)
        canvas.create_rectangle(app.box1CX-app.box1R,app.box1CY-app.box1R,app.box1CX+app.box1R,app.box1CY+app.box1R,fill="red")
        canvas.create_rectangle(app.box2CX-app.box2R,app.box2CY-app.box2R,app.box2CX+app.box2R,app.box2CY+app.box2R,fill="blue")

    def redrawAll(app, canvas):
    #drawMainMenu(app, canvas)
        ######INELASTIC#######
        ###ANIMATION###
        if app.play4:
            app.drawFloorAndBoxes(canvas)
        if app.timesUp:
            canvas.create_rectangle(250,50,1250,500,width=3)
            canvas.create_line(300,500,300,100,width=2)
            canvas.create_line(300,450,1200,450,width=2)
            canvas.create_rectangle(650,60,660,70,fill="red")
            canvas.create_text(725,65,text="= Red Box Velocity")
            canvas.create_rectangle(890,60,900,70,fill="blue")
            canvas.create_text(975,65,text="= Blue Box Velocity")
            for i in range(len(app.redBoxList)):
                if (app.redBoxList[i][1] < 350):
                    canvas.create_oval(300+app.redBoxList[i][0]-2,450-app.redBoxList[i][1]-2,300+app.redBoxList[i][0]+2,450-app.redBoxList[i][1]+2,fill="red")
            for i in range(len(app.blueBoxList)):
                if (app.blueBoxList[i][1] < 350):
                    canvas.create_oval(300+app.blueBoxList[i][0]-2,450-app.blueBoxList[i][1]-2,300+app.blueBoxList[i][0]+2,450-app.blueBoxList[i][1]+2,fill="blue")
            canvas.create_text(340,90,text="Velocity (meters/second)",font="Times 12 bold")
            canvas.create_text(750,460,text="Time (seconds)",font="Times 12 bold")
            canvas.create_rectangle(1450,100,1600,230,fill="green",width=3)
            canvas.create_text(1525,150,text="MORE",font="Times 14 bold")
            canvas.create_text(1525,180,text="INFO",font="Times 14 bold")

            if app.infoOn:
                canvas.create_rectangle(500,275,1325,500,fill="white",width=3)
                canvas.create_text(900,400,text=app.text,font="Times 12")

        ##############
        ###SIDE MENU###
        canvas.create_rectangle(0,0,200,800,fill="MediumOrchid3",width=3)
        canvas.create_rectangle(app.textBox1X,app.textBox1Y,app.textBox1X+180,app.textBox1Y+25,fill="white",width=2)
        canvas.create_rectangle(app.textBox2X,app.textBox2Y,app.textBox2X+180,app.textBox2Y+25,fill="white",width=2)
        canvas.create_rectangle(app.textBox3X,app.textBox3Y,app.textBox3X+180,app.textBox3Y+25,fill="white",width=2)
        canvas.create_rectangle(app.textBox4X,app.textBox4Y,app.textBox4X+180,app.textBox4Y+25,fill="white",width=2)
        canvas.create_text(100,10,text="Click white boxes to type a number.")
        canvas.create_text(100,25,text="Press Backspace to delete a character.")
        canvas.create_text(100,40,text="Press Enter when you type a number.")
        canvas.create_text(100,55,text="Have fun!")
        canvas.create_text(100,425,text="Press 'r' to restart anything.")
        canvas.create_text(100,450,text="Press 'q' to go back to main menu.")
        "VELOCITY 1"
        canvas.create_text(100,130,text="Enter velocity for red box:")
        canvas.create_text(100,145,text="(-450m/s - 450 m/s):")
        canvas.create_rectangle(app.textBox1X,app.textBox1Y,app.textBox1X+180,app.textBox1Y+25,fill="white",width=2)
        canvas.create_text(100,172,text=f"{app.userBox1V}")
        "VELOCITY 2"
        canvas.create_text(100,200,text="Enter velocity for blue box:")
        canvas.create_text(100,215,text="(-450m/s - 450 m/s):")
        canvas.create_rectangle(app.textBox2X,app.textBox2Y,app.textBox2X+180,app.textBox2Y+25,fill="white",width=2)
        canvas.create_text(100,242,text=f"{app.userBox2V}")
        "MASS 1"
        canvas.create_text(100,285,text="Enter mass for red box:")
        canvas.create_rectangle(app.textBox3X,app.textBox3Y,app.textBox3X+180,app.textBox3Y+25,fill="white",width=2)
        canvas.create_text(100,312,text=f"{app.userBox1Mass}")

        "MASS 2"
        canvas.create_text(100,355,text="Enter mass for blue box:")
        canvas.create_rectangle(app.textBox4X,app.textBox4Y,app.textBox4X+180,app.textBox4Y+25,fill="white",width=2)
        canvas.create_text(100,382,text=f"{app.userBox2Mass}")

class pendulumMenu(Mode):
    def appStarted(app):
        #if app.pendulumOn:
            #########################PENDULUM ATTRIBUTES#######################
            ##########ATTRIBUTES############
            app.ballR = 100
            app.dt = 0.01
            app.g = 9.8*100
            app.elapsedTime = 0
            app.timerDelay = -50
            app.ceilingX1, app.ceilingY1 = 800, 0
            app.ceilingX2, app.ceilingY2 = 1000, 50
            app.totalEnergy = None
            app.KEPoints = []
            app.PEPoints = []
            app.EPoints = []
            app.energyScale = 1
            app.text = '''Pendulums deals with one of the most fundamental concepts in physics: conservationg of energy.
In ideal conditions, where no work is done on the bob of the pendulum besides gravity, pendulums swing back
and forth at the same height. For example, if I were to let the bob fall at an angle (and essentially at that height),
it'll rise up at that height. Also we note that at the equilibrium point (bob not at an angle), the bob is at its
fastest and at the lowest point. And at the highest point of its motion, it is at its slowest. Because this motion
is periodic, we will have our kinetic energy (which depends on velocity) and potential energy (which depends on
its height relative to the equilibrium point height) increase and decrease like a cosine wave.
            '''
            #################################
            ##########USER INPUT############# 
            app.userStringLength = ""
            app.userAngle = ""
            app.userMass = ""
            app.dummyUserStringLength = None
            app.dummyUserAngle = None
            app.dummyUserMass = None
            app.textBox1Bool = False
            app.textBox2Bool = False
            app.textBox3Bool = False
            app.textBox1X = 10
            app.textBox1Y = 160
            app.textBox2X = 10
            app.textBox2Y = 230
            app.textBox3X = 10
            app.textBox3Y = 285
            app.play2 = False
            app.timesUp = False
            app.infoOn = False
            #################################

    def timerFired(app):
        if app.play2 == True:
            app.doStep()

    def mousePressed(app, event):
        if app.timesUp == False  and app.play2 == False:
            if (app.textBox1X < event.x < app.textBox1X + 180) and (app.textBox1Y < event.y < app.textBox1Y+25):
                app.textBox1Bool = True
            else: app.textBox1Bool = False
            if (app.textBox2X < event.x < app.textBox2X + 180) and (app.textBox2Y < event.y < app.textBox2Y+25):
                app.textBox2Bool = True
            else: app.textBox2Bool = False
            if (app.textBox3X < event.x < app.textBox3X + 180) and (app.textBox3Y < event.y < app.textBox3Y+25):
                app.textBox3Bool = True
            else: app.textBox3Bool = False
        if app.timesUp == True:
            if (1450 < event.x < 1600) and (100 < event.y < 230):
                app.infoOn = not app.infoOn
    def keyPressed(app, event):
        #######PENDULUM#########
        if app.timesUp == False  and app.play2 == False:
            if app.textBox1Bool:
                if (event.key in string.digits) or (event.key == "."): 
                    if (app.userStringLength.count(".") <= 1) and (len(app.userStringLength) <= 18):
                        app.userStringLength += event.key
                elif event.key == "Backspace": app.userStringLength = app.userStringLength[:-1]
                elif event.key == "Enter":
                    if float(app.userStringLength) > 6 or float(app.userStringLength) == 0:
                        app.userStringLength = ""
                    if app.userStringLength != "":
                        app.dummyUserStringLength = float(app.userStringLength)
                        app.stringLength = app.dummyUserStringLength*100

            if app.textBox2Bool:
                if event.key in string.digits or event.key == ".": 
                    if app.userAngle.count(".") <= 1 and (len(app.userAngle) <= 18):
                        app.userAngle += event.key
                elif event.key == "Backspace": app.userAngle = app.userAngle[:-1]
                elif event.key == "Enter":
                    if float(app.userAngle) > 0.49 or float(app.userAngle) < 0:
                        app.userAngle = ""
                    elif app.userAngle != "":
                        app.dummyUserAngle = float(app.userAngle)
                        app.angle = app.dummyUserAngle*math.pi + math.pi/2

            if app.textBox3Bool:
                if event.key in string.digits or event.key == ".": 
                    if app.userMass.count(".") <= 1 and (len(app.userStringLength) <= 18):
                        app.userMass += event.key
                elif event.key == "Backspace": app.userMass = app.userMass[:-1]
                elif event.key == "Enter":
                    if float(app.userMass) > 3:
                        app.userMass = "" 
                    elif app.userMass != "":
                        app.dummyUserMass = float(app.userMass)
                        app.mass = app.dummyUserMass

            if (app.dummyUserStringLength != None) and (app.dummyUserAngle != None) and (app.dummyUserMass != None):
                app.textBox1Bool = False
                app.textBox2Bool = False
                app.textBox3Bool = False
                app.play2 = True
                app.ballCX = 900 + app.stringLength * math.sin(app.angle)
                app.ballCY = app.ceilingY2 - app.stringLength*math.cos(app.angle)
                app.omega = 0
                app.period = 2*math.pi*math.sqrt(app.stringLength/app.g)

        if event.key == "r":
            app.appStarted()

        if event.key == "q":
            app.appStarted()
            app.app.setActiveMode(app.app.mainMenu)

    def doStep(app):
        #######PENDULUM##########
        if app.elapsedTime > app.period:
            app.play2 = False
            app.timesUp = True
            app.showGraph = True
        scale = app.period / 950
        scaledTime = 50000*app.elapsedTime*scale
        if scaledTime < 950:
            app.potentialEnergy = app.mass*app.g*((app.stringLength+50)-app.ballCY)*(0.001)
            #PE = mgl(1-cos(theta))
            if app.totalEnergy == None:
                if app.potentialEnergy < 60:
                    app.energyScale = 5
                elif app.potentialEnergy > 375:
                    app.energyScale = 1/5
            updatedPE = app.potentialEnergy*app.energyScale
            if updatedPE < 375:
                app.PEPoints.append((scaledTime,updatedPE))

            if app.totalEnergy == None:
                app.totalEnergy = updatedPE #PE_max = Total Energy
            
            if app.totalEnergy < 375:
                app.EPoints.append((scaledTime, app.totalEnergy))

            app.kineticEnergy = app.totalEnergy - updatedPE
            if app.kineticEnergy < 375:
                app.KEPoints.append((scaledTime, app.kineticEnergy))

        app.alpha = (app.g/app.stringLength)*math.sin(app.angle)
        #angular acceleration of pendulum, a function of theta: a = -(g/l)sin(theta)
        app.angle = app.angle + app.omega*app.dt
        #angular kinematic equation: theta_f = theta_i + w*t
        app.omega = app.omega + app.alpha*app.dt
        #angular kinematic equation: w_f = w_i + a*t
        app.ballCX = 900 + app.stringLength*math.sin(app.angle)
        app.ballCY = app.ceilingY2 - app.stringLength*math.cos(app.angle)
        app.elapsedTime += app.dt

    def drawCeilingBallString(app, canvas):
        canvas.create_rectangle(app.ceilingX1,app.ceilingY1,app.ceilingX2,app.ceilingY2,fill="gray",width=2)
        canvas.create_line(900,app.ceilingY2,app.ballCX,app.ballCY)
        canvas.create_oval(app.ballCX-app.ballR,app.ballCY-app.ballR,app.ballCX+app.ballR,app.ballCY+app.ballR,fill="blue")

    def redrawAll(app, canvas):
        ######PENDULUM#######
        ###ANIMATION###
        if app.play2:
            app.drawCeilingBallString(canvas)
        if app.timesUp:
            canvas.create_rectangle(250,50,1250,500,width=3)
            canvas.create_line(300,450,300,100,width=2)
            canvas.create_line(300,450,1200,450,width=2)
            canvas.create_text(390,60,text="Energy (y-axis) vs Time (x-axis)",font="Times 15 bold")
            canvas.create_rectangle(650,60,660,70,fill="red")
            canvas.create_text(710,65,text="= Kinetic Energy")
            canvas.create_rectangle(770,60,780,70,fill="green")
            canvas.create_text(830,65,text="= Potential Energy")
            canvas.create_rectangle(890,60,900,70,fill="blue")
            canvas.create_text(925,65,text="= Energy")
            for i in range(len(app.EPoints)):
                canvas.create_oval(300+app.KEPoints[i][0]-2,450-app.KEPoints[i][1]-2,300+app.KEPoints[i][0]+2,450-app.KEPoints[i][1]+2,fill="red")
                canvas.create_oval(300+app.PEPoints[i][0]-2,450-app.PEPoints[i][1]-2,300+app.PEPoints[i][0]+2,450-app.PEPoints[i][1]+2,fill="green")
                canvas.create_oval(300+app.EPoints[i][0]-2,450-app.EPoints[i][1]-2,300+app.EPoints[i][0]+2,450-app.EPoints[i][1]+2,fill="blue")
            canvas.create_rectangle(1450,100,1600,230,fill="green",width=3)
            canvas.create_text(1525,150,text="MORE",font="Times 14 bold")
            canvas.create_text(1525,180,text="INFO",font="Times 14 bold")

            if app.infoOn:
                canvas.create_rectangle(500,275,1325,500,fill="white",width=3)
                canvas.create_text(900,400,text=app.text,font="Times 12")
        ##############
        ###SIDE MENU###
        canvas.create_rectangle(0,0,200,800,fill="SpringGreen3",width=3)
        canvas.create_rectangle(app.textBox1X,app.textBox1Y,app.textBox1X+180,app.textBox1Y+25,fill="white",width=2)
        canvas.create_rectangle(app.textBox2X,app.textBox2Y,app.textBox2X+180,app.textBox2Y+25,fill="white",width=2)
        canvas.create_rectangle(app.textBox3X,app.textBox3Y,app.textBox3X+180,app.textBox3Y+25,fill="white",width=2)
        canvas.create_text(100,10,text="Click white boxes to type a number.")
        canvas.create_text(100,25,text="Press Backspace to delete a character.")
        canvas.create_text(100,40,text="Press Enter when you type a number.")
        canvas.create_text(100,55,text="Have fun!")
        canvas.create_text(100,425,text="Press 'r' to restart anything.")
        canvas.create_text(100,450,text="Press 'q' to go back to main menu.")
        "STRING LENGTH"
        canvas.create_text(100,145,text="Enter string length (0 - 6.5):")
        canvas.create_rectangle(app.textBox1X,app.textBox1Y,app.textBox1X+180,app.textBox1Y+25,fill="white",width=2)
        canvas.create_text(100,172,text=f"{app.userStringLength}")
        "ANGLE"
        canvas.create_text(100,200,text="Enter constant that'll be multiplied")
        canvas.create_text(100,215,text="by pi (0.01 - 0.50):")
        canvas.create_rectangle(app.textBox2X,app.textBox2Y,app.textBox2X+180,app.textBox2Y+25,fill="white",width=2)
        canvas.create_text(100,242,text=f"{app.userAngle}")
        "MASS"
        canvas.create_text(100,270,text="Enter a mass (0.01 - 3):")
        canvas.create_rectangle(app.textBox3X,app.textBox3Y,app.textBox3X+180,app.textBox3Y+25,fill="white",width=2)
        canvas.create_text(100,297,text=f"{app.userMass}")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.mainMenu = mainMenu()
        app.orbitMenu = orbitMenu()
        app.pendulumMenu = pendulumMenu()
        app.projectileMenu = projectileMenu()
        app.inelasticMenu = inelasticMenu()
        app.setActiveMode(app.mainMenu)
        app.timerDelay = 0

app = MyModalApp(width=1600, height=800)