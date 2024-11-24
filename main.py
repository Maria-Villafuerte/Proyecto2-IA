import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents.agent_toolkits import create_csv_agent

load_dotenv()


def inicializar_agentes():
    """Inicializa todos los agentes de análisis."""
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    instrucciones = """
    - Eres un agente especializado en análisis energético que puede escribir y ejecutar código Python
    - Utiliza siempre las herramientas proporcionadas para responder preguntas, incluso para cálculos simples
    - Enfócate en el análisis de energías renovables e interpretación de datos
    - Si no puedes responder una pregunta, responde con "No tengo suficiente información para responder esa pregunta"
    - Proporciona explicaciones claras junto con tus cálculos
    - Siempre usa Python para realizar los cálculos
    """
    prompt = base_prompt.partial(instructions=instrucciones)

    llm = ChatOpenAI(temperature=0, model="gpt-4")
    tools = [PythonREPLTool()]

    python_agent = create_react_agent(
        prompt=prompt,
        llm=llm,
        tools=tools,
    )

    return AgentExecutor(agent=python_agent, tools=tools, verbose=True)


def crear_preguntas_predefinidas():
    """Crea un diccionario con preguntas predefinidas por categoría."""
    return {
        "Generación Térmica y Nuclear": [
            "Compara la generación nuclear estimada vs actual por región",
            "¿Qué región tuvo la mayor generación térmica?",
            "Muestra la tendencia de generación nuclear a lo largo del tiempo"
        ],
        "Plantas de Energía Global": [
            "¿Cuántas plantas hidroeléctricas hay por país?",
            "¿Cuál es la capacidad total instalada por tipo de combustible?",
            "Muestra las 5 plantas con mayor capacidad",
            "¿Cuál es la distribución geográfica de las plantas por tipo de combustible?"
        ],
        "Datos de Generación de Plantas": [
            "¿Cuál es la producción diaria promedio por planta?",
            "Muestra la tendencia de generación AC vs DC",
            "¿Cuál es el rendimiento total acumulado por planta?",
            "Compara el rendimiento entre diferentes plantas"
        ],
        "Energías Renovables": [
            "¿Cómo varía la generación de energía con la temperatura?",
            "¿Cuál es la correlación entre GHI y producción de energía?",
            "Analiza la producción de energía en diferentes condiciones climáticas",
            "¿Cuál es el impacto de la velocidad del viento en la generación?"
        ]
    }


def crear_agentes_csv():
    """Crea los agentes para análisis de archivos CSV."""
    llm = ChatOpenAI(temperature=0, model="gpt-4")

    return {
        "renovable": create_csv_agent(
            llm=llm,
            path="DocumentosCsv/Renewable.csv",
            verbose=True,
            allow_dangerous_code=True
        ),
        "generacion": create_csv_agent(
            llm=llm,
            path="DocumentosCsv/file_02.csv",
            verbose=True,
            allow_dangerous_code=True
        ),
        "planta_energia": create_csv_agent(
            llm=llm,
            path="DocumentosCsv/Global Power Plant.csv",
            verbose=True,
            allow_dangerous_code=True
        ),
        "generacion_planta": create_csv_agent(
            llm=llm,
            path="DocumentosCsv/Plant_2_Generation_Data.csv",
            verbose=True,
            allow_dangerous_code=True
        )
    }


