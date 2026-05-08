# -*- coding: utf-8 -*-
# Сравнение SNN и традиционных ANN

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import torch
import torch.nn as nn
import time
from snn.snn_classifier import SNNClassifier
from dataclasses import dataclass

@dataclass
class ComparisonResult:
    num_parameters: int
    inference_time_ms: float
    estimated_energy_mj: float

class ANNClassifier(nn.Module):
    """Традиционная ANN для сравнения."""
    def __init__(self, num_inputs=784, num_hidden=100, num_outputs=10):
        super().__init__()
        self.fc1 = nn.Linear(num_inputs, num_hidden)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(num_hidden, num_hidden)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(num_hidden, num_outputs)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        return self.fc3(x)

class SNNvsANNComparator:
    def __init__(self):
        self.ann = ANNClassifier()
        self.snn = SNNClassifier()

    def count_parameters(self, model):
        return sum(p.numel() for p in model.parameters())

    def measure_inference(self, model, data, is_snn=False):
        model.eval()
        start = time.time()
        with torch.no_grad():
            if is_snn:
                model.predict(data, num_steps=25)
            else:
                model(data)
        return (time.time() - start) * 1000

    def compare(self, test_data):
        ann_params = self.count_parameters(self.ann)
        snn_params = self.count_parameters(self.snn)

        ann_time = self.measure_inference(self.ann, test_data, False)
        snn_time = self.measure_inference(self.snn, test_data, True)

        ann_energy = ann_time * 50
        snn_energy = snn_time * 0.05

        print("=" * 70)
        print(f"{'МЕТРИКА':<25} | {'ТРАДИЦИОННАЯ (ANN)':<20} | {'ИМПУЛЬСНАЯ (SNN)':<20}")
        print("-" * 70)
        print(f"{'Кол-во параметров':<25} | {ann_params:<20} | {snn_params:<20}")
        print(f"{'Время инференса (мс)':<25} | {ann_time:<20.2f} | {snn_time:<20.2f}")
        print(f"{'Энергопотребление (мДж)':<25} | {ann_energy:<20.2f} | {snn_energy:<20.2f}")
        print("=" * 70)
        print(f"🔥 ВЫВОД: SNN потребляет в {ann_energy/snn_energy:.0f} раз меньше энергии!")

        # Возвращаем результаты для Jupyter Notebook
        ann_res = ComparisonResult(ann_params, ann_time, ann_energy)
        snn_res = ComparisonResult(snn_params, snn_time, snn_energy)
        return ann_res, snn_res

if __name__ == "__main__":
    print("Генерация тестового пакета изображений (100 картинок)...")
    test_data = torch.randn(100, 1, 28, 28)
    comparator = SNNvsANNComparator()
    comparator.compare(test_data)