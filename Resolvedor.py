import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

class Resolvedor(Agent):
    x = random.randint(-1000, 1000)
    a = 0
    while a == 0:
        a = random.randint(-100, 100)
    y = -1 * (a * x)

    class funcao_1grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float(Resolvedor.a * x + Resolvedor.y)
                print("Enviou para " + str(res.sender) + " f(", res.body, ")= ", x, "=>", int(x))
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)
    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body = "1grau" 
                await self.send(msg)
                print("Respondeu para" + str(msg.sender) + " com " + msg.body)
    async def setup(self):
        t = Template()
        t.set_metadata("performative", "subscribe")

        tf = self.funcao_1grau()
        print("Funcao de 1o grau: ", Resolvedor.x)
        print("Funcao: ", Resolvedor.a, "x + (", Resolvedor.y, ")")

        self.add_behaviour(tf, t)

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)
async def main():
    resolvedor = Resolvedor("jvfg@jabb.im", "TrabS1")
    await resolvedor.start()

    while resolvedor.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            resolvedor.stop()
            break
    print("Agente encerrou!")
if __name__ == "__main__":
    spade.run(main())
    print("Agente Resolvedor iniciado!")