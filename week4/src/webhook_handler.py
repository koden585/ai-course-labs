# -*- coding: utf-8 -*-
import requests
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class WorkflowClient:
    def __init__(self):
        # Используем тестовый вебхук, чтобы видеть анимацию в n8n
        self.webhook_url = "http://localhost:5678/webhook-test/security-incident"

    def send_yolo_detection(self, payload: dict):
        logger.info(f"Отправка данных от YOLO: {json.dumps(payload, ensure_ascii=False)}")
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.webhook_url, headers=headers, json=payload, timeout=30)
            logger.info(f"n8n принял данные! Статус: {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка отправки: {e}")


if __name__ == "__main__":
    print("=" * 80)
    print("ТЕСТИРОВАНИЕ WORKFLOW: ИНТЕЛЛЕКТУАЛЬНЫЙ ВИДЕОМОНИТОРИНГ (YOLO)")
    print("=" * 80)

    client = WorkflowClient()

    # Имитируем вывод нейросети YOLO
    yolo_event = {
        "camera_id": "CAM-01_Ограждение",
        "geozone": "Охранная зона А (Периметр)",
        "object_class": "person",
        "confidence": 0.94,
        "timestamp": datetime.now().isoformat()
    }

    client.send_yolo_detection(yolo_event)