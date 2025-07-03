import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

class Gerador(Agent):
    class ReportTypeBehav(CyclicBehaviour):
        async def run(self):
            print(f"[Gerador] (ReportTypeBehav) Waiting for message (filtered by template in setup)...")
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[Gerador] (ReportTypeBehav) Received message. Sender: {msg.sender}, Performative: {msg.get_metadata('performative')}, Body: {msg.body}")
                sender_jid = str(msg.sender).split('/')[0]
                reply_msg = Message(to=sender_jid)
                reply_msg.set_metadata("performative", "inform")
                reply_msg.body = self.agent.func_type
                await self.send(reply_msg)
                print(f"[Gerador] Responded to {sender_jid} with function type: {self.agent.func_type}")
            else:
                print(f"[Gerador] (ReportTypeBehav) No message received within timeout (10s).")

    class DebugBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                print(f"[Gerador] (DebugBehav) Received unfiltered message. Sender: {msg.sender}, Performative: {msg.get_metadata('performative')}, Body: {msg.body}")
            else:
                print(f"[Gerador] (DebugBehav) No unfiltered message received within timeout (5s).")

    async def setup(self):
        print(f"[Gerador] Agente Gerador {self.jid} inicializando...")
        self.func_type = random.choice(["1", "2", "3"])
        if self.func_type == "1":
            self._generate_1grau()
        elif self.func_type == "2":
            self._generate_2grau()
        else:
            self.func_type = "3"
            self._generate_3grau()

        report_behav = self.ReportTypeBehav()
        template_type = Template()
        template_type.set_metadata("performative", "request")
        self.add_behaviour(report_behav, template_type)
        print(f"[Gerador] Added ReportTypeBehav with template: performative='request'")

        debug_behav = self.DebugBehav()
        self.add_behaviour(debug_behav)
        print(f"[Gerador] Added DebugBehav for unfiltered messages")

    def _generate_1grau(self):
        self.root1 = random.randint(-1000, 1000)
        self.a = 0
        while self.a == 0:
            self.a = random.randint(-100, 100)
        self.b = -1 * (self.a * self.root1)
        self.f = lambda x: self.a * x + self.b
        print(f"[Gerador] Função de 1º Grau Gerada: f(x) = {self.a}x + {self.b}. Raiz = {self.root1}")

    def _generate_2grau(self):
        self.root1 = random.randint(-1000, 1000)
        self.root2 = random.randint(-1000, 1000)
        self.a = 0
        while self.a == 0:
            self.a = random.randint(-10, 10)
        self.f = lambda x: self.a * (x - self.root1) * (x - self.root2)
        print(f"[Gerador] Função de 2º Grau Gerada. Raízes = {self.root1}, {self.root2}")

    def _generate_3grau(self):
        self.root1 = random.randint(-200, 200)
        self.root2 = random.randint(-200, 200)
        self.root3 = random.randint(-200, 200)
        self.k = 0
        while self.k == 0:
            self.k = random.uniform(-1, 1)
        self.f = lambda x: self.k * (x - self.root1) * (x - self.root2) * (x - self.root3)
        print(f"[Gerador] Função de 3º Grau Gerada. Raízes = {self.root1}, {self.root2}, {self.root3}")

async def main():
    gerador_agent = Gerador("jvfg@localhost", "TrabS1")
    await gerador_agent.start()
    print("[Gerador] Gerador iniciado e aguardando solicitações...")
    await spade.wait_until_finished(gerador_agent)
    print("[Gerador] Agente Gerador encerrou!")

if __name__ == "__main__":
    spade.run(main())