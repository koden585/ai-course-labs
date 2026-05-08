# -*- coding: utf-8 -*-
# SNN классификатор на snntorch

import torch
import torch.nn as nn
import snntorch as snn


class SNNClassifier(nn.Module):
    """Импульсная нейронная сеть для классификации."""

    def __init__(self, num_inputs=784, num_hidden=100, num_outputs=10, beta=0.95):
        super().__init__()
        self.fc1 = nn.Linear(num_inputs, num_hidden)
        self.lif1 = snn.Leaky(beta=beta)

        self.fc2 = nn.Linear(num_hidden, num_hidden)
        self.lif2 = snn.Leaky(beta=beta)

        self.fc3 = nn.Linear(num_hidden, num_outputs)
        self.lif3 = snn.Leaky(beta=beta)

    def forward(self, x: torch.Tensor, num_steps: int = 25):
        # Правильная инициализация мембран
        mem1 = self.lif1.init_leaky()
        mem2 = self.lif2.init_leaky()
        mem3 = self.lif3.init_leaky()

        spike_record = []
        x = x.view(x.size(0), -1)  # Выравнивание картинки в вектор

        for step in range(num_steps):
            cur1 = self.fc1(x)
            spk1, mem1 = self.lif1(cur1, mem1)

            cur2 = self.fc2(spk1)
            spk2, mem2 = self.lif2(cur2, mem2)

            cur3 = self.fc3(spk2)
            spk3, mem3 = self.lif3(cur3, mem3)

            spike_record.append(spk3)

        return torch.stack(spike_record)

    def predict(self, x: torch.Tensor, num_steps: int = 25):
        self.eval()
        with torch.no_grad():
            spike_record = self.forward(x, num_steps)
            spike_count = spike_record.sum(dim=0)
            return spike_count.argmax(dim=1)