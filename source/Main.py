import ai.Training
import game.Main


camera_position = [-250, -250]

for _ in range(0):
    game.Main.control_self(camera_position)

for i in range(3):
    
    ai.Training.training(camera_position, i)
