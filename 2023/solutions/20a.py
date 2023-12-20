import re
from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.inputs = []
        self.outputs = []
        self.tally = {"high": 0, "low": 0}

    @abstractmethod
    def invoke(self, pulse, source: 'Agent'):
        pass

    def add_output(self, source: 'Agent'):
        self.outputs.append(source)
        source.inputs.append(self)

    def send(self, pulse):
        out = {}
        for o in self.outputs:
            self.tally[pulse] += 1
            out[o.name] = pulse
        return [self.name, out]

    def null_send(self):
        return [self.name, {}]

    @abstractmethod
    def state_str(self):
        pass


class Conjunction(Agent):
    """
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected
    input modules; they initially default to remembering a low pulse for each input. When a pulse is received,
    the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.
    """
    def __init__(self, name):
        super().__init__(name)
        self.pulses = {}

    def invoke(self, pulse, source: Agent):
        self.pulses[source.name] = pulse
        send = "low" if all(self.pulses.get(x.name, "low") == "high" for x in self.inputs) else "high"
        return self.send(send)

    def state_str(self):
        return f"C{self.pulses}"


class FlipFlop(Agent):
    """
    Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high
    pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between
    on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
    """
    def __init__(self, name):
        super().__init__(name)
        self.state = "off"

    def invoke(self, pulse, source):
        if pulse == "high":
            return self.null_send()
        if self.state == "off":
            self.state = "on"
            return self.send("high")
        else:
            self.state = "off"
            return self.send("low")

    def state_str(self):
        return f"F{self.state}"


class Broadcast(Agent):
    """
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all
    of its destination modules.
    """
    def invoke(self, pulse, source: Agent):
        return self.send(pulse)

    def state_str(self):
        return f"B"


def total_state(agents):
    return ', '.join(x.state_str() for x in agents.values())


def main(file):

    agents: dict[str, 'Agent'] = {}

    with open(file) as fh:
        for line in fh.readlines():
            kind, name, outputs = re.match(r'(|%|&)(\w+) -> ([\w, ]+)', line).groups()
            agents[name] = FlipFlop(name) if kind == '%' else Conjunction(name) if kind == '&' else Broadcast(name)

        fh.seek(0)
        for line in fh.readlines():
            kind, name, outputs = re.match(r'(|%|&)(\w+) -> ([\w, ]+)', line).groups()
            for output in outputs.split(', '):
                if output not in agents:
                    agents[output] = Broadcast(output)
                agents[name].add_output(agents[output])

        agents['button'] = Broadcast('button')
        agents['button'].add_output(agents['broadcaster'])

    for _ in range(1000):
        stack = [['button', {'broadcaster': 'low'}]]
        agents['button'].tally['low'] += 1
        while stack:
            from_a, recipients = stack.pop(0)
            for to_a, pulse in recipients.items():
                stack.append(agents[to_a].invoke(pulse, agents[from_a]))

    highs = sum(x.tally['high'] for x in agents.values())
    lows = sum(x.tally['low'] for x in agents.values())
    print(f"{highs} * {lows} = {highs * lows}")


main('data/20')
# main('/tmp/example')
