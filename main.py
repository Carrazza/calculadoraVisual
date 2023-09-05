import os
import time
import getDigit
import getSimbolo
import tkinter as tk
from PIL import Image, ImageDraw
from tkinter import filedialog, messagebox, simpledialog

SIZE = 28*5
# Create a tkinter window

def load_model():
    loading_window = tk.Tk()
    loading_window.title("Carregando...")
    loading_window.attributes('-topmost', True)
    
    loading_window.geometry("500x200") 
    
    loading_text = tk.Text(loading_window, height=10, width=50, font=("Helvetica", 12), bg=loading_window.cget("bg"), borderwidth=0, highlightthickness=0, relief="flat")
    loading_text.pack(pady=20)



    loading_text.insert(tk.END, "Carregando o agente...\n")
    loading_window.update()
    time.sleep(1)


    #checar se pkl existe
        #se nao exite, chamar generate model
    if( not os.path.isfile("rede_digitos.pkl")):
        loading_text.insert(tk.END, "Modelo não encontrado, treinando um novo agente...\n")
        loading_window.update()
        
        loading_text.insert(tk.END, "Aguarde um momento...\n")
        loading_window.update()

        modelo = getDigit.generate_model(False)

    else:
        loading_text.insert(tk.END, "Modelo encontrado! Carregando...\n")
        loading_window.update()
        time.sleep(1)

        modelo = getDigit.load_model_from("rede_digitos.pkl")

    loading_text.insert(tk.END, "Carregando pontuação\n")

   


    loading_text.insert(tk.END, "Iniciando aplicação...\n")
    loading_window.update()
    time.sleep(1)


    
    loading_window.destroy()
    return modelo

def retrain_model(image_d1, label_d1, image_d2, label_d2):
    loading_window = tk.Tk()
    loading_window.title("Ensinando o Agente...")
    #loading_window.attributes('-topmost', True)

    loading_window.geometry("500x200") 
    
    loading_text = tk.Text(loading_window, height=10, width=50, font=("Helvetica", 12), bg=loading_window.cget("bg"), borderwidth=0, highlightthickness=0, relief="flat")
    loading_text.pack(pady=20)


    loading_text.insert(tk.END, "Retreinando o agente...\n")
    loading_window.update()
    time.sleep(1)

    getDigit.update_model(modelo,image_d1, label_d1)
    getDigit.update_model(modelo,image_d2, label_d2)

    getDigit.save_model_to(modelo,"rede_digitos.pkl")


    loading_text.insert(tk.END, "Agente treinado com sucesso!\n")
    loading_window.update()
    time.sleep(2)

    loading_window.destroy()

    return

def clear_all():
    canvas1.delete("all")
    canvas2.delete("all")
    canvas3.delete("all")


def on_dialog_result(dialog, result_var, result):
    result_var.set(result)
    dialog.destroy()

def confirm_result(d1, op, d2):
        result = tk.BooleanVar()
        message = f"A expressão predita foi:\n {d1} {op} {d2} = {eval(f'{d1} {op} {d2}')} \n" 
        
        #result = messagebox.askquestion("Confirmar Resultado", message)
        
        dialog = tk.Tk()
        #dialog.attributes("-topmost", True)

        dialog.title("Confirmar Resultado")
        dialog.geometry("300x150")  # Set the initial size of the dialog

        label = tk.Label(dialog, text=message)
        label.pack(pady=10)

        question_label = tk.Label(dialog, text="A expressão acima está correta?")
        question_label.pack()

        yes_button = tk.Button(dialog, text="Sim", command=lambda: on_dialog_result(dialog, result, True))
        yes_button.pack(pady=10, padx=20, side="left")

        no_button = tk.Button(dialog, text="Não", command=lambda: on_dialog_result(dialog, result, False))
        no_button.pack(pady=10, padx=20, side="right")
    
        dialog.wait_window(dialog)
        return result.get()

def confirm_op(op):
        result = tk.BooleanVar()

        opStr = "Soma" if op == "+" else "Subtração"

        message = f"O operador predito foi:\n{opStr}\n" 
        
        #result = messagebox.askquestion("Confirmar Resultado", message)
        
        dialog = tk.Tk()
        #dialog.attributes("-topmost", True)
        
        dialog.title("Confirmar Operador")
        dialog.geometry("300x150")  # Set the initial size of the dialog

        label = tk.Label(dialog, text=message)
        label.pack(pady=10)

        question_label = tk.Label(dialog, text="O operador acima está correto?")
        question_label.pack()

        yes_button = tk.Button(dialog, text="Sim", command=lambda: on_dialog_result(dialog, result, True))
        yes_button.pack(pady=10, padx=20, side="left")

        no_button = tk.Button(dialog, text="Não", command=lambda: on_dialog_result(dialog, result, False))
        no_button.pack(pady=10, padx=20, side="right")
    
        dialog.wait_window(dialog)
        return result.get()

def check_digit(input_string):
    # Check if the input string is not empty and consists of a single digit
    if input_string and input_string.isdigit() and 0 <= int(input_string) <= 9:
        return True
    else:
        return False
    
    
def get_digits():
    input1 = simpledialog.askinteger("Treinando o Agente...", "Por favor, digite o primeiro dígito:")
    input2 = simpledialog.askinteger("Treinando o Agente...", "Por favor, digite o segundo dígito:")

    return str(input1), str(input2)
#Função para poder selecionar o canvas e começar a desenhar
def start_drawing(event):
    global drawing, last_x, last_y
    drawing = True
    last_x, last_y = event.x, event.y

#Função para desenhar na tela
def draw(event):
    global drawing, last_x, last_y
    if drawing:
        canvas = event.widget
        x, y = event.x, event.y
        line_width = 3  # Set the desired line width
        canvas.create_line(last_x, last_y, x, y, fill="black", width=line_width)
        last_x, last_y = x, y




