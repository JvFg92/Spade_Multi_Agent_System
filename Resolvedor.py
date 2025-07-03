import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import asyncio
import random

class Resolvedor(Agent):
    class RequestFunctionType(CyclicBehaviour):
        async def on_start(self):
            self.retry_count = 0
            self.max_retries = 3
            self.iteration_count = 0
            self.max_iterations = 5  # Limite de 5 iterações

        async def run(self):
            if self.iteration_count >= self.max_iterations:
                print(f"[Resolvedor] Max iterations ({self.max_iterations}) reached. Stopping.")
                self.kill()
                return

            if self.retry_count >= self.max_retries:
                print(f"[Resolvedor] Max retries ({self.max_retries}) reached for this iteration. Moving to next iteration.")
                self.retry_count = 0
                self.iteration_count += 1
                return

            print(f"[Resolvedor] Sending request for function type to Gerador... (Attempt {self.retry_count + 1}/{self.max_retries}, Iteration {self.iteration_count + 1}/{self.max_iterations})")
            msg = Message(to="jvfg@localhost")
            msg.set_metadata("performative", "request")
            msg.body = "Qual é o tipo da função?"
            await self.send(msg)
            print(f"[Resolvedor] Request sent.")

            resposta = await self.receive(timeout=15)
            if resposta:
                print(f"[Resolvedor] (RequestFunctionType) Received message. Sender: {resposta.sender}, Performative: {resposta.get_metadata('performative')}, Body: {resposta.body}")
                if resposta.get_metadata("performative") == "inform":
                    if resposta.body in ["1", "2", "3"]:
                        print(f"[Resolvedor] Correct response received from Gerador: {resposta.body}")
                        self.agent.function_type = resposta.body
                        print(f"[Resolvedor] Function type stored: {self.agent.function_type}")
                        self.agent.add_behaviour(self.agent.CalculateRequestBehav(self.iteration_count))
                        print(f"[Resolvedor] Added CalculateRequestBehav for iteration {self.iteration_count + 1}")
                        self.retry_count = 0
                        self.iteration_count += 1
                    else:
                        print(f"[Resolvedor] Invalid function type received: {resposta.body}")
                        self.retry_count += 1
                else:
                    print(f"[Resolvedor] Received unexpected message in RequestFunctionType.")
            else:
                print(f"[Resolvedor] No response received from Gerador within the timeout (15s).")
                self.retry_count += 1

    class CalculateRequestBehav(OneShotBehaviour):
        def __init__(self, iteration):
            super().__init__()
            self.iteration = iteration

        async def run(self):
            x = random.randint(-10, 10)
            print(f"[Resolvedor] Sending calculation request for x = {x} to Gerador (Iteration {self.iteration + 1})...")
            msg = Message(to="jvfg@localhost")
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x)
            await self.send(msg)
            print(f"[Resolvedor] Calculation request sent.")

            resposta = await self.receive(timeout=15)
            if resposta:
                print(f"[Resolvedor] (CalculateRequestBehav) Received message. Sender: {resposta.sender}, Performative: {resposta.get_metadata('performative')}, Body: {resposta.body}")
                if resposta.get_metadata("performative") == "inform":
                    print(f"[Resolvedor] Received calculation result from Gerador: f({x}) = {resposta.body}")
                else:
                    print(f"[Resolvedor] Received unexpected message in CalculateRequestBehav.")
            else:
                print(f"[Resolvedor] No response received for calculation request within the timeout (15s).")

    class DebugBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                if str(msg.sender).split('/')[0] == str(self.agent.jid).split('/')[0]:
                    print(f"[Resolvedor] (DebugBehav) Ignored message from self. Sender: {msg.sender}, Performative: {msg.get_metadata('performative')}, Body: {msg.body}")
                else:
                    print(f"[Resolvedor] (DebugBehav) Received unfiltered message. Sender: {msg.sender}, Performative: {msg.get_metadata('performative')}, Body: {msg.body}")
            else:
                print(f"[Resolvedor] (DebugBehav) No unfiltered message received within timeout (5s).")

    async def setup(self):
        print(f"[Resolvedor] Resolvedor agent {self.jid} started.")
        self.function_type = None

        rcvr_behav = self.RequestFunctionType()
        receive_template = Template()
        receive_template.set_metadata("performative", "inform")
        self.add_behaviour(rcvr_behav, receive_template)
        print(f"[Resolvedor] Added RequestFunctionType with template: performative='inform'")

        debug_behav = self.DebugBehav()
        self.add_behaviour(debug_behav)
        print(f"[Resolvedor] Added DebugBehav for unfiltered messages")

async def main():
    resolvedor_agent = Resolvedor("rcvr@localhost", "TrabS1")
    await resolvedor_agent.start()
    print("[Resolvedor] Giving Gerador a moment to get ready...")
    await asyncio.sleep(2)
    await spade.wait_until_finished(resolvedor_agent)
    print("[Resolvedor] Agente Resolvedor encerrou!")

if __name__ == "__main__":
    spade.run(main())