import re

def count_whole_word(text: str, keyword: str) -> int:
  pattern = rf"\b{re.escape(keyword)}\b"
  return len(re.findall(pattern, text, flags=re.IGNORECASE))

def evaluate(text: str, policy: list[dict]):
  detected = []
  found_ids = []

  for dt in policy:
    keywords = dt.get("content") or []
    threshold = int(dt.get("threshold") or 1)
    match_count = 0

    for kw in keywords:
      if isinstance(kw, str) and kw.strip():
        match_count += count_whole_word(text, kw.strip())

    if match_count >= threshold:
      detected.append({"id": dt["id"], "name": dt["name"], "match_count": match_count})
      found_ids.append(dt["id"])

  if detected:
    return {
      "status": "match",
      "result": {"detected_objects": detected}
    }, found_ids, "match"

  return {"status": "not matched"}, [], "not matched"