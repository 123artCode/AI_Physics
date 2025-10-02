import torch.optim as optim
import torch
from . import Model as M
from numpy import random
import game.Main
import torch.nn.functional as F
import pygame
import pymunk.pygame_util
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import wandb
import io





def training(camera_position, i):

    scene = pygame.Surface((1920*4, 1080*4))
    screen = pygame.display.set_mode((1920, 1080))
    draw_options = pymunk.pygame_util.DrawOptions(scene)
    draw_options.shape_static_color = (255, 255, 255)
    draw_options.shape_dynamic_color = (255, 0, 0)
    running = True
    i = 0

    while running:
        i += 1
        net = M.DQN(10, 3)
        model = net    
        model.load_state_dict(torch.load('./model', weights_only=True))
        model.eval()
        optimizer = optim.Adam(model.parameters(), lr=0.01)

        state = torch.randn(10)

        raw_logits = model(state)
        action_probs = F.softmax(raw_logits, dim=-1)

        if torch.isnan(action_probs).any():
            print("NaN detected in action_probs:", action_probs)
            action_probs = torch.ones_like(action_probs) / action_probs.numel()






        action = torch.multinomial(action_probs, 1)
        reward = game.Main.motor_manager(draw_options, scene, screen, camera_position, False, i, action.item())[0]

        loss = -torch.log(action_probs[action]) * reward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        restart = game.Main.handle_collision(game.Main.motor_manager(draw_options, scene, screen, camera_position, False, action.item())[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart = False


        if restart == False:
            print(i)
            torch.save(model.state_dict(), './model')
            game.Main.init(i)
            running = False








def plot_loss_landscape(model, loss_fn, dataloader, num_points=20, alpha=1.0):
    # Store original parameters
    original_params = [p.clone() for p in model.parameters()]
    
    # Calculate two random directions
    direction1 = [torch.randn_like(p) for p in model.parameters()]
    direction2 = [torch.randn_like(p) for p in model.parameters()]
    
    # Normalize directions
    norm1 = torch.sqrt(sum(torch.sum(d**2) for d in direction1))
    norm2 = torch.sqrt(sum(torch.sum(d**2) for d in direction2))
    direction1 = [d / norm1 for d in direction1]
    direction2 = [d / norm2 for d in direction2]
    
    # Create grid
    x = np.linspace(-alpha, alpha, num_points)
    y = np.linspace(-alpha, alpha, num_points)
    X, Y = np.meshgrid(x, y)
    
    # Calculate loss for each point
    Z = np.zeros_like(X)
    for i in range(num_points):
        for j in range(num_points):
            # Update model parameters
            for p, d1, d2 in zip(model.parameters(), direction1, direction2):
                p.data = p.data + X[i,j] * d1 + Y[i,j] * d2
            
            # Calculate loss
            total_loss = 0
            num_batches = 0
            for batch in dataloader:
                inputs, targets = batch
                outputs = model(inputs)
                loss = loss_fn(outputs, targets)
                total_loss += loss.item()
                num_batches += 1
            Z[i,j] = total_loss / num_batches
            
            # Reset model parameters
            for p, orig_p in zip(model.parameters(), original_params):
                p.data = orig_p.clone()
    
    # Plot the loss landscape
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('Direction 1')
    ax.set_ylabel('Direction 2')
    ax.set_zlabel('Loss')
    ax.set_title('Loss Landscape')
    fig.colorbar(surf)
    
    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Close the plot to free up memory
    plt.close(fig)
    
    return buf

def log_loss_landscape(model, loss_fn, dataloader, step):
    # Generate the loss landscape plot
    buf = plot_loss_landscape(model, loss_fn, dataloader)
    
    # Log the plot to wandb
    wandb.log({
        "loss_landscape": wandb.Image(buf, caption="Loss Landscape"),
        "step": step
    })