import pymunk.pygame_util
import pymunk
import json   


ground_y = 2100
space = pymunk.Space()      
space.gravity = 0,981
x = 1000
position = (x, 1000)
position500 = (x, 500)

body1 = pymunk.Body()
body1.position = position
body2 = pymunk.Body()       
body2.position = position
body3 = pymunk.Body()       
body3.position = position
body4 = pymunk.Body()       
body4.position = position500

def init():
    print("init")
    poly1 = pymunk.Segment(body1, (-10, 0), (10, 0), 25)
    poly1.mass = 50
    space.add(body1, poly1)
    poly1.collision_type = 3
    poly2 = pymunk.Segment(body2, (0, 0), (0 , -500), 10)
    poly2.mass = 50
    poly2.collision_type = 3
    space.add(body2, poly2)
    poly3 = pymunk.Circle(body3, 50)
    poly3.mass = 50
    poly3.friction = 1
    poly3.collision_type = 3
    poly4 = pymunk.Circle(body4, 20)
    poly4.collision_type = 2
    poly4.mass = 1000



    joint1 = pymunk.PivotJoint(body1, body2, position)
    joint1.collide_bodies = False
    joint2 = pymunk.PivotJoint(body1, body3, position)
    joint2.collide_bodies = False
    joint3 = pymunk.PivotJoint(body2, body3, position)
    joint3.collide_bodies = False
    joint5 = pymunk.PivotJoint(body2, body4, position500)
    joint5.collide_bodies = False
    joint4 = pymunk.GearJoint(body1, body2, 0, 1)
    


    ground = pymunk.Body(body_type = pymunk.Body.STATIC)
    ground.position = 0, ground_y
    poly1_1 = pymunk.Poly.create_box(ground, (15360, ground_y))
    poly1_1.friction = 5
    poly1_1.collision_type = 1
    poly2_1 = pymunk.Poly.create_box(ground, (50, ground_y*2))
    poly2_1.collision_type = 4




    try:
        space.add(ground, poly1_1, poly2_1, body1, body2, body3, body4, poly1, poly2, poly3, poly4, joint1, joint2, joint3, joint4, joint5)
    except Exception as e:
        print(e)
        try:
            space.remove(ground, poly1_1, poly2_1, body1, body2, body3, body4, poly1, poly2, poly3, poly4, joint1, joint2, joint3, joint4, joint5)
            space.add(ground, poly1_1, poly2_1, body1, body2, body3, body4, poly1, poly2, poly3, poly4, joint1, joint2, joint3, joint4, joint5)
        except Exception as e: 
            print(e)


def motor(speed, space1, body3, body1, i):
    motor = pymunk.constraints.SimpleMotor(body3, body1, speed)

    try:
        space.add(motor)
    except Exception as e:
        print(e)
        try:
            space.add(motor)
            space1.add(motor)
        except Exception as e:
            print(e)

    return motor.rate, space1

def handle_collision(space1):

    def collision(arbiter, space, data):
        with open('collision.json', "w", encoding="utf-8") as f:
            json.dump(False, f, ensure_ascii=False, indent=4)



    space1.on_collision(1, 2, begin=collision)




    with open('collision.json', 'r') as f:
        x = json.load(f)
    
    with open('collision.json', "w", encoding="utf-8") as f:
        json.dump(str(True), f, ensure_ascii=False, indent=4)

    return x

init()