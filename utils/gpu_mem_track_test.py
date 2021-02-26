import torch
import inspect

from torchvision import models
from gpu_mem_track import MemTracker  # 引用显存跟踪代码

device = torch.device('cuda:0')

frame = inspect.currentframe()
gpu_tracker = MemTracker(frame)      # 创建显存检测对象

gpu_tracker.track()                  # 开始检测