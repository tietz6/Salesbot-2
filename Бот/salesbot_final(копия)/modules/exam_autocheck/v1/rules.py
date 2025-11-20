
RULES = {
    "greeting": ["здравствуйте", "добрый день", "добрый вечер", "приветствую"],
    "qualification": ["уточните", "подскажите", "помогите понять", "расскажите"],
    "offer": ["предлагаю", "могу предложить", "вариант", "пакет"],
    "closing": ["готовы оплатить", "перейдем к оплате", "сейчас выставлю счет"]
}

def check_rules(text: str):
    text = text.lower()
    score = 0
    details = {}
    for k,words in RULES.items():
        hits = sum(1 for w in words if w in text)
        details[k] = hits
        score += hits
    return score, details
