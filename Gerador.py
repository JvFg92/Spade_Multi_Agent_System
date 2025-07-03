import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random

class Gerador(Agent):
    class GenerateFunction(OneShotBehaviour):
        async def run(self):
            self.agent.x = random.randint(-100, 100)  # Single known root
            self.agent.degree = random.choice([1, 2, 3])
            self.agent.coefs = []
            for i in range(self.agent.degree):  # Generate coefficients
                k = 0
                while k == 0:
                    k = random.randint(-100, 100)
                self.agent.coefs.append(k)
            self.agent.ki = 0  # Independent term
            for i in range(self.agent.degree):
                self.agent.ki -= self.agent.coefs[i] * (self.agent.x ** (i + 1))
            
            # Format and print function
            func_str = "f(x) = "
            for i in range(self.agent.degree, 0, -1):
                coef = self.agent.coefs[i-1]
                func_str += f"({coef})*x^{i} + "
            func_str += f"({self.agent.ki})"
            print(f"[Gerador] Função gerada: {func_str}")
            print(f"[Gerador] Raiz da função: x = {self.agent.x}")

    class CalculateFunction(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                try:
                    x = float(msg.body)
                    y = 0
                    for i in range(self.agent.degree, 0, -1):
                        coef = self.agent.coefs[i-1]
                        y += coef * x ** i
                    y += self.agent.ki
                    reply = Message(to=str(msg.sender))
                    reply.set_metadata("performative", "inform")
                    reply.body = str(y)
                    await self.send(reply)
                    print(f"[Gerador] Enviado para {msg.sender}: f({x}) = {y}")
                except ValueError:
                    print(f"[Gerador] Valor x inválido recebido: {msg.body}")

    class InformFunctionDegree(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                reply = Message(to=str(msg.sender))
                reply.set_metadata("performative", "inform")
                reply.body = str(self.agent.degree)
                await self.send(reply)
                print(f"[Gerador] Respondeu para {msg.sender} com grau {self.agent.degree}")

    async def setup(self):
        print(f"[Gerador] Gerador iniciado: {self.jid}")
        self.add_behaviour(self.GenerateFunction())
        t1 = Template()
        t1.set_metadata("performative", "subscribe")
        self.add_behaviour(self.CalculateFunction(), t1)
        t2 = Template()
        t2.set_metadata("performative", "request")
        self.add_behaviour(self.InformFunctionDegree(), t2)

async def main():
    gerador = Gerador("jvfg@localhost", "TrabS1")
    await gerador.start()
    await spade.wait_until_finished(gerador)
    print("[Gerador] Gerador encerrou!")

if __name__ == "__main__":
    spade.run(main())