from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalculatorApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        layout = GridLayout(cols=4, spacing=10, padding=10)
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        layout.add_widget(self.solution)
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            ".", "0", "C", "+"
        ]
        for button in buttons:
            layout.add_widget(Button(
                text=button, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                on_press=self.on_button_press
            ))

        equals_button = Button(
            text="=", pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_press=self.on_solution
        )
        layout.add_widget(equals_button)
        return layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = instance
        self.last_was_operator = button_text in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                self.solution.text = str(eval(self.solution.text))
            except Exception:
                self.solution.text = "Error"

if __name__ == "__main__":
    CalculatorApp().run()
