import torch
import shutil
import os


def log_gradient_norm(model, writer, step, mode, norm_type=2):
    """Writes model param's gradients norm to tensorboard"""
    total_norm = 0
    for p in model.parameters():
        if p.requires_grad:
            param_norm = p.grad.data.norm(norm_type)
            total_norm += param_norm.item() ** 2
    total_norm = total_norm ** (1. / 2)
    writer.add_scalar(f"Gradient/{mode}", total_norm, step)


def save_checkpoint(model, start_time, epoch):
    """Saves specified model checkpoint."""
    target_dir = os.path.join("checkpoints", f"{start_time}")
    os.makedirs(target_dir, exist_ok=True)
    # Save model weights
    save_path = os.path.join(target_dir, f"model_{epoch}.pth")
    torch.save(model.state_dict(), save_path)
    print("Model saved to:", save_path)

    # Save model configuration
    if not os.path.exists(os.path.join(target_dir, "config.json")):
        shutil.copy("config.json", os.path.join(target_dir, "config.json"))
        shutil.copy(
            "src/models/classifier.py", os.path.join(target_dir, "classifier.py")
        )
        shutil.copy(
            "src/models/transformer.py", os.path.join(target_dir, "transformer.py")
        )
        shutil.copy("src/trainer/util.py", os.path.join(target_dir, "utils.py"))
