import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import math
import asyncio # Import asyncio for sleep

"""
Credenciais dos Agentes
Gerador: jvfg@jabb.im
Resolvedor: rcvr@jabb.im
Senha de ambos: TrabS1
"""

class Resolvedor(Agent):

    class RequestFunctionType(CyclicBehaviour):
        async def run(self):
            print(f"[Resolvedor] Sending request for function type to Gerador...")
            msg = Message(to="jvfg@jabb.im")
            msg.set_metadata("performative", "request")
            msg.body = "Qual é o tipo da função?"
            await self.send(msg)
            print(f"[Resolvedor] Request sent.")

            resposta = await self.receive(timeout=10)  # Wait for a response
            if resposta:
                print(f"[Resolvedor] (RequestFunctionType) Received message. Sender: {resposta.sender}, Performative: {resposta.get_metadata('performative')}, Body: {resposta.body}")
                if resposta.get_metadata("performative") == "inform" and str(resposta.sender) == "jvfg@jabb.im":
                    print(f"[Resolvedor] Correct response received from Gerador: {resposta.body}")
                    self.agent.function_type = resposta.body
                    print(f"[Resolvedor] Function type stored: {self.agent.function_type}")
                else:
                    print(f"[Resolvedor] Received unexpected message (did not match expected 'inform' or sender from template).")
            else:
                print(f"[Resolvedor] No response received from Gerador within the timeout (10s). Re-trying in next cycle.")

    async def setup(self):
        print(f"[Resolvedor] Resolvedor agent {self.jid} started.")
        self.function_type = None

        rcvr_behav = self.RequestFunctionType()

        receive_template = Template()
        receive_template.set_metadata("performative", "inform")

        self.add_behaviour(rcvr_behav, receive_template)


async def main():
    resolvedor_agent = Resolvedor("rcvr@jabb.im", "TrabS1")
    await resolvedor_agent.start()
    # Add a small delay here to ensure Gerador is fully online
    print("[Resolvedor] Giving Gerador a moment to get ready...")
    await asyncio.sleep(2) # Wait for 2 seconds
    await spade.wait_until_finished(resolvedor_agent)
    print("[Resolvedor] Agente Resolvedor encerrou!")

if __name__ == "__main__":
    spade.run(main())