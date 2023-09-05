#carregando as bibliotecas necessárias
from PIL import Image #biblioteca de processamento de imagem
import joblib #biblitoeca responsável por congelar o modelo 
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml #a biblioteca scikit-learn tem bases de dados reconhecidas embutidas nela
#esses datasets são disponibilizados pela OpenML

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt



SIZE = 28

"""
  Cria um plot com os dígitos de um conjunto de imagens

  Se X é um conjunto de dados, chamar a função com is_array = True
  Dessa maneira, a função irá criar uma grid 10x10 e plotar as 100 primeiras imagens de X

  Se X é uma única imagem, chamar a função com is_array = False, 
  para plotar apenas uma imagem.
"""
def plot_digits(X, title, is_array=True):

    if is_array:
        #se X é um array, cria uma grid 10x10 e plota 100 entradas de X
        #função axuiliar para plotar 100 digitos
        fig, axs = plt.subplots(nrows=10, ncols=10, figsize=(8, 8)) 
        #cria um subplot 10x10 e preenche com 100 digitos
        for img, ax in zip(X, axs.ravel()):
            ax.imshow(img.reshape((SIZE, SIZE)), cmap="Greys")
            ax.axis("off")
        fig.suptitle(title, fontsize=24)
    else:
        #plota apenas um digito
        plt.imshow(X.reshape((SIZE, SIZE)), cmap='Greys')
        plt.axis('off')  # Turn off axis labels
        plt.title(title)
        plt.show()  


"""
  Converte um array numpy para binario, utilizando um limiar,
  por padrão, o limiar tem o valor 128.
  Como o valor máximo de um pixel é 255, 128 representa cerca de metade,
  tendo um cutoff de 50%.
"""
def to_binary(array, threshold=128):
   
    binary_vector = [1 if value >= threshold else 0 for value in array]
    return np.array(binary_vector)


"""
    Carrega a base de dados do MNIST e retorna os dados particionados e já préprocessados
    Também plota uma amostra de 100 dígitos da base de dados.
"""
def load_data():
    #carregando a base de dados abaixo: 
    #https://www.openml.org/search?type=data&status=active&id=554
    #essa é a base de dados MNIST
    #as imagens possuem 28x28 e estão em escala de cinza
    mnist_X, mnist_y = fetch_openml("mnist_784", as_frame=False, return_X_y=True, parser="pandas") #usando as_frame=False, consideramos os dados como vetores

    mnist_X = np.array([to_binary(x) for x in mnist_X])

    #usps_X.apply(lambda x: to_binary(x))

    #divisão dos dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        mnist_X, mnist_y, stratify=mnist_y, random_state=0, test_size=0.2)

    plot_digits(X_train, "Imagens de Treino", is_array=True)

    return X_train, X_test, y_train, y_test



"""
    Carrega o modelo gerado a partir de um caminho dado, o caminho passado como parâmetro deve conter o modelo .pkl
    Retorna o modelo.
"""
def load_model_from(model_path):
    
    model = joblib.load(model_path)
    return model

"""
    Salva o modelo com o nome dado. o nome deve conter a extensão .pkl
"""
def save_model_to(model, model_path):

    joblib.dump(model, model_path)




"""
    Cria uma rede neural e treina com os dados da MNIST
    Com a opção freeze_model=True, a função salva o modelo gerado para que não seja necessário retreiná-lo
    A variável model_path é o nome do arquivo em que o modelo será salvo
    O arquivo em que o modelo será salvo deve ter a extensão .pkl
"""
def generate_model(freeze_model=True, model_path="rede_digitos.pkl"):

    #
    X_train, X_test, y_train, y_test = load_data()

    model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=20, alpha=1e-4,
                        solver='adam', verbose=10, random_state=42, learning_rate_init=0.001)
    #
    #treinando a rede neural
    model.fit(X_train, y_train)
    #
    #predição no conjunto de testes
    y_pred = model.predict(X_test)
    #
    #calculando a acurácia do modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    #
    
    #gera um arquivo .pkl com o modelo pré-treinado salvo
    #isso permite que o modelo não tenha que ser treinado todas as vezes que a aplicação for executada
    if freeze_model:
        #antes de congelar o modelo, adiciona os dados de teste ao treinamento
        model.partial_fit(X_test, y_test)
        #salva o modelo
        save_model_to(model, model_path)

    return model



"""
    Preprocessa uma imagem para servir como entrada para o modelo
"""
def preprocess_image(image_path, plot_image=False, limiar=128):

    image = Image.open(image_path)

    #redimensiona a imagem para o tamanho correto e aplica anti-aliasing
    image = image.resize((SIZE, SIZE), Image.LANCZOS)
    
    #converte a imagem para escala de cinza
    image = image.convert('L')

    #gera um array 1-dimensional
    image_array = np.array(image).flatten()
    
    #converte a imagem para binário e inverte os dígitos, para que esteja no mesmo padrão das imagens do MNIST
    image_array = 1 - to_binary(image_array, threshold=limiar)

    #se plot_image = True, plota a imagem
    if plot_image:
        plot_digits(image_array, "Imagem Processada", is_array=False)

    image_array = image_array.reshape(1, -1) 

    return image_array



"""
    Executa um teste com dígitos escritos à mão de 0 a 9, como benchmark;
"""
def run_sample_test(model):

    acertos = 0
    for i in range(0,10):
        
        image_array = preprocess_image("imagens_teste/"+str(i)+".png", plot_image=True)

        res = model.predict(image_array)
        print(res[0])
        if res[0] == str(i):
            acertos += 1

    print(f"Accuracy: {acertos/10}")


"""
    Realiza uma predição para uma imagem (ainda não préprocessada), retornando a predição feita.
    Recebe um modelo já treinado, um caminho para uma imagem e uma variável que indica se quer visualizar a imagem em um gráfico
"""
def get_prediction(model, image_path, plt=False, limiar=128):
    
    image = preprocess_image(image_path, plot_image=plt, limiar=limiar)

    result = model.predict(image)
    return image, result[0]


"""
    Recebe um modelo já treinado e utiliza os dados para executar um partial_fit
    Isso atualizará o modelo com os dados.
    Essa função deve receber uma imagem pré-processada (saída do get_prediction) e uma string correspondente ao seu dígito correto
"""
def update_model(model, image, label):

    label = np.array([[label]]).ravel()
    model.partial_fit(image, label)
    return model



"""
    #Para executar a primeira vez, rode
    
        generate_model(freeze_model=True, model_path="rede_digitos.pkl")
    
    #uma vez feito isso, não será necessário fazê-lo novamente.
        
    #isso irá gerar uma rede neural treinada e irá criar um arquivo .pkl com o modelo já treinado
    #então, para gerar as próximas predições, carregue o modelo com
    
        modelo = load_model_from("rede_digitos.pkl")
    
    #isso irá carregar o modelo do arquivo salvo
    #para realizar uma predição de uma imagem salva, execute
    
        image, num =  get_prediction(modelo, caminho_daimagem, plt=True) #com plt igual a True se quiser visualizar a imagem préprocessada
    
    #isso irá retornar a imagem pré-processada e uma string com a classe predita para a imagem

    #se quiser atualizar a predição do modelo e ter aprendizado online, execute:

        update_model(modelo, image, rotulo) #sendo rotulo o número que está realmente contido na imagem, em formato de string 
    
    #para guardar o modelo atualizado, execute:

        save_model_to(modelo, "rede_digitos.pkl")

"""

