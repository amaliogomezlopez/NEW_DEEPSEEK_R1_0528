import ollama
import sys
from pydantic import BaseModel, Field
from typing import List
import time

MODEL_NAME = "deepseek-r1:8b-0528-qwen3-fp16"

try:
    ollama.list()
    print(f"Ollama server está funcionando. Modelo seleccionado: {MODEL_NAME}")
except Exception as e:
    print(f"Error: No se pudo conectar al servidor de Ollama.")
    print(f"Detalles del error: {e}")
    sys.exit(1)


user_prompt = """tell me all the fruits and their colours"""

# --- Configuración Detallada de Opciones de Generación con Comentarios ---
generation_options = {
    # Control de aleatoriedad (0=determinista, 1=muy creativo)
    "temperature": 0.5,  # Punto medio para equilibrio entre creatividad y estructura
    
    # Número de tokens más probables a considerar en cada paso (afecta diversidad)
    "top_k": 50,  # Valor moderado para permitir variedad pero mantener relevancia
    
    # Muestreo por probabilidad acumulada (0.9 = considera hasta el 90% de probabilidad acumulada)
    "top_p": 0.9,  # Estándar para buenos resultados balanceados
    
    # Máximo de tokens a generar (512 permite respuesta detallada)
    "num_predict": 512,
    
    # Secuencias que detienen la generación (vacío para no detener prematuramente)
    "stop": [],
    
    # Semilla para reproducibilidad (0=aleatorio, cualquier otro número=fijo)
    "seed": 42,  # Fijo para resultados reproducibles
    
    # Penalización por repetición (1=no penaliza, >1 penaliza más)
    "repeat_penalty": 1.1,  # Ligera penalización para evitar repeticiones
    
    # Algoritmo de control de calidad (0=off, 1=mirostat, 2=mirostat 2.0)
    "mirostat": 2,  # Versión 2.0 para mejor coherencia en textos largos
    
    # Objetivo de perplejidad para mirostat (5.0 es valor estándar)
    "mirostat_tau": 5.0,
    
    # Tasa de aprendizaje para mirostat (0.1 es valor estándar)
    "mirostat_eta": 0.1,
    
    # Tail Free Sampling (1.0=desactivado, valores menores favorecen tokens menos probables)
    "tfs_z": 1.0,  
}

try:
    print(f"\n--- Generando respuesta JSON con razonamiento ---")
    print(f"Modelo: {MODEL_NAME}")
    print(f"Prompt: {user_prompt[:150]}...")  
    
    start_time = time.time() 

    print(f"\nIniciando generación de respuesta a las: {time.ctime(start_time)}")

    '''response = ollama.chat(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': user_prompt}],
        options=generation_options,
        format='json',
        stream=False
    )'''

    class Fruit(BaseModel):
        name: str = Field(..., description="The name of the fruit")
        color: str = Field(..., description="The primary color of the fruit")


    class FruitsListResponse(BaseModel):

        fruits: List[Fruit] = Field(..., description="A list of various fruits and their colors")

    response = ollama.chat(
    messages=[{'role': 'user', 'content': user_prompt}],
    model=MODEL_NAME,
    format=FruitsListResponse.model_json_schema(),
    )

    end_time = time.time() 

    elapsed_seconds = end_time - start_time
    elapsed_minutes = elapsed_seconds / 60

    print(f"\nGeneración completada a las: {time.ctime(end_time)}")
    print(f"--- Tiempo total de generación: {elapsed_seconds:.2f} segundos ({elapsed_minutes:.2f} minutos) ---")

    eval_count = response.get('eval_count')

    eval_duration_ns = response.get('eval_duration')

    if eval_count is not None and eval_duration_ns is not None:
       
        eval_duration_s = eval_duration_ns / 1_000_000_000
        
        # Evitar división por cero
        if eval_duration_s > 0:
            tokens_per_second = eval_count / eval_duration_s
            print(f"--- Tokens Generados: {eval_count} ---")
            print(f"--- Tiempo de Evaluación del Modelo: {eval_duration_s:.4f} segundos ---")
            print(f"--- Tasa de Generación (Tokens/segundo): {tokens_per_second:.2f} tokens/s ---")
        else:
            print("Advertencia: El tiempo de evaluación fue cero, no se puede calcular TPS.")
    else:
        print("Advertencia: Métricas 'eval_count' o 'eval_duration' no encontradas en la respuesta de Ollama.")


    #print(response)
    ai_response = response['message']['content']
    
    print("\n--- Respuesta JSON Cruda ---")
    print(ai_response)

        
except ollama.ResponseError as e:
    print(f"\nError de Ollama: {e}")
    if "model not found" in str(e).lower():
        print(f"¿Has instalado el modelo? Prueba: ollama pull {MODEL_NAME}")
except Exception as e:
    print(f"\nError inesperado: {e}")