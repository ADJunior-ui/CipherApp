import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Core application class handling cipher logic, file operations, and graphing

class CipherApp:
    MIN_ASCII = 32
    MAX_ASCII = 126

# Initialize application state: message text, shift key, and coordinate data

    def __init__(self):
        self.message = ""
        self.key = 0
        self.SepSentenc = []

# Validate input text to ensure all characters fall within the printable ASCII range    def is_valid_text(self, text):

        for ch in text:
            if ord(ch) < self.MIN_ASCII or ord(ch) > self.MAX_ASCII:
                return False
        return True

    def encode_message(self):

# Convert characters to X,Y coordinates using the ASCII value shifted by the key

        self.SepSentenc = []
        for ch in self.message:
            value = ord(ch) + self.key
            self.SepSentenc.append((value % 10, value // 10))

# Reconstruct the text message from coordinate sets using the reverse shift key

    def load_coordinates(self):
        self.message = ""
        for x, y in self.SepSentenc:
            value = y * 10 + x - self.key
            self.message += chr(value)
        return self.message

# Export the generated coordinate pairs into a plain text file

    def save_coordinates(self, filename):
        with open(filename, "w") as file:
            for x, y in self.SepSentenc:
                file.write(f"{x} {y}\n")

# Import coordinate pairs from an existing text file

    def load_coordinates(self, filename):
        self.SepSentenc = []
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    self.SepSentenc.append((int(parts[0]), int(parts[1])))

# Render a formatted text table mapping characters to their coordinates

    def print_table(self):
        print("\nCharacter ASCII Table")
        print("-" * 30)
        print(f"{'Char':<6}{'ASCII':<8}{'X':<4}{'Y'}")

        for i in range(len(self.message)):
            ch = self.message[i]
            x, y = self.SepSentenc[i]
            if ch == " ":
                ch = "' '"
            print(f"{ch:<6}{ord(self.message[i]):<8}{x:<4}{y}")

# Generate and visualize the sequential path of coordinates using matplotlib

    def draw_plot(self, image_name=None):
        if not self.SepSentenc:
            print("Nothing to plot.")
            return

        x_values = [p[0] for p in self.SepSentenc]
        y_values = [p[1] for p in self.SepSentenc]
        plt.figure(figsize=(9, 7))
        colors = cm.plasma(np.linspace(0, 1, max(len(self.SepSentenc) - 1, 1)))

        for i in range(len(self.SepSentenc) - 1):
            plt.plot(
                x_values[i:i + 2],
                y_values[i:i + 2],
                color=colors[i],
                linewidth=2
            )
            plt.annotate(
                "",
                xy=(x_values[i + 1], y_values[i + 1]),
                xytext=(x_values[i], y_values[i]),
                arrowprops=dict(arrowstyle="->", color=colors[i], lw=1.2)
            )

        plt.scatter(x_values, y_values)

        for i, (x, y) in enumerate(self.SepSentenc):
            plt.annotate(
                str(i + 1),
                (x, y),
                textcoords="offset points",
                xytext=(5, 5)
            )

        plt.title("Encoded Path")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.grid(True)

        if image_name:
            plt.savefig(image_name, dpi=150)
            print(f"Saved image as {image_name}")

        plt.show()

# Handle the user interactive input flow for the encoding sequence

    def run_encode_flow(self):
        self.message = input("Enter message: ")

        if not self.is_valid_text(self.message):
            print("No ASCII characters was entered.")
            return

        key_text = input("Key: ").strip()
        try:
            self.key = int(key_text)

# Fallback to a default key value of 0 if parsing fails

        except ValueError:
            self.key = 0
        self.encode_message()

# Prompt user for output location or fall back to default filename

        filename = input("Output file [default.txt]: ").strip()
        if filename == "":
            filename = "default.txt"

        self.save_coordinates(filename)
        print(f"Coordinates saved to {filename}")
        self.print_table()

        save_image = input("Save graph as PNG? (y/n): ").lower()
        image_file = None
        if save_image == "y":
            image_file = input("Image filename [plot.png]: ").strip()
            if image_file == "":
                image_file = "plot.png"

        self.draw_plot(image_file)

    def run_decode_flow(self):
        filename = input("Coordinate file: ").strip()
        key_text = input("Key (press Enter for 0): ").strip()
        try:
            self.key = int(key_text)
        except ValueError:
            self.key = 0

        self.load_coordinates(filename)
        print("\nDecoded message:")
        print(self.load_coordinates())

# Main application runtime loop and command menu execution

def main():
    app = CipherApp()
    while True:
        print("\n===== MENU =====")
        print("1. Encode")
        print("2. Decode")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            app.run_encode_flow()

        elif choice == "2":
            app.run_decode_flow()

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
