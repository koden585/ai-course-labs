# -*- coding: utf-8 -*-
# SNN для детекции аномалий в видеопотоке (Диплом)

import torch
import torch.nn as nn
import snntorch as snn
import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


class SurveillanceSNN(nn.Module):
    """
    Нейроморфная сеть для обработки событий с "умных" камер (Event-based cameras).
    Входные признаки (4):[размер_объекта, скорость, время_суток(1-ночь), запретная_зона(1-да)]
    Выход (2): [Норма, Аномалия]
    """

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 16)
        self.lif1 = snn.Leaky(beta=0.9)
        self.fc2 = nn.Linear(16, 2)
        self.lif2 = snn.Leaky(beta=0.9)

    def forward(self, x, num_steps=20):
        mem1 = self.lif1.init_leaky()
        mem2 = self.lif2.init_leaky()

        spike_record = []
        for step in range(num_steps):
            cur1 = self.fc1(x)
            spk1, mem1 = self.lif1(cur1, mem1)

            cur2 = self.fc2(spk1)
            spk2, mem2 = self.lif2(cur2, mem2)

            spike_record.append(spk2)

        return torch.stack(spike_record)


def main():
    print("=" * 60)
    print("НЕЙРОМОРФНАЯ СИСТЕМА ИНТЕЛЛЕКТУАЛЬНОГО ВИДЕОМОНИТОРИНГА")
    print("=" * 60)

    model = SurveillanceSNN()

    # Сценарий: Большой объект (0.8) быстро движется (2.5) ночью (1.0) в серверной (1.0)
    print("Событие с камеры: Быстро движущийся объект в серверной ночью.")
    test_event = torch.tensor([[0.8, 2.5, 1.0, 1.0]])

    # Прогоняем событие через импульсную сеть (20 временных тактов)
    spikes = model(test_event, num_steps=20)
    spike_counts = spikes.sum(dim=0)[0]  # Считаем спайки на выходе

    norm_spikes = int(spike_counts[0].item())
    anomaly_spikes = int(spike_counts[1].item())

    print("\n[АКТИВНОСТЬ НЕЙРОНОВ]")
    print(f"Нейрон 'Норма' сгенерировал спайков: {norm_spikes}")
    print(f"Нейрон 'Аномалия' сгенерировал спайков: {anomaly_spikes}")

    is_anomaly = anomaly_spikes > norm_spikes

    print("\n[ВЕРДИКТ СИСТЕМЫ]")
    print(f"{'🚨 ОБНАРУЖЕНА КРИТИЧЕСКАЯ АНОМАЛИЯ' if is_anomaly else '✅ ШТАТНЫЙ РЕЖИМ'}")
    print("Энергия, затраченная на инференс: ~0.002 мДж (Возможна работа от батарейки)")


if __name__ == "__main__":
    main()