import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

"""
Credenciais dos Agentes
Gerador: jvfg@jabb.im
Resolvedor: rcvr@jabb.im
Senha de ambos: TrabS1
"""

class Gerador(Agent):

    def _generate_1grau(self):
        """Gera uma função de 1º grau: f(x) = ax + b"""
        self.root1 = random.randint(-1000, 1000)
        self.a = 0
        while self.a == 0:
            self.a = random.randint(-100, 100)
        self.b = -1 * (self.a * self.root1)
        self.f = lambda x: self.a * x + self.b
        print(f"Função de 1º Grau Gerada: f(x) = {self.a}x + {self.b}. Raiz = {self.root1}")

    def _generate_2grau(self):
        """Gera uma função de 2º grau: f(x) = a(x-r1)(x-r2)"""
        self.root1 = random.randint(-1000, 1000)
        self.root2 = random.randint(-1000, 1000)
        self.a = 0
        while self.a == 0:
            self.a = random.randint(-10, 10)
        self.f = lambda x: self.a * (x - self.root1) * (x - self.root2)
        print(f"Função de 2º Grau Gerada. Raízes = {self.root1}, {self.root2}")

    def _generate_3grau(self):
        """Gera uma função de 3º grau: f(x) = k(x-r1)(x-r2)(x-r3)"""
        self.root1 = random.randint(-200, 200)
        self.root2 = random.randint(-200, 200)
        self.root3 = random.randint(-200, 200)
        self.k = 0
        while self.k == 0:
            self.k = random.uniform(-1, 1)
        self.f = lambda x: self.k * (x - self.root1) * (x - self.root2) * (x - self.root3)
        print(f"Função de 3º Grau Gerada. Raízes = {self.root1}, {self.root2}, {self.root3}")

    class CalculateBehav(CyclicBehaviour):
        async def run(self):
            #Espera por uma mensagem com um valor de x para calcular
            res = await self.receive(timeout=10)
            if res:
                try:
                    x = float(res.body)
                    result = self.agent.f(x)
                    
                    print(f"Recebeu pedido de {res.sender} para x = {x}. f(x) = {int(result)}")

                    #Envia o resultado de volta
                    msg = Message(to=str(res.sender))
                    msg.set_metadata("performative", "inform")
                    msg.body = str(int(result))
                    await self.send(msg)
                except (ValueError, TypeError) as e:
                    print(f"Erro ao processar o pedido de {res.sender}: {e}")


    class ReportTypeBehav(CyclicBehaviour):
        async def run(self):
            # Espera por uma solicitação do tipo da função
            msg = await self.receive(timeout=10)
            if msg:
                # Envia o tipo da função de volta
                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "inform")
                response.body = self.agent.func_type
                await self.send(response)
                print(f"Respondeu para {msg.sender} com o tipo: {self.agent.func_type}")

    async def setup(self):
        """Setup do agente Gerador."""
        print(f"Agente Gerador {self.jid} inicializando...")

        self.func_type = random.choice(["1grau", "2grau", "3grau"])
        if self.func_type == "1grau":
            self._generate_1grau()
        elif self.func_type == "2grau":
            self._generate_2grau()
        else:
            self.func_type = "3grau"
            self._generate_3grau()
        
        #Comportamento para responder o tipo da função
        type_behav = self.ReportTypeBehav()
        template_type = Template()
        template_type.set_metadata("performative", "request")
        self.add_behaviour(type_behav, template_type)

        #Comportamento para calcular o valor da função
        calc_behav = self.CalculateBehav()
        template_calc = Template()
        template_calc.set_metadata("performative", "subscribe")
        self.add_behaviour(calc_behav, template_calc)


async def main():
    gerador_agent = Gerador("jvfg@jabb.im", "TrabS1")
    await gerador_agent.start(auto_register=True)
    print("Gerador iniciado e aguardando solicitações...")

    while gerador_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            await gerador_agent.stop()
            break
    print("Agente Gerador encerrou!")

if __name__ == "__main__":
    spade.run(main())