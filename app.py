import streamlit as st
import random
import requests

# Configuración página de streamlit
st.set_page_config(
    page_title= "Pokemon Explorer",
    page_icon="🔥",
    layout="centered"
)

# Función para obtener datos de un Pokemon
def get_pokemon_data(pokemon_name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Función para obtener un Pokemon aleatorio
def get_random_pokemon():
    random_id = random.randint(1, 1010)
    return get_pokemon_data(str(random_id))

# Título y descripción de la app
st.title("🔥 Explorador de Pokemon")
st.markdown("Descubre información sobre tus Pokemon favoritos o encuentra nuevos Pokemon al azar!")

# Crear dos columnas para la búsqueda y el botób aleatorio
col1, col2 = st.columns([2, 1])

#Columna de búsqueda
with col1:
    pokemon_name = st.text_input("Ingresa el nombre de un Pokemon:", "")

#Columna de botón aleatorio
with col2:
    random_button = st.button("¡Pokemon Aleatorio! 🎲")

pokemon_data = None

# Manejar la búsqueda o el botón aleatorio
if pokemon_name:
    pokemon_data = get_pokemon_data(pokemon_name)
elif random_button:
    pokemon_data = get_random_pokemon()

# Mostrar información del Pokemon
if pokemon_data:
    # Crear dos columnas para la imagen y para la información
    img_col, info_col = st.columns([3, 2])

    with img_col:
        # Mostrar imaten del Pokemon
        st.image(
            pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
            caption=f"#{pokemon_data['id']} {pokemon_data['name'].title()}",
            use_container_width=True
        )
    
    with info_col:
        # Información básica
        st.subheader("Información Básica")
        st.write(f"**Altura** {pokemon_data['height']/10} m")
        st.write(f"**Peso:** {pokemon_data['weight']/10} kg")

        # Tipos
        st.subheader("Tipos")
        tipos = [tipo["type"]["name"] for tipo in pokemon_data["types"]]
        for tipo in tipos:
            st.write(f" ♦ {tipo.title()}")
    
    # Estadístísticas
    st.subheader("Estadísticas")
    stats_cols = st.columns(3)
    stats = pokemon_data["stats"]

    for idx, stat in enumerate(stats):
        col_idx = idx % 3
        with stats_cols[col_idx]:
            st.metric(
                label=stat["stat"]["name"].replace("-", " ").title(),
                value=stat["base_stat"]
            )

    # Habilidades
    st.subheader("Habilidades")
    abilities = [ability["ability"]["name"].replace("-", " ").title()
                for ability in pokemon_data["abilities"]]

    for ability in abilities:
        st.write(f"⭐ {ability}")

elif pokemon_name:
    st.error("¡Pokemon no encontrado! Verifica el nombre e intenta nuevamente")
else:
    st.info(" Ingresa 👆 el nombre de un Pokemon o prueba con uno aleatorio")





