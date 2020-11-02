import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

class GenericData:
    def __init__(self):
        self._bdata = ""

    def raw(self):
        output = []
        for c in self._bdata:
            output.append(int(c))
        return output

    def nrz_unipolar(self):
        output = []
        for c in self._bdata:
            output.append(int(c))
        return output

    def b8zs(self):
        output = []
        m = 1
        s=self._bdata.replace("00000000","000vb0vb")
        for i in range(len(s)):
            if(s[i]=='0' or s[i]==0):
                output.append(0)
            elif(s[i]=='1'):
                if(m%2==1):
                    output.append(1)
                else:
                    output.append(-1)
                m=m+1
            elif(s[i]=='v'):
                if(m%2==1):
                    output.append(-1)
                else:
                    output.append(1)
            else:
                if(m%2==1):
                    output.append(1)
                else:
                    output.append(-1)
                m=m+1

        return output

    def empty(self):
        return(len(self._bdata) == 0)

        
class DataFile(GenericData):
    def __init__(self, filePath):
        super().__init__()
        self._fpath = filePath

    def load(self):
        f = open(self._fpath,'rb')  
        fdata = f.read()
        f.close()
        self._bdata = ''.join(format(byte, '08b') for byte in fdata)


class DataString(GenericData):
    def __init__(self, data : str):
        super().__init__()
        self._bdata = ''.join(format(ord(i), '08b') for i in data)


class PlotlyDataPlotter:
    def __init__(self):
        self.data = []

    # Adiciona dados para plotagem. Maximo implementaado: 3
    def add_data(self, data, label : str = ""):
        self.data.append((data,label))

    # Processa os dados para plotagem
    def plot(self, scale=1.0):
        r = len(self.data)
        assert r>0, "No data to plot."
        data = self.data
        data.reverse()

        self.fig = go.Figure()

        xmax = []
        for i in range(len(data)-1,-1,-1):
            x,y = PlotlyDataPlotter.dataPlot(data[i][0],scale)
            self.fig.add_trace(go.Scatter(x=x,y=y,yaxis=('y'+(str(i+1) if i!=0 else "")),name=(data[i][1] if data[i][1] != "" else ("Data" + str(i)))))
            if(len(x)>len(xmax)):
                xmax = x

        self.fig.update_traces(
                        hoverinfo="name+x+text",
                        marker={"size": 5},
                        mode="lines+markers",
                        showlegend=True
                    )

        if(len(xmax) > 50):
            initial_range = [0,xmax[50]]
        else:
            initial_range = [0,xmax[-1]]

        if(len(data) == 1):
            self.fig.update_layout(xaxis=dict(showgrid=True, range=initial_range, 
                                    rangeslider=dict(visible=True, thickness=0.10, range=[xmax[0],xmax[-1]])),
                                    yaxis=dict(zeroline=True,zerolinewidth=1, zerolinecolor='darkblue',anchor="x",range=[-0.1 + min(data[0][0]), max(data[0][0]) + 0.1], showline=True, mirror=True, domain=[0,1],tickmode="auto", ticks=""))
        if(len(data) == 2):
            self.fig.update_layout(xaxis=dict(showgrid=True, range=initial_range, 
                                    rangeslider=dict(visible=True, thickness=0.10, range=[xmax[0],xmax[-1]],autorange=False)),
                                    yaxis=dict(zeroline=True,zerolinewidth=1, zerolinecolor='darkblue',anchor="x",range=[-0.1 + min(data[0][0]), max(data[0][0]) + 0.1], showline=True, mirror=True, domain=[0,0.5],tickmode="auto", ticks=""),
                                    yaxis2=dict(zeroline=True,zerolinewidth=1, zerolinecolor='darkblue',anchor="x", range=[-0.1 + min(data[1][0]), max(data[1][0]) + 0.1], showline=True, mirror=True, domain=[0.5,1],tickmode="auto",ticks=""))

        if(len(data) == 3):
            self.fig.update_layout(xaxis=dict(showgrid=True, range=initial_range,
                                    rangeslider=dict(visible=True, thickness=0.10, range=[xmax[0],xmax[-1]],)),
                                    yaxis=dict(zeroline=True,zerolinewidth=1, zerolinecolor='darkblue',anchor="x",range=[-0.1 + min(data[0][0]), max(data[0][0]) + 0.1], showline=True, mirror=True, domain=[0,0.33],tickmode="auto", ticks=""),
                                    yaxis2=dict(zeroline=True,zerolinewidth=1, zerolinecolor='darkblue',anchor="x", range=[-0.1 + min(data[1][0]), max(data[1][0]) + 0.1], showline=True, mirror=True, domain=[0.33,0.66],tickmode="auto",ticks=""),
                                    yaxis3=dict(zeroline=True,zerolinewidth=1, zerolinecolor='darkblue',anchor="x", range=[-0.1 + min(data[2][0]), max(data[2][0]) + 0.1], showline=True, mirror=True, domain=[0.66,0.99],tickmode="auto",ticks=""))

        self.fig.update_layout(dragmode="pan", legend=dict(orientation="h",xanchor="right",x=1,y=1.02,yanchor="bottom"))

    # Gera um host local com a página do código e abre no browser padrao
    def show(self):
        self.fig.show()

    # Escreve um arquivo HTML
    def write_html(self, file="output.html"):
        self.fig.write_html(file)

    # Retorna uma string com o código HTML
    def to_html(self):
        return self.fig.to_html(full_html=True)

    # Retorna True se a lista de dados estiver vazia
    def empty(self):
        return(len(self.data) == 0)


    # Funcao auxiliar, gera o eixo x
    def dataPlot(data, xscale=1.0):
        i = 0.0
        y = []
        x = []

        for d in data:
            x.append(i*xscale)
            x.append((i+0.99999)*xscale)
            y.append(d)
            y.append(d)
            i = i+1
        return x,y


if __name__ == "__main__":
    d = GenericData()
    d._bdata = "110000000011100000000001111"
    plt = PlotlyDataPlotter()
    plt.add_data(d.raw(),"Raw")
    plt.add_data(d.nrz_unipolar(),"NRZ")
    plt.add_data(d.b8zs(),"B8ZS")
    plt.plot()
    plt.show()
