from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from PIL import Image as PILImage, ImageSequence
from kivy.graphics.texture import Texture
from kivy.clock import Clock  # Tambahkan impor Clock di sini
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle  # Pastikan impor sudah benar
import random

LabelBase.register(name='Roboto', fn_regular='Roboto-Regular.ttf', fn_bold='Roboto-Bold.ttf')
LabelBase.register(name='3Dumb', fn_regular='3Dumb.ttf')

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        layout = RelativeLayout()

        # Set background to mathbg.jpg
        bg = Image(source='mathbg.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)

        # Place rslt.png in the center of the screen
        result_box = Image(source='rslt.png', size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(result_box)

        # Label to display the result, placed in the center of rslt.png
        self.result_label = Label(
            text="", 
            font_size='24sp', 
            bold=True, 
            color=(0, 0, 0, 1),  # Text color
            halign='center', 
            valign='middle',
            size_hint=(0.6, 0.4), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Centered inside rslt.png
        )
        layout.add_widget(self.result_label)

        # Try Again button (tr.png) below the rslt.png
        try_again_button = Button(
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0.3},
            background_normal='tr.png',  # Use tr.png for the button
            background_down='tr.png'
        )
        try_again_button.bind(on_press=self.try_again)
        layout.add_widget(try_again_button)

        # Add the giphy.gif in the center below the Try Again button, 2x size
        gif_image = AnimatedGif('giphy.gif', size_hint=(0.4, 0.4), pos_hint={'center_x': 0.5, 'y': 0.1})
        layout.add_widget(gif_image)

        self.add_widget(layout)

    def update_result(self, correct, total):
        """Update the result label with the correct answers and score."""
        if total > 0:
            score = (correct / total) * 100
            self.result_label.text = f"{correct} BENAR\n{total - correct} SALAH\n{int(score)}% SCORE"
        else:
            self.result_label.text = "No questions answered yet."

    def try_again(self, *args):
        """Reset score, clear result label, and go back to the main menu."""
        # Clear the result label
        self.result_label.text = ""

        # Reset scores in all screens that track results
        app = App.get_running_app()
        app.root.get_screen('third').reset_score()
        app.root.get_screen('fourth').reset_score()
        app.root.get_screen('fifth').reset_score()

        # Navigate back to the main menu
        app.root.current = 'main'



# Kelas untuk halaman utama
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = RelativeLayout()

        # Set ukuran window untuk ukuran Android
        Window.size = (500, 700)

        # Gambar background
        bg = Image(source='newbg.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)

        # Gambar papan tulis (kotak besar tengah)
        inner_layout = RelativeLayout(size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.3})

        # Menampilkan GIF animasi menggunakan PIL dan Kivy
        self.gif_image = AnimatedGif('play.gif', size_hint=(0.70, 0.75), pos_hint={'x': 0.15, 'y': 0.15})
        self.gif_image.bind(on_touch_down=self.go_to_second_screen)  # Menghubungkan ke fungsi untuk berpindah halaman
        inner_layout.add_widget(self.gif_image)

        # Menambahkan inner_layout ke layout utama
        layout.add_widget(inner_layout)

        # Gambar LET'S PLAY (tulisan di atas kanan)
        lets_image = Image(source='lets.png', size_hint=(0.25, 0.1), pos_hint={'x': 0.38, 'y': 0.60})
        layout.add_widget(lets_image)

        # Gambar Math (di atas kiri)
        math_image = Image(source='mathword.png', size_hint=(0.8, 0.4), pos_hint={'x': 0.10, 'y': 0.70})
        layout.add_widget(math_image)

        # Gambar Kids (di atas kanan Math)
        kids_image = Image(source='kidsword.png', size_hint=(0.8, 0.4), pos_hint={'x': 0.10, 'y': 0.65})
        layout.add_widget(kids_image)

        # Gambar Kids (di atas kanan Math)
        kids_image = Image(source='anakk.png', size_hint=(0.5, 0.4), pos_hint={'x': 0.25, 'y': 0.01})
        layout.add_widget(kids_image)

        self.add_widget(layout)

    def go_to_second_screen(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):  # Memeriksa apakah GIF ditekan
            app = App.get_running_app()
            app.root.current = 'second'  # Mengubah layar saat ini menjadi layar kedua

# Halaman 2
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.layout = RelativeLayout()

        # Gambar background untuk halaman kedua
        bg = Image(source='scnd.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(bg)

        # Gambar-gambar tombol
        label_plus = Image(source='plus.png', size_hint=(0.40, 0.30), pos_hint={'x': 0.50, 'y': 0.55})
        self.layout.add_widget(label_plus)

        label_minus = Image(source='minus.png', size_hint=(0.40, 0.30), pos_hint={'x': 0.10, 'y': 0.55})
        self.layout.add_widget(label_minus)

        label_compare = Image(source='compare.png', size_hint=(0.40, 0.30), pos_hint={'x': 0.35, 'y': 0.28})
        self.layout.add_widget(label_compare)

        # Tombol untuk minus, plus, dan compare dengan GIF
        ms_image = Image(source='ps.png', size_hint=(0.15, 0.25), pos_hint={'x': 0.31, 'y': 0.60})
        ms_image.bind(on_touch_down=self.show_minus_gif)
        self.layout.add_widget(ms_image)

        ps_image = Image(source='ms.png', size_hint=(0.1, 0.20), pos_hint={'x': 0.60, 'y': 0.60})
        ps_image.bind(on_touch_down=self.show_plus_gif)
        self.layout.add_widget(ps_image)

        cs_image = Image(source='cs.png', size_hint=(0.19, 0.20), pos_hint={'x': 0.36, 'y': 0.33})
        cs_image.bind(on_touch_down=self.show_compare_gif)
        self.layout.add_widget(cs_image)

        self.gif_widget = None  # Untuk menyimpan referensi GIF
        self.add_widget(self.layout)

        # Button for quitting to main menu
        quit_button = Button(
            size_hint=(0.25, 0.25),  # Size of the button
            pos_hint={'center_x': 0.5, 'y': 0.12},  # Position it below cs_image
            background_normal='back2.png',  # Use quit.png as button image
            background_down='back2.png'
        )
        quit_button.bind(on_press=self.go_to_main_menu)  # Bind to go_to_main_menu function
        self.layout.add_widget(quit_button)

    def random_position(self):
        """Fungsi untuk mendapatkan posisi acak di area lingkaran merah yang Anda tentukan."""
        x = random.uniform(0.2, 0.6)  # Set sesuai area lingkaran (horizontal)
        y = random.uniform(0.0, 0.3)  # Set sesuai area lingkaran (vertical)
        return {'x': x, 'y': y}

    def show_gif(self, gif_source):
        # Hapus GIF yang ada (jika ada)
        if self.gif_widget:
            self.layout.remove_widget(self.gif_widget)

        # Tentukan posisi acak
        position = self.random_position()

        # Tambahkan GIF baru di posisi acak
        self.gif_widget = AnimatedGif(gif_source, size_hint=(0.4, 0.4), pos_hint=position)
        self.layout.add_widget(self.gif_widget)

    def show_minus_gif(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):  # Cek apakah gambar minus ditekan
            self.show_gif('bintangku1.gif')
            Clock.schedule_once(self.go_to_fourth_screen, 2)  # Pindah layar ke penjumlahan (halaman keempat)

    def show_plus_gif(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):  # Cek apakah gambar plus ditekan
            self.show_gif('bintangku2.gif')
            Clock.schedule_once(self.go_to_third_screen, 2)  # Pindah layar ke pengurangan (halaman ketiga)

    def show_compare_gif(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):  # Cek apakah gambar ditekan
            self.show_gif('bintangku3.gif')
            Clock.schedule_once(self.go_to_fifth_screen, 2)

    def go_to_third_screen(self, dt):
        app = App.get_running_app()
        app.root.current = 'third'

    def go_to_fourth_screen(self, dt):
        app = App.get_running_app()
        app.root.current = 'fourth'

    def go_to_fifth_screen(self, dt):
        app = App.get_running_app()
        app.root.current = 'fifth'

    def go_to_main_menu(self, *args):
        app = App.get_running_app()
        app.root.current = 'main'

    def on_leave(self):
        """Fungsi yang dipanggil ketika meninggalkan layar ini."""
        # Hapus GIF saat kembali ke main menu
        if self.gif_widget:
            self.layout.remove_widget(self.gif_widget)
            self.gif_widget = None

class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)
        self.correct_answers = 0
        self.total_questions = 0
        self.answer_checked = False  # Track if an answer was checked
        self.time_limit = 10  # Time limit in seconds
        self.remaining_time = self.time_limit
        self.timer_event = None

        layout = RelativeLayout()

        # Background image (kk1.jpg)
        bg = Image(source='kk1.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)

        # Add bintangku1.gif in the bottom-right corner
        gif_widget = AnimatedGif('bintangku1.gif', size_hint=(0.4, 0.6), pos_hint={'right': 0.98, 'bottom': 0.02})
        layout.add_widget(gif_widget)

        cilik1_image = Image(source='cilik1.png', size_hint=(0.5, 0.4), pos_hint={'x': 0.25, 'y': 0.01})
        layout.add_widget(cilik1_image)

        # Question label
        self.question_label = Label(
            text="",
            font_size='36sp',
            bold=True,
            font_name='3Dumb',  # Use the 3Dumb font
            color=(1, 0, 0, 1),  # Red color (RGBA)
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        layout.add_widget(self.question_label)

        # Timer label
        self.timer_label = Label(
            text=f"Time left: {self.time_limit}s",
            font_size='24sp',
            bold=True,
            color=(0, 0, 1, 1),  # Blue color for timer
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(self.timer_label)

        # Input container
        input_container = RelativeLayout(size_hint=(0.35, 0.1), pos_hint={'center_x': 0.39, 'center_y': 0.65})

        # Shadow and input box
        with input_container.canvas.before:
            Color(1, 1, 0, 1)
            RoundedRectangle(size=(input_container.size_hint[0] * Window.width, input_container.size_hint[1] * Window.height), radius=[20])

        # TextInput for answer input
        self.answer_input = TextInput(
            font_size=24,
            size_hint=(1, 1),
            background_normal='',
            background_active='',
            foreground_color=(0, 0, 0, 1),
            multiline=False,
            halign='center',
            padding=(10, 10),
            background_color=(0, 0, 0, 0)
        )
        input_container.add_widget(self.answer_input)
        layout.add_widget(input_container)

        # Label for showing the result
        self.result_label = Label(text="", font_size='24sp', bold=True, color=(0, 0, 0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        layout.add_widget(self.result_label)

        # Button for checking the answer
        check_button = Button(
            size_hint=(0.4, 0.2),
            pos_hint={'x': 0.1, 'y': 0.38},
            background_normal='cek.png',
            background_down='cek.png'
        )
        check_button.bind(on_press=lambda instance: self.check_answer())
        layout.add_widget(check_button)

        # Button for generating the next question
        self.next_question_button = Button(
            size_hint=(0.4, 0.2),
            pos_hint={'x': 0.5, 'y': 0.38},
            background_normal='next.png',
            background_down='next.png'
        )
        self.next_question_button.bind(on_press=lambda instance: self.new_question())
        layout.add_widget(self.next_question_button)

        # Back button to show results or return to main menu
        back_button = Button(
            size_hint=(0.25, 0.25),
            pos_hint={'right': 0.98, 'top': 1.05},
            background_normal='back2.png',
            background_down='back2.png'
        )
        back_button.bind(on_press=lambda instance: self.on_back())
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Load sounds for correct and incorrect answers
        self.correct_sound = SoundLoader.load('right.wav')
        self.incorrect_sound = SoundLoader.load('no.wav')

        # Generate the first question
        self.new_question()

    def start_timer(self):
        """Start the countdown timer."""
        self.remaining_time = self.time_limit
        self.update_timer_label()

        if self.timer_event:
            self.timer_event.cancel()  # Cancel any existing timer

        # Schedule a repeated event to decrease the time every second
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Update the timer each second and check if time is up."""
        self.remaining_time -= 1
        self.update_timer_label()

        if self.remaining_time <= 0:
            self.timer_event.cancel()
            self.time_is_up()

    def update_timer_label(self):
        """Update the display of the timer."""
        self.timer_label.text = f"Time left: {self.remaining_time}s"

    def time_is_up(self):
        """Handle the case when the time is up."""
        self.result_label.text = "Waktu Habis! Jawaban Salah!"
        self.total_questions += 1
      
        
        # Automatically generate a new question after 1 second
        Clock.schedule_once(lambda dt: self.new_question(), 1)

    def check_answer(self):
        """Check the user's answer, update score, and proceed to the next question."""
        if self.answer_checked:  # Prevent multiple checks for the same question
            return

        try:
            user_answer = int(self.answer_input.text)
            self.answer_checked = True
            self.total_questions += 1
            if user_answer == self.correct_answer:
                self.correct_answers += 1
                self.result_label.text = "Jawaban Benar!"
                if self.correct_sound:
                    self.correct_sound.play()
            else:
                self.result_label.text = "Jawaban Salah!"
                if self.incorrect_sound:
                    self.incorrect_sound.play()
        except ValueError:
            self.result_label.text = "Masukkan angka yang valid!"
            return

        if self.timer_event:
            self.timer_event.cancel()  # Stop the timer if an answer is checked

        # Automatically proceed to the next question after 1 second
        Clock.schedule_once(lambda dt: self.new_question(), 1)

    def new_question(self):
        """Generate a new question and reset inputs."""
        self.answer_checked = False  # Allow for new answer check
        self.first_number = random.randint(1, 10)
        self.second_number = random.randint(1, self.first_number)
        self.correct_answer = self.first_number - self.second_number

        # Update the question label
        self.question_label.text = f"{self.first_number} - {self.second_number}?"
        self.answer_input.text = ""
        self.result_label.text = ""

        # Start the timer for the new question
        self.start_timer()

    def on_back(self):
        """Handle the back button to either show the result screen or return to the main menu."""
        app = App.get_running_app()
        if self.total_questions == 0:
            # If no questions answered, return to main menu
            app.root.current = 'main'
        else:
            # Show the result screen
            result_screen = app.root.get_screen('result')
            result_screen.update_result(self.correct_answers, self.total_questions)
            app.root.current = 'result'

    def reset_score(self):
        """Reset the score and question count to 0."""
        self.correct_answers = 0
        self.total_questions = 0



class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super(FourthScreen, self).__init__(**kwargs)
        self.correct_answers = 0
        self.total_questions = 0
        self.answer_checked = False  # Track if an answer was checked
        self.time_limit = 10  # Time limit in seconds
        self.remaining_time = self.time_limit
        self.timer_event = None  # To track the timer event
        layout = RelativeLayout()

        # Gambar background untuk halaman keempat
        bg = Image(source='kk2.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)

        # Add bintangku2.gif in the bottom-left corner
        gif_widget = AnimatedGif('bintangku2.gif', size_hint=(0.4, 0.5), pos_hint={'x': 0, 'bottom': 0})
        layout.add_widget(gif_widget)

        # Gambar cilik2.png
        cilik2_image = Image(source='cilik2.png', size_hint=(0.5, 0.4), pos_hint={'x': 0.5, 'y': 0.01})
        layout.add_widget(cilik2_image)

        # Label untuk pertanyaan
        self.question_label = Label(
            text="", 
            font_size='36sp', 
            bold=True, 
            font_name='3Dumb',  # Use the 3Dumb font
            color=(1, 0, 0, 1),  # Red color (RGBA)
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        layout.add_widget(self.question_label)

        # Timer label
        self.timer_label = Label(
            text=f"Time left: {self.time_limit}s",
            font_size='24sp',
            bold=True,
            color=(0, 0, 1, 1),  # Blue color for timer
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(self.timer_label)

        # Input container for answer
        input_container = RelativeLayout(size_hint=(0.35, 0.1), pos_hint={'center_x': 0.39, 'center_y': 0.65})

        # Bayangan dan background oval kuning
        with input_container.canvas.before:
            Color(1, 1, 0, 1)
            RoundedRectangle(size=(input_container.size_hint[0] * Window.width, input_container.size_hint[1] * Window.height), radius=[20])

        # TextInput untuk jawaban
        self.answer_input = TextInput(
            font_size=24,
            size_hint=(1, 1),
            background_normal='',
            background_active='',
            foreground_color=(0, 0, 0, 1),
            multiline=False,
            halign='center',
            padding=(self.width * 0.35, 10),
            background_color=(0, 0, 0, 0)
        )
        input_container.add_widget(self.answer_input)
        layout.add_widget(input_container)

        # Label untuk hasil
        self.result_label = Label(text="", font_size='24sp', bold=True, color=(0, 0, 0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        layout.add_widget(self.result_label)

        # Tombol untuk memeriksa jawaban
        check_button = Button(
            size_hint=(0.4, 0.2),
            pos_hint={'x': 0.1, 'y': 0.38},
            background_normal='cek.png',
            background_down='cek.png'
        )
        check_button.bind(on_press=lambda instance: self.check_answer())
        layout.add_widget(check_button)

        # Tombol untuk soal selanjutnya
        next_question_button = Button(
            size_hint=(0.4, 0.2),
            pos_hint={'x': 0.5, 'y': 0.38},
            background_normal='next.png',
            background_down='next.png'
        )
        next_question_button.bind(on_press=lambda instance: self.new_question())
        layout.add_widget(next_question_button)

        # Back button to show results or return to main menu
        back_button = Button(
            size_hint=(0.25, 0.25),
            pos_hint={'right': 0.98, 'top': 1.05},
            background_normal='back2.png',
            background_down='back2.png'
        )
        back_button.bind(on_press=lambda instance: self.on_back())
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Load sounds for correct and incorrect answers
        self.correct_sound = SoundLoader.load('right.wav')
        self.incorrect_sound = SoundLoader.load('no.wav')

        # Generate the first question
        self.new_question()

    def start_timer(self):
        """Start the countdown timer."""
        self.remaining_time = self.time_limit
        self.update_timer_label()

        if self.timer_event:
            self.timer_event.cancel()  # Cancel any existing timer

        # Schedule a repeated event to decrease the time every second
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Update the timer each second and check if time is up."""
        self.remaining_time -= 1
        self.update_timer_label()

        if self.remaining_time <= 0:
            self.timer_event.cancel()
            self.time_is_up()

    def update_timer_label(self):
        """Update the display of the timer."""
        self.timer_label.text = f"Time left: {self.remaining_time}s"

    def time_is_up(self):
        """Handle the case when the time is up."""
        self.result_label.text = "Waktu Habis! Jawaban Salah!"
        self.total_questions += 1
        # Automatically generate a new question after 1 second
        Clock.schedule_once(lambda dt: self.new_question(), 1)

    def check_answer(self):
        """Check the user's answer, update score, and proceed to the next question."""
        if self.answer_checked:
            return

        try:
            user_answer = int(self.answer_input.text)
            self.answer_checked = True
            self.total_questions += 1
            if user_answer == self.correct_answer:
                self.correct_answers += 1
                self.result_label.text = "Jawaban Benar!"
                if self.correct_sound:
                    self.correct_sound.play()
            else:
                self.result_label.text = "Jawaban Salah!"
                if self.incorrect_sound:
                    self.incorrect_sound.play()
        except ValueError:
            self.result_label.text = "Masukkan angka yang valid!"
            return

        if self.timer_event:
            self.timer_event.cancel()  # Stop the timer if an answer is checked

        # Automatically go to the next question after 2 seconds
        Clock.schedule_once(lambda dt: self.new_question(), 2)

    def new_question(self):
        """Generate a new question and reset inputs."""
        self.answer_checked = False
        self.first_number = random.randint(1, 10)
        self.second_number = random.randint(1, 10)
        self.correct_answer = self.first_number + self.second_number

        # Update the question label
        self.question_label.text = f"Berapakah {self.first_number} + {self.second_number}?"
        self.answer_input.text = ""
        self.result_label.text = ""

        # Start the timer for the new question
        self.start_timer()

    def on_back(self):
        """Handle the back button to either show the result screen or return to the main menu."""
        app = App.get_running_app()
        if self.total_questions == 0:
            # If no questions answered, return to main menu
            app.root.current = 'main'
        else:
            # Show the result screen
            result_screen = app.root.get_screen('result')
            result_screen.update_result(self.correct_answers, self.total_questions)
            app.root.current = 'result'

    def reset_score(self):
        """Reset the score and question count to 0."""
        self.correct_answers = 0
        self.total_questions = 0


class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super(FifthScreen, self).__init__(**kwargs)
        self.correct_answers = 0
        self.total_questions = 0
        self.answer_checked = False
        self.time_limit = 10  # Time limit in seconds
        self.remaining_time = self.time_limit
        self.timer_event = None  # To track the timer event
        layout = RelativeLayout()

        # Background image for FifthScreen
        bg = Image(source='kk3.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)

        # Add bintangku1.gif in the bottom-right corner
        gif_widget = AnimatedGif('bintangku3.gif', size_hint=(0.4, 0.6), pos_hint={'right': 0.98, 'bottom': 0.02})
        layout.add_widget(gif_widget)

        # Image cilik3.png
        cilik3_image = Image(source='cilik3.png', size_hint=(0.5, 0.4), pos_hint={'x': 0.25, 'y': 0.01})
        layout.add_widget(cilik3_image)

        # Question label
        self.question_label = Label(
            text="", 
            font_size='20sp', 
            bold=True, 
            font_name='3Dumb',  # Use the 3Dumb font
            color=(1, 0, 0, 1),  # Red color (RGBA)
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        layout.add_widget(self.question_label)

        # Timer label
        self.timer_label = Label(
            text=f"Time left: {self.time_limit}s",
            font_size='24sp',
            bold=True,
            color=(0, 0, 1, 1),  # Blue color for timer
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(self.timer_label)

        # Input container
        input_container = RelativeLayout(size_hint=(0.35, 0.1), pos_hint={'center_x': 0.39, 'center_y': 0.65})

        # Shadow and input box
        with input_container.canvas.before:
            Color(1, 1, 0, 1)
            RoundedRectangle(size=(input_container.size_hint[0] * Window.width, input_container.size_hint[1] * Window.height), radius=[20])

        # TextInput for answer input
        self.answer_input = TextInput(
            font_size=24,
            size_hint=(1, 1),
            background_normal='',
            background_active='',
            foreground_color=(0, 0, 0, 1),
            multiline=False,
            halign='center',
            padding=(self.width * 0.35, 10),
            background_color=(0, 0, 0, 0)
        )
        input_container.add_widget(self.answer_input)
        layout.add_widget(input_container)

        # Result label
        self.result_label = Label(text="", font_size='24sp', bold=True, color=(0, 0, 0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        layout.add_widget(self.result_label)

        # Button to check answer
        check_button = Button(
            size_hint=(0.4, 0.2),
            pos_hint={'x': 0.1, 'y': 0.38},
            background_normal='cek.png',
            background_down='cek.png'
        )
        check_button.bind(on_press=lambda instance: self.check_answer())
        layout.add_widget(check_button)

        # Button for the next question
        next_question_button = Button(
            size_hint=(0.4, 0.2),
            pos_hint={'x': 0.5, 'y': 0.38},
            background_normal='next.png',
            background_down='next.png'
        )
        next_question_button.bind(on_press=lambda instance: self.new_question())
        layout.add_widget(next_question_button)

        # Back button to show results or return to main menu
        back_button = Button(
            size_hint=(0.25, 0.25),
            pos_hint={'right': 0.98, 'top': 1.05},
            background_normal='back2.png',
            background_down='back2.png'
        )
        back_button.bind(on_press=lambda instance: self.on_back())
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Load sounds for correct and incorrect answers
        self.correct_sound = SoundLoader.load('right.wav')
        self.incorrect_sound = SoundLoader.load('no.wav')

        # Generate the first question
        self.new_question()

    def start_timer(self):
        """Start the countdown timer."""
        self.remaining_time = self.time_limit
        self.update_timer_label()

        if self.timer_event:
            self.timer_event.cancel()  # Cancel any existing timer

        # Schedule a repeated event to decrease the time every second
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Update the timer each second and check if time is up."""
        self.remaining_time -= 1
        self.update_timer_label()

        if self.remaining_time <= 0:
            self.timer_event.cancel()
            self.time_is_up()

    def update_timer_label(self):
        """Update the display of the timer."""
        self.timer_label.text = f"Time left: {self.remaining_time}s"

    def time_is_up(self):
        """Handle the case when the time is up."""
        self.result_label.text = "Waktu Habis! Jawaban Salah!"
        self.total_questions += 1
        # Automatically generate a new question after 1 second
        Clock.schedule_once(lambda dt: self.new_question(), 1)

    def check_answer(self):
        """Check the user's answer, update score, and proceed to the next question."""
        if self.answer_checked:
            return

        try:
            user_answer = int(self.answer_input.text)
            self.answer_checked = True
            self.total_questions += 1
            if user_answer == self.correct_answer:
                self.correct_answers += 1
                self.result_label.text = "Jawaban Benar!"
                if self.correct_sound:
                    self.correct_sound.play()
            else:
                self.result_label.text = f"Jawaban Salah, Jawabannya adalah {self.correct_answer}."
                if self.incorrect_sound:
                    self.incorrect_sound.play()
        except ValueError:
            self.result_label.text = "Masukkan angka yang valid!"
            return

        if self.timer_event:
            self.timer_event.cancel()  # Stop the timer if an answer is checked

        # Automatically proceed to the next question after 2 seconds
        Clock.schedule_once(lambda dt: self.new_question(), 2)

    def new_question(self):
        """Generate a new question and reset inputs."""
        self.answer_checked = False
        self.first_number = random.randint(1, 10)
        self.second_number = random.randint(1, 10)
        self.correct_answer = max(self.first_number, self.second_number)

        # Update the question label
        self.question_label.text = f"ANGKA MANA YANG LEBIH BESAR: {self.first_number} atau {self.second_number}?"
        self.answer_input.text = ""
        self.result_label.text = ""

        # Start the timer for the new question
        self.start_timer()

    def on_back(self):
        """Handle the back button to either show the result screen or return to the main menu."""
        app = App.get_running_app()
        if self.total_questions == 0:
            # If no questions answered, return to main menu
            app.root.current = 'main'
        else:
            # Show the result screen
            result_screen = app.root.get_screen('result')
            result_screen.update_result(self.correct_answers, self.total_questions)
            app.root.current = 'result'

    def reset_score(self):
        """Reset the score and question count to 0."""
        self.correct_answers = 0
        self.total_questions = 0






# Kelas untuk menampilkan GIF animasi
class AnimatedGif(Image):
    def __init__(self, gif_source, **kwargs):
        super(AnimatedGif, self).__init__(**kwargs)
        self.gif_source = gif_source
        self.pil_image = PILImage.open(self.gif_source)
        self.frames = [frame.copy() for frame in ImageSequence.Iterator(self.pil_image)]
        self.frame_index = 0

        # Pramuat frame pertama segera setelah widget dibuat
        self.texture = self.pil_to_texture(self.frames[0])
        
        # Memulai animasi
        Clock.schedule_interval(self.update_frame, 0.1)  # Update setiap 0.1 detik (sesuaikan sesuai kebutuhan)

    def update_frame(self, dt):
        self.frame_index = (self.frame_index + 1) % len(self.frames)  # Loop ke frame berikutnya
        frame = self.frames[self.frame_index]
        texture = self.pil_to_texture(frame)
        self.texture = texture
        self.canvas.ask_update()

    def pil_to_texture(self, pil_image):
        pil_image = pil_image.convert("RGBA")

        # Only flip the image if it's giphy.gif
        if self.gif_source == 'giphy.gif':
            pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)

        texture = Texture.create(size=pil_image.size, colorfmt='rgba')  # Buat texture baru
        texture.blit_buffer(pil_image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture



# Kelas utama aplikasi
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        sm.add_widget(FourthScreen(name='fourth'))
        sm.add_widget(FifthScreen(name='fifth'))
        sm.add_widget(ResultScreen(name='result'))  # Add result screen
        
        # Load the opening sound
        self.opening_sound = SoundLoader.load('opening.wav')
        if self.opening_sound:
            self.opening_sound.loop = True  # Set to loop the sound
            self.opening_sound.play()  # Play the sound

        return sm

    def on_stop(self):
        # Stop the opening sound when the app is closed
        if self.opening_sound:
            self.opening_sound.stop()


if __name__ == '__main__':
    MyApp().run()