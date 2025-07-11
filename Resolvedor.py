import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import numpy as np

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
                    if self.agent.degree == 1:
                        self.agent.solve_method = self.agent.SolveFunction.solve_1grau
                    elif self.agent.degree == 2:
                        self.agent.solve_method = self.agent.SolveFunction.solve_2grau
                    else:
                        self.agent.solve_method = self.agent.SolveFunction.solve_3grau
                    self.agent.add_behaviour(self.agent.SolveFunction())
                    self.kill()

                else:
                    print(f"[Resolvedor] Grau inválido: {degree}")
                    self.kill()

    class SolveFunction(CyclicBehaviour):
        async def on_start(self):
            print(f"[Resolvedor] Iniciando resolução para função de {self.agent.degree}º grau...")
            self.results = []
            self.points_needed = self.agent.degree + 1
            self.available_x = list(range(-1000, 1001))
            random.shuffle(self.available_x)

        async def run(self):
            if len(self.results) >= self.points_needed:
                print(f"[Resolvedor] Pontos suficientes coletados: {self.results}")
                await self.agent.solve_method(self)
                self.kill()
                await self.agent.stop()
                return

            if not self.available_x:
                print("[Resolvedor] Sem mais valores de x disponíveis.")
                self.kill()
                await self.agent.stop()
                return

            x = self.available_x.pop()
            y = await self.check_fx(x)
            if y is not None:
                self.results.append((x, y))
                print(f"[Resolvedor] Ponto adicionado: ({x}, {y})")

        async def check_fx(self, x):
            msg = Message(to="jvfg@localhost")
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x)
            await self.send(msg)
            resposta = await self.receive(timeout=10)
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

        async def solve_1grau(self):
            print("[Resolvedor] Resolvendo função de 1º grau...")
            x0, y0 = self.results[0]
            x1, y1 = self.results[1]
            if x0 == x1:
                print("[Resolvedor] Pontos com mesmo x, não é possível resolver.")
                return
            a = (y1 - y0) / (x1 - x0)
            b = y0 - a * x0
            if a == 0:
                print("[Resolvedor] Função constante, sem raiz única.")
                return
            root = -b / a
            print(f"[Resolvedor] Função estimada: f(x) = {a:.6f}x + {b:.6f}")
            print(f"[Resolvedor] Raiz encontrada: x = {root:.6f}")

        async def solve_2grau(self):
            print("[Resolvedor] Resolvendo função de 2º grau...")
            x0, y0 = self.results[0]
            x1, y1 = self.results[1]
            x2, y2 = self.results[2]
            try:
                A = np.array([[x0**2, x0, 1], [x1**2, x1, 1], [x2**2, x2, 1]])
                B = np.array([y0, y1, y2])
                a, b, c = np.linalg.solve(A, B)
                print(f"[Resolvedor] Função estimada: f(x) = {a:.6f}x^2 + {b:.6f}x + {c:.6f}")
                discriminant = b**2 - 4*a*c
                if discriminant < 0:
                    print("[Resolvedor] Função não possui raízes reais.")
                    return
                root1 = (-b + discriminant**0.5) / (2*a)
                root2 = (-b - discriminant**0.5) / (2*a)
                print(f"[Resolvedor] Raízes encontradas: x1 = {root1:.6f}, x2 = {root2:.6f}")
            except np.linalg.LinAlgError:
                print("[Resolvedor] Não foi possível ajustar a função quadrática (matriz singular).")

        async def solve_3grau(self):
            print("[Resolvedor] Resolvendo função de 3º grau...")
            x0, y0 = self.results[0]
            x1, y1 = self.results[1]
            x2, y2 = self.results[2]
            x3, y3 = self.results[3]
            try:
                A = np.array([[x0**3, x0**2, x0, 1], [x1**3, x1**2, x1, 1], [x2**3, x2**2, x2, 1], [x3**3, x3**2, x3, 1]])
                B = np.array([y0, y1, y2, y3])
                k, b, c, d = np.linalg.solve(A, B)
                print(f"[Resolvedor] Função estimada: f(x) = {k:.6f}x^3 + {b:.6f}x^2 + {c:.6f}x + {d:.6f}")
            except np.linalg.LinAlgError:
                print("[Resolvedor] Não foi possível ajustar a função cúbica (matriz singular).")
                return

            points = sorted(self.results, key=lambda p: p[0])
            root1 = None
            for i in range(len(points) - 1):
                x0, y0 = points[i]
                x1, y1 = points[i + 1]
                if y0 * y1 < 0:
                    print(f"[Resolvedor] Intervalo com mudança de sinal: [{x0}, {x1}]")
                    root1 = await self._bisection(x0, x1)
                    if root1 is not None:
                        print(f"[Resolvedor] Raiz encontrada: x1 = {root1:.6f}")
                        break
            if root1 is None:
                print("[Resolvedor] Não foi encontrado intervalo com mudança de sinal.")
                return

            q_a = k
            q_b = b + k * root1
            q_c = c + b * root1 + k * root1**2
            discriminant = q_b**2 - 4*q_a*q_c
            if discriminant >= 0:
                root2 = (-q_b + discriminant**0.5) / (2*q_a)
                root3 = (-q_b - discriminant**0.5) / (2*q_a)
                print(f"[Resolvedor] Raízes adicionais encontradas: x2 = {root2:.6f}, x3 = {root3:.6f}")
            else:
                print("[Resolvedor] Nenhuma raiz real adicional (discriminante negativo na quadrática restante).")

        async def _bisection(self, a, b, tolerance=1e-6, max_iter=100):
            ya = await self.check_fx(a)
            yb = await self.check_fx(b)
            if ya is None or yb is None or ya * yb >= 0:
                return None
            for _ in range(max_iter):
                c = (a + b) / 2
                yc = await self.check_fx(c)
                if yc is None:
                    return None
                if abs(yc) < tolerance or (b - a) / 2 < tolerance:
                    return c
                if ya * yc < 0:
                    b = c
                    yb = yc
                else:
                    a = c
                    ya = yc
            return (a + b) / 2

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
