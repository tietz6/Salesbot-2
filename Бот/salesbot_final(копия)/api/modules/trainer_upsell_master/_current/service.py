
def advise(context: dict)->dict:
    stage = (context or {}).get("stage","")
    if stage in ("demo","payment"):
        step = "double_demo_push"
    elif stage == "upsell":
        step = "ladder_2_to_4"
    else:
        step = "pre_texts_warmup"
    return {"next_step": step, "hint": "Используй тёплую формулировку бренда без давления."}
