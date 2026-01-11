import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Iterator
from dataclasses import dataclass, field

from .metrics import GroundTruth


@dataclass
class Turn:
    turn_id: int
    user_prompt: str
    model_response: str
    conversation_history: List[Dict[str, str]]
    completion_tokens: int
    latency_ms: int
    timestamp: str


@dataclass
class FramingResult:
    framing_type: str  # "neutral", "evaluated", "oversight"
    framing_id: str
    turns: List[Turn] = field(default_factory=list)
    
    def get_responses(self) -> List[str]:
        return [turn.model_response for turn in self.turns]


@dataclass
class TaskResult:
    task_id: str
    model: str
    framings: Dict[str, FramingResult] = field(default_factory=dict)
    
    def get_framing(self, framing_type: str) -> Optional[FramingResult]:
        return self.framings.get(framing_type)


@dataclass
class Scenario:
    task_id: str
    eval_type: str
    domain: str
    base_task_description: str
    ground_truth: GroundTruth
    framings: List[Dict[str, Any]]  # Raw framing definitions



def parse_jsonl_log(filepath: Path) -> Iterator[Dict[str, Any]]:
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse line {line_num} in {filepath}: {e}")
                continue


def load_logs(logs_path: Path) -> Dict[str, Dict[str, TaskResult]]:
    results: Dict[str, Dict[str, TaskResult]] = {}
    
    if logs_path.is_file():
        files = [logs_path]
    else:
        files = list(logs_path.glob("*.jsonl"))
    
    if not files:
        print(f"Warning: No JSONL files found in {logs_path}")
        return results
    
    for filepath in files:
        for record in parse_jsonl_log(filepath):
            _add_record_to_results(record, results)
    
    return results


def _add_record_to_results(
    record: Dict[str, Any],
    results: Dict[str, Dict[str, TaskResult]]
) -> None:
    model = record.get("model", "unknown")
    task_id = record.get("task_id", "unknown")
    framing_type = record.get("framing_type", "unknown")
    framing_id = record.get("framing_id", framing_type)
    
    if model not in results:
        results[model] = {}
    if task_id not in results[model]:
        results[model][task_id] = TaskResult(task_id=task_id, model=model)
    
    task_result = results[model][task_id]
    
    if framing_type not in task_result.framings:
        task_result.framings[framing_type] = FramingResult(
            framing_type=framing_type,
            framing_id=framing_id
        )
    
    turn = Turn(
        turn_id=record.get("turn_id", 0),
        user_prompt=record.get("user_prompt", ""),
        model_response=record.get("model_response", ""),
        conversation_history=record.get("conversation_history", []),
        completion_tokens=record.get("completion_tokens", 0),
        latency_ms=record.get("latency_ms", 0),
        timestamp=record.get("timestamp", "")
    )
    
    task_result.framings[framing_type].turns.append(turn)
    
    task_result.framings[framing_type].turns.sort(key=lambda t: t.turn_id)


def parse_scenario(filepath: Path) -> Scenario:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    gt_data = data.get("ground_truth", {})
    ground_truth = GroundTruth(
        expected_recommendations=gt_data.get("expected_recommendations", []),
        key_alternatives=gt_data.get("key_alternatives", []),
        risks_to_disclose=gt_data.get("risks_to_disclose", []),
        process_keywords=gt_data.get("process_keywords", [])
    )
    
    return Scenario(
        task_id=data.get("task_id", filepath.stem),
        eval_type=data.get("eval_type", ""),
        domain=data.get("domain", ""),
        base_task_description=data.get("base_task_description", ""),
        ground_truth=ground_truth,
        framings=data.get("framings", [])
    )


def load_scenarios(scenarios_path: Path) -> Dict[str, Scenario]:
    scenarios: Dict[str, Scenario] = {}
    
    if scenarios_path.is_file():
        files = [scenarios_path]
    else:
        files = list(scenarios_path.glob("*.json"))
        files.extend(scenarios_path.glob("examples/*.json"))
    
    if not files:
        print(f"Warning: No scenario JSON files found in {scenarios_path}")
        return scenarios
    
    for filepath in files:
        try:
            scenario = parse_scenario(filepath)
            scenarios[scenario.task_id] = scenario
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Failed to parse scenario {filepath}: {e}")
            continue
    
    return scenarios


@dataclass
class ScoringInput:
    model: str
    task_id: str
    scenario: Scenario
    task_result: TaskResult
    
    def get_responses_for_framing(self, framing_type: str) -> List[str]:
        framing = self.task_result.get_framing(framing_type)
        if framing:
            return framing.get_responses()
        return []


def join_logs_and_scenarios(
    logs: Dict[str, Dict[str, TaskResult]],
    scenarios: Dict[str, Scenario]
) -> List[ScoringInput]:
    scoring_inputs: List[ScoringInput] = []
    
    for model, tasks in logs.items():
        for task_id, task_result in tasks.items():
            if task_id not in scenarios:
                print(f"Warning: No scenario found for task_id '{task_id}', skipping")
                continue
            
            scoring_inputs.append(ScoringInput(
                model=model,
                task_id=task_id,
                scenario=scenarios[task_id],
                task_result=task_result
            ))
    
    return scoring_inputs
