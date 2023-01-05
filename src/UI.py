import tkinter as tk
from tkinter.ttk import Label, Button, Entry

from main import GUICallback

class debatableGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.linkVar = tk.StringVar()
        window_width = 700
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.title('Debatable')
        self.resizable(0, 0)

        # setup the grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.create_widgets()

    def analyseSourceFunction(self):
        linkVar = self.linkVar.get()
        try:
            self.resultBox.delete(1.0, tk.END) # Clear the box
            results = GUICallback(linkVar)
            for _, query in enumerate(results):  # here, "query" refers to each article that was analysed, in case multiple were provided
                self.resultBox.insert(tk.END, "The recomendations for articles to read are (in order of dissimilarity):\n")
            for index, result in enumerate(query[1]):
                # Print recommendations and their similarity score.
                reccomendation = str(index + 1) + ") " + str(result[0]) + " (content similarity = " + str(round(result[1], 2)) + ")\n"
                # print(str(index + 1) + ") " + str(result[0]) + " (content similarity = " + str(round(result[1], 2)) + ")")
                self.resultBox.insert(tk.END, reccomendation)
        except:
            self.resultBox.insert(tk.END, "Error: Invalid URL") # Insert the output
    
    def create_widgets(self):
        # Create a label describing the input field
        inputLabel = Label(self,
                           text='Input URL:',
                           foreground='black',
                           background='white')
        inputLabel.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)

        # Create textbox
        boxForLink = tk.Entry(self,
                              textvariable=self.linkVar,
                              foreground='black',
                              background='white',
                              width=50)
        boxForLink.grid(column=1, row=0, sticky=tk.NW, padx=5, pady=5)

        # Create an analyse button
        analyseBtn = tk.Button(self,
                               text='Analyse!',
                               bg='white',
                               command=lambda: self.analyseSourceFunction())

        analyseBtn.grid(column=2, row=0, sticky=tk.NE, padx=5, pady=5)
        analyseBtn.focus()

        # Create box for the output
        self.resultBox = tk.Text(self, foreground='black', background='white')
        self.resultBox.grid(column=1, row=1, columnspan=3)
        
        
        # Create an exit button
        exitButton = tk.Button(self,
                               text='Exit',
                               command=lambda: self.quit(),
                               foreground='black',
                               background='white')
        exitButton.grid(column=2, row=2, sticky=tk.SE, padx=5, pady=5)


if __name__ == "__main__":
    app = debatableGUI()
    app.mainloop()
