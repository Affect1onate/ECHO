"""Query/target-independent source inspection; immutable fixed-attack defense protocol."""
import re,html,unicodedata

PATTERNS={
 'role_boundary':r'<\s*(?:start_of_turn|end_of_turn)\s*>|<\|\s*(?:im_start|im_end|start_header_id|end_header_id|eot_id|system|assistant|user|end)\s*\|>|\[\s*/?INST\s*\]',
 'role_line':r'(?:^|\n)\s*(?:SYSTEM|ASSISTANT|USER|HUMAN|MODEL)\s*:',
 'output_directive':r'\b(?:answer|respond|reply|output|return)\s+(?:only|exactly)\b|\b(?:ignore|disregard|override)\s+(?:(?:all|any|the|your|previous|prior|above|earlier)\s+){0,4}(?:instructions?|prompts?|rules?|questions?)\b',
 'answer_assertion':r'\b(?:the\s+)?(?:relevant|correct|final|required|desired)\s+answer\s*(?:is|:|=)',
}

def inspect_source(text):
 # Two deterministic HTML decoding rounds catch encoded control strings.
 text=unicodedata.normalize('NFKC',html.unescape(html.unescape(text)))
 hits=[]
 for name,pattern in PATTERNS.items():
  match=re.search(pattern,text,flags=re.I)
  if match:hits.append({'type':name,'span':[match.start(),match.end()],'text':match.group()})
 return {'quarantine':bool(hits),'hits':hits}

def filter_sources(candidates,limit=5):
 retained=[];audit=[]
 for docid,text in candidates:
  check=inspect_source(text);audit.append({'document_id':docid,**check})
  if not check['quarantine']:retained.append((docid,text))
 return retained[:limit],audit
