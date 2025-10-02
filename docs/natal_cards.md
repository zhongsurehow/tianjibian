---
## 本命卦牌 (Natal Cards)
---
### **☰ 乾 (The Celestial)**
**被动 - 天行健:** 每当你从【天部】区域获得金币奖励时，额外多获得1金币。
**主动 - 飞龙在天:** 在你的【移动阶段】，你可以不按常规移动，而是直接将你的棋子移动到棋盘上任意一个**未被占据**的【天部】区域。
```json
{
    "id": "natal_qian",
    "type": "natal",
    "name": "乾",
    "symbol": "☰",
    "triggers": [
        {
            "condition": "ON_GAIN_RESOURCE",
            "params": {"zone": "HEAVEN", "resource": "gold"},
            "effect": {
                "description": "从【天部】获得金币时，额外+1。"
            }
        }
    ],
    "effect": {
        "description": "移动阶段，可直接移至任意未被占据的【天部】。"
    }
}
```
---
### **☷ 坤 (The Earthly)**
**被动 - 地势坤:** 你的初始生命值额外增加30点。
**主动 - 厚德载物:** 你可以立即取消一次即将对你生效的【地部】惩罚，或一次“论道”事件的失败惩罚。
```json
{
    "id": "natal_kun",
    "type": "natal",
    "name": "坤",
    "symbol": "☷",
    "triggers": [
        {
            "condition": "ON_GAME_START",
            "effect": {
                "description": "初始生命值+30。"
            }
        }
    ],
    "effect": {
        "description": "立即取消一次【地部】惩罚或“论道”失败惩罚。"
    }
}
```
---
### **☳ 震 (The Arousing)**
**被动 - 洊雷:** 每当有其他玩家的金币或生命值因你的牌效果而减少时，你额外获得2金币。
**主动 - 震惊百里:** 在【放牌阶段】，你可以打出两张不同的【基础牌】。在【解读阶段】，你可以选择其中一张的效果来执行。
```json
{
    "id": "natal_zhen",
    "type": "natal",
    "name": "震",
    "symbol": "☳",
    "triggers": [
        {
            "condition": "ON_CAUSE_LOSS",
            "effect": {
                "description": "因你的牌效果使他人损失时，你额外+2金币。"
            }
        }
    ],
    "effect": {
        "description": "放牌阶段，可盖放两张基础牌，解读时二选一。"
    }
}
```
---
### **☴ 巽 (The Gentle)**
**被动 - 随风:** 在你的【移动阶段】，你可以选择额外移动一格（即总共移动两格）。
**主动 - 无孔不入:** 在【结算阶段】，你可以选择一个【天部】区域，获得其上一半（向上取整）的累积金币，而不需要移动到那里。
```json
{
    "id": "natal_xun",
    "type": "natal",
    "name": "巽",
    "symbol": "☴",
    "triggers": [
        {
            "condition": "ON_PHASE_START",
            "params": {"phase": "MOVEMENT"},
            "effect": {
                "description": "移动阶段，可选择额外移动一格。"
            }
        }
    ],
    "effect": {
        "description": "结算阶段，可获得任一【天部】区域一半的累积金币。"
    }
}
```
---
### **☵ 坎 (The Abyssal)**
**被动 - 习坎:** 当你的棋子停留在“水”属性（坎宫）或“木”属性（震宫、巽宫）的区域时，你发起的“论道”笔画数-1。
**主动 - 险中求胜:** 在【解读阶段】轮到你之前，你可以声明使用此技能。在本轮，你受到的所有金币惩罚减半，但获得的所有金币奖励也减半。
```json
{
    "id": "natal_kan",
    "type": "natal",
    "name": "坎",
    "symbol": "☵",
    "triggers": [
        {
            "condition": "ON_PLAYER_ACTION",
            "params": {"action_type": "TRIGGER_DEBATE", "zone_type": ["WATER", "WOOD"]},
            "effect": {
                "description": "在水或木属性区域，你发起的“论道”笔画数-1。"
            }
        }
    ],
    "effect": {
        "description": "本轮你的金币奖惩减半。"
    }
}
```
---
### **☲ 离 (The Luminous)**
**被动 - 附丽:** 在【天时阶段】，若“流年干支”任一为“火”，你可以额外抽取一张【基础牌】。
**主动 - 光明普照:** 在【解读阶段】，你可以选择不执行你自己牌的【核心机制效果】，而是复制场上另一名玩家本轮已经解读过的【核心机制效果】。
```json
{
    "id": "natal_li",
    "type": "natal",
    "name": "离",
    "symbol": "☲",
    "triggers": [
        {
            "condition": "ON_PHASE_START",
            "params": {"phase": "YEAR_STEM", "stem": "FIRE"},
            "effect": {
                "description": "若流年干支为火，额外抽1张基础牌。"
            }
        }
    ],
    "effect": {
        "description": "复制场上另一名玩家本轮已解读的爻辞效果。"
    }
}
```
---
### **☶ 艮 (The Keeping Still)**
**被动 - 兼山:** 你的生命值上限额外增加20。每当你受到超过10点的单次生命值伤害时，该伤害减少5点。
**主动 - 艮其背:** 在【解读阶段】，你可以指定场上任意一名玩家，该玩家本轮不能执行其牌的【核心机制效果】。
```json
{
    "id": "natal_gen",
    "type": "natal",
    "name": "艮",
    "symbol": "☶",
    "triggers": [
        {
            "condition": "ON_GAME_START",
            "effect": {
                "description": "生命上限+20，受到的单次>10的伤害-5。"
            }
        }
    ],
    "effect": {
        "description": "指定一名玩家，其本轮不能执行爻辞效果。"
    }
}
```
---
### **☱ 兑 (The Joyous)**
**被动 - 丽泽:** 每当有玩家（包括你自己）自愿为基金补充金币时，你获得补充总额的20%（向上取整）作为奖励。
**主动 - 和悦:** 你可以发起一次“和谈”，指定一名玩家。在本轮的【解读阶段】，你们双方可以将各自的金币收益与损失合并后平分。
```json
{
    "id": "natal_dui",
    "type": "natal",
    "name": "兑",
    "symbol": "☱",
    "triggers": [
        {
            "condition": "ON_RESOURCE_CHANGE",
            "params": {"resource": "gold", "change_type": "FUND_REPLENISH"},
            "effect": {
                "description": "任一玩家为基金补充金币时，你获得其补充额的20%。"
            }
        }
    ],
    "effect": {
        "description": "指定一名玩家，本轮你们双方金币得失合并后平均分。"
    }
}
```