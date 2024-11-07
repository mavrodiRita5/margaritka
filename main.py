import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class ProstoAnalizatorDannih:
    def __init__(self, okno):
        self.okno = okno
        self.okno.title("Простой Анализатор Данных CSV")
        self.okno.geometry("800x600")


        self.dannie = None
        self.originalnie_dannie = None


        self.sozdat_elementi()

    def sozdat_elementi(self):
        osnovnoi_freim = ttk.Frame(self.okno)
        osnovnoi_freim.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        knopki_freim = ttk.Frame(osnovnoi_freim)
        knopki_freim.pack(side=tk.RIGHT, fill=tk.Y, padx=10)


        knopka_zagruzit = ttk.Button(knopki_freim, text="Загрузить файл", command=self.zagruzit_fayl)
        knopka_zagruzit.pack(pady=10)


        self.knopka_srednee = ttk.Button(knopki_freim, text="Среднее", command=self.poschitat_srednee)
        self.knopka_minimum = ttk.Button(knopki_freim, text="Минимум", command=self.poschitat_minimum)
        self.knopka_maksimum = ttk.Button(knopki_freim, text="Максимум", command=self.poschitat_maksimum)
        self.knopka_filtr = ttk.Button(knopki_freim, text="Фильтрация", command=self.filtr_dannih)
        self.knopka_pokazat_vsyo = ttk.Button(knopki_freim, text="Показать все данные",
                                              command=self.pokazat_polniy_danniye)


        self.knopka_srednee.pack(fill=tk.X, pady=5)
        self.knopka_minimum.pack(fill=tk.X, pady=5)
        self.knopka_maksimum.pack(fill=tk.X, pady=5)
        self.knopka_filtr.pack(fill=tk.X, pady=5)
        self.knopka_pokazat_vsyo.pack(fill=tk.X, pady=5)

        self.nadpis_filtr = ttk.Label(osnovnoi_freim, text="Фильтр по значению:")
        self.nadpis_filtr.pack(pady=5)
        self.pole_filtr = ttk.Entry(osnovnoi_freim)
        self.pole_filtr.pack(pady=5, fill=tk.X)

        self.tablica = ttk.Treeview(osnovnoi_freim)
        self.tablica.pack(fill=tk.BOTH, expand=True)

    def zagruzit_fayl(self):
        put_k_faylu = filedialog.askopenfilename(filetypes=[("CSV файлы", "*.csv")])
        if put_k_faylu:
            try:
                self.dannie = pd.read_csv(put_k_faylu)
                self.originalnie_dannie = self.dannie.copy()
                self.pokazat_dannie()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def pokazat_dannie(self):
        self.tablica.delete(*self.tablica.get_children())


        self.tablica["columns"] = list(self.dannie.columns)
        self.tablica["show"] = "headings"
        for kolonka in self.dannie.columns:
            self.tablica.heading(kolonka, text=kolonka)
            self.tablica.column(kolonka, anchor=tk.CENTER)

        for _, stroka in self.dannie.iterrows():
            self.tablica.insert("", "end", values=list(stroka))

    def poschitat_srednee(self):
        kolonka = self.vibrat_kolonka()
        if kolonka:
            srednee = self.dannie[kolonka].mean()
            messagebox.showinfo("Среднее", f"Среднее значение для {kolonka}: {srednee:.2f}")

    def poschitat_minimum(self):
        kolonka = self.vibrat_kolonka()
        if kolonka:
            minimum = self.dannie[kolonka].min()
            messagebox.showinfo("Минимум", f"Минимальное значение для {kolonka}: {minimum}")

    def poschitat_maksimum(self):
        kolonka = self.vibrat_kolonka()
        if kolonka:
            maksimum = self.dannie[kolonka].max()
            messagebox.showinfo("Максимум", f"Максимальное значение для {kolonka}: {maksimum}")

    def filtr_dannih(self):
        znachenie_filtra = self.pole_filtr.get()
        if znachenie_filtra and self.dannie is not None:
            dannie_posle_filtra = self.dannie[
                self.dannie.apply(lambda stroka: znachenie_filtra in stroka.values.astype(str), axis=1)]
            self.dannie = dannie_posle_filtra
            self.pokazat_dannie()

    def pokazat_polniy_danniye(self):
        if self.originalnie_dannie is not None:
            self.dannie = self.originalnie_dannie.copy()
            self.pokazat_dannie()

    def vibrat_kolonka(self):
        if self.dannie is None:
            messagebox.showwarning("Внимание", "Сначала загрузите файл.")
            return None

        kolonka = tk.simpledialog.askstring("Выбор колонки", "Введите имя колонки:")
        if kolonka not in self.dannie.columns:
            messagebox.showerror("Ошибка", f"Колонка '{kolonka}' не найдена.")
            return None
        return kolonka


if __name__ == "__main__":
    okno = tk.Tk()
    app = ProstoAnalizatorDannih(okno)
    okno.mainloop()