#Função para parar de desenhar
def stop_drawing(event):
    global drawing
    drawing = False


def save_canvas():
    try:
        # Create an image and a drawing context for each canvas
        canvases = [(canvas1, "digito_1"), (canvas2, "operador"), (canvas3, "digito_2")]
        for canvas, filename in canvases:
            img = Image.new("RGB", (SIZE, SIZE), color="white")  # Create a white image
            draw = ImageDraw.Draw(img)  # Create a drawing context
            
            # Iterate over the canvas items and draw them on the image
            for item in canvas.find_all():
                coords = canvas.coords(item)
                color = canvas.itemcget(item, "fill")

                #try:
                #    width = int(canvas.itemcget(item, "width"))
                #except ValueError:
                #    # Handle the case where width is not a valid integer (provide a default width)
                #    width = 2  # You can change this to any desired default width
                draw.line(coords, fill=color, width=5)
            
            img.save(filename + ".png", format="PNG")  # Save the image as PNG
                    
    except Exception as e:
        messagebox.showerror("Erro!", f"An error occurred: {str(e)}")


def calculate_prediction():
    #primeiro salva todos os desenhos
    save_canvas()
   
    #chama a função para verificar a operação
    operador = getSimbolo.get('operador.png')  

    #carrega as predições dos dígitos
    image_d1, digito1 =  getDigit.get_prediction(modelo, "digito_1.png", plt=False, limiar=200)
    image_d2, digito2 =  getDigit.get_prediction(modelo, "digito_2.png", plt=False, limiar=200)


    #Carrega pontuação
    pontuacao_total = 0

    with open('pontuacao', 'r') as file:
        # Read the desired line (e.g., line 1)
        line = file.readline()

    # Convert the line to an integer
    
    try:
        pontuacao_total = int(line)
        # Now, 'number' contains the integer value from the file
        print(f"Pontuação Total: {pontuacao_total}")

    except ValueError:
        print("The line in the file is not a valid integer.")


    pontos_da_iteracao = 0
    #saída da predição
    if confirm_result(digito1, operador, digito2) == False:

        if(confirm_op(operador) == False): pontos_da_iteracao -= 15
        else: pontos_da_iteracao+=2
        
        dig_1, dig_2 = get_digits()

        if(dig_1 == digito1): pontos_da_iteracao += 10
        else: pontos_da_iteracao -= 2
        
        if(dig_2 == digito2): pontos_da_iteracao += 10
        else: pontos_da_iteracao -= 2

        
        if(not check_digit(dig_1) or not check_digit(dig_2)):
            messagebox.showerror("Erro", "Entrada inválida. Treinamento Abortado!")
        #dig_1 = input("Digite o primeiro número: ").strip()
        #dig_2 = input("Digite o segundo número: ").strip()
        else:
            retrain_model(image_d1, dig_1, image_d2, dig_2)
    
    else:
        pontos_da_iteracao += 22

    pontuacao_total = pontuacao_total + pontos_da_iteracao

    print(f"Pontos da iteração: {pontos_da_iteracao}\nNova Pontuação Total: {pontuacao_total}")

        
    # Convert the integer to a string
    number_str = str(pontuacao_total)

    # Open the file in write mode
    with open('pontuacao', 'w') as file:
        # Write the integer as a string to the file
        file.write(number_str)



    #termina limpando a tela para a próxima iteração
    clear_all()


if __name__ == "__main__":


    #carrega o modelo e a tela de inicio
    modelo = load_model()
    
    #Carrega a aplicação principal
    root = tk.Tk()
    root.title("Calculadora Visual")
    #root.attributes('-topmost', True)

    #Subtitulos
    label1 = tk.Label(root, text="Primeiro Dígito")
    label2 = tk.Label(root, text="Operação")
    label3 = tk.Label(root, text="Segundo Dígito")

    #Criando três superfícies desenháveis
    canvas1 = tk.Canvas(root, bg="white", width=SIZE, height=SIZE)
    canvas2 = tk.Canvas(root, bg="white", width=SIZE, height=SIZE)
    canvas3 = tk.Canvas(root, bg="white", width=SIZE, height=SIZE)

    #Geometria da tela para organizar elementos
    label1.grid(row=0, column=0)
    canvas1.grid(row=1, column=0)

    label2.grid(row=0, column=1)
    canvas2.grid(row=1, column=1)

    label3.grid(row=0, column=2)
    canvas3.grid(row=1, column=2)

    #Variáveis para acompanhar estado do desenho
    drawing = False
    last_x, last_y = None, None


    #Agrupa eventos do mouse às telas de desenho
    canvas1.bind("<Button-1>", start_drawing)
    canvas1.bind("<B1-Motion>", draw)
    canvas1.bind("<ButtonRelease-1>", stop_drawing)

    canvas2.bind("<Button-1>", start_drawing)
    canvas2.bind("<B1-Motion>", draw)
    canvas2.bind("<ButtonRelease-1>", stop_drawing)

    canvas3.bind("<Button-1>", start_drawing)
    canvas3.bind("<B1-Motion>", draw)
    canvas3.bind("<ButtonRelease-1>", stop_drawing)


    # Buttons to save all canvases and get user input
    calculate_result = tk.Button(root, text="Calcular", command=calculate_prediction)
    limpar = tk.Button(root, text="Limpar Tela", command=clear_all)

    # Use grid to place buttons
    calculate_result.grid(row=2, column=0, padx=(10, 5), pady=10)  # Adjust padx for spacing
    limpar.grid(row=2, column=1, padx=(5, 10), pady=10)  # Adjust padx for spacing
    
    # Run the tkinter main loop
    root.mainloop()