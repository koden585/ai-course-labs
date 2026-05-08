# -*- coding: utf-8 -*-
# Реализация LIF-нейрона (Leaky Integrate-and-Fire)

import torch
import snntorch as snn
import matplotlib.pyplot as plt
from typing import Tuple, Optional
import os


class LIFNeuron:
    """LIF-нейрон (Leaky Integrate-and-Fire) на snntorch."""

    def __init__(self, beta: float = 0.95, threshold: float = 1.0):
        self.beta = beta
        self.threshold = threshold

        # Создание LIF-нейрона
        self.lif = snn.Leaky(
            beta=beta,
            threshold=threshold
        )

    def simulate(self, input_current: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Симуляция работы нейрона."""
        # ПРАВИЛЬНАЯ инициализация: создаем пустой мембранный потенциал
        mem = self.lif.init_leaky()

        num_steps = len(input_current)
        spikes_record = []
        mem_record = []

        # Симуляция по шагам времени
        for step in range(num_steps):
            # ПРАВИЛЬНЫЙ вызов: передаем ток И текущее состояние мембраны
            spike, mem = self.lif(input_current[step], mem)
            spikes_record.append(spike)
            mem_record.append(mem)

        spikes = torch.stack(spikes_record)
        mem = torch.stack(mem_record)

        return spikes, mem

    def visualize(self, input_current: torch.Tensor, spikes: torch.Tensor, mem: torch.Tensor, save_path: str):
        """Визуализация активности нейрона."""
        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        time_axis = range(len(input_current))

        # График 1: Входной ток
        axes[0].plot(time_axis, input_current.numpy(), 'b-', linewidth=2)
        axes[0].set_ylabel('Входной ток', fontsize=10)
        axes[0].set_title('Активность биологического LIF-нейрона', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)

        # График 2: Мембранный потенциал (накопление заряда)
        axes[1].plot(time_axis, mem.detach().numpy(), 'g-', linewidth=2, label='Мембрана')
        axes[1].axhline(y=self.threshold, color='r', linestyle='--', label='Порог (Threshold)')
        axes[1].set_ylabel('Потенциал (мВ)', fontsize=10)
        axes[1].legend(loc='upper right')
        axes[1].grid(True, alpha=0.3)

        # График 3: Спайки (Импульсы)
        axes[2].scatter(time_axis, spikes.detach().numpy(), c='black', marker='|', s=100, label='Спайки')
        axes[2].set_ylabel('Импульс', fontsize=10)
        axes[2].set_xlabel('Время (мс)', fontsize=10)
        axes[2].set_ylim(-0.1, 1.1)
        axes[2].legend(loc='upper right')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✅ График сохранён: {save_path}")
        plt.close(fig)


if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ БИОЛОГИЧЕСКОГО LIF-НЕЙРОНА")
    print("=" * 60)

    neuron = LIFNeuron(beta=0.90, threshold=1.0)

    # Создаем тестовый ток (100 миллисекунд)
    num_steps = 100
    input_current = torch.zeros(num_steps)

    # Бьем нейрон током в разные моменты времени
    input_current[10:20] = 1.5  # Слабый ток
    input_current[40:60] = 2.5  # Сильный ток
    input_current[80:90] = 0.8  # Ток ниже порога

    spikes, mem = neuron.simulate(input_current)

    total_spikes = spikes.sum().item()
    print(f"Всего сгенерировано импульсов (спайков): {total_spikes}")

    # Сохраняем график в папку docs
    save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs'))
    os.makedirs(save_dir, exist_ok=True)

    neuron.visualize(input_current, spikes, mem, save_path=os.path.join(save_dir, 'lif_neuron_activity.png'))