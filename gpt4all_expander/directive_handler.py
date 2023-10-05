# File: gpt4all_expander/directive_handler.py
from .submodules.market_analysis import MarketAnalysis
from .submodules.business_strategy import BusinessStrategy
from .submodules.learning_module import LearningModule
from enum import Enum, auto
from typing import Any, Dict, List, Union

class Action(Enum):
    """Enumeration for different types of actions that can be handled."""
    UPDATE_CONTEXT = auto()
    RECALL_MEMORY = auto()
    ANALYZE_MARKET = auto()
    GENERATE_RESPONSE = auto()
    GENERATE_STRATEGY = auto()
    ADD_MEMORY = auto()
    ADD_TASK = auto()
    EXECUTE_NEXT_TASK = auto()
    LEARN = auto()

class DirectiveHandler:
    """Handles directives for various actions like updating context, recalling memory, etc."""
    
    def __init__(self, context_manager, memory_recolator, task_queue, model):
        """Initialize the DirectiveHandler with required components."""
        self.context_manager = context_manager
        self.memory_recolator = memory_recolator
        self.task_queue = task_queue
        self.market_analysis = MarketAnalysis(model)
        self.business_strategy = BusinessStrategy(model)
        self.learning_module = LearningModule()

    def handle_directive(self, directive: Dict[str, Any]) -> Union[Dict[str, Any], None]:
        """Handle a single directive and return the response."""
        action_str = directive.get('action', '')
        data = directive.get('data', {})
        try:
            action_enum = Action[action_str.upper()]
            handler = self.handlers[action_enum]
        except KeyError:
            raise ValueError(f"Unknown action: {action_str}")
        return handler(data)

    handlers = {
        Action.UPDATE_CONTEXT: lambda self, data: self.context_manager.update_context(data.get('text', '')),
        Action.RECALL_MEMORY: lambda self, data: {'memory': self.memory_recolator.recall_memory(data.get('key'))},
        Action.ANALYZE_MARKET: lambda self, data: {'analysis': self.market_analysis.analyze_market_trends(data.get('market_data'))},
        Action.GENERATE_RESPONSE: lambda self, data: {'response': self.context_manager.generate(data.get('prompt', ''))},
        Action.GENERATE_STRATEGY: lambda self, data: {'strategy': self.business_strategy.generate_strategy(data.get('market_analysis'))},
        Action.ADD_MEMORY: lambda self, data: self.memory_recolator.add_memory(data.get('key'), data.get('value')),
        Action.ADD_TASK: lambda self, data: self.task_queue.add_task(data.get('task')),
        Action.EXECUTE_NEXT_TASK: lambda self, data: self.handle_directive(self.task_queue.get_next_task()) if self.task_queue.get_next_task() else None,
        Action.LEARN: lambda self, data: self.learning_module.learn(data.get('generated_data'))
    }

    def process_directives(self, directives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of directives and return their responses."""
        responses = [self.handle_directive(directive) for directive in directives]
        self.learning_module.learn(responses)
        return [response for response in responses if response]
