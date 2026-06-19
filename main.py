from matplotlib.pylab import f
import os
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt 

load_dotenv()

app = Flask(__name__)

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

class Tabela:
    def __init__(self, nome):
        self.nome = nome

    def listarconteudo(self):
          response = (
              supabase.table(self.nome)
              .select("*")
              .execute()
          )

          return response

    def criarDataframe(self):
        return pd.DataFrame(self.listarconteudo().data)

    def mediaSegmneto(self, segmento):
        df = self.criarDataframe()
        return df[df["segmento"] == segmento]["total_venda"].mean()

@app.route('/')
def index():
   vendasInformatica = Tabela("vendas_informatica") 
   df = vendasInformatica.criarDataframe()

   media_educacao = vendasInformatica.mediaSegmneto("educacao")
   media_corporativo = vendasInformatica.mediaSegmneto("corporativo")
   media_gamer = vendasInformatica.mediaSegmneto("gamer")
    
   segmentos = ["educacao", "corporativo", "gamer"]
   medidas = [media_educacao, media_corporativo, media_gamer]
   plt.figure(figsize=(8,5))
   plt.bar(segmentos, medidas, color="red")
   plt.title("Média de Vendas por segmento")
   plt.xlabel("Segmento")
   plt.ylabel("Média")
   plt.savefig("static/medias_segmento.png")
   plt.close()
    
   return (
       df.to_html(index=False, border=1)
       + f"<h3>Média de segmento Educação R$ {media_educacao:.2f}</h3>"
       + f"<h3>Média de segmento Corporativo R$ {media_corporativo:.2f}</h3>"
       + f"<h3>Média de segmento Gamer R$ {media_gamer:.2f}</h3>"
       + f"<img src='static/medias_segmento.png'></img>"
   )
if __name__ == '__main__':
    app.run(debug=True)