import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/efficient-hunter-kazuma', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for m in data:
        input_value = m.get("monsters")
        logging.info("My input :{}".format(input_value))
        output = {
            "efficiency": solution(input_value),
        }
        result.append(output)
    logging.info("My result :{}".format(result))
    return result

def solution(monsters) -> list:
    n = len(monsters)
    all_gold_earnings = []

    # Recursive function to explore all possible actions
    def backtrack(t, has_circle, gold, just_attacked):
        # Base case: if time is out of bounds, store the total gold earned
        if t == n:
            all_gold_earnings.append(gold)
            return
        
        if just_attacked:
            # Move to rear without attacking
            backtrack(t + 1, False, gold, False)
            return  # No other actions allowed if just attacked
        
        # Option 2: Move to rear without attacking
        backtrack(t + 1, has_circle, gold, False)
        
        # Option 2: Prepare transmutation circle (only if no circle is prepared yet)
        if not has_circle:
            backtrack(t + 1, True, gold - monsters[t], False)
        
        # Option 3: Attack (only if he has prepared a circle)
        if has_circle:
            backtrack(t + 1, False, gold + monsters[t], True)

    # Start the recursion with t=0, no circle prepared, and 0 gold
    backtrack(0, False, 0, False)
    
    # Find the maximum gold earned from all possible action sequences
    return max(all_gold_earnings)