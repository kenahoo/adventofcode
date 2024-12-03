from emsat_simulator.agent.dependency_aware_processing_agent import SubscriptionAwareProcessingAgent


class Conjunction(SubscriptionAwareProcessingAgent):
    """
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected
    input modules; they initially default to remembering a low pulse for each input. When a pulse is received,
    the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.
    """
    def __init__(self, name, dependencies):
        super().__init__(name, dependencies)

    def run(self):
        pass


class FlipFlop(SubscriptionAwareProcessingAgent):
    """
    Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high
    pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between
    on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
    """
    def __init__(self, name, dependencies):
        super().__init__(name, dependencies)
        self.state = "off"

    def run(self):
        pass


class Broadcast(SubscriptionAwareProcessingAgent):
    """
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all
    of its destination modules.
    """
    def __init__(self, name, dependencies):
        super().__init__(name, dependencies)

    def run(self):
        pass
