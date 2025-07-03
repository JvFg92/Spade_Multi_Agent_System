import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random

class Resolvedor(Agent):
    class DiscoverDegree(CyclicBehaviour):
        async def run(self):
            print("[Resolvedor] Solicitando grau da função...")
            msg = Message(to="jvfg@localhost")
            msg.set_metadata("performative", "request")
            msg.body = "Qual o grau da função?"
            await self.send(msg)

            resposta = await self.receive(timeout=5)
            if resposta:
                degree = resposta.body
                print(f"[Resolvedor] Grau da função: {degree}")
                if degree in ["1", "2", "3"]:
                    self.agent.degree = int(degree)
                    print(f"[Resolvedor] Função de {degree}º grau")
                    self.agent.add_behaviour(self.agent.SecantMethod())
                    self.kill()
                else:
                    print(f"[Resolvedor] Grau inválido: {degree}")
                    self.kill()

    class SecantMethod(CyclicBehaviour):
        async def on_start(self):
            print("[Resolvedor] Iniciando método da secante...")
            self.results = []  # Store (x, f(x)) pairs
            self.x0 = random.randint(-100, 100)
            self.x1 = random.randint(-100, 100)
            while self.x1 == self.x0:
                self.x1 = random.randint(-100, 100)
            self.y0 = await self.check_fx(self.x0)
            self.y1 = await self.check_fx(self.x1)
            self.results.append((self.x0, self.y0))
            self.results.append((self.x1, self.y1))
            self.i = 0
            self.max_iterations = 100
        
        async def run(self):
            if self.i >= self.max_iterations:
                print(f"[Resolvedor] Máximo de iterações ({self.max_iterations}) atingido.")
                self.kill()
                await self.agent.stop()
                return

            if (self.y1 - self.y0) == 0:
                print("[Resolvedor] Derivada nula, escolhendo novos pontos...")
                self.x0 = random.randint(-100, 100)
                self.x1 = random.randint(-100, 100)
                while self.x1 == self.x0:
                    self.x1 = random.randint(-100, 100)
                self.y0 = await self.check_fx(self.x0)
                self.y1 = await self.check_fx(self.x1)
                self.results.append((self.x0, self.y0))
                self.results.append((self.x1, self.y1))
                return

            x = self.x1 - self.y1 * (self.x1 - self.x0) / (self.y1 - self.y0)
            x = max(min(x, 100), -100)  # Keep within bounds
            y = await self.check_fx(x)
            self.results.append((x, y))

            print(f"[Resolvedor] Iteração {self.i}: f({x:.6f}) = {y:.6f}")
            if abs(y) < 1e-6:
                print(f"[Resolvedor] Raiz encontrada: f({x:.6f}) ≈ 0")
                print(f"[Resolvedor] Pontos coletados: {self.results}")
                self.kill()
                await self.agent.stop()
                return

            self.x0, self.x1 = self.x1, x
            self.y0, self.y1 = self.y1, y
            self.i += 1

        async def check_fx(self, x):
            msg = Message(to="jvfg@localhost")
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x)
            await self.send(msg)
            resposta = await self.receive(timeout=10)  # Increased timeout
            if resposta:
                try:
                    y = float(resposta.body)
                    print(f"[Resolvedor] Recebido: f({x}) = {y}")
                    return y
                except ValueError:
                    print(f"[Resolvedor] Resposta inválida: {resposta.body}")
                    return None
            print(f"[Resolvedor] Sem resposta para f({x})")
            return None

    async def setup(self):
        print(f"[Resolvedor] Resolvedor iniciado: {self.jid}")
        self.add_behaviour(self.DiscoverDegree())

async def main():
    resolvedor = Resolvedor("rcvr@localhost", "TrabS1")
    await resolvedor.start()
    await spade.wait_until_finished(resolvedor)
    print("[Resolvedor] Resolvedor encerrou!")

if __name__ == "__main__":
    spade.run(main())