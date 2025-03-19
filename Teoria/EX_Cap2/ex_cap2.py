#Exercício Capítulo 2: Simula Sensores
##Aluno: Matheus Vieira de Honorio Souza - GES - 525

import threading
import random
import time
from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bancoiot"]
collection = db["sensores"]

# Garante que os sensores existem no banco de dados
sensores = ["Temp1", "Temp2", "Temp3"]

for sensor in sensores:
    if not collection.find_one({"nomeSensor": sensor}):
        collection.insert_one({
            "nomeSensor": sensor,
            "valorSensor": 0,
            "unidadeMedida": "C°",
            "sensorAlarmado": False
        })

# Função para simular o sensor
def simular_sensor(nome_sensor):
    while True:
        # Gera uma temperatura aleatória entre 30 e 40
        temperatura = random.uniform(30, 40)
        print(f"{nome_sensor} - Temperatura: {temperatura:.2f}°C")

        # Atualiza o documento do sensor no MongoDB
        result = collection.update_one(
            {"nomeSensor": nome_sensor},
            {
                "$set": {
                    "valorSensor": temperatura,
                    "unidadeMedida": "C°",
                    "sensorAlarmado": temperatura > 38
                }
            }
        )

        # Verifica se a atualização foi bem-sucedida
        if result.matched_count == 0:
            print(f"Erro: Sensor {nome_sensor} não encontrado no banco de dados.")
        elif result.modified_count == 0:
            print(f"Aviso: Nenhum dado foi modificado para o sensor {nome_sensor}.")

        # Se a temperatura for maior que 38, exibe um alerta
        if temperatura > 38:
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {nome_sensor}!")

        # Espera um tempo antes de gerar a próxima leitura
        time.sleep(5)

        
        
# Função para lidar com o encerramento via Ctrl+C
def main():
    try:
        # Cria as threads para cada sensor
        sensor1 = threading.Thread(target=simular_sensor, args=("Temp1",))
        sensor2 = threading.Thread(target=simular_sensor, args=("Temp2",))
        sensor3 = threading.Thread(target=simular_sensor, args=("Temp3",))
                
        # Configura as threads como daemon para encerrar quando o programa principal terminar
        sensor1.daemon = True
        sensor2.daemon = True
        sensor3.daemon = True
                
        # Inicia as threads
        sensor1.start()
        sensor2.start()
        sensor3.start()
                
        # Mantém o programa principal rodando até que Ctrl+C seja pressionado
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando programa...")
                # As threads daemon serão automaticamente encerradas

if __name__ == "__main__":
    main()
