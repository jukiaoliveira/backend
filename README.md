# 🎬 Desafio WATTIO - CRUD de Filmes

Este projeto foi desenvolvido como parte do desafio técnico da WATTIO. O sistema consiste em um CRUD completo de filmes, com upload de imagem e consumo via frontend em React.

## 💡 Sobre o projeto

A aplicação foi dividida em dois repositórios:

- 🔧 **Backend (FastAPI)** – este repositório
- 🎨 **Frontend (React)** – [Repositório do front-end](https://github.com/jukiaoliveira/filmes-react)

O frontend exibe os filmes em cards com estilo de DVD, usando a paleta preta e amarela. Todos os filmes são cadastrados com imagem, título, diretor e ano.

---

## ⚙️ Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [React](https://react.dev/)
- [Axios](https://axios-http.com/)
- [React Toastify](https://fkhadra.github.io/react-toastify/)
- HTML + CSS (estilização personalizada no front)

---

## 📁 Como rodar o projeto

### 🔹 Backend (FastAPI)

> Requisitos: Python 3.11+, pip

1. Clone o repositório:
```bash
git clone https://github.com/WATTIO/NOME-DO-REPO-BACKEND
cd NOME-DO-REPO-BACKEND
```
2. Crie um ambiente virtual e ative:
```bassh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Rode o servidor:
```bash
uvicorn main:app --reload
```
O backend estará disponível em: http://127.0.0.1:8000

### 🔸 Frontend (React)

Requisitos: Node.js + npm

1. Clone o repositório
```bash
git clone https://github.com/jukiaoliveira/filmes-react
cd filmes-react
```
2. Instale as dependências:
```bash
npm install
```
3. Inicie o projeto:
```bash
npm start
```
O frontend estará em: http://localhost:3000

Obs: Certifique-se de que o backend está rodando em http://127.0.0.1:8000 

## 🎁 Diferenciais
Frontend com estilo moderno (paleta preta e amarela)

Toasts de feedback ao usuário

Upload real de imagens com pré-visualização

Layout personalizado imitando capas de DVD

Uso completo de React Hooks

💡 Obs: Não utilizei Docker (que era um diferencial), mas foquei em entregar uma interface rica e fluida com React como diferencial visual.

🙋‍♀️ Desenvolvedora
Júlia Oliveira
Tecnóloga em Análise e Desenvolvimento de Sistemas
[LinkedIn](https://www.linkedin.com/in/jurafaoliveira/) | [Portfólio](https://juliaoliveira.netlify.app/)
