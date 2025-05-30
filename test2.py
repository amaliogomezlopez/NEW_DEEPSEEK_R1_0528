import ollama
import sys

MODEL_NAME = "deepseek-r1:8b-0528-qwen3-fp16"


try:
    ollama.list()
    print(f"Ollama server está funcionando. Modelo seleccionado: {MODEL_NAME}")
except Exception as e:
    print(f"Error: No se pudo conectar al servidor de Ollama.")
    print(f"Asegúrate de que Ollama está instalado y ejecutándose.")
    print(f"Detalles del error: {e}")
    sys.exit(1)


user_prompt = """give me python code to create a simple calculator. Use Tkinter for graphic interface"""


default_generation_options = {
    "temperature": 0.7,      
    "top_k": 50,
    "top_p": 0.9,
    "num_predict": 5000,      
    "stop": [],
    "seed": 42,              
    "repeat_penalty": 1.1,
}

my_options = default_generation_options.copy()


my_options.update({
    "mirostat": 2,           
    "mirostat_tau": 5.0,
    "mirostat_eta": 0.1,
})

try:
    print(f"\n--- Generando respuesta con razonamiento para el modelo: {MODEL_NAME} ---")
    print(f"Prompt: {user_prompt[:200]}...")  
    print(f"Opciones de Generación: {my_options}\n")

    
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': user_prompt}],
        options=my_options,
        stream=True  
    )
    
    print("\n--- Razonamiento y Respuesta ---")
    full_response = ""
    for chunk in response:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_response += content
    
    
    with open("razonamiento_respuesta.txt", "w", encoding="utf-8") as f:
        f.write(full_response)
    
    print("\n\n--- Resumen ---")
    print(f"Respuesta completa guardada en 'razonamiento_respuesta.txt'")
    print(f"Longitud total de la respuesta: {len(full_response)} caracteres")

except ollama.ResponseError as e:
    print(f"\nError de Ollama: {e}")
    if "model not found" in str(e).lower():
        print(f"¡El modelo '{MODEL_NAME}' no está instalado!")
        print(f"Puedes instalarlo con: ollama pull {MODEL_NAME}")
except Exception as e:
    print(f"\nError inesperado: {e}")