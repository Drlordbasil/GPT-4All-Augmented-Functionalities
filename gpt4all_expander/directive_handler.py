# File: gpt4all_expander/directive_handler.py

from .submodules.market_analysis import MarketAnalysis
from .submodules.business_strategy import BusinessStrategy
from .submodules.learning_module import LearningModule
from enum import Enum, auto
from typing import Any, Dict, List, Union

class Action(Enum):
    UPDATE_CONTEXT = auto()
    RECALL_MEMORY = auto()
    ANALYZE_MARKET = auto()
    GENERATE_RESPONSE = auto()  # Added this line
    GENERATE_STRATEGY = auto()
    ADD_MEMORY = auto()
    ADD_TASK = auto()   
    EXECUTE_NEXT_TASK = auto()
    LEARN = auto()

class DirectiveHandler:
    def __init__(self, context_manager, memory_recolator, task_queue, model):
        self.context_manager = context_manager
        self.memory_recolator = memory_recolator
        self.task_queue = task_queue
        self.market_analysis = MarketAnalysis(model)
        self.business_strategy = BusinessStrategy(model)
        self.learning_module = LearningModule()

    def handle_directive(self, directive: Dict[str, Any]) -> Union[Dict[str, Any], None]:
        action_str = directive.get('action', '')  # Get the action as a string
        data = directive.get('data', {})

        handlers = {
            Action.UPDATE_CONTEXT: self.update_context,
            Action.RECALL_MEMORY: self.recall_memory,
            Action.ANALYZE_MARKET: self.analyze_market,
            Action.GENERATE_RESPONSE: self.generate_response,
            Action.GENERATE_STRATEGY: self.generate_strategy,
            Action.ADD_MEMORY: self.add_memory,
            Action.ADD_TASK: self.add_task,
            Action.EXECUTE_NEXT_TASK: self.execute_next_task,
            Action.LEARN: self.learn
        }

        try:
            action_enum = Action[action_str.upper()]  # Convert the action string to an enum member
            handler = handlers[action_enum]  # Look up the handler using the enum member
        except KeyError:
            raise ValueError(f"Unknown action: {action_str}")

        return handler(data)

    def update_context(self, data: Dict[str, Any]) -> None:
        self.context_manager.update_context(data.get('text', ''))

    def recall_memory(self, data: Dict[str, Any]) -> Dict[str, Any]:
        key = data.get('key')
        return {'memory': self.memory_recolator.recall_memory(key)}

    def analyze_market(self, data: Dict[str, Any]) -> Dict[str, Any]:
        market_data = data.get('market_data')
        analysis = self.market_analysis.analyze_market_trends(market_data)
        return {'analysis': analysis}

    def generate_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = data.get('prompt', '')
        min_tokens = data.get('min_tokens', 100)
        response = self.context_manager.generate(prompt)
        return {'response': response}

    def generate_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        market_analysis = data.get('market_analysis')
        strategy = self.business_strategy.generate_strategy(market_analysis)
        return {'strategy': strategy}

    def add_memory(self, data: Dict[str, Any]) -> None:
        key = data.get('key')
        value = data.get('value')
        self.memory_recolator.add_memory(key, value)

    def add_task(self, data: Dict[str, Any]) -> None:
        self.task_queue.add_task(data.get('task'))

    def execute_next_task(self, data: Dict[str, Any]) -> Union[Dict[str, Any], None]:
        task = self.task_queue.get_next_task()
        if task:
            return self.handle_directive(task)

    def learn(self, data: Dict[str, Any]) -> None:
        generated_data = data.get('generated_data')
        self.learning_module.learn(generated_data)
    def process_directives(self, directives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        responses = [self.handle_directive(directive) for directive in directives]
        self.learning_module.learn(responses)
        return [response for response in responses if response]