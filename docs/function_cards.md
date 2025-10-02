---
## 功能牌 (Function Cards)
---
### **错卦 (Cuo Gua)**
**核心机制:** 将基础牌的每一个爻都进行阴阳反转，变为一个全新的卦来解读。
```json
{
    "id": "function_cuo",
    "type": "function",
    "name": "错卦",
    "quantity": 4,
    "core_mechanism": {
        "description": "将基础牌的每一个爻都进行阴阳反转，变为一个全新的卦来解读。"
    },
    "metadata": {
        "image_url": "assets/images/cards/function/function_cuo.png"
    }
}
```
---
### **覆卦 (Fu Gua)**
**核心机制:** 解读基础牌时，执行爻辞的顺序颠倒，变为【天部】→【人部】→【地部】。
```json
{
    "id": "function_fu",
    "type": "function",
    "name": "覆卦",
    "quantity": 4,
    "core_mechanism": {
        "description": "解读基础牌时，执行爻辞的顺序颠倒，变为【天部】→【人部】→【地部】。"
    },
    "metadata": {
        "image_url": "assets/images/cards/function/function_fu.png"
    }
}
```
---
### **互卦 (Hu Gua)**
**核心机制:** 解读基础牌后，额外从牌库顶翻开一张牌，只执行其【人部】的效果。
```json
{
    "id": "function_hu",
    "type": "function",
    "name": "互卦",
    "quantity": 4,
    "core_mechanism": {
        "description": "解读基础牌后，额外从牌库顶翻开一张牌，只执行其【人部】的效果。"
    },
    "metadata": {
        "image_url": "assets/images/cards/function/function_hu.png"
    }
}
```
---
### **虚招 (Xu Zhao)**
**核心机制:** 本轮免疫惩罚，但亦无奖励。之后从基础牌库补充2张牌。
```json
{
    "id": "function_xu",
    "type": "function",
    "name": "虚招",
    "quantity": 4,
    "core_mechanism": {
        "description": "本轮免疫惩罚，但亦无奖励。之后从基础牌库补充2张牌。"
    },
    "metadata": {
        "image_url": "assets/images/cards/function/function_xu.png"
    }
}
```
---
### **综卦 (Zong Gua)**
**核心机制:** 将基础牌的卦象上下颠倒，变为一个全新的卦来解读。
```json
{
    "id": "function_zong",
    "type": "function",
    "name": "综卦",
    "quantity": 4,
    "core_mechanism": {
        "description": "将基础牌的卦象上下颠倒，变为一个全新的卦来解读。"
    },
    "metadata": {
        "image_url": "assets/images/cards/function/function_zong.png"
    }
}
```