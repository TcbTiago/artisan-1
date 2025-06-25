from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('127.0.0.1', port=502)
result = client.read_input_registers(address=0, count=3, slave=1)
print(result.registers)