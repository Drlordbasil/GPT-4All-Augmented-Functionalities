from gpt4all_expander import ContextManager, DirectiveHandler, MemoryRecolator, TaskQueue
from flask import Flask, render_template
from threading import Thread
import json
import logging

app = Flask(__name__)
output = None

def run_autonomous_program():
    global output
    logging.basicConfig(level=logging.INFO)
    model_path = "orca-mini-7b.ggmlv3.q4_0.bin"  
    context_manager = ContextManager(model_path)  
    memory_recolator = MemoryRecolator()
    task_queue = TaskQueue()
    directive_handler = DirectiveHandler(context_manager, memory_recolator, task_queue, model_path)

    business_directive = {
        "action": "generate_response",
        "data": {
            "prompt": "Create a business plan that uses free online resources for huge profits.",
        }
    }

    directives = [
        business_directive,  # Updated this line
        {"action": "add_task", "data": {"task": business_directive}},
        {"action": "update_context", "data": {"text": "New context for the directive handler."}},  # Updated this line
        {"action": "add_memory", "data": {"key": "some_key", "value": "some_value"}},  # Updated this line
        {"action": "learn", "data": {"generated_data": "Sample generated data."}},  # Updated this line
        {"action": "execute_next_task"}
    ]

    # Collect responses and update the global output variable
    responses = directive_handler.process_directives(directives)
    output = json.dumps(responses, indent=4)

@app.route('/')
def index():
    if output is None:
        return "Processing. Please refresh the page in a few seconds."
    return render_template('index.html', output=output)

if __name__ == '__main__':
    t = Thread(target=run_autonomous_program)
    t.start()
    app.run(debug=True)
