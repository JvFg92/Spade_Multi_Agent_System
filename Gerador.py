"""
Please take a look in the repository https://github.com/JvFg92/Spade_Multi_Agent_System in github.
"""

import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random

class Gerador(Agent):
    class GenerateFunction(OneShotBehaviour):
        def _generate_1grau(self):
            """Gera uma função de 1º grau: f(x) = ax + b"""
            self.agent.root1 = random.randint(-1000, 1000)
            self.agent.a = 0
            while self.agent.a == 0:
                self.agent.a = random.randint(-1000, 1000)
            self.agent.b = -self.agent.a * self.agent.root1
            self.agent.coefs = [self.agent.b, self.agent.a]  # [constant, x]
            func_str = f"f(x) = {self.agent.a}x + {self.agent.b}"
            print(f"[Gerador] Função de 1º Grau Gerada: {func_str}. Raiz = {self.agent.root1}")

        def _generate_2grau(self):
            """Gera uma função de 2º grau: f(x) = a(x-r1)(x-r2)"""
            self.agent.root1 = random.randint(-1000, 1000)
            self.agent.root2 = random.randint(-1000, 1000)
            self.agent.a = 0
            while self.agent.a == 0:
                self.agent.a = random.randint(-10, 10)
            # f(x) = a * (x^2 - (r1+r2)x + r1*r2)
            b = -self.agent.a * (self.agent.root1 + self.agent.root2)
            c = self.agent.a * self.agent.root1 * self.agent.root2
            self.agent.coefs = [c, b, self.agent.a]  # [constant, x, x^2]
            func_str = f"f(x) = {self.agent.a}x^2 + {b}x + {c}"
            print(f"[Gerador] Função de 2º Grau Gerada: {func_str}. Raízes = {self.agent.root1}, {self.agent.root2}")

        def _generate_3grau(self):
            """Gera uma função de 3º grau: f(x) = k(x-r1)(x-r2)(x-r3)"""
            self.agent.root1 = random.randint(-1000, 1000)
            self.agent.root2 = random.randint(-1000, 1000)
            self.agent.root3 = random.randint(-1000, 1000)
            self.agent.k = 0
            while self.agent.k == 0:
                self.agent.k = random.randint(-10, 10)
            # f(x) = kx^3 - k(r1+r2+r3)x^2 + k(r1r2+r1r3+r2r3)x - k*r1*r2*r3
            b = -self.agent.k * (self.agent.root1 + self.agent.root2 + self.agent.root3)
            c = self.agent.k * (self.agent.root1 * self.agent.root2 + self.agent.root1 * self.agent.root3 + self.agent.root2 * self.agent.root3)
            d = -self.agent.k * self.agent.root1 * self.agent.root2 * self.agent.root3
            self.agent.coefs = [d, c, b, self.agent.k]  # [constant, x, x^2, x^3]
            func_str = f"f(x) = {self.agent.k}x^3 + {b}x^2 + {c}x + {d}"
            print(f"[Gerador] Função de 3º Grau Gerada: {func_str}. Raízes = {self.agent.root1}, {self.agent.root2}, {self.agent.root3}")

        async def run(self):
            self.agent.degree = random.choice([1, 2, 3])
            if self.agent.degree == 1:
                self._generate_1grau()
            elif self.agent.degree == 2:
                self._generate_2grau()
            else:
                self._generate_3grau()

    class CalculateFunction(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                
                x = float(msg.body)
                y = 0
                for i in range(len(self.agent.coefs)):
                    y += self.agent.coefs[i] * (x ** i)
                reply = Message(to=str(msg.sender))
                reply.set_metadata("performative", "inform")
                reply.body = str(y)
                await self.send(reply)
                print(f"[Gerador] Enviado para {msg.sender}: f({x}) = {y}")
                

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