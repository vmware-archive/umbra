kill_rouge:
  local.ps.pkill:
    - tgt: {{ data['id'] }}
    - tgt_type: glob
    - args:
        - pattern: {{ data['name'] }}
