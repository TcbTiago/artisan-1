from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
import threading
import time

# Logging de escritas
class CustomDataBlock(ModbusSequentialDataBlock):
    def setValues(self, address, values):
        print(f"[MODBUS WRITE] Endereço: {address}, Valores: {values}")
        super().setValues(address, values)

store = ModbusSlaveContext(
    di=CustomDataBlock(0, [0]*3000),
    co=CustomDataBlock(0, [0]*3000),
    hr=CustomDataBlock(0, [0]*3000),
    ir=CustomDataBlock(0, [0]*3000)
)
context = ModbusServerContext(slaves=store, single=True)

def atualiza_dinamico():
    while True:
        try:
            potencia = context[0].getValues(3, 2221, count=1)[0]  # Potência
            tambor = context[0].getValues(3, 2241, count=1)[0]    # Tambor
            ar = context[0].getValues(3, 2261, count=1)[0]        # Ar
        except:
            potencia = tambor = ar = 0

        bt = tambor
        et = ar
        ror = potencia

        # Escreve nos Holding Registers para o Artisan ler (endereços 1, 2 e 3)
        context[0].setValues(3, 1, [bt, et, ror])  # HR[1], HR[2], HR[3]

        print(f"[DINÂMICO] BT: {bt}, ET: {et}, RoR: {ror}")
        time.sleep(1)

threading.Thread(target=atualiza_dinamico, daemon=True).start()

print("Servidor Modbus TCP rodando em 127.0.0.1:502")
StartTcpServer(context, address=("127.0.0.1", 502))
