# -*- coding: utf-8 -*-
# Правила для системы интеллектуального видеомониторинга

from symbolic.rule_engine import Rule, RulePriority

def get_video_rules() -> list:
    """Получение 5 правил безопасности для видеомониторинга."""
    return[
        Rule(
            rule_id="VID_001", name="Ночное проникновение",
            condition=lambda f: f.get("object") == "person" and f.get("geozone") == "Периметр" and f.get("is_night", False),
            conclusion="КРИТИЧЕСКАЯ ТРЕВОГА: Вызов ГБР",
            priority=RulePriority.CRITICAL,
            description="Человек в периметре в ночное время", domain="video_surveillance"
        ),
        Rule(
            rule_id="VID_002", name="Оставленный багаж",
            condition=lambda f: f.get("object") in ["backpack", "suitcase"] and f.get("time_unattended_sec", 0) > 60,
            conclusion="ТРЕВОГА: Проверить на ВУ",
            priority=RulePriority.HIGH,
            description="Предмет без владельца более 60с", domain="video_surveillance"
        ),
        Rule(
            rule_id="VID_003", name="Транспорт в пешеходной зоне",
            condition=lambda f: f.get("object") in ["car", "truck"] and f.get("geozone") == "Пешеходная аллея",
            conclusion="ПРЕДУПРЕЖДЕНИЕ: Оповестить парковщика",
            priority=RulePriority.MEDIUM,
            description="Транспорт заехал в пешеходную зону", domain="video_surveillance"
        ),
        Rule(
            rule_id="VID_004", name="Массовое скопление",
            condition=lambda f: f.get("people_count", 0) > 10 and f.get("geozone") == "Узкий коридор",
            conclusion="ИНФО: Включить вентиляцию",
            priority=RulePriority.LOW,
            description="Более 10 человек в узком пространстве", domain="video_surveillance"
        ),
        Rule(
            rule_id="VID_005", name="Обнаружение оружия",
            condition=lambda f: f.get("weapon_detected", False) == True,
            conclusion="КРИТИЧЕСКАЯ ТРЕВОГА: БЛОКИРОВКА ДВЕРЕЙ",
            priority=RulePriority.CRITICAL,
            description="Нейросеть детектировала оружие", domain="video_surveillance"
        )
    ]