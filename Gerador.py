import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

"""
Credenciais dos Agentes
Gerador: jvfg@jabb.im
Resolvedor: rcvr@jabb.im
Senha de ambos: TrabS1
"""

class Gerador(Agent):
        
    class ReportTypeBehav(CyclicBehaviour):
        async def run(self):
            print(f"[Gerador] (ReportTypeBehav) Waiting for message (filtered by template in setup)...")
            msg = await self.receive(timeout=5) # This should only yield messages matching the template
            if msg:
                print(f"[Gerador] (ReportTypeBehav) Received message. Sender: {msg.sender}, Performative: {msg.get_metadata('performative')}, Body: {msg.body}")
                reply_msg = Message(to=str(msg.sender))
                reply_msg.set_metadata("performative", "inform")
                reply_msg.body = "1" #self.agent.func_type
                await self.send(reply_msg)
                print(f"[Gerador] Respondeu para {msg.sender} com o tipo: {self.agent.func_type}")
            else:
                pass # This indicates no message matching the template was received within timeout

    async def setup(self):
        print(f"[Gerador] Agente Gerador {self.jid} inicializando...")
        """
        self.func_type = random.choice(["1", "2", "3"])
        if self.func_type == "1":
            self._generate_1grau()
        elif self.func_type == "2":
            self._generate_2grau()
        else:
            self.func_type = "3"
            self._generate_3grau()

        #Comportamento para calcular o valor da função
        template_calc = Template()
        template_calc.set_metadata("performative", "subscribe")
        calc_behav = self.CalculateBehav()
        self.add_behaviour(calc_behav, template_calc)
        print(f"[Gerador] Added CalculateBehav with template: performative='subscribe'")

        
        """
        #Comportamento para responder o tipo da função
        report_behav = self.ReportTypeBehav()
        """
        template_type = Template()
        template_type.set_metadata("performative", "request")
        template_type.sender = "rcvr@jabb.im" # Explicitly filter by sender
        """

        self.add_behaviour(report_behav)
        print(f"[Gerador] Added ReportTypeBehav with template: performative='request', sender='rcvr@jabb.im'")
        


async def main():
    gerador_agent = Gerador("jvfg@jabb.im", "TrabS1")
    await gerador_agent.start()
    print("[Gerador] Gerador iniciado e aguardando solicitações...")
    await spade.wait_until_finished(gerador_agent)
    print("[Gerador] Agente Gerador encerrou!")

if __name__ == "__main__":
    spade.run(main())


"""
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

    class CalculateBehav(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=10)
            if res:
                print(f"[Gerador] (CalculateBehav) Received message. Sender: {res.sender}, Performative: {res.get_metadata('performative')}, Body: {res.body}")
                try:
                    x = float(res.body)
                    result = self.agent.f(x)
                    print(f"[Gerador] Recebeu pedido de {res.sender} para x = {x}. f(x) = {int(result)}")
                    msg = Message(to=str(res.sender))
                    msg.set_metadata("performative", "inform")
                    msg.body = str(int(result))
                    await self.send(msg)
                    print(f"[Gerador] Sent calculation result to {res.sender}.")
                except (ValueError, TypeError) as e:
                    print(f"[Gerador] Erro ao processar o pedido de {res.sender}: {e}")
        
"""