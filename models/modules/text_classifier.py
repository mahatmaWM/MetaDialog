#!/usr/bin/env python
from typing import Tuple, Union, List, Dict
import torch
from torch import nn


class SingleLabelTextClassifier(torch.nn.Module):

    def __init__(self):
        super(SingleLabelTextClassifier, self).__init__()
        self.criterion = nn.CrossEntropyLoss()

    def forward(self,
                logits: torch.Tensor,
                mask: torch.Tensor,
                tags: torch.Tensor) -> torch.Tensor:
        """
        :param logits: (batch_size, 1, n_tags)
        :param mask: (batch_size, 1)
        :param tags: (batch_size, 1)
        :return:
        """
        logits = logits.squeeze(-2)
        tags = tags.squeeze(-2)
        loss = self.criterion(logits, tags)
        return loss

    def decode(self, logits):
        ret = []
        for logit in logits:
            tmp = []
            for pred in logit:
                # TODO 这里增加一个阈值判断
                # tmp.append(int(torch.argmax(pred)))
                tmp.append(int(torch.argmax(pred) if torch.max(pred) > 0.4 else -1))
            ret.append(tmp)
        return ret


