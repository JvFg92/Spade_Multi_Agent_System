import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import asyncio
import math

#Oi jv
"""
Credenciais dos Agentes
Gerador: jvfg@jabb.im
Resolvedor: rcvr@jabb.im
Senha de ambos: TrabS1
"""

# Endereço JID do Agente Gerador
GERADOR_JID = "jvfg@jabb.im"

# Definição dos estados da máquina de estados
STATE_GET_TYPE = "GET_FUNCTION_TYPE"
STATE_SOLVE = "SOLVE_FUNCTION"
STATE_SUCCESS = "SUCCESS"
STATE_FAIL = "FAIL"

class ResolvedorAgent(Agent):

    class SolverFSM(FSMBehaviour):
        async def on_start(self):
            print("Iniciando FSM: Começando pelo estado GET_FUNCTION_TYPE.")
            self.agent.func_type = None

        async def on_end(self):
            print("FSM finalizada.")
            await self.agent.stop()

    class GetTypeState(State):
        async def run(self):
            print("[Estado GetType] Solicitando tipo da função ao Gerador...")
            
            #Envia uma mensagem de 'request' para obter o tipo da função
            msg = Message(to=GERADOR_JID)
            msg.set_metadata("performative", "request")
            msg.body = "Qual o tipo da sua função?"
            await self.send(msg)

            # Aguarda a resposta por até 20 segundos
            response = await self.receive(timeout=20)
            if response:
                self.agent.func_type = response.body
                print(f"[Estado GetType] Tipo recebido: {self.agent.func_type}")
                self.set_next_state(STATE_SOLVE)
            else:
                print("[Estado GetType] O Gerador não respondeu a tempo.")
                self.set_next_state(STATE_FAIL)

    class SolveState(State):
        async def ask_gerador(self, x_value):
            """Envia um valor x e retorna a resposta f(x) do gerador."""
            msg = Message(to=GERADOR_JID)
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x_value)
            await self.send(msg)

            response = await self.receive(timeout=20)
            if response and response.body:
                return int(response.body)
            return None

        async def solve_1grau(self):
            print("[Estado Solve] Iniciando resolução para função de 1º grau.")
            # Passo 1: Obter f(0) para encontrar 'b'
            f0 = await self.ask_gerador(0)
            if f0 is None: return False
            b = f0
            print(f"   f(0) = {b}")

            # Passo 2: Obter f(1) para encontrar 'a'
            f1 = await self.ask_gerador(1)
            if f1 is None: return False
            a = f1 - b
            print(f"   f(1) = {f1} => a = {a}")

            if a == 0:
                print("   'a' é zero. Não é possível dividir por zero.")
                return False
            
            # Passo 3: Calcular a raiz e verificar
            root = -b / a
            if root.is_integer():
                print(f"   Raiz calculada: {int(root)}. Verificando...")
                result = await self.ask_gerador(int(root))
                if result == 0:
                    self.agent.solution = int(root)
                    return True
            return False

        async def solve_2grau(self):
            print("[Estado Solve] Iniciando resolução para função de 2º grau.")
            # Obter 3 pontos para resolver o sistema: f(x) = ax^2 + bx + c
            f0 = await self.ask_gerador(0) # f(0) = c
            f1 = await self.ask_gerador(1) # f(1) = a + b + c
            fn1 = await self.ask_gerador(-1) # f(-1) = a - b + c
            
            if f0 is None or f1 is None or fn1 is None: return False

            c = f0
            # a+b = f1-c  ; a-b = fn1-c
            # 2a = f1+fn1-2c => a = (f1+fn1-2c)/2
            # 2b = f1-fn1 => b = (f1-fn1)/2
            a = (f1 + fn1 - 2*c) / 2
            b = (f1 - fn1) / 2
            
            print(f"   Coeficientes encontrados: a={a}, b={b}, c={c}")

            if a == 0: # Não é uma equação quadrática
                return await self.solve_1grau() # Tenta resolver como 1º grau

            # Calcula o discriminante
            delta = b**2 - 4*a*c
            if delta < 0: return False # Não há raízes reais

            # Fórmula de Bhaskara
            root1 = (-b + math.sqrt(delta)) / (2*a)
            root2 = (-b - math.sqrt(delta)) / (2*a)

            # Testa a primeira raiz inteira
            if root1.is_integer():
                if await self.ask_gerador(int(root1)) == 0:
                    self.agent.solution = int(root1)
                    return True
            # Testa a segunda raiz inteira
            if root2.is_integer():
                if await self.ask_gerador(int(root2)) == 0:
                    self.agent.solution = int(root2)
                    return True
            
            return False

        async def solve_3grau(self):
            print("[Estado Solve] Iniciando resolução para função de 3º grau (busca sistemática).")
            # Busca sistemática de -1000 a 1000
            for x in range(-1000, 1001):
                print(f"   Tentando x = {x}...")
                result = await self.ask_gerador(x)
                if result is None: return False # Falha na comunicação
                if result == 0:
                    self.agent.solution = x
                    return True
                # Otimização: se o sinal mudar, a raiz está próxima, mas a busca linear já cobre isso.
            return False

        async def run(self):
            func_type = self.agent.func_type
            success = False
            if func_type == "1grau":
                success = await self.solve_1grau()
            elif func_type == "2grau":
                success = await self.solve_2grau()
            elif func_type == "3grau":
                success = await self.solve_3grau()
            else:
                print(f"[Estado Solve] Tipo de função desconhecido: {func_type}")

            if success:
                self.set_next_state(STATE_SUCCESS)
            else:
                print("[Estado Solve] Não foi possível encontrar a solução.")
                self.set_next_state(STATE_FAIL)

    # #################################################################
    # ESTADOS FINAIS: SUCCESS e FAIL
    # #################################################################
    class SuccessState(State):
        async def run(self):
            print("\n" + "="*40)
            print("  SUCESSO! O zero da função foi encontrado.")
            print(f"  A raiz é: {self.agent.solution}")
            print("="*40)

    class FailState(State):
        async def run(self):
            print("\n" + "!"*40)
            print("  FALHA! Não foi possível encontrar a raiz.")
            print("!"*40)

    async def setup(self):
        print(f"Agente Resolvedor {self.jid} inicializando...")
        # Cria a máquina de estados (FSM)
        fsm = self.SolverFSM()
        # Adiciona os estados
        fsm.add_state(name=STATE_GET_TYPE, state=self.GetTypeState(), initial=True)
        fsm.add_state(name=STATE_SOLVE, state=self.SolveState())
        fsm.add_state(name=STATE_SUCCESS, state=self.SuccessState())
        fsm.add_state(name=STATE_FAIL, state=self.FailState())
        # Adiciona as transições
        fsm.add_transition(source=STATE_GET_TYPE, dest=STATE_SOLVE)
        fsm.add_transition(source=STATE_GET_TYPE, dest=STATE_FAIL)
        fsm.add_transition(source=STATE_SOLVE, dest=STATE_SUCCESS)
        fsm.add_transition(source=STATE_SOLVE, dest=STATE_FAIL)
        
        self.add_behaviour(fsm)

async def main():
    # O user do resolvedor é rcvr@jabb.im
    resolvedor_agent = ResolvedorAgent("rcvr@jabb.im", "TrabS1")
    await resolvedor_agent.start(auto_register=True)

    # Aguarda o agente finalizar
    while resolvedor_agent.is_alive():
        await asyncio.sleep(1)

    print("Agente Resolvedor encerrou.")


if __name__ == "__main__":
    spade.run(main())