
import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_translation_impact(queries_path, predictions_path, ground_truth_path, top_k=5):
    queries = load_json(queries_path)
    predictions = load_json(predictions_path)
    ground_truth = load_json(ground_truth_path)

    examples = {
        "correct_translation_hit": [],
        "correct_translation_miss": [],
        "wrong_translation_hit": [],
        "wrong_translation_miss": []
    }

    for q in queries:
        qid = str(q["qid"])
        zh = q.get("query_zh_gpt", "").strip()
        en = q.get("query_en", "").strip()
        gt = set(map(str, ground_truth.get(qid, [])))

        for model_name, model_preds in predictions.items():
            pred_topk = model_preds.get(qid, [])[:top_k]
            hit = any(pid in gt for pid in pred_topk)

            is_translation_good = (len(zh) > 0 and zh != en)

            if is_translation_good and hit:
                examples["correct_translation_hit"].append((qid, en, zh, pred_topk, list(gt)))
            elif is_translation_good and not hit:
                examples["correct_translation_miss"].append((qid, en, zh, pred_topk, list(gt)))
            elif not is_translation_good and hit:
                examples["wrong_translation_hit"].append((qid, en, zh, pred_topk, list(gt)))
            else:
                examples["wrong_translation_miss"].append((qid, en, zh, pred_topk, list(gt)))

    return examples

# Example usage:
# impact = extract_translation_impact("translated_query.json", "retrieval_rankings.json", "ground_truths_example.json")
# for k, v in impact.items():
#     print(f"\n== {k.upper()} ==")
#     for item in v[:3]:  # Show only first 3 per category
#         print(item)
