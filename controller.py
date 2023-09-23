import json
import asyncio
import aiofiles

from toio import *
from toio.cube.api.motor import MovementType, Speed, TargetPosition
from toio.position import CubeLocation,Point


async def read_id():
    device_list = await BLEScanner.scan(2)
    assert len(device_list)

    print(device_list)

    cube_1 = ToioCoreCube(device_list[0].interface)
    cube_2 = ToioCoreCube(device_list[1].interface)
    await cube_1.connect()
    await cube_2.connect()


    await cube_1.api.motor.motor_control_target(
        10,
        MovementType.CurveWithoutReverse ,
        Speed(max=200),
        TargetPosition(cube_location=CubeLocation(point=Point(236,250), angle=0))
    )

    await cube_2.api.motor.motor_control_target(
        10,
        MovementType.CurveWithoutReverse ,
        Speed(max=200),
        TargetPosition(cube_location=CubeLocation(point=Point(260,250), angle=180))
    )

    try:
        while True:
            pos_cube_1 = await cube_1.api.id_information.read()
            pos_cube_2 = await cube_2.api.id_information.read()

            data = {
                "controller_1": {
                    "x": pos_cube_1.center.point.x,
                    "y": pos_cube_1.center.point.y,
                    "angle": pos_cube_1.center.angle
                } if pos_cube_1 and 'center' in dir(pos_cube_1) else None,
                "controller_2": {
                    "x": pos_cube_2.center.point.x,
                    "y": pos_cube_2.center.point.y,
                    "angle": pos_cube_2.center.angle
                } if pos_cube_2 and 'center' in dir(pos_cube_2) else None
            }

            async with aiofiles.open('./controller.json', mode='w') as file:
                content = json.dumps(data, indent=4)
                await file.write(content)


            
    except KeyboardInterrupt:
        print('interrupted!')
        await cube_1.disconnect()
        await cube_2.disconnect()

if __name__ == "__main__":
    asyncio.run(read_id())