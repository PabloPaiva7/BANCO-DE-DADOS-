import streamlit as st
from supabase import create_client, Client
import os

# Configuração do Supabase
SUPABASE_URL = "https://srusmktjnakijurgyydm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNydXNta3RqbmFraWp1cmd5eWRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM0Mzg2NjQsImV4cCI6MjA1OTAxNDY2NH0.dpF9IU1p3vMeilfcGBf7wVuAKl8QcjXTol_7oJai6r8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Controle de Estoque")

# Função para carregar os produtos
def carregar_produtos(filtro=None):
    query = supabase.table("produtos").select("*")
    if filtro:
        query = query.ilike("nome", f"%{filtro}%")
    response = query.execute()
    return response.data if response.data else []

# Função para adicionar produto
def adicionar_produto(nome, quantidade, preco):
    supabase.table("produtos").insert({"nome": nome, "quantidade": quantidade, "preco": preco}).execute()
    st.success("Produto adicionado com sucesso!")

# Função para atualizar produto
def atualizar_produto(id, quantidade, preco):
    supabase.table("produtos").update({"quantidade": quantidade, "preco": preco}).eq("id", id).execute()
    st.success("Produto atualizado com sucesso!")

# Função para excluir produto
def excluir_produto(id):
    supabase.table("produtos").delete().eq("id", id).execute()
    st.success("Produto excluído com sucesso!")

# Interface
st.sidebar.title("Menu")
aba = st.sidebar.radio("Escolha uma opção", ["Listar Estoque", "Adicionar Produto", "Atualizar Produto", "Excluir Produto"])

if aba == "Listar Estoque":
    filtro_nome = st.text_input("Pesquisar Produto")
    produtos = carregar_produtos(filtro_nome)
    if produtos:
        st.table(produtos)
    else:
        st.write("Nenhum produto encontrado.")

elif aba == "Adicionar Produto":
    nome = st.text_input("Nome do Produto")
    quantidade = st.number_input("Quantidade", min_value=0, step=1)
    preco = st.number_input("Preço", min_value=0.0, format="%.2f")
    if st.button("Adicionar"):
        adicionar_produto(nome, quantidade, preco)

elif aba == "Atualizar Produto":
    produtos = carregar_produtos()
    ids = [produto["id"] for produto in produtos]
    id_selecionado = st.selectbox("Selecione o ID do Produto", ids)
    quantidade = st.number_input("Nova Quantidade", min_value=0, step=1)
    preco = st.number_input("Novo Preço", min_value=0.0, format="%.2f")
    if st.button("Atualizar"):
        atualizar_produto(id_selecionado, quantidade, preco)

elif aba == "Excluir Produto":
    produtos = carregar_produtos()
    ids = [produto["id"] for produto in produtos]
    id_selecionado = st.selectbox("Selecione o ID do Produto para Excluir", ids)
    if st.button("Excluir"):
        excluir_produto(id_selecionado)
