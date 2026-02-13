from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from sympy import sympify, diff, integrate, symbols, factorial, sin, cos, tan, pi, N, simplify

Window.clearcolor = (1, 1, 1, 1)

class RoundButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (0, 0, 0, 1)
        self.bold = True
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if hasattr(self, 'custom_bg'):
                Color(*self.custom_bg)
            else:
                Color(0.97, 0.97, 0.97, 1) 
            size = min(self.width, self.height) * 0.98
            Ellipse(pos=(self.center_x - size/2, self.center_y - size/2), size=(size, size))

class SamsungProductionCalc(App):
    def build(self):
        self.title = "Math Pro Max"
        self.main_layout = BoxLayout(orientation='vertical', padding=[10, 15, 10, 15], spacing=4)
        
        self.result = TextInput(
            font_size=70, readonly=True, halign="right", multiline=False,
            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1),
            size_hint=(1, 0.2), padding=[10, 25], border=(0,0,0,0)
        )
        self.main_layout.add_widget(self.result)
        
        self.buttons_container = BoxLayout(size_hint=(1, 0.8))
        self.load_basic_ui()
        self.main_layout.add_widget(self.buttons_container)
        return self.main_layout

    def load_basic_ui(self, *args):
        self.buttons_container.clear_widgets()
        grid = GridLayout(cols=4, spacing=2)
        btns = ["C", "( )", "%", "÷", "7", "8", "9", "×", "4", "5", "6", "-", "1", "2", "3", "+", "ADV", "0", ".", "="]
        for txt in btns:
            f_size = 45 if txt in "0123456789+-×÷=" else 25
            btn = RoundButton(text=txt, font_size=f_size)
            if txt in ["÷", "×", "-", "+"]: btn.color = (0.2, 0.8, 0.2, 1)
            elif txt == "=": 
                btn.custom_bg = (0.2, 0.8, 0.2, 1); btn.color = (1, 1, 1, 1)
            elif txt == "ADV": btn.color = (0.2, 0.7, 0.9, 1)
            btn.bind(on_press=self.on_input)
            grid.add_widget(btn)
        self.buttons_container.add_widget(grid)

    def load_advanced_ui(self, *args):
        self.buttons_container.clear_widgets()
        grid = GridLayout(cols=4, spacing=2)
        adv_btns = ["sin", "cos", "tan", "log", "d/dx", "∫", "x", "^", "√", "π", "e", "!", "BACK", "rad", "deg", "="]
        for txt in adv_btns:
            btn = RoundButton(text=txt, font_size=28)
            if txt == "BACK": btn.bind(on_press=self.load_basic_ui)
            else: btn.bind(on_press=self.on_input)
            grid.add_widget(btn)
        self.buttons_container.add_widget(grid)

    def on_input(self, instance):
        val = instance.text
        if val == "C": self.result.text = ""
        elif val == "ADV": self.load_advanced_ui()
        elif val == "=": self.calculate()
        else: self.result.text += val

    def calculate(self):
        try:
            # Pre-processing for Sympy
            expr_str = self.result.text.replace("×", "*").replace("÷", "/").replace("^", "**").replace("π", "pi")
            x = symbols('x')

            # --- Logic Fix for Differentiation and Integration ---
            if "diff" in expr_str or "∫" in expr_str or "d/dx" in expr_str:
                # Remove function wrappers if any to get raw expression
                raw_expr = expr_str.replace("d/dx", "").replace("∫", "").replace("(", "").replace(")", "").strip()
                parsed_expr = sympify(raw_expr)
                
                if "d/dx" in expr_str:
                    res = diff(parsed_expr, x)
                else:
                    res = integrate(parsed_expr, x)
            
            # --- Trigonometry Fix ---
            elif any(f in expr_str for f in ["sin", "cos", "tan"]):
                for f in ["sin", "cos", "tan"]:
                    if f in expr_str:
                        angle = sympify(expr_str.replace(f, ""))
                        res = simplify(sympify(f"{f}({angle} * pi / 180)"))
                        if res.is_number: res = N(res, 4)

            # --- Percentage & Normal Math ---
            elif "-" in expr_str and "%" in expr_str:
                base, perc = expr_str.split("-")
                res = float(base) - (float(base) * float(perc.replace("%", "")) / 100)
            elif "!" in expr_str:
                res = factorial(int(expr_str.replace("!", "")))
            else:
                res = simplify(sympify(expr_str.replace("%", "/100")))

            self.result.text = str(res)
        except Exception as e:
            self.result.text = "Error"

if __name__ == "__main__":
    SamsungProductionCalc().run()
