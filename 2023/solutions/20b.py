import re
from abc import ABC, abstractmethod

import math


class Agent(ABC):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.inputs = []
        self.outputs = []

    @abstractmethod
    def run(self, pulse, source: 'Agent'):
        pass

    def add_output(self, source: 'Agent'):
        self.outputs.append(source)
        source.inputs.append(self)

    def send(self, pulse):
        return {o.name: pulse for o in self.outputs}


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

    def run(self, pulse, source: Agent):
        self.pulses[source.name] = pulse
        return self.send("low" if self.all_high() else "high")

    def all_high(self):
        return all(self.pulses.get(x.name, "low") == "high" for x in self.inputs)


class FlipFlop(Agent):
    """
    Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high
    pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between
    on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
    """
    def __init__(self, name):
        super().__init__(name)
        self.state = "off"

    def run(self, pulse, source):
        if pulse == "high":
            return {}
        if self.state == "off":
            self.state = "on"
            return self.send("high")
        else:
            self.state = "off"
            return self.send("low")


class Broadcast(Agent):
    """
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all
    of its destination modules.
    """
    def run(self, pulse, source: Agent):
        return self.send(pulse)


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

    periods = {}
    watch = ['rc', 'gv', 'qf', 'll']  # The four central conjunctionators, spotted using GraphViz
    i = 1
    while True:
        stack = [['button', {'broadcaster': 'low'}]]
        while stack:
            from_a, recipients = stack.pop(0)
            for to_a, pulse in recipients.items():
                stack.append([to_a, agents[to_a].run(pulse, agents[from_a])])
                if to_a in watch and to_a not in periods and agents[to_a].all_high():
                    periods[to_a] = i
                    print(f"{to_a} period is {i}")
                if len(periods) == len(watch):
                    print(f"lcm = {math.lcm(*periods.values())}")
                    exit(7)
        i += 1


main('data/20')
# main('/tmp/example')
