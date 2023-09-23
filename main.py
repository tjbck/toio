import json
import asyncio
import aiofiles
import random


from toio import *
from toio.cube.api.motor import MovementType, Speed, TargetPosition
from toio.position import CubeLocation,Point



async def move(cube, coords: tuple,angle = 90):

    # MovementType.Linear
    try:
        cube_sensor = await cube.api.sensor.read()
        print(cube_sensor)
    except:
        pass
    await cube.api.motor.motor_control_target(
                5,
                random.randint(0,2),
                Speed(max=150, speed_change_type=3),
                TargetPosition(cube_location=CubeLocation(point=Point(coords[0],coords[1]),angle=angle))
            )



def tile_to_coords(tile_x: int, tile_y: int):
    # (0,0) = (120, 336)
    # (6,0) = (378, 336)
    # (6,4) = (378, 164)
    if tile_x >= 0 and tile_x <= 6:
        x = 120 + 43*tile_x
    else:
        x = 250

    if tile_y >= 0 and tile_y <= 6:
        y = 336 - 43*tile_y
    else:
        y = 250


    return (x,y)

async def move_to_location():
    device_list = await BLEScanner.scan(5)
    assert len(device_list)

    print(device_list)

    cube_1 = ToioCoreCube(device_list[0].interface)
    cube_2 = ToioCoreCube(device_list[1].interface)
    cube_3 = ToioCoreCube(device_list[2].interface)
    cube_4 = ToioCoreCube(device_list[3].interface)
    cube_5 = ToioCoreCube(device_list[4].interface)

    await cube_1.connect()
    await cube_2.connect()
    await cube_3.connect()
    await cube_4.connect()
    await cube_5.connect()


    await move(cube_1,tile_to_coords(1,4))
    await move(cube_2,tile_to_coords(2,4))
    await move(cube_3,tile_to_coords(3,4))
    await move(cube_4,tile_to_coords(4,4))
    await move(cube_5,tile_to_coords(5,4))

    try:
        while True:

            try:
                async with aiofiles.open('./controller.json', mode='r') as file:
                    content = await file.read()
                    data = json.loads(content)


                print(data)

                if(data['controller_1'] != None and data['controller_2'] != None):


                    x_distance = data['controller_2']['x'] - data['controller_1']['x']
                    y_distance = data['controller_2']['y'] - data['controller_1']['y']


                    distance = (x_distance ** 2 + y_distance **2)**(1/2)

                    if(distance >= 235):
                        await move(cube_1,(int(x_distance*0.16 + data['controller_1']['x']),int(y_distance*0.16 + data['controller_1']['y'])), angle=270)
                        await move(cube_2,(int(x_distance*0.32 + data['controller_1']['x']),int(y_distance*0.32 + data['controller_1']['y'])), angle=270)
                        await move(cube_3,(int(x_distance*0.5 + data['controller_1']['x']),int(y_distance*0.5 + data['controller_1']['y'])), angle=270)
                        await move(cube_4,(int(x_distance*0.66 + data['controller_1']['x']),int(y_distance*0.66 + data['controller_1']['y'])), angle=270)
                        await move(cube_5,(int(x_distance*0.82 + data['controller_1']['x']),int(y_distance*0.82 + data['controller_1']['y'])), angle=270)

                    elif(distance >= 195):
                        await move(cube_1,(int(x_distance*0.2 + data['controller_1']['x']),int(y_distance*0.2 + data['controller_1']['y'])), angle=270)
                        await move(cube_2,(int(x_distance*0.4 + data['controller_1']['x']),int(y_distance*0.4 + data['controller_1']['y'])), angle=270)
                        await move(cube_3,(int(x_distance*0.6 + data['controller_1']['x']),int(y_distance*0.6 + data['controller_1']['y'])), angle=270)
                        await move(cube_4,(int(x_distance*0.8 + data['controller_1']['x']),int(y_distance*0.8 + data['controller_1']['y'])), angle=270)
                        await move(cube_5,tile_to_coords(5,4))
                    elif(distance >= 155):
                        await move(cube_2,(int(x_distance*0.25 + data['controller_1']['x']),int(y_distance*0.25 + data['controller_1']['y'])), angle=270)
                        await move(cube_3,(int(x_distance*0.5 + data['controller_1']['x']),int(y_distance*0.5 + data['controller_1']['y'])), angle=270)
                        await move(cube_4,(int(x_distance*0.75 + data['controller_1']['x']),int(y_distance*0.75 + data['controller_1']['y'])), angle=270)
                        await move(cube_1,tile_to_coords(1,4))
                        await move(cube_5,tile_to_coords(5,4))
                    elif(distance >= 115):
                        await move(cube_2,(int(x_distance*0.33 + data['controller_1']['x']),int(y_distance*0.33 + data['controller_1']['y'])), angle=270)
                        await move(cube_3,(int(x_distance*0.66 + data['controller_1']['x']),int(y_distance*0.66 + data['controller_1']['y'])), angle=270)
                        await move(cube_4,tile_to_coords(4,4))
                        await move(cube_1,tile_to_coords(1,4))
                        await move(cube_5,tile_to_coords(5,4))
                    elif(distance >= 75):
                        await move(cube_3,(int(x_distance*0.5 + data['controller_1']['x']),int(y_distance*0.5 + data['controller_1']['y'])), angle=270)
                        await move(cube_2,tile_to_coords(2,4))
                        await move(cube_4,tile_to_coords(4,4))
                        await move(cube_1,tile_to_coords(1,4))
                        await move(cube_5,tile_to_coords(5,4))
                    else:
                        await move(cube_3,tile_to_coords(3,4))
                        await move(cube_2,tile_to_coords(2,4))
                        await move(cube_4,tile_to_coords(4,4))
                        await move(cube_1,tile_to_coords(1,4))
                        await move(cube_5,tile_to_coords(5,4))

                       
                
                    await asyncio.sleep(0.2)
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        print('interrupted!')
        await cube_1.disconnect()
        await cube_2.disconnect()
        await cube_3.disconnect()
        await cube_4.disconnect()
        await cube_5.disconnect()




if __name__ == "__main__":
    asyncio.run(move_to_location())