import tkinter as tk
from tkinter.ttk import Label
from main import runner


class debatableGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.linkVar = tk.StringVar()
        window_width = 750
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.minsize(window_width, window_height)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.title('Debatable')
        self.resizable(1, 1)

        # setup the grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.create_widgets()

    def openLinkInBrowser(url):
        webbrowser.open_new(url)
    
    def analyseSourceFunction(self):
        linkVar = self.linkVar.get()
        try:
            self.resultBox.delete(1.0, tk.END)  # Clear the box
            results = runner([linkVar])
            for _, query in enumerate(
                    results
            ):  # here, "query" refers to each article that was analysed, in case multiple were provided
                self.resultBox.insert(
                    tk.END,
                    "The recomendations for articles to read are (in order of dissimilarity):\n"
                )
            for index, result in enumerate(query[1]):
                # Print recommendations and their similarity score.
                reccomendation = str(index + 1) + ") " + str(
                    result[0]) + " (content similarity = " + str(
                        round(result[1], 2)) + ")"
                self.resultBox.insert(tk.END, reccomendation)
                self.resultBox.insert(tk.END, "\n---------------\n")
        except:
            self.resultBox.insert(tk.END,
                                  "Error: Invalid URL")  # Insert the output

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
                              width=60)
        boxForLink.grid(column=1, row=0, columnspan=2, sticky=tk.N, padx=5, pady=5)

        # Create an analyse button
        analyseBtn = tk.Button(self,
                               text='Analyse!',
                               bg='white',
                               command=lambda: self.analyseSourceFunction())

        analyseBtn.grid(column=3, row=0, sticky=tk.NE, padx=5, pady=5)
        analyseBtn.focus()

        outputLabel = Label(
            self,
            text=
            'The recomendations for articles to read are (in order of dissimilarity with the submitted article):',
            foreground='black',
            background='white')
        outputLabel.grid(column=0,
                         row=1,
                         columnspan=4,
                         sticky=tk.NSEW,
                         padx=5,
                         pady=5)

        # Create box for the output
        self.resultBox = tk.Text(self, foreground='black', background='white', wrap=tk.WORD)
        self.resultBox.grid(column=0,
                            row=2,
                            columnspan=4,
                            sticky=tk.NSEW,
                            padx=5,
                            pady=5)

        # Create an exit button
        exitButton = tk.Button(self,
                               text='Exit',
                               command=lambda: self.quit(),
                               foreground='black',
                               background='white')
        exitButton.grid(column=3, row=3, sticky=tk.SE, padx=5, pady=5)


if __name__ == "__main__":
    app = debatableGUI()
    app.mainloop()