def main():
    st.set_page_config(
        page_title="Agente de Análisis Energético Interactivo",
        page_icon="⚡",
        layout="wide"
    )

    # Estilo personalizado
    st.markdown(
        """
            <style>
    /* Estilos generales */
    .stApp {
        color: #1e1e1e;
    }

    /* Títulos y encabezados */
    .title {
        color: #2e7d32;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    h1 {
        color: #2e7d32 !important;
        font-weight: 700 !important;
    }

    h2 {
        color: #1e4620 !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }

    h3 {
        color: #357a38 !important;
        font-weight: 500 !important;
    }

    /* Botones */
    .stButton button {
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }

    .stButton button:hover {
        background-color: #1b5e20 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        transform: translateY(-1px);
    }


    /* Markdown y texto */
    .stMarkdown {
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #424242 !important;
    }

    /* Spinner de carga */
    .stSpinner > div {
        border-top-color: #2e7d32 !important;
    }

    /* Mensajes de error y éxito */
    .stAlert {
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* Código y resultados */
    .stCode {
        border-radius: 8px !important;
        background-color: #f8f9fa !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Divisor */
    hr {
        margin: 2rem 0 !important;
        border-color: #e0e0e0 !important;
    }

    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb {
        background: #2e7d32;
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #1b5e20;
    }

    /* Tarjetas para secciones principales */
    .stCard {
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 1px solid #e0e0e0;
    }

    /* Animaciones para elementos interactivos */
    .stSelectbox, .stTextInput, .stButton {
        transition: all 0.3s ease;
        color: #1e4620 !important;
    }

    .stSelectbox:hover, .stTextInput:hover {
        transform: translateY(-1px);
    }
    
     .stAlert.info {
            border: 1px solid #bbdefb !important; /* Borde azul claro */
            border-radius: 8px !important;
            padding: 1rem !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        }
    
    </style>
        """,
        unsafe_allow_html=True
    )

    st.title("⚡ Agente de Análisis Energético Interactivo")
    st.markdown("### Acerca de este Agente")
    st.markdown("""
    Este agente combina capacidades de computación Python con análisis de datos de plantas de energía globales.
    Puede ejecutar código Python para cálculos y analizar datos de energía renovable de varias fuentes.
    Use el campo de entrada para hacer preguntas específicas o seleccione de ejemplos predefinidos.
    """)

    # Inicialización de agentes
    python_agent_executor = inicializar_agentes()
    agentes_csv = crear_agentes_csv()

    # Sección de ejemplos Python
    st.markdown("## Ejemplos de Python")
    ejemplos_python = [
        "Calcula la suma de 2 y 3",
        "Genera una lista del 1 al 10",
        "Crea una función que calcule el factorial de un número",
    ]
    ejemplo_seleccionado = st.selectbox(
        "Seleccione un ejemplo:",
        ejemplos_python,
        key="ejemplo_python"
    )

    if st.button("Ejecutar Ejemplo", key="ejecutar_python"):
        with st.spinner("Procesando su solicitud..."):
            try:
                respuesta = python_agent_executor.invoke({"input": ejemplo_seleccionado})
                if 'output' in respuesta:
                    st.markdown("### Respuesta del Agente:")
                    st.code(respuesta['output'], language="python")
                else:
                    st.error("No se recibió respuesta del agente.")
            except Exception as e:
                st.error(f"Error al ejecutar el agente: {str(e)}")

    st.markdown("---")

    # Sección de Análisis de Datos de Energía Renovable
    st.markdown("## Análisis de Datos de Energía Renovable")
    st.markdown("### Conjuntos de Datos Disponibles")
    preguntas = crear_preguntas_predefinidas()

    # Selector de categoría
    categoria = st.selectbox(
        "Seleccione una categoría de análisis:",
        list(preguntas.keys()),
        key="categoria_analisis"
    )

    # Selector de pregunta predefinida
    pregunta_predefinida = st.selectbox(
        "Seleccione una pregunta predefinida o escriba la suya propia:",
        ["Seleccione una pregunta..."] + preguntas[categoria],
        key="pregunta_predefinida"
    )

    # Campo de texto para pregunta personalizada
    pregunta_personalizada = st.text_input(
        "O escriba su propia pregunta:",
        value="" if pregunta_predefinida == "Seleccione una pregunta..." else pregunta_predefinida,
        key="pregunta_personalizada"
    )

    # Botón de análisis con contador de tiempo
    if st.button("Analizar Datos", key="ejecutar_analisis"):
        pregunta_final = pregunta_personalizada if pregunta_personalizada else pregunta_predefinida

        if pregunta_final and pregunta_final != "Seleccione una pregunta...":
            with st.spinner("Analizando datos..."):
                try:
                    # Determinar qué agente usar basado en la categoría
                    agente_a_usar = None
                    if "Térmica y Nuclear" in categoria:
                        agente_a_usar = agentes_csv["generacion"]
                    elif "Global" in categoria:
                        agente_a_usar = agentes_csv["planta_energia"]
                    elif "Generación de Plantas" in categoria:
                        agente_a_usar = agentes_csv["generacion_planta"]
                    elif "Renovables" in categoria:
                        agente_a_usar = agentes_csv["renovable"]

                    if agente_a_usar:
                        # Agregar contexto a la pregunta
                        pregunta_con_contexto = f"""
                        Analiza los datos para responder: {pregunta_final}
                        Por favor, incluye:
                        1. Un resumen claro de los hallazgos
                        2. Cualquier dato numérico relevante
                        3. Tendencias o patrones importantes
                        4. Sugerencias basadas en el análisis
                        """

                        respuesta = agente_a_usar.invoke({"input": pregunta_con_contexto})

                        # Mostrar resultados
                        st.markdown("### Resultados del Análisis")
                        st.write(respuesta['output'])

                        # Mostrar tiempo de ejecución
                        st.info("Análisis completado con éxito")
                    else:
                        st.error("No se pudo determinar el agente apropiado para esta categoría.")
                except Exception as e:
                    st.error(f"Error durante el análisis: {str(e)}")
                    st.warning("Intente con una pregunta más específica o diferente.")
        else:
            st.error("Por favor, seleccione o escriba una pregunta válida.")


if __name__ == "__main__":
    main()