import json
import asyncio
import aiofiles


from toio import *
from toio.cube.api.motor import MovementType, Speed, TargetPosition
from toio.position import CubeLocation,Point



async def move(cube, coords: tuple,angle = 90):
    await cube.api.motor.motor_control_target(
                5,
                MovementType.Curve,
                Speed(max=100),
                TargetPosition(cube_location=CubeLocation(point=Point(coords[0],coords[1]),angle=angle))
            )



# dx=43 dy=43
# (120,164) (120,207) (120,250) (120,293) (120,336)
# (163,164)
# (206,164)
# (250,164)
# (292,164)
# (335,164)
# (378,164)



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


                    if (data['controller_1']['x'] <= 215 and data['controller_2']['x'] >= 280):
                        await move(cube_3,tile_to_coords(3,2), angle=270)
                    else:
                        await move(cube_3,tile_to_coords(3,4))


                    if (data['controller_1']['x'] <= 170 and data['controller_2']['x'] >= 325):
                        await move(cube_2,tile_to_coords(2,2), angle=270)
                        await move(cube_4,tile_to_coords(4,2), angle=270)
                    else:
                        await move(cube_2,tile_to_coords(2,4))
                        await move(cube_4,tile_to_coords(4,4))


                    if (data['controller_1']['x'] <= 128 and data['controller_2']['x'] >= 370):
                        await move(cube_1,tile_to_coords(1,2), angle=270)
                        await move(cube_5,tile_to_coords(5,2), angle=270)
                    else:
                        await move(cube_1,tile_to_coords(1,4))
                        await move(cube_5,tile_to_coords(5,4))

                    await asyncio.sleep(0.3)
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