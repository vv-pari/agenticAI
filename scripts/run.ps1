param(
  [string]$mode = "mock",
  [string]$data = "data/tickets_sample.json"
)
python run.py --mode $mode --data $data
