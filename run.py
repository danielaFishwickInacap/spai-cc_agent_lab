import streamlit as st

if message_history not in st.session_state:
    st.session_state.message_history = []

def mostrar_chat():
    for message in st.session_state.message_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
def main():
    st.title("asistente IA")
    st.write("<h2>bienvenido</h2>", unsafe_allow_html=True)
    st.markdown("### ¿en qué puedo ayudarte?")
    
    consulta = st.text_input("Escribe tu consulta aquí", value="", key="")

    if consulta:
        st.session_state.message_history.append(HumanMessage(content=consulta))


        respuesta = llamar_ivan_torres(consulta, message_history=st.session_state.message_history)
        data = respuesta["messages"][-1]
        content = data.content
        texto = content[0]["text"] if isinstance(content, list) else None
        st.session_state.message_history.append(AIMessage(content=[{"type": "text", "text": texto}]))

        st.write(texto)

        st.rerun()
if __name__ == "__main__":
    main()