import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

# --- Dynamic Schema Loading ---

SCRIPT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SCRIPT_DIR.parent
DEFAULT_SCHEMA_PATH = ROOT_DIR / "card_logic_schema.md"

def load_definitions_from_schema(schema_path: Path) -> Dict[str, Set[str]]:
    """
    Parses the schema markdown file to extract all validation rule sets using robust,
    section-specific regular expressions.
    """
    definitions = {
        "required_keys": set(),
        "allowed_keys": set(),
        "card_types": set(),
        "actions": set(),
        "triggers": set(),
    }
    print(f"--- Loading all definitions from schema: {schema_path.name} ---")

    try:
        content = schema_path.read_text(encoding="utf-8")

        # Parser for Markdown lists under a specific "###" header.
        # Anchors to the start of a line to be more robust.
        def _parse_md_list(header: str) -> Set[str]:
            match = re.search(rf"### \d\.\d {header}(.*?)(?:###|##|\Z)", content, re.S)
            if not match:
                print(f"Warning: Could not find list section for '{header}'", file=sys.stderr)
                return set()
            # This regex finds list items like "- `item`" or "- item" at the start of a line.
            return {item.strip() for item in re.findall(r"^\s*-\s*`?([\w_]+)`?", match.group(1), re.M)}

        # Parser for the main "Actions" table under a "## 4." header.
        def _parse_actions_table() -> Set[str]:
            match = re.search(r"## 4\. 动作 \(Action\).*?\|.*?\n\|[-|: ]+\n(.*?)(?:---|\Z)", content, re.S)
            if not match:
                print("Warning: Could not find Actions table", file=sys.stderr)
                return set()
            return {item.strip() for item in re.findall(r"\|\s*`([A-Z_]+)`", match.group(1))}

        # Parser for the "Triggers" table based on its unique column header.
        def _parse_triggers_table() -> Set[str]:
            match = re.search(r"\| 条件 \(`EVENT_TYPE`\).*?\n\|[-|: ]+\n(.*?)(?:---|\Z)", content, re.S)
            if not match:
                print("Warning: Could not find Triggers table", file=sys.stderr)
                return set()
            return {item.strip() for item in re.findall(r"\|\s*`([A-Z_]+)`", match.group(1))}

        definitions["required_keys"] = _parse_md_list("必选顶层键")
        optional_keys = _parse_md_list("可选顶层键")
        definitions["allowed_keys"] = definitions["required_keys"].union(optional_keys)
        definitions["card_types"] = _parse_md_list("合法卡牌类型")

        definitions["actions"] = _parse_actions_table()
        definitions["triggers"] = _parse_triggers_table()

        print(f"  - Loaded {len(definitions['required_keys'])} required keys: {sorted(list(definitions['required_keys']))}")
        print(f"  - Loaded {len(definitions['allowed_keys'])} total allowed keys.")
        print(f"  - Loaded {len(definitions['card_types'])} card types: {sorted(list(definitions['card_types']))}")
        print(f"  - Loaded {len(definitions['actions'])} actions.")
        print(f"  - Loaded {len(definitions['triggers'])} trigger conditions: {sorted(list(definitions['triggers']))}")
        print("--- Schema loading complete ---\n")

    except FileNotFoundError:
        print(f"  [Error] Schema file not found at: {schema_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"  [Error] Failed to parse schema file: {e}", file=sys.stderr)
        sys.exit(1)

    return definitions

# --- Schema Definition (loaded dynamically) ---
schema_defs = load_definitions_from_schema(DEFAULT_SCHEMA_PATH)

VALID_TOP_LEVEL_KEYS = schema_defs["allowed_keys"]
REQUIRED_TOP_LEVEL_KEYS = schema_defs["required_keys"]
VALID_CARD_TYPES = schema_defs["card_types"]
VALID_ACTIONS = schema_defs["actions"]
VALID_TRIGGER_CONDITIONS = schema_defs["triggers"]

if not all([VALID_TOP_LEVEL_KEYS, REQUIRED_TOP_LEVEL_KEYS, VALID_CARD_TYPES, VALID_ACTIONS, VALID_TRIGGER_CONDITIONS]):
    print("Critical schema definitions could not be loaded. Aborting.", file=sys.stderr)
    sys.exit(1)

# This remains hardcoded as the schema format is not easily machine-readable for this part.
REQUIRED_ACTION_PARAMS: Dict[str, Set[str]] = {
    # Resource Actions
    "GAIN_RESOURCE": {"target", "resource", "value"},
    "LOSE_RESOURCE": {"target", "resource", "value"},
    "PAY_COST": {"target", "resource", "value"},
    "DEAL_DAMAGE": {"target", "value"},
    "SWAP_RESOURCES": {"target_a", "target_b", "resource"},
    "SET_RESOURCE": {"target", "resource", "value"},
    "TRANSFER_RESOURCE": {"from", "to", "resource", "value"},
    # Movement Actions
    "MOVE": {"target", "value"},
    "SWAP_POSITION": {"target_a", "target_b"},
    # Status and Rule Actions
    "APPLY_STATUS": {"target", "status_id"},
    "REMOVE_STATUS": {"target", "status_id"},
    "MODIFY_RULE": {"rule_id", "scope", "mutation", "duration"},
    # Interaction and Information Actions
    "CHOICE": {"target", "options"},
    "LOOKUP": {"target", "info_type"},
    "INTERRUPT": {"target_action", "interrupt_type"},
    "COPY_EFFECT": {"target", "source_effect"},
    # Card and Deck Actions
    "DRAW_CARD": {"target", "deck", "count"},
    "DISCARD_CARD": {"target", "count"},
    "SWAP_HAND_CARDS": {"target_a", "target_b", "count", "atomic"},
    "SWAP_DISCARD_PILES": {"target_a", "target_b", "atomic"},
    "RECOVER_CARD_FROM_DISCARD": {"target", "deck", "count"},
    # Entity Actions
    "CREATE_ENTITY": {"entity_type", "position"},
    "DESTROY_ENTITY": {"target_entity_id"},
    # Game Flow Actions
    "SKIP_PHASE": {"phase"},
    "PROPOSE_ALLIANCE": {"target", "duration"},
    "EXECUTE_LATER": {"delay", "effect", "expiry_time"},
    "TRIGGER_EVENT": {"event_id", "participants"},
}

# --- Linter Logic ---

def lint_card(card_data: Dict[str, Any], card_id: str) -> List[str]:
    """
    Validates a single card's data against the schema.
    Returns a list of error messages.
    """
    errors = []

    # 1. Check for required top-level keys
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in card_data:
            errors.append(f"Missing required top-level key: '{key}'")

    # 2. Check for unknown top-level keys
    for key in card_data:
        if key not in VALID_TOP_LEVEL_KEYS:
            errors.append(f"Unknown top-level key: '{key}'")

    # 3. Validate card type
    card_type = card_data.get('type')
    if card_type and card_type not in VALID_CARD_TYPES:
        errors.append(f"Invalid card type: '{card_type}'")

    # 4. Validate 'id' consistency
    if card_data.get('id') != card_id:
        errors.append(f"Card ID in file '{card_id}' does not match 'id' field in JSON: '{card_data.get('id')}'")

    # 5. Recursively validate effects and actions
    if 'core_mechanism' in card_data and isinstance(card_data.get('core_mechanism'), dict) and 'variants' in card_data['core_mechanism']:
        for variant, content in card_data['core_mechanism']['variants'].items():
            if isinstance(content, dict) and 'effect' in content:
                errors.extend(_validate_effect_object(content['effect'], f"core_mechanism.variants.{variant}"))

    if 'effect' in card_data:
        errors.extend(_validate_effect_object(card_data['effect'], "effect"))

    # 6. Validate triggers
    if 'triggers' in card_data:
        if not isinstance(card_data['triggers'], list):
            errors.append("'triggers' must be a list of trigger objects.")
        else:
            for i, trigger in enumerate(card_data['triggers']):
                if not isinstance(trigger, dict) or 'condition' not in trigger:
                    errors.append(f"Trigger {i} is missing a 'condition' key.")
                elif trigger['condition'] not in VALID_TRIGGER_CONDITIONS:
                    errors.append(f"Trigger {i} has an invalid condition: '{trigger['condition']}'.")

    return errors

def _validate_effect_object(effect: Dict[str, Any], path: str) -> List[str]:
    """Helper to validate an effect object."""
    errors = []
    if not isinstance(effect, dict):
        return [f"Effect at '{path}' is not a valid object."]

    if 'actions' in effect:
        if not isinstance(effect['actions'], list):
            errors.append(f"'{path}.actions' must be a list.")
        else:
            for i, action in enumerate(effect['actions']):
                errors.extend(_validate_action_object(action, f"{path}.actions[{i}]"))

    if 'cost' in effect:
        if not isinstance(effect['cost'], list):
            errors.append(f"'{path}.cost' must be a list.")
        else:
            for i, cost_item in enumerate(effect['cost']):
                is_resource_cost = isinstance(cost_item, dict) and all(k in cost_item for k in ['resource', 'value'])
                is_action_cost = isinstance(cost_item, dict) and 'action' in cost_item

                if not (is_resource_cost or is_action_cost):
                    errors.append(f"Invalid cost item at '{path}.cost[{i}]'. Must be a resource object or an action object.")

                # If the cost is an action, recursively validate it.
                if is_action_cost:
                    errors.extend(_validate_action_object(cost_item, f"{path}.cost[{i}]"))

    return errors

def _validate_action_object(action: Dict[str, Any], path: str) -> List[str]:
    """Helper to validate an action object."""
    errors = []
    if not isinstance(action, dict):
        return [f"Action at '{path}' is not a valid object."]

    action_type = action.get('action')
    if not action_type:
        errors.append(f"Action at '{path}' is missing the 'action' key.")
    elif action_type not in VALID_ACTIONS:
        errors.append(f"Unknown action type '{action_type}' at '{path}'.")

    # Basic check for parameters
    if 'params' not in action:
        errors.append(f"Action at '{path}' is missing the 'params' key.")

    # Check for required params for known actions
    if action_type in REQUIRED_ACTION_PARAMS:
        missing_params = REQUIRED_ACTION_PARAMS[action_type] - set(action.get('params', {}).keys())
        if missing_params:
            errors.append(f"Action '{action_type}' at '{path}' is missing required params: {missing_params}")

    # --- High-level safety checks / engine contract checks ---
    params = action.get('params', {}) if isinstance(action.get('params', {}), dict) else {}

    # MODIFY_RULE must include scope and rollback info
    if action_type == 'MODIFY_RULE':
        scope = params.get('scope')
        if not scope:
            errors.append(f"MODIFY_RULE at '{path}' must include a 'scope' param (turn/phase/persistent).")
        else:
            if scope not in {'turn', 'phase', 'persistent'}:
                errors.append(f"MODIFY_RULE at '{path}' has invalid scope '{scope}'. Use one of turn/phase/persistent.")
        if not (params.get('rollback_condition') or params.get('duration')):
            errors.append(f"MODIFY_RULE at '{path}' should include 'duration' or 'rollback_condition' to allow safe rollback.")

    # EXECUTE_LATER should have expiry or max_turns to avoid dangling events
    if action_type == 'EXECUTE_LATER':
        if not (params.get('expiry_time') or params.get('max_turns') or params.get('delay')):
            errors.append(f"EXECUTE_LATER at '{path}' should include 'expiry_time', 'max_turns' or 'delay' to avoid dangling events.")
        # Recommend snapshot behavior (warning-level implemented as error to force explicitness)
        if not params.get('snapshot_args') and not params.get('late_resolve'):
            errors.append(f"EXECUTE_LATER at '{path}' should state 'snapshot_args' or 'late_resolve' to clarify resolution semantics.")

    # COPY_EFFECT should declare copy semantics when used
    if action_type == 'COPY_EFFECT':
        copy_sem = params.get('copy_semantics')
        if not copy_sem:
            errors.append(f"COPY_EFFECT at '{path}' must declare 'copy_semantics' (snapshot|reference|forbidden).")
        else:
            if copy_sem not in {'snapshot', 'reference', 'forbidden'}:
                errors.append(f"COPY_EFFECT at '{path}' has invalid copy_semantics '{copy_sem}'. Use snapshot|reference|forbidden.")

    # CREATE_ENTITY should bound creation to avoid infinite loops
    if action_type == 'CREATE_ENTITY':
        if not (params.get('max_instances') or params.get('create_stack_limit')):
            errors.append(f"CREATE_ENTITY at '{path}' should include 'max_instances' or 'create_stack_limit' to prevent runaway creation.")

    # SWAP_* operations must be atomic or declare fallback
    if action_type and action_type.startswith('SWAP'):
        if 'atomic' not in params and 'fallback_policy' not in params:
            errors.append(f"{action_type} at '{path}' must include 'atomic' boolean or 'fallback_policy' to avoid partial swaps.")

    return errors

def main():
    """
    Main execution function.
    Lints a specific file or all files in the assets/data/cards directory.
    """
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"Error: File not found at '{filepath}'")
            sys.exit(1)
        files_to_lint = [filepath]
    else:
        print("No specific file provided. Searching for all card data files...")
        base_path = 'assets/data/cards'
        if not os.path.exists(base_path):
            print(f"Error: Directory '{base_path}' not found. Run generate_card_data.py first.")
            sys.exit(1)

        files_to_lint = []
        for root, _, files in os.walk(base_path):
            for file in files:
                # Exclude the manifest file from the linting process
                if file.endswith('.json') and file != 'card_manifest.json':
                    files_to_lint.append(os.path.join(root, file))

    print(f"Found {len(files_to_lint)} JSON file(s) to lint.")
    total_errors = 0

    for filepath in files_to_lint:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            card_id = os.path.splitext(os.path.basename(filepath))[0]
            errors = lint_card(data, card_id)

            # Top-level usage_limit semantics check
            if 'usage_limit' in data:
                ul = data.get('usage_limit')
                if not isinstance(ul, dict):
                    errors.append(f"Top-level 'usage_limit' in {filepath} must be an object with 'reset_timing'.")
                else:
                    if not ul.get('reset_timing'):
                        errors.append(f"Top-level 'usage_limit' in {filepath} must include 'reset_timing' (e.g., end_of_turn).")

            if errors:
                print(f"\n--- Errors found in {filepath}:")
                for error in errors:
                    print(f"  - {error}")
                total_errors += len(errors)
            else:
                # Keep output clean for successful runs
                pass

        except json.JSONDecodeError as e:
            print(f"\n--- Error decoding JSON in {filepath}:")
            print(f"  - {e}")
            total_errors += 1
        except Exception as e:
            print(f"\n--- An unexpected error occurred with {filepath}:")
            print(f"  - {e}")
            total_errors += 1

    if total_errors > 0:
        print(f"\nLinting complete. Found a total of {total_errors} error(s).")
        sys.exit(1)
    else:
        print("\nLinting complete. All files are valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()